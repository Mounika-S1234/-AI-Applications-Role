# Deployment guide for production

## Prerequisites
- Docker & Docker Compose
- 2GB RAM minimum
- 1 CPU core minimum

## Quick Start with Docker

1. **Clone repository**
```bash
git clone <repo-url>
cd crm-hcp-system
```

2. **Configure environment**
```bash
cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
DB_USER=postgres
DB_PASSWORD=strong_password_here
EOF
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Access application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Variables

### Backend (.env)
```
GROQ_API_KEY=xxxxx
DATABASE_URL=postgresql://user:password@db:5432/crm_hcp_db
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Database Initialization

First run:
```bash
docker-compose exec backend python -c "from app.database import engine, Base; from app.models.models import *; Base.metadata.create_all(bind=engine)"
```

## Monitoring

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check services status
docker-compose ps
```

## Scaling

For production, use:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Backup & Restore

### Backup Database
```bash
docker-compose exec db pg_dump -U postgres crm_hcp_db > backup.sql
```

### Restore Database
```bash
docker-compose exec -T db psql -U postgres < backup.sql
```

## Security Checklist

- [ ] Change default database password
- [ ] Enable HTTPS (use nginx reverse proxy)
- [ ] Set GROQ_API_KEY securely
- [ ] Update CORS origins for production
- [ ] Enable database backups
- [ ] Set up monitoring and logging
- [ ] Use strong JWT secrets
- [ ] Enable rate limiting

## Performance Tuning

### Backend
- Increase gunicorn workers: `gunicorn -w 4`
- Enable caching layer (Redis)
- Optimize database queries

### Frontend
- Enable gzip compression
- Implement service worker for PWA
- Use CDN for static assets

## Troubleshooting

### Database connection error
```bash
docker-compose logs db
docker-compose restart db
```

### Backend failing to start
```bash
docker-compose exec backend python -c "import app.main"
```

### Frontend not loading
```bash
docker-compose logs frontend
docker-compose restart frontend
```

## Production Deployment

### AWS ECS
```bash
docker build -t crm-hcp-backend ./backend
docker tag crm-hcp-backend:latest <aws-account>.dkr.ecr.<region>.amazonaws.com/crm-hcp-backend:latest
docker push <aws-account>.dkr.ecr.<region>.amazonaws.com/crm-hcp-backend:latest
```

### Heroku
```bash
heroku create crm-hcp-app
heroku addons:create heroku-postgresql:standard-0
git push heroku main
```

### DigitalOcean App Platform
```bash
doctl apps create --spec app.yaml
```
