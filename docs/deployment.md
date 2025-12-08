# Deployment Guide

## Production Deployment Options

This guide covers various deployment strategies for the Hybrid-Analyzer application.

---

## Option 1: Docker Compose (Recommended for Small-Medium Scale)

### Prerequisites
- Docker and Docker Compose installed
- Domain name (optional)
- SSL certificate (recommended)

### Steps

1. **Clone and Configure**
   ```bash
   git clone <repository>
   cd Hybrid-Analyzer
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Update Environment**
   ```env
   DATABASE_URL=postgresql://user:password@postgres:5432/hybrid_analyzer
   JWT_SECRET=<generate-strong-secret>
   HUGGINGFACE_API_TOKEN=<your-token>
   GEMINI_API_KEY=<your-key>
   CORS_ORIGINS=["https://yourdomain.com"]
   ```

3. **Deploy**
   ```bash
   docker-compose up -d
   ```

4. **Setup Reverse Proxy (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:3000;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
       }
   }
   ```

5. **Enable HTTPS**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

---

## Option 2: Cloud Deployment (AWS)

### Architecture
```
Internet → ALB → ECS (Frontend + Backend) → RDS (PostgreSQL)
```

### Steps

1. **Create RDS Instance**
   ```bash
   aws rds create-db-instance \
     --db-instance-identifier hybrid-analyzer-db \
     --db-instance-class db.t3.micro \
     --engine postgres \
     --master-username admin \
     --master-user-password <password>
   ```

2. **Build and Push Images**
   ```bash
   # Backend
   docker build -t hybrid-analyzer-backend ./backend
   docker tag hybrid-analyzer-backend:latest <ecr-url>/backend:latest
   docker push <ecr-url>/backend:latest
   
   # Frontend
   docker build -t hybrid-analyzer-frontend ./frontend
   docker tag hybrid-analyzer-frontend:latest <ecr-url>/frontend:latest
   docker push <ecr-url>/frontend:latest
   ```

3. **Create ECS Task Definition**
   ```json
   {
     "family": "hybrid-analyzer",
     "containerDefinitions": [
       {
         "name": "backend",
         "image": "<ecr-url>/backend:latest",
         "portMappings": [{"containerPort": 8000}],
         "environment": [...]
       },
       {
         "name": "frontend",
         "image": "<ecr-url>/frontend:latest",
         "portMappings": [{"containerPort": 80}]
       }
     ]
   }
   ```

4. **Create ECS Service**
   ```bash
   aws ecs create-service \
     --cluster hybrid-analyzer \
     --service-name hybrid-analyzer-service \
     --task-definition hybrid-analyzer \
     --desired-count 2
   ```

---

## Option 3: Kubernetes Deployment

### Prerequisites
- Kubernetes cluster
- kubectl configured
- Helm (optional)

### Deployment Files

**backend-deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: hybrid-analyzer-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
```

**frontend-deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: hybrid-analyzer-frontend:latest
        ports:
        - containerPort: 80
```

**Deploy:**
```bash
kubectl apply -f k8s/
kubectl expose deployment backend --type=LoadBalancer --port=8000
kubectl expose deployment frontend --type=LoadBalancer --port=80
```

---

## Environment Variables (Production)

### Required
```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# JWT
JWT_SECRET=<64-char-random-string>

# AI APIs
HUGGINGFACE_API_TOKEN=<token>
GEMINI_API_KEY=<key>

# CORS
CORS_ORIGINS=["https://yourdomain.com"]
```

### Optional
```env
# Timeouts
HUGGINGFACE_TIMEOUT=30
GEMINI_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
```

---

## Security Checklist

- [ ] Strong JWT secret (min 64 characters)
- [ ] HTTPS enabled
- [ ] Database credentials secured
- [ ] API keys in environment variables
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Firewall rules configured
- [ ] Regular security updates
- [ ] Backup strategy in place

---

## Monitoring

### Logging
```bash
# Docker Compose
docker-compose logs -f backend

# Kubernetes
kubectl logs -f deployment/backend
```

### Health Checks
```bash
# Backend
curl http://localhost:8000/health

# Database
docker exec -it hybrid-analyzer-db pg_isready
```

### Metrics (Optional)
- Prometheus for metrics collection
- Grafana for visualization
- ELK stack for log aggregation

---

## Backup Strategy

### Database Backups
```bash
# Manual backup
docker exec hybrid-analyzer-db pg_dump -U postgres hybrid_analyzer > backup.sql

# Automated (cron)
0 2 * * * docker exec hybrid-analyzer-db pg_dump -U postgres hybrid_analyzer > /backups/$(date +\%Y\%m\%d).sql
```

### Restore
```bash
docker exec -i hybrid-analyzer-db psql -U postgres hybrid_analyzer < backup.sql
```

---

## Scaling

### Horizontal Scaling
```bash
# Docker Compose
docker-compose up -d --scale backend=3

# Kubernetes
kubectl scale deployment backend --replicas=5
```

### Load Balancing
- Use Nginx or cloud load balancer
- Session affinity not required (stateless JWT)

---

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Common issues:
# - Database not ready (wait for health check)
# - Missing environment variables
# - Port already in use
```

### Database connection failed
```bash
# Test connection
docker exec -it hybrid-analyzer-db psql -U postgres

# Check network
docker network inspect hybrid-network
```

### Frontend can't reach backend
```bash
# Check CORS settings
# Verify API_URL in frontend environment
# Check network connectivity
```

---

## Performance Optimization

### Database
- Enable connection pooling
- Add indexes on frequently queried fields
- Use read replicas for scaling

### Backend
- Increase worker processes
- Enable response caching
- Use async operations

### Frontend
- Enable Nginx gzip compression
- Use CDN for static assets
- Implement browser caching

---

## Cost Optimization

### AWS
- Use Reserved Instances for predictable workloads
- Auto-scaling for variable load
- S3 for static assets
- CloudFront CDN

### API Costs
- Cache frequent analyses
- Implement rate limiting
- Monitor usage quotas

---

## Maintenance

### Updates
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Database Migrations
```bash
# Using Alembic
cd backend
alembic upgrade head
```

---

## Support

For deployment issues:
1. Check logs first
2. Review environment variables
3. Verify network connectivity
4. Check API quotas
5. Consult documentation
