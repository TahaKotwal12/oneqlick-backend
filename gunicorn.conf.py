"""
Gunicorn configuration file for OneQlick Backend
Production-ready settings for Railway/AWS deployment
"""

import multiprocessing
import os

# ============================================
# Server Socket
# ============================================
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
backlog = 2048

# ============================================
# Worker Processes
# ============================================
# Calculate workers based on CPU cores
workers = int(os.getenv('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 300  # Increased from 120 to 300 for email sending
keepalive = 5

# ============================================
# Logging
# ============================================
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# ============================================
# Process Naming
# ============================================
proc_name = 'oneqlick-backend'

# ============================================
# Server Mechanics
# ============================================
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# ============================================
# SSL (if needed)
# ============================================
# keyfile = None
# certfile = None

# ============================================
# Server Hooks
# ============================================
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting OneQlick Backend Server")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading OneQlick Backend Server")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Server is ready. Spawning workers")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("Forked child, re-executing.")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info(f"Worker received INT or QUIT signal (pid: {worker.pid})")

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info(f"Worker received SIGABRT signal (pid: {worker.pid})")
