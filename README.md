# AI-First CRM HCP Module - Log Interaction Screen

A comprehensive Healthcare Professional (HCP) Customer Relationship Management system with AI-powered interaction logging, built with modern full-stack technologies.

## 🎯 Project Overview

This system provides pharmaceutical sales representatives with a powerful tool to:
- Log interactions with Healthcare Professionals via structured forms or conversational AI interface
- Automatically summarize interactions using LLMs
- Extract relevant entities and key information
- Generate action items and follow-up tasks
- Analyze sentiment and engagement levels
- Maintain comprehensive interaction history

## 🔧 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI Agent**: LangGraph
- **LLM**: Groq (gemma2-9b-it model)
- **Database**: PostgreSQL / MySQL
- **ORM**: SQLAlchemy
- **API**: RESTful with FastAPI

### Frontend
- **Framework**: React 18
- **State Management**: Redux Toolkit
- **Language**: TypeScript
- **Styling**: CSS3 with Inter Font (Google Fonts)
- **HTTP Client**: Axios

## 📋 Core Features

### 1. **Dual Interface for Logging Interactions**
   - **Structured Form**: Traditional form-based interaction logging
   - **Chat Interface**: Conversational AI-powered interaction capture

### 2. **LangGraph Agent with 6+ Tools**

#### Tool 1: Log Interaction
- Captures interaction data with LLM-powered summarization
- Automatically extracts key information
- Generates structured summaries

#### Tool 2: Edit Interaction
- Allows modification of previously logged interactions
- Updates summaries and extracted data
- Maintains audit trail

#### Tool 3: Generate Follow-Up
- Creates suggested follow-up actions
- Based on interaction context and type
- Pharmaceutical-specific recommendations

#### Tool 4: Extract Entities
- Advanced entity extraction from interactions
- Categories: Products, Conditions, People, Organizations, Commitments
- Structured data output for CRM analysis

#### Tool 5: Sentiment Analysis
- Analyzes HCP sentiment and engagement level
- Assesses product adoption likelihood
- Identifies concerns and objections

#### Tool 6: Conversational Interface
- Multi-turn conversation support
- Context-aware responses
- Seamless integration with logging workflow

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+ or MySQL 8.0+
- Groq API Key (Get from: https://console.groq.com/)

### Backend Setup

1. **Clone the repository**
```bash
cd backend
```

2. **Create Python virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Create .env file with:
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user:password@localhost/crm_hcp_db
# OR for MySQL:
# DATABASE_URL=mysql+pymysql://user:password@localhost/crm_hcp_db
```

5. **Initialize database**
```bash
python -c "from app.database import engine, Base; from app.models.models import *; Base.metadata.create_all(bind=engine)"
```

6. **Run backend server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
# Create .env file with:
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GROQ_API_KEY=your_groq_api_key
```

4. **Run development server**
```bash
npm start
```

Frontend will be available at: `http://localhost:3000`

## 📚 API Endpoints

### HCP Management
```
POST   /api/hcps/              - Create new HCP
GET    /api/hcps/              - List all HCPs
GET    /api/hcps/{id}          - Get HCP details
PUT    /api/hcps/{id}          - Update HCP
DELETE /api/hcps/{id}          - Delete HCP
```

### Interactions
```
POST   /api/interactions/                    - Create interaction
GET    /api/interactions/                    - List all interactions
GET    /api/interactions/{id}                - Get interaction details
PUT    /api/interactions/{id}                - Update interaction
DELETE /api/interactions/{id}                - Delete interaction
GET    /api/interactions/hcp/{hcp_id}        - Get HCP's interactions
```

### AI Chat & Tools
```
POST   /api/chat/message                      - Send chat message
POST   /api/chat/log-interaction             - Log interaction with AI
POST   /api/chat/edit-interaction/{id}       - Edit interaction with AI
POST   /api/chat/extract-entities            - Extract entities from text
POST   /api/chat/sentiment-analysis          - Analyze sentiment
POST   /api/chat/generate-follow-up          - Generate follow-ups
```

## 📊 Database Schema

### HCP Table
```sql
- id (PK)
- name
- specialty
- organization
- email
- phone
- location
- created_at
- updated_at
```

### Interaction Table
```sql
- id (PK)
- hcp_id (FK)
- interaction_type (call/meeting/email/conference/webinar)
- title
- description
- summary (AI-generated)
- date
- created_at
- updated_at
```

### FollowUp Table
```sql
- id (PK)
- interaction_id (FK)
- action_item
- due_date
- completed
- created_at
- updated_at
```

## 🧠 AI Agent Architecture

### LangGraph Workflow
```
User Input
    ↓
Conversational Interface (Tool 6)
    ↓
Log Interaction (Tool 1)
    ↓
Extract Entities (Tool 4)
    ↓
Sentiment Analysis (Tool 5)
    ↓
Generate Follow-Ups (Tool 3)
    ↓
Output: Summary, Entities, Actions
```

### LLM Integration
- **Model**: Groq gemma2-9b-it
- **Temperature**: 0.6-0.7 (balanced creativity)
- **Max Tokens**: 1000 per response
- **Context Window**: Full conversation history maintained

## 🎨 UI Components

### Main Components
- **HCPList**: Browse and select Healthcare Professionals
- **ChatInterface**: Conversational interaction logging
- **InteractionForm**: Structured form-based logging
- **InteractionHistory**: View past interactions with summaries

### Redux State Management
- **hcpSlice**: HCP data and selection
- **interactionSlice**: Interaction logging and history
- **chatSlice**: Chat messages and state

## 🔐 Security Considerations

- Environment variables for sensitive keys
- CORS enabled for development
- Input validation on both frontend and backend
- SQL injection protection via SQLAlchemy ORM
- HTTPS recommended for production

## 📦 Deployment

### Backend (Gunicorn + Uvicorn)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend (Build & Deploy)
```bash
npm run build
# Deploy 'build' folder to static hosting (Vercel, Netlify, AWS S3, etc.)
```

### Database Setup for Production
```bash
# PostgreSQL
createdb crm_hcp_db
psql crm_hcp_db < schema.sql

# MySQL
mysql -u root -p
CREATE DATABASE crm_hcp_db;
```

## 📝 Usage Guide

### Logging an Interaction

#### Via Chat Interface
1. Select an HCP from the list
2. Switch to "Chat Interface" tab
3. Choose interaction type
4. Describe the interaction naturally
5. AI will extract summary, entities, and action items

#### Via Structured Form
1. Select an HCP from the list
2. Switch to "Structured Form" tab
3. Fill in interaction details
4. Click "Log Interaction"

### Editing Interactions
1. Navigate to "History" tab
2. View past interactions
3. Switch to "Chat Interface"
4. Toggle to "Edit Interaction" mode
5. Describe the changes needed

### Viewing Interaction History
1. Click on an HCP in the sidebar
2. Navigate to "History" tab
3. Browse all interactions with summaries
4. Review extracted entities and action items

## 🧪 Testing

### Backend Testing
```bash
# Run tests
pytest tests/

# Test specific tools
pytest tests/test_agent.py -v
```

### API Testing
```bash
# Using curl
curl -X POST http://localhost:8000/api/hcps/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Dr. Smith","specialty":"Cardiology"}'

# Using Postman
# Import collection from: docs/postman_collection.json
```

## 🎬 Video Demo Contents

Your 10-15 minute video should cover:

1. **Frontend Walkthrough (3-4 min)**
   - HCP selection and management
   - Structured form interface
   - Chat interface with AI responses
   - Interaction history view

2. **AI Tools Demo (4-5 min)**
   - Tool 1: Log Interaction (with summary generation)
   - Tool 2: Edit Interaction (modification demo)
   - Tool 3: Generate Follow-Ups (action item creation)
   - Tool 4: Extract Entities (category extraction)
   - Tool 5: Sentiment Analysis (engagement assessment)
   - Tool 6: Conversational Interface (multi-turn conversation)

3. **Code Walkthrough (2-3 min)**
   - LangGraph agent architecture
   - FastAPI endpoints structure
   - Redux state management
   - Database models

4. **Project Summary (1-2 min)**
   - Key learnings from the task
   - Architecture decisions
   - AI/ML integration benefits

## 📂 Project Structure

```
crm-hcp-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   └── schemas.py
│   │   ├── routes/
│   │   │   ├── hcp_routes.py
│   │   │   ├── interaction_routes.py
│   │   │   └── chat_routes.py
│   │   └── agents/
│   │       └── hcp_agent.py
│   ├── requirements.txt
│   ├── .env
│   └── wsgi.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── App.tsx
│   │   │   ├── HCPList.tsx
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── InteractionForm.tsx
│   │   │   └── InteractionHistory.tsx
│   │   ├── redux/
│   │   │   ├── store.ts
│   │   │   ├── hcpSlice.ts
│   │   │   ├── interactionSlice.ts
│   │   │   └── chatSlice.ts
│   │   ├── styles/
│   │   │   ├── App.css
│   │   │   ├── HCPList.css
│   │   │   ├── ChatInterface.css
│   │   │   ├── InteractionForm.css
│   │   │   └── InteractionHistory.css
│   │   ├── index.tsx
│   │   └── types.ts
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── .env
│   └── .gitignore
│
└── README.md
```

## 🛠️ Troubleshooting

### Backend Issues
```
Error: "GROQ_API_KEY not found"
→ Add GROQ_API_KEY to .env file

Error: "Database connection failed"
→ Verify DATABASE_URL and ensure DB is running

Error: "Module not found"
→ Run: pip install -r requirements.txt
```

### Frontend Issues
```
Error: "Cannot find module '@reduxjs/toolkit'"
→ Run: npm install

Error: "API call failed"
→ Ensure backend is running on http://localhost:8000
→ Check REACT_APP_API_URL in .env
```

## 📖 Documentation

- [LangGraph Docs](https://github.com/langchain-ai/langgraph)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Redux Docs](https://redux.js.org/)
- [Groq API Docs](https://console.groq.com/docs)

## 🎓 Key Learnings

This project demonstrates:
1. **AI Integration**: Using LLMs with structured tools for CRM automation
2. **Full-Stack Development**: Modern React + FastAPI architecture
3. **State Management**: Redux for complex application state
4. **LangGraph**: Building agentic workflows with AI tools
5. **Database Design**: Relational schemas for healthcare data
6. **API Design**: RESTful endpoints with proper validation

## 📄 License

This project is provided as-is for the assignment round.

## 👤 Author

Created for the AI Applications Role Assignment Round

---

**Last Updated**: May 2024
**Version**: 1.0.0
