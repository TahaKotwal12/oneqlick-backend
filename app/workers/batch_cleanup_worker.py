"""
Batch Cleanup Worker

This worker integrates the batch cleanup service with the main application.
It can be started as part of the application startup or as a separate worker process.
"""

import threading
import time
from app.services.batch_cleanup_service import BatchCleanupService
from app.config.logger import get_logger

logger = get_logger(__name__)


class BatchCleanupWorker:
    """Worker class to manage the batch cleanup service."""
    
    def __init__(self, interval_hours: int = 1):
        """
        Initialize the batch cleanup worker.
        
        Args:
            interval_hours (int): Hours between cleanup runs. Default is 1 hour.
        """
        self.cleanup_service = BatchCleanupService(interval_hours=interval_hours)
        self.worker_thread = None
        self.running = False
        
    def start(self):
        """Start the batch cleanup worker."""
        if self.running:
            logger.warning("Batch cleanup worker is already running")
            return
            
        self.running = True
        self.worker_thread = threading.Thread(target=self._run_worker, daemon=True)
        self.worker_thread.start()
        logger.info("Batch cleanup worker started")
        
    def stop(self):
        """Stop the batch cleanup worker."""
        if not self.running:
            logger.warning("Batch cleanup worker is not running")
            return
            
        self.running = False
        self.cleanup_service.stop()
        
        if self.worker_thread:
            self.worker_thread.join(timeout=10)
            
        logger.info("Batch cleanup worker stopped")
        
    def _run_worker(self):
        """Main worker loop."""
        try:
            self.cleanup_service.start()
            
            # Keep the worker alive
            while self.running and self.cleanup_service.running:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error in batch cleanup worker: {str(e)}")
            self.running = False
            
    def get_status(self) -> dict:
        """Get the status of the batch cleanup worker."""
        return {
            "worker_running": self.running,
            "cleanup_service_status": self.cleanup_service.get_status()
        }


# Global worker instance
batch_cleanup_worker = BatchCleanupWorker(interval_hours=1)


def start_batch_cleanup_worker():
    """Start the batch cleanup worker."""
    batch_cleanup_worker.start()


def stop_batch_cleanup_worker():
    """Stop the batch cleanup worker."""
    batch_cleanup_worker.stop()


def get_worker_status():
    """Get the worker status."""
    return batch_cleanup_worker.get_status()
