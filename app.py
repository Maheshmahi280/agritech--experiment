#!/usr/bin/env python
"""
AgriConnect Django Application Entry Point
Suitable for Hugging Face Spaces and container deployments

This script handles Django setup and starts the Gunicorn server.
For Hugging Face Spaces, the default port is 7860.
"""

import os
import sys
import subprocess
from pathlib import Path

# Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
PORT = int(os.getenv('PORT', 7860))  # Default HF Spaces port
WORKERS = 1 if DEBUG else 2
PROJECT_ROOT = Path(__file__).parent

def setup_django():
    """Setup Django environment."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriconnect.settings')
    
    # Add project to path
    backend_path = PROJECT_ROOT / 'myproject' / 'backend'
    if backend_path.exists():
        sys.path.insert(0, str(backend_path.parent))

def run_migrations():
    """Run Django database migrations."""
    try:
        print("🔄 Running database migrations...")
        result = subprocess.run(
            [sys.executable, 'backend/manage.py', 'migrate', '--noinput'],
            cwd=PROJECT_ROOT / 'myproject',
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ Migrations completed successfully")
            return True
        else:
            print(f"⚠️  Warning: Migration returned non-zero status")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return True  # Don't fail startup
            
    except subprocess.TimeoutExpired:
        print("⚠️  Migrations timed out, continuing anyway...")
        return True
    except Exception as e:
        print(f"⚠️  Migration error: {e}, continuing...")
        return True

def collect_static_files():
    """Collect static files for production."""
    try:
        print("📦 Collecting static files...")
        result = subprocess.run(
            [sys.executable, 'backend/manage.py', 'collectstatic', '--noinput', '--clear'],
            cwd=PROJECT_ROOT / 'myproject',
            capture_output=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Static files collected")
            return True
        else:
            print("⚠️  Warning: Static file collection had issues")
            return True  # Don't fail startup
            
    except subprocess.TimeoutExpired:
        print("⚠️  Static file collection timed out")
        return True
    except Exception as e:
        print(f"⚠️  Static file collection error: {e}")
        return True

def start_server():
    """Start Gunicorn web server."""
    print(f"\n🚀 Starting AgriConnect on port {PORT}...")
    print(f"   Workers: {WORKERS}")
    print(f"   Debug: {DEBUG}")
    print(f"   Access: http://localhost:{PORT}\n")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            '--bind', f'0.0.0.0:{PORT}',
            '--workers', str(WORKERS),
            '--worker-class', 'sync',
            '--worker-tmp-dir', '/dev/shm',  # Use shared memory for worker temp files
            '--timeout', '120' if DEBUG else '60',
            '--max-requests', '100' if DEBUG else '1000',
            '--max-requests-jitter', '50',
            '--keep-alive', '5',
            '--access-logfile', '-',
            '--error-logfile', '-',
            '--log-level', 'debug' if DEBUG else 'info',
            '--statsd-host', 'localhost:8125',
            'backend.agriconnect.wsgi:application'
        ], cwd=PROJECT_ROOT / 'myproject')
        
    except KeyboardInterrupt:
        print("\n\n✋ Shutdown signal received")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

def main():
    """Main entry point."""
    print("=" * 60)
    print("🌾 AgriConnect - Container Startup")
    print("=" * 60)
    
    # Setup Django
    print("\n📋 Setting up Django environment...")
    setup_django()
    
    # Change to project directory
    project_dir = PROJECT_ROOT / 'myproject'
    if project_dir.exists():
        os.chdir(project_dir)
        print(f"📂 Working directory: {os.getcwd()}")
    else:
        print(f"📂 Working directory: {PROJECT_ROOT}")
        os.chdir(PROJECT_ROOT)
    
    # Run startup tasks
    print("\n🔧 Running startup tasks...")
    run_migrations()
    collect_static_files()
    
    # Start server
    print("\n" + "=" * 60)
    start_server()

if __name__ == '__main__':
    main()
