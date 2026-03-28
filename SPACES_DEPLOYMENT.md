# Hugging Face Spaces Deployment Guide

Step-by-step instructions for deploying AgriConnect to Hugging Face Spaces.

## Prerequisites

- GitHub account with your AgriConnect repository
- Hugging Face account (free)
- Repository must be public or you need HF push access

## Quick Setup (5 minutes)

### 1. Create New Space

1. Visit https://huggingface.co/new-space
2. Fill in details:
   - **Owner**: Your username or organization
   - **Space name**: `agriconnect` (or custom name)
   - **License**: Choose (e.g., MIT)
   - **Space SDK**: Docker
3. Click "Create Space"

### 2. Enable GitHub Integration

1. In Space settings, click "Repository settings"
2. Enable "Persistent data storage"
3. Under "Linked Repository", enter:
   - GitHub repository URL: `https://github.com/your-username/your-repo`
4. Space will sync with GitHub

### 3. Add Secrets

In Space settings → "Repository secrets", add these environment variables:

```
SECRET_KEY=<generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">

DEBUG=False

ALLOWED_HOSTS=<your-space-name>.hf.space

DATABASE_URL=sqlite:////data/db.sqlite3

ENVIRONMENT=production

LOG_LEVEL=INFO
```

### 4. Create app.py

In **root of repository**, create `app.py`:

```python
#!/usr/bin/env python
"""
Hugging Face Spaces entry point for AgriConnect
Runs on the Spaces allocated port (7860)
"""

import subprocess
import os
import signal
import sys
import time

def main():
    # Change to project directory
    os.chdir('/app/myproject' if os.path.exists('/app/myproject') else '/app')
    
    # Run migrations
    print("🔄 Running database migrations...")
    result = subprocess.run(
        [sys.executable, 'backend/manage.py', 'migrate'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"⚠️  Migration warning:\n{result.stderr}")
    
    # Collect static files
    print("📦 Collecting static files...")
    subprocess.run(
        [sys.executable, 'backend/manage.py', 'collectstatic', '--noinput', '--clear'],
        capture_output=True
    )
    
    # Start Gunicorn on port 7860 (Spaces default)
    print("🚀 Starting AgriConnect server on port 7860...")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            '--bind', '0.0.0.0:7860',
            '--workers', '1',
            '--worker-class', 'sync',
            '--timeout', '60',
            '--max-requests', '1000',
            '--access-logfile', '-',
            '--error-logfile', '-',
            'backend.agriconnect.wsgi:application'
        ])
    except KeyboardInterrupt:
        print("\n✋ Shutdown signal received")
        sys.exit(0)

if __name__ == '__main__':
    main()
```

### 5. Update Dockerfile (Optional)

If using Docker, ensure Dockerfile is in root with proper configuration:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "app.py"]
```

### 6. Push to GitHub

```bash
# Commit all changes
git add .
git commit -m "Add HF Spaces deployment support"
git push origin main
```

Space will auto-build and deploy!

---

## Access Your Space

Once deployed:

- **URL**: `https://your-username-agriconnect.hf.space`
- **Admin**: `https://your-username-agriconnect.hf.space/admin/`
- **API**: All endpoints available at base URL

## Features in Spaces

✅ **Persistent Storage**: Database survives app restarts  
✅ **GPU Support**: Optional for ML compute  
✅ **Free Tier**: Generous free usage  
✅ **Auto-restart**: Keeps app running  
✅ **Custom Domain**: Available for paid tiers  
✅ **Collaboration**: Share with others

---

## Data & Files

### Database Location
- **SQLite**: `/data/db.sqlite3` (persistent)
- Data survives app restarts

### Directories
- `/app` - Application code
- `/data` - Persistent data storage
- `/tmp` - Ephemeral storage

### Persisting Files
In `docker-compose.yml` or Dockerfile:
```yaml
volumes:
  - /data:/app/data  # Persist database
```

---

## Troubleshooting

### App fails to start

**Check logs:**
- Click "App logs" in Space interface
- Look for migration errors or import issues

**Fix:**
- Ensure `app.py` is in repo root
- Verify Python version matches in requirements
- Check that imports work: `python -c "import django; print(django.__version__)"`

### Static files not loading

```bash
# Force collection
python backend/manage.py collectstatic --noinput --clear
```

### Database issues

```bash
# Reset database
rm /data/db.sqlite3

# Re-migrate
python backend/manage.py migrate
```

### Port issues

Spaces uses port 7860. Ensure code uses this:
```python
# ✅ Correct
gunicorn --bind 0.0.0.0:7860 ...

# ❌ Wrong
gunicorn --bind 0.0.0.0:8000 ...
```

---

## Example Workflow

### For Hackathon Demo

1. **Create Space** (public, anyone can fork)
2. **Add Secrets** (automated seeding data)
3. **Push Code** with demo setup:
   ```python
   # In management command
   if not User.objects.exists():
       create_demo_farmers()
       create_demo_restaurants()
   ```
4. **Share link**: `https://hf.space/your-space`
5. **Users can fork** and modify

### For Production(ish)

1. **Use private Space** (if needed)
2. **Use PostgreSQL** (paid tier or external)
3. **Enable custom domain**
4. **Set up monitoring**
5. **Regular backups** of `/data` folder

---

## Security Notes

🔐 **Spaces Features:**
- User authentication supported
- Environment variables kept secret
- HTTPS by default
- No direct filesystem access

⚠️ **Recommendations:**
- Change SECRET_KEY from .env.example
- Never commit .env file
- Use environment secrets for all credentials
- Review logs for sensitive data
- Enable session security in production

---

## Cost Considerations

**Free Tier:**
- 1 Space with 50GB storage
- Public or private (quota)
- Limited computational resources
- App idles after 24 hours of inactivity

**Pro Tier:**
- Multiple Spaces
- Custom domain
- More storage
- Always-on capability
- Priority support

---

## Useful Spaces Features

### Custom README

Create `README.md` in Space:
```markdown
# AgriConnect Hackathon Demo

[Your description here]

### Features
- Farmer management
- Restaurant ordering
- Real-time updates

### Access
- Admin: [link]
- User login available
```

### Streamlit Alternative

Instead of Django, can use Streamlit:
```python
# app.py
import streamlit as st
st.set_page_config(page_title="AgriConnect")
st.title("Welcome to AgriConnect!")
# ... rest of Streamlit code
```

But Django + app.py works well too!

---

## Example app.py for Django

Here's a production-ready version:

```python
#!/usr/bin/env python
"""
AgriConnect Django application for Hugging Face Spaces
Runs as container with Django/Gunicorn stack
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
PORT = 7860  # Spaces default
WORKERS = 1 if DEBUG else 2
PROJECT_DIR = Path('/app')

def setup_environment():
    """Initialize environment variables."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriconnect.settings')
    
def run_migrations():
    """Run Django migrations."""
    print("▶️  Running migrations...")
    result = subprocess.run(
        [sys.executable, 'backend/manage.py', 'migrate', '--noinput'],
        cwd=PROJECT_DIR
    )
    return result.returncode == 0

def collect_static():
    """Collect static files."""
    print("▶️  Collecting static files...")
    subprocess.run(
        [sys.executable, 'backend/manage.py', 'collectstatic', '--noinput', '--clear'],
        cwd=PROJECT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def start_server():
    """Start Gunicorn server."""
    print(f"▶️  Starting server on port {PORT}...")
    subprocess.run([
        sys.executable, '-m', 'gunicorn',
        '--bind', f'0.0.0.0:{PORT}',
        '--workers', str(WORKERS),
        '--worker-class', 'sync',
        '--timeout', '120' if DEBUG else '60',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--log-level', 'debug' if DEBUG else 'info',
        'backend.agriconnect.wsgi:application'
    ], cwd=PROJECT_DIR)

if __name__ == '__main__':
    setup_environment()
    
    # Change to project root
    os.chdir(PROJECT_DIR / 'myproject' if (PROJECT_DIR / 'myproject').exists() else PROJECT_DIR)
    
    # Setup
    print("🚀 Starting AgriConnect...")
    run_migrations()
    collect_static()
    
    # Start server
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n✋ Shutting down...")
        sys.exit(0)
```

---

## Deployment Timeline

| Time | Step | Status |
|------|------|--------|
| 0m | Create Space | ⏳ 1-2 min |
| 2m | Add secrets | ⏳ 2 min |
| 4m | Create app.py | ⏳ 2 min |
| 6m | Push to GitHub | ⏳ Auto-deploy 5-10 min |
| 16m | ✅ App live! | 🎉 Ready |

---

## Next Steps

1. ✅ Deploy to Spaces
2. ✅ Test all features
3. ✅ Share demo link
4. ✅ Collect feedback
5. 📝 Iterate and improve

---

**Happy deploying! 🚀**

For more: https://huggingface.co/docs/hub/spaces
