# AI Agent Architecture & Tools Documentation

## Overview

The CRM HCP Module uses LangGraph to create a sophisticated AI agent that manages healthcare professional interactions. The agent can perform various tasks related to CRM data management through specialized tools.

## LangGraph Workflow Architecture

```
User Input
    ↓
[Conversational Interface Tool]
    ↓
[Log Interaction Tool]
    ↓
[Extract Entities Tool]
    ↓
[Sentiment Analysis Tool]
    ↓
[Generate Follow-Ups Tool]
    ↓
Output (Summary, Entities, Action Items)
```

## 6+ Tools Implementation

### Tool 1: Log Interaction
**Purpose**: Capture and summarize HCP interaction data

**Functionality**:
- Takes raw interaction text as input
- Uses LLM (Groq gemma2-9b-it) to generate concise summary
- Extracts key entities automatically
- Stores structured data in database

**Usage**:
```python
state = InteractionLogState(
    hcp_id=1,
    interaction_type="call",
    user_input="Discussed new cardiac medication with Dr. Smith...",
    messages=[]
)
result = agent.log_interaction_tool(state)
# Returns: state with summary, entities extracted
```

**Output**:
- Summary: 2-3 sentence concise overview
- Entities: Dict with extracted information
- Action Items: List of follow-up tasks

---

### Tool 2: Edit Interaction
**Purpose**: Modify previously logged interactions

**Functionality**:
- Updates existing interaction records
- Re-analyzes modified content
- Maintains interaction history
- Updates related summaries and entities

**Usage**:
```python
state.summary = "Original summary..."
state.user_input = "Update: Also discussed pricing concerns..."
result = agent.edit_interaction_tool(state)
# Returns: updated state with new summary and entities
```

**Output**:
- Updated Summary
- Refined Entities
- Modified Action Items

---

### Tool 3: Generate Follow-Up
**Purpose**: Create actionable follow-up items

**Functionality**:
- Analyzes interaction context
- Generates 2-3 specific follow-up tasks
- Considers interaction type and HCP context
- Provides pharmaceutical-industry-specific recommendations

**Usage**:
```python
state.summary = "Positive feedback on new product..."
state.interaction_type = "meeting"
result = agent.generate_follow_up_tool(state)
# Returns: state with action_items list
```

**Output**:
- Action Items: ["Schedule follow-up meeting", "Send clinical data", ...]

---

### Tool 4: Extract Entities
**Purpose**: Advanced entity extraction from interaction text

**Functionality**:
- Categorizes mentions into specific types:
  - **Products**: Medications, devices mentioned
  - **Conditions**: Medical conditions discussed
  - **People**: Other HCPs or decision makers
  - **Organizations**: Hospitals, clinics, pharmas
  - **Commitments**: Promises or commitments made

**Usage**:
```python
state.user_input = "Dr. Johnson from Cleveland Clinic wants to trial our new diabetes treatment..."
result = agent.extract_entities_tool(state)
# Returns: state with entities = {
#   "organizations": ["Cleveland Clinic"],
#   "products": ["diabetes treatment"],
#   "conditions": ["diabetes"],
#   ...
# }
```

**Output**:
```json
{
  "products": ["medication name"],
  "conditions": ["medical condition"],
  "people": ["Dr. Name"],
  "organizations": ["Hospital Name"],
  "commitments": ["promised action"]
}
```

---

### Tool 5: Sentiment Analysis
**Purpose**: Analyze HCP engagement and sentiment

**Functionality**:
- Measures HCP sentiment (positive/neutral/negative)
- Assesses engagement level (high/medium/low)
- Evaluates product adoption likelihood
- Identifies concerns and objections

**Usage**:
```python
state.user_input = "Dr. Brown expressed strong interest but had concerns about pricing..."
state.interaction_type = "call"
result = agent.sentiment_analysis_tool(state)
# Returns: state with entities containing sentiment_analysis
```

**Output**:
```json
{
  "sentiment": "positive",
  "engagement_level": "high",
  "adoption_likelihood": "medium",
  "concerns": ["pricing", "implementation timeline"]
}
```

---

### Tool 6: Conversational Interface
**Purpose**: Multi-turn conversation with context awareness

**Functionality**:
- Maintains conversation history
- Provides contextual responses
- Guides users through logging process
- Asks clarifying questions when needed
- Integrates with other tools seamlessly

**Usage**:
```python
state.messages = [
    {"role": "user", "content": "Had a call today"},
    {"role": "assistant", "content": "Tell me more about the call..."}
]
state.user_input = "Discussed new product launch with Dr. Smith"
result = agent.conversational_interface_tool(state)
# Returns: state with messages updated
```

**Features**:
- Multi-turn capability
- Context retention
- Natural language understanding
- Response generation with LLM

---

## State Management

### InteractionLogState
```python
class InteractionLogState(BaseModel):
    hcp_id: int                                    # Target HCP
    interaction_type: str                          # call/meeting/email/conference/webinar
    user_input: str                                # Current user input
    summary: Optional[str] = None                  # AI-generated summary
    entities: Optional[Dict[str, Any]] = None      # Extracted entities
    action_items: Optional[List[str]] = None       # Follow-up actions
    saved_interaction_id: Optional[int] = None     # Database ID after saving
    messages: List[Dict[str, str]] = []           # Conversation history
```

## LLM Integration

### Model Configuration
- **Provider**: Groq
- **Model**: gemma2-9b-it
- **Temperature**: 0.6-0.7 (balanced creativity)
- **Max Tokens**: 1000
- **Context Window**: Full conversation maintained

### Prompt Engineering
Each tool includes optimized prompts:
- Clear task definition
- Input/output format specification
- Pharmaceutical domain context
- JSON response structure requirement

## Database Integration

### Workflow to Database
```
Tool Output
    ↓
Validation
    ↓
Database Model Mapping
    ↓
SQLAlchemy ORM
    ↓
PostgreSQL/MySQL Storage
```

### Data Persistence
- Interactions saved with summaries
- Entities stored in description/summary
- Action items in FollowUp table
- Full audit trail maintained

## Performance Considerations

### Optimization
- Batch tool execution where possible
- Cache common LLM responses
- Async API calls for I/O operations
- Database query optimization

### Scalability
- Stateless agent design
- Horizontal scaling ready
- Load balancing compatible
- Database connection pooling

## Error Handling

### Tool-Level
```python
try:
    result = tool(state)
except Exception as e:
    # Fallback to default behavior
    state.summary = state.user_input
    return state
```

### API-Level
- Graceful error responses
- Detailed error messages
- Request validation
- Proper HTTP status codes

## Testing Tools

### Unit Tests
```python
def test_log_interaction_tool(agent):
    state = InteractionLogState(...)
    result = agent.log_interaction_tool(state)
    assert result.summary is not None
```

### Integration Tests
- End-to-end workflow testing
- API endpoint testing
- Database integration testing
- LLM response validation

## Future Enhancements

1. **Multi-Model Support**: Add Claude, GPT-4
2. **Custom Fine-tuning**: Domain-specific model adaptation
3. **Memory Enhancement**: Persistent agent memory
4. **Tool Composition**: Complex multi-step workflows
5. **Real-time Collaboration**: Team shared context
6. **Advanced Analytics**: Interaction insights and trends

---

## References

- [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
- [Groq API Docs](https://console.groq.com/docs)
- [FastAPI Advanced Features](https://fastapi.tiangolo.com/advanced/)
