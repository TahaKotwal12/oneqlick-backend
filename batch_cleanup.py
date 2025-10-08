#!/usr/bin/env python3
"""
Standalone Batch Cleanup Script for Unverified Users

This script can be run independently to clean up unverified users from the pending_users table
if they already exist in the main users table with the same email address.

Usage:
    python batch_cleanup.py [--interval HOURS] [--run-once] [--daemon]

Options:
    --interval HOURS    Set the cleanup interval in hours (default: 1)
    --run-once         Run cleanup once and exit
    --daemon           Run as a daemon process (continuous)
"""

import sys
import os
import argparse
import signal
import time
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.batch_cleanup_service import BatchCleanupService
from app.config.logger import get_logger

logger = get_logger(__name__)


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    if 'cleanup_service' in globals():
        cleanup_service.stop()
    sys.exit(0)


def main():
    """Main function to run the batch cleanup."""
    parser = argparse.ArgumentParser(description='Batch Cleanup for Unverified Users')
    parser.add_argument('--interval', type=int, default=1, 
                       help='Cleanup interval in hours (default: 1)')
    parser.add_argument('--run-once', action='store_true',
                       help='Run cleanup once and exit')
    parser.add_argument('--daemon', action='store_true',
                       help='Run as a daemon process (continuous)')
    
    args = parser.parse_args()
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create cleanup service
    cleanup_service = BatchCleanupService(interval_hours=args.interval)
    
    try:
        if args.run_once:
            # Run once and exit
            logger.info("Running one-time cleanup...")
            deleted_count = cleanup_service.run_cleanup_now()
            logger.info(f"One-time cleanup completed. Deleted {deleted_count} records.")
            
        elif args.daemon:
            # Run as daemon
            logger.info(f"Starting batch cleanup daemon with {args.interval} hour interval...")
            cleanup_service.start()
            
            # Keep the main thread alive
            try:
                while True:
                    time.sleep(60)  # Check every minute
                    if not cleanup_service.running:
                        break
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, shutting down...")
                cleanup_service.stop()
                
        else:
            # Default: run once
            logger.info("Running cleanup (use --daemon for continuous mode)...")
            deleted_count = cleanup_service.run_cleanup_now()
            logger.info(f"Cleanup completed. Deleted {deleted_count} records.")
            
    except Exception as e:
        logger.error(f"Error in batch cleanup: {str(e)}")
        sys.exit(1)
        
    logger.info("Batch cleanup script finished.")


if __name__ == "__main__":
    main()
