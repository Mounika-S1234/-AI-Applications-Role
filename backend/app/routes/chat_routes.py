from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Interaction, HCP
from app.schemas.schemas import ChatMessage, ChatResponse
from app.agents.hcp_agent import HCPInteractionAgent, InteractionLogState
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Initialize agent
agent = HCPInteractionAgent()

@router.post("/message", response_model=ChatResponse)
async def chat_message(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Send a message to the HCP interaction agent
    Supports both new interactions and conversational interface
    """
    try:
        # Initialize state
        state = InteractionLogState(
            hcp_id=message.hcp_id or 0,
            interaction_type="call",  # Default, can be updated
            user_input=message.message,
            messages=[]
        )
        
        # Process through conversational agent
        result_state = agent.conversational_interface_tool(state)
        
        # Get the last assistant response
        response_text = ""
        if result_state.messages:
            for msg in reversed(result_state.messages):
                if msg.get("role") == "assistant":
                    response_text = msg.get("content", "")
                    break
        
        # If we have both summary and action items, save to database
        saved_interaction_id = None
        if result_state.summary and message.hcp_id:
            db_interaction = Interaction(
                hcp_id=message.hcp_id,
                interaction_type=result_state.interaction_type,
                title="AI-Logged Interaction",
                description=message.message,
                summary=result_state.summary,
                date=datetime.utcnow()
            )
            db.add(db_interaction)
            db.commit()
            db.refresh(db_interaction)
            saved_interaction_id = db_interaction.id
        
        return ChatResponse(
            response=response_text,
            interaction_id=saved_interaction_id,
            action_items=result_state.action_items
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/log-interaction")
async def log_interaction_endpoint(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Direct endpoint to log interactions using the Log Interaction tool and return AI-parsed form fields.
    """
    try:
        # Verify HCP exists if provided
        if message.hcp_id:
            hcp = db.query(HCP).filter(HCP.id == message.hcp_id).first()
            if not hcp:
                raise HTTPException(status_code=404, detail="HCP not found")

        # Initialize state
        state = InteractionLogState(
            hcp_id=message.hcp_id or 0,
            interaction_type="call",
            user_input=message.message,
            messages=[]
        )

        # Use the new LangGraph-powered parse and summarization tools
        state = agent.populate_form_tool(state)
        state = agent.sentiment_analysis_tool(state)
        state = agent.generate_follow_up_tool(state)
        state = agent.log_interaction_tool(state)

        form_data = state.entities.get("parsed_form") if state.entities else {}
        saved_interaction_id = None

        if message.hcp_id:
            db_interaction = Interaction(
                hcp_id=message.hcp_id,
                interaction_type=form_data.get("interaction_type", "call"),
                title=form_data.get("title", "AI Logged Interaction"),
                description=form_data.get("description", message.message),
                summary=state.summary,
                date=datetime.utcnow()
            )
            db.add(db_interaction)
            db.commit()
            db.refresh(db_interaction)
            saved_interaction_id = db_interaction.id

        return ChatResponse(
            response=f"Interaction parsed and filled successfully.",
            interaction_id=saved_interaction_id,
            action_items=state.action_items,
            form_data=form_data,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/edit-interaction/{interaction_id}")
async def edit_interaction_endpoint(interaction_id: int, message: ChatMessage, db: Session = Depends(get_db)):
    """
    Edit an existing interaction using the AI-powered edit tool and return updated form fields.
    """
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            raise HTTPException(status_code=404, detail="Interaction not found")

        existing_form = message.existing_form or {
            "title": interaction.title,
            "description": interaction.description,
            "interaction_type": interaction.interaction_type,
            "hcp_name": None,
            "sentiment": None,
            "brochures_shared": None,
            "products_discussed": None,
            "action_items": []
        }

        state = InteractionLogState(
            hcp_id=interaction.hcp_id,
            interaction_type=interaction.interaction_type,
            user_input=message.message,
            summary=interaction.summary,
            entities={"parsed_form": existing_form},
            messages=[]
        )

        state = agent.update_form_tool(state)
        state = agent.sentiment_analysis_tool(state)
        state = agent.log_interaction_tool(state)

        parsed_form = state.entities.get("parsed_form", {})
        interaction.title = parsed_form.get("title", interaction.title)
        interaction.description = parsed_form.get("description", interaction.description)
        interaction.interaction_type = parsed_form.get("interaction_type", interaction.interaction_type)
        interaction.summary = state.summary
        interaction.updated_at = datetime.utcnow()
        db.add(interaction)
        db.commit()

        return ChatResponse(
            response=f"Interaction form updated successfully.",
            interaction_id=interaction_id,
            action_items=state.action_items,
            form_data=parsed_form,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-entities")
async def extract_entities_endpoint(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Extract entities from interaction text using the Extract Entities tool
    """
    try:
        state = InteractionLogState(
            hcp_id=message.hcp_id or 0,
            interaction_type="call",
            user_input=message.message,
            messages=[]
        )
        
        result_state = agent.extract_entities_tool(state)
        
        return ChatResponse(
            response=f"Entities extracted successfully",
            action_items=list(result_state.entities.keys()) if result_state.entities else []
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sentiment-analysis")
async def sentiment_analysis_endpoint(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Analyze sentiment of interaction using the Sentiment Analysis tool
    """
    try:
        state = InteractionLogState(
            hcp_id=message.hcp_id or 0,
            interaction_type="call",
            user_input=message.message,
            messages=[]
        )
        
        result_state = agent.sentiment_analysis_tool(state)
        
        sentiment_data = result_state.entities.get("sentiment_analysis", {}) if result_state.entities else {}
        
        return ChatResponse(
            response=f"Sentiment Analysis: {sentiment_data}",
            action_items=[str(sentiment_data)]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
