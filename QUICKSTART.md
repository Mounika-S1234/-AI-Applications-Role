# Quick Start Guide

## 🚀 5-Minute Quick Start (Development)

### Prerequisites Check
```bash
python --version      # Should be 3.9+
node --version        # Should be 16+
```

### 1. Backend Setup (2 minutes)
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Mac/Linux
# OR
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env
echo "DATABASE_URL=postgresql://user:password@localhost/crm_hcp_db" >> .env

# Start backend
uvicorn app.main:app --reload
```

**Backend ready at**: http://localhost:8000

### 2. Frontend Setup (2 minutes)
```bash
# In new terminal
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env

# Start frontend
npm start
```

**Frontend ready at**: http://localhost:3000

### 3. Access Application (1 minute)
- Open browser: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Start using the application!

---

## 🔑 Getting Your Groq API Key

1. Visit https://console.groq.com
2. Sign up / Log in
3. Create new API key
4. Copy key and add to backend `.env`:
   ```
   GROQ_API_KEY=gsk_xxxxx
   ```

---

## 📦 Docker Quick Start

```bash
# Build and start all services
docker-compose up --build

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

## 🎯 Key Workflows

### Logging an Interaction (Chat)
1. Select HCP from sidebar
2. Click "Chat Interface" tab
3. Type interaction description
4. AI generates summary and action items

### Logging an Interaction (Form)
1. Select HCP from sidebar
2. Click "Structured Form" tab
3. Fill in interaction details
4. Click "Log Interaction"

### Viewing History
1. Select HCP from sidebar
2. Click "History" tab
3. View all past interactions with summaries

---

## 🔧 Configuration

### Backend Environment Variables
```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://user:password@localhost/crm_hcp_db
```

### Frontend Environment Variables
```env
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 📚 API Examples

### Create HCP
```bash
curl -X POST http://localhost:8000/api/hcps/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. John Smith",
    "specialty": "Cardiology",
    "email": "john@example.com"
  }'
```

### Log Interaction via Chat
```bash
curl -X POST http://localhost:8000/api/chat/log-interaction \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Had a great call with Dr. Smith about new medication",
    "hcp_id": 1
  }'
```

### Get HCP Interactions
```bash
curl http://localhost:8000/api/interactions/hcp/1
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check Python version, install dependencies |
| Frontend shows API error | Verify backend is running, check REACT_APP_API_URL |
| GROQ API errors | Verify API key in .env, check quota |
| Database connection error | Ensure PostgreSQL is running, check DATABASE_URL |

---

## 📖 Next Steps

1. **Create some HCPs** - Start building your database
2. **Log interactions** - Try both chat and form interfaces
3. **Review AI tools** - Check extracted entities and summaries
4. **Deploy to production** - Follow DEPLOYMENT.md

---

## 🎓 Learning Resources

- Backend docs: [FastAPI](https://fastapi.tiangolo.com/)
- Frontend docs: [React](https://react.dev/) & [Redux](https://redux.js.org/)
- AI framework: [LangGraph](https://github.com/langchain-ai/langgraph)
- LLM API: [Groq Docs](https://console.groq.com/docs)

---

**Happy coding! 🚀**
