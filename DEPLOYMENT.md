# AgriConnect Deployment Guide

Complete instructions for deploying AgriConnect to various platforms.

## Quick Start

### Local Development with Docker

```bash
# Clone and navigate
cd myproject

# Copy environment template
cp .env.example .env

# Start services
docker-compose up --build

# Access the app
open http://localhost:8000
```

### Local Development (Native)

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
cd backend
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## Deployment Platforms

### 1. Hugging Face Spaces (Recommended for Hackathon)

**Advantages:**
- Free tier available
- Easy GitHub integration
- Built-in computation resources
- Perfect for demos

**Setup Steps:**

1. **Create Space**
   - Go to https://huggingface.co/new-space
   - Choose "Docker" runtime
   - Set up GitHub integration

2. **Add Secrets in Space Settings**
   ```
   SECRET_KEY=<generate-new-key>
   DEBUG=False
   ALLOWED_HOSTS=your-space-name.hf.space
   DATABASE_URL=sqlite:////data/db.sqlite3
   ENVIRONMENT=production
   ```

3. **Create `app.py` in root**
   ```python
   import subprocess
   import os

   # Set up database
   os.system("python backend/manage.py migrate")

   # Run server
   subprocess.run([
       "gunicorn",
       "--bind", "0.0.0.0:7860",
       "--workers", "1",
       "backend.agriconnect.wsgi:application"
   ])
   ```

4. **Push to GitHub**
   - Hugging Face will auto-build and deploy

**Access:** `https://your-username-space-name.hf.space`

---

### 2. Render.com (Best for Production)

**Advantages:**
- PostgreSQL database included
- Free tier available
- Better performance
- Production-ready

**Setup Steps:**

1. **Push code to GitHub**

2. **Create new Web Service**
   - Connect your GitHub repo
   - Choose "Python"
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -b 0.0.0.0 -w 3 backend.agriconnect.wsgi:application`

3. **Set Environment Variables**
   ```
   SECRET_KEY=<generate-new-key>
   DEBUG=False
   ALLOWED_HOSTS=your-app.onrender.com
   DATABASE_URL=<render-postgresql-url>
   ENVIRONMENT=production
   PYTHON_VERSION=3.11
   ```

4. **Create PostgreSQL Database** (optional)
   - Add PostgreSQL service
   - Copy DATABASE_URL to web service

5. **Run Migrations**
   - In Render dashboard, add build command:
     ```
     pip install -r requirements.txt && python backend/manage.py migrate
     ```

**Access:** `https://your-app.onrender.com`

---

### 3. Docker (Local or Cloud)

**Build Image:**
```bash
docker build -t agriconnect:latest .
```

**Run Container:**
```bash
docker run -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost:8000 \
  agriconnect:latest
```

**With Docker Compose:**
```bash
docker-compose up --build
```

---

### 4. AWS (EC2 with Docker)

**Setup:**

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier)
   - Security group: Allow 80, 443, 8000

2. **SSH into instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   ```

4. **Clone and Deploy**
   ```bash
   git clone https://github.com/your-repo/agriconnect.git
   cd agriconnect/myproject
   cp .env.example .env
   # Edit .env with production values
   docker-compose up -d
   ```

5. **Set up SSL (Let's Encrypt)**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot certonly --standalone -d your-domain.com
   ```

---

### 5. Heroku (Legacy - No Free Tier)

**Setup:**
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set config
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python backend/manage.py migrate
```

---

## Environment Variable Reference

### Required Variables
- **SECRET_KEY**: Django secret key (generate fresh for each deployment)
- **DEBUG**: Set to `False` in production

### Recommended Variables
- **ALLOWED_HOSTS**: Comma-separated allowed domains
- **DATABASE_URL**: Database connection string
- **ENVIRONMENT**: `development`, `staging`, or `production`

### Optional Variables
- **SENTRY_DSN**: Error tracking
- **LOG_LEVEL**: Logging level (DEBUG, INFO, WARNING, ERROR)
- **SESSION_COOKIE_SECURE**: Set to `True` with HTTPS
- **SECURE_HSTS_SECONDS**: HSTS max age (production)

---

## Security Checklist

- [ ] **Secret Key**: Generated fresh, not committed to repo
- [ ] **DEBUG Mode**: Set to `False` in production
- [ ] **ALLOWED_HOSTS**: Configured correctly for your domain
- [ ] **Database**: Using strong password, not exposed
- [ ] **SSL/HTTPS**: Enabled on production
- [ ] **Static Files**: Served with WhiteNoise or CDN
- [ ] **CSRF Protection**: Django middleware enabled
- [ ] **Session Security**: `HTTPONLY` and `SECURE` flags enabled
- [ ] **Dependencies**: Updated and vetted
- [ ] **Secrets**: Never committed to version control
- [ ] **Logs**: Checked for sensitive data leaks

---

## Production Best Practices

### 1. Database
```bash
# Use PostgreSQL for production (not SQLite)
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 2. Static Files
- Use WhiteNoise (already in requirements.txt)
- Or serve from CDN (CloudFront, S3, etc.)

### 3. Worker Configuration
```bash
# Gunicorn settings (adjust for your capacity)
workers=3              # 2-4 per CPU core
worker_class=sync     # Use 'gevent' for async
timeout=60            # Request timeout
max_requests=1000     # Worker restart interval
```

### 4. Monitoring
- Set up error tracking (Sentry)
- Configure logging
- Monitor server resources
- Set up alerts

### 5. Backups
```bash
# Backup SQLite database
docker exec agriconnect_web cp /app/backend/db.sqlite3 /data/backup/db.sqlite3
```

---

## Troubleshooting

### Port Already in Use
```bash
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Migration Issues
```bash
# Reset migrations (development only!)
python backend/manage.py migrate core zero
python backend/manage.py migrate
```

### Static Files Not Loading
```bash
# Collect static files
python backend/manage.py collectstatic --noinput --clear
```

### Database Locked (SQLite)
```bash
# SQLite is not great for concurrent access
# Switch to PostgreSQL for production
DATABASE_URL=postgresql://...
```

### Memory Issues in Container
```bash
# Reduce workers
# In Dockerfile or Procfile
gunicorn --workers 1 ...  # Production: 2-4
```

---

## Scaling Considerations

### SQLite → PostgreSQL
Before scaling beyond single container:
```bash
# Create PostgreSQL database
# Set DATABASE_URL
python backend/manage.py migrate
```

### Single Container → Multiple Containers
Use orchestration platform:
- Render (recommended for beginners)
- AWS ECS
- Google Cloud Run
- Kubernetes

### Caching Layer
Enable Redis:
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

---

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Secret key generated and set
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Debug mode disabled
- [ ] Allowed hosts configured
- [ ] SSL certificate installed (HTTPS)
- [ ] Error tracking configured
- [ ] Backups scheduled
- [ ] Monitoring/alerts set up
- [ ] Database backed up pre-deployment
- [ ] Load tested with expected traffic
- [ ] Tested error pages (404, 500)
- [ ] Team trained on deployment process

---

## Support & Resources

- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **Gunicorn**: https://gunicorn.org/
- **Docker**: https://docs.docker.com/
- **Render Docs**: https://render.com/docs
- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces

---

**Last Updated**: 2026-03-28  
**Status**: Production Ready
