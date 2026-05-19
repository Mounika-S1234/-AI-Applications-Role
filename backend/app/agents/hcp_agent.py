import os
from groq import Groq
from typing import List, Dict, Any
from langgraph.graph import StateGraph
from langgraph.types import Send
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime
import json

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

class InteractionLogState(BaseModel):
    hcp_id: int
    interaction_type: str
    user_input: str
    summary: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    action_items: Optional[List[str]] = None
    saved_interaction_id: Optional[int] = None
    messages: List[Dict[str, str]] = Field(default_factory=list)

class HCPInteractionAgent:
    def __init__(self):
        self.client = client
        self.model = "gemma2-9b-it"

    def _extract_json(self, text: str):
        import re
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        return None

    def populate_form_tool(self, state: InteractionLogState) -> InteractionLogState:
        """
        Tool 1: Populate Form - Extract structured interaction form fields from freeform user input.
        """
        prompt = f"""
You are an AI assistant for a pharmaceutical CRM platform.
A sales representative provides an interaction note in natural language.
Extract the structured form fields needed for the interaction record.

Return exactly one JSON object with the following keys:
- hcp_name
- interaction_date
- interaction_type
- sentiment
- brochures_shared
- title
- description
- products_discussed
- action_items

Use the values from the user text. If a field is not present, return a sensible default.

User note:
{state.user_input}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.65,
            max_tokens=800,
        )

        response_text = response.choices[0].message.content
        parsed = self._extract_json(response_text) or {}
        state.entities = state.entities or {}
        state.entities["parsed_form"] = parsed
        state.action_items = parsed.get("action_items", [])
        state.summary = parsed.get("title", state.summary)

        return state

    def update_form_tool(self, state: InteractionLogState) -> InteractionLogState:
        """
        Tool 2: Update Form - Apply user edit instructions to existing structured form fields.
        """
        existing_form = state.entities.get("parsed_form", {}) if state.entities else {}
        prompt = f"""
You are an AI assistant editing an existing HCP interaction form.
Existing form values: {json.dumps(existing_form)}
User edit request: {state.user_input}

Update only the fields mentioned in the request and preserve all other values.
Respond with a JSON object using the same keys as the form:
- hcp_name
- interaction_date
- interaction_type
- sentiment
- brochures_shared
- title
- description
- products_discussed
- action_items
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=800,
        )

        response_text = response.choices[0].message.content
        parsed = self._extract_json(response_text) or {}
        merged = {**existing_form, **parsed}
        state.entities = state.entities or {}
        state.entities["parsed_form"] = merged
        state.action_items = merged.get("action_items", state.action_items)
        state.summary = merged.get("title", state.summary)

        return state

    def log_interaction_tool(self, state: InteractionLogState) -> InteractionLogState:
        """
        Tool 3: Log Interaction - Captures interaction data and uses LLM for summarization and entity extraction
        """
        prompt = f"""
You are a CRM assistant helping a pharmaceutical sales representative log their interaction with a Healthcare Professional (HCP).

Interaction Details:
- HCP ID: {state.hcp_id}
- Interaction Type: {state.interaction_type}
- User Input: {state.user_input}

Please analyze this interaction and provide:
1. A concise summary (2-3 sentences) of the interaction
2. Key entities mentioned (names, products, medications, etc.)
3. Any follow-up actions needed

Respond in JSON format with keys: summary, entities (as dict), action_items (as list of strings)
"""
        message = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
        )
        
        try:
            response_text = message.choices[0].message.content
            result = self._extract_json(response_text)
            if result:
                state.summary = result.get("summary", "")
                state.entities = result.get("entities", state.entities or {})
                state.action_items = result.get("action_items", [])
            else:
                state.summary = response_text
        except Exception as e:
            state.summary = state.user_input
            
        return state

    def edit_interaction_tool(self, state: InteractionLogState) -> InteractionLogState:
        """
        Tool 2: Edit Interaction - Allows modification of logged data
        """
        prompt = f"""
You are helping to edit a previously logged HCP interaction.

Original Interaction:
- Summary: {state.summary}
- Entities: {json.dumps(state.entities)}
- Action Items: {json.dumps(state.action_items)}

User's Edit Request: {state.user_input}

Please update the interaction details based on the edit request and provide updated:
1. Summary
2. Entities
3. Action Items

Respond in JSON format with keys: summary, entities (as dict), action_items (as list of strings)
"""
        message = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
        )
        
        try:
            response_text = message.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                state.summary = result.get("summary", state.summary)
                state.entities = result.get("entities", state.entities)
                state.action_items = result.get("action_items", state.action_items)
        except Exception as e:
            pass
            
        return state

    def generate_follow_up_tool(self, state: InteractionLogState) -> InteractionLogState:
        """
        Tool 3: Generate Follow-Up - Creates suggested follow-up actions based on interaction
        """
        prompt = f"""
Based on this HCP interaction, generate 2-3 specific, actionable follow-up items.

Interaction Summary: {state.summary}
Interaction Type: {state.interaction_type}
Key Entities: {json.dumps(state.entities)}

Generate follow-up actions that are specific to pharmaceutical sales context.
Respond with a JSON object with key 'follow_ups' containing a list of action items.
"""
        message = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        
        try:
            response_text = message.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                follow_ups = result.get("follow_ups", [])
                state.action_items = state.action_items + follow_ups if state.action_items else follow_ups
        except Exception as e:
            pass
            
        return state

    def extract_entities_tool(self, state: InteractionLogState) -> InteractionLogState:
        """
        Tool 4: Extract Entities - Advanced entity extraction for CRM data
        """
        prompt = f"""
Extract all relevant entities from this HCP interaction:

Text: {state.user_input}

Extract and categorize:
- Products mentioned (pharmaceuticals, devices, etc.)
- Healthcare conditions discussed
- Decision makers or other HCPs mentioned
- Organizations or hospitals mentioned
- Next steps or commitments

Respond with JSON object with keys: products, conditions, people, organizations, commitments
Each value should be a list.
"""
        message = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800,
        )
        
        try:
            response_text = message.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                state.entities = result
        except Exception as e:
            pass
            
        return state

    def sentiment_analysis_tool(self, state: InteractionLogState) -> InteractionLogState:
        """
        Tool 5: Sentiment Analysis - Analyzes HCP sentiment and engagement level
        """
        prompt = f"""
Analyze the sentiment and engagement level of this HCP interaction.

Interaction Text: {state.user_input}
Interaction Type: {state.interaction_type}

Assess:
1. Overall sentiment (positive, neutral, negative)
2. Engagement level (high, medium, low)
3. Likelihood of product adoption (high, medium, low)
4. Key concerns or objections (if any)

Respond with JSON object with keys: sentiment, engagement_level, adoption_likelihood, concerns (list)
"""
        message = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=600,
        )
        
        try:
            response_text = message.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                state.entities["sentiment_analysis"] = result
        except Exception as e:
            pass
            
        return state

    def conversational_interface_tool(self, state: InteractionLogState) -> InteractionLogState:
        """
        Tool 6: Conversational Interface - Multi-turn conversation with HCP interaction context
        """
        # Build conversation history
        system_prompt = """You are an AI assistant helping a pharmaceutical sales representative 
document and analyze their interactions with Healthcare Professionals (HCPs). 
You help them log interactions, extract key information, and identify follow-up actions.
Be helpful, concise, and focused on CRM best practices."""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(state.messages)
        messages.append({"role": "user", "content": state.user_input})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )

        assistant_response = response.choices[0].message.content
        state.messages.append({"role": "user", "content": state.user_input})
        state.messages.append({"role": "assistant", "content": assistant_response})

        return state

    def create_workflow(self):
        """Create LangGraph workflow for HCP interactions"""
        workflow = StateGraph(InteractionLogState)

        # Add nodes
        workflow.add_node("populate_form", self.populate_form_tool)
        workflow.add_node("update_form", self.update_form_tool)
        workflow.add_node("log_interaction", self.log_interaction_tool)
        workflow.add_node("generate_follow_up", self.generate_follow_up_tool)
        workflow.add_node("extract_entities", self.extract_entities_tool)
        workflow.add_node("sentiment_analysis", self.sentiment_analysis_tool)
        workflow.add_node("conversational", self.conversational_interface_tool)

        # Set entry point
        workflow.set_entry_point("populate_form")

        # Add edges
        workflow.add_edge("populate_form", "sentiment_analysis")
        workflow.add_edge("sentiment_analysis", "generate_follow_up")
        workflow.add_edge("generate_follow_up", "extract_entities")
        workflow.add_edge("extract_entities", "log_interaction")

        # Additional edit path
        workflow.add_edge("conversational", "update_form")
        workflow.add_edge("update_form", "log_interaction")

        return workflow.compile()
