"""
Test cases for HCP Agent and Tools
"""
import pytest
from app.agents.hcp_agent import HCPInteractionAgent, InteractionLogState

@pytest.fixture
def agent():
    return HCPInteractionAgent()

def test_log_interaction_tool(agent):
    """Test Log Interaction Tool"""
    state = InteractionLogState(
        hcp_id=1,
        interaction_type="call",
        user_input="Had a discussion with Dr. Smith about new cardiac medication. Very interested in the product.",
        messages=[]
    )
    
    result = agent.log_interaction_tool(state)
    
    assert result.summary is not None
    assert len(result.summary) > 0
    print(f"Summary: {result.summary}")

def test_extract_entities_tool(agent):
    """Test Extract Entities Tool"""
    state = InteractionLogState(
        hcp_id=1,
        interaction_type="meeting",
        user_input="Dr. Johnson from Cleveland Hospital expressed interest in our beta trial for treatment of diabetes. Mentioned competition from GSK.",
        messages=[]
    )
    
    result = agent.extract_entities_tool(state)
    
    assert result.entities is not None
    print(f"Entities: {result.entities}")

def test_sentiment_analysis_tool(agent):
    """Test Sentiment Analysis Tool"""
    state = InteractionLogState(
        hcp_id=1,
        interaction_type="call",
        user_input="Dr. Brown was very enthusiastic about the clinical data and wants to schedule a follow-up meeting next week.",
        messages=[]
    )
    
    result = agent.sentiment_analysis_tool(state)
    
    assert result.entities is not None
    assert "sentiment_analysis" in result.entities
    print(f"Sentiment Analysis: {result.entities.get('sentiment_analysis')}")

def test_generate_follow_up_tool(agent):
    """Test Generate Follow-Up Tool"""
    state = InteractionLogState(
        hcp_id=1,
        interaction_type="call",
        user_input="Discussion about new drug launch",
        summary="Positive response from HCP regarding new medication",
        messages=[]
    )
    
    result = agent.generate_follow_up_tool(state)
    
    assert result.action_items is not None
    print(f"Follow-ups: {result.action_items}")

def test_conversational_interface_tool(agent):
    """Test Conversational Interface Tool"""
    state = InteractionLogState(
        hcp_id=1,
        interaction_type="call",
        user_input="I had a call with Dr. Smith about our new product. He seemed interested but concerned about pricing.",
        messages=[]
    )
    
    result = agent.conversational_interface_tool(state)
    
    assert len(result.messages) > 0
    assert result.messages[-1]["role"] == "assistant"
    print(f"Response: {result.messages[-1]['content']}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
