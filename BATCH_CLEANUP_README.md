# Batch Cleanup System for Unverified Users

This system automatically cleans up unverified users from the `pending_users` table if they already exist in the main `users` table with the same email address.

## Overview

The batch cleanup system consists of:
- **BatchCleanupService**: Core service that performs the cleanup operations
- **BatchCleanupWorker**: Worker that manages the service lifecycle
- **Standalone Scripts**: Scripts for manual execution and testing

## Features

- ✅ Automatic cleanup every hour (configurable)
- ✅ Dry run mode for testing
- ✅ Comprehensive logging
- ✅ Graceful shutdown handling
- ✅ No external dependencies (uses only built-in Python libraries)
- ✅ Thread-safe operation

## Usage

### 1. Standalone Script (Recommended for Production)

#### Run Once
```bash
cd oneqlick-backend
python batch_cleanup.py --run-once
```

#### Run as Daemon (Continuous)
```bash
cd oneqlick-backend
python batch_cleanup.py --daemon --interval 1
```

#### Custom Interval
```bash
cd oneqlick-backend
python batch_cleanup.py --daemon --interval 2  # Run every 2 hours
```

### 2. Test the System

#### Dry Run Test
```bash
cd oneqlick-backend
python test_batch_cleanup.py
```

This will show you how many records would be deleted without actually deleting them.

### 3. Integration with Main Application

To integrate with your main application, add this to your startup code:

```python
from app.workers.batch_cleanup_worker import start_batch_cleanup_worker

# Start the batch cleanup worker
start_batch_cleanup_worker()
```

## Configuration

### Environment Variables

The system uses the same database configuration as your main application:
- `DATABASE_URL`: PostgreSQL connection string
- `LOG_LEVEL`: Logging level (default: debug)

### Service Configuration

You can modify the cleanup interval by changing the `interval_hours` parameter:

```python
# In batch_cleanup_service.py
cleanup_service = BatchCleanupService(interval_hours=1)  # 1 hour interval
```

## How It Works

1. **Detection**: The service queries both tables to find emails that exist in both:
   - `core_mstr_one_qlick_users_tbl` (main users)
   - `core_mstr_one_qlick_pending_users_tbl` (pending users)

2. **Cleanup**: For each duplicate email found:
   - Deletes the record from the `pending_users` table
   - Logs the operation
   - Continues to the next duplicate

3. **Scheduling**: Runs automatically every hour (configurable)

## Database Tables

### Main Users Table
```sql
core_mstr_one_qlick_users_tbl
- user_id (UUID, Primary Key)
- email (VARCHAR, Unique)
- phone (VARCHAR, Unique)
- ... other fields
```

### Pending Users Table
```sql
core_mstr_one_qlick_pending_users_tbl
- pending_user_id (UUID, Primary Key)
- email (VARCHAR, Unique)
- phone (VARCHAR, Unique)
- ... other fields
```

## Logging

The system provides comprehensive logging:
- **INFO**: Normal operations, cleanup counts
- **DEBUG**: Detailed operation logs
- **ERROR**: Error conditions and exceptions
- **WARNING**: Non-critical issues

Logs are written to the same log file as your main application.

## Error Handling

- Database connection errors are logged and retried
- Individual record deletion errors don't stop the entire process
- Graceful shutdown on SIGINT/SIGTERM signals
- Transaction rollback on errors

## Monitoring

### Check Service Status
```python
from app.services.batch_cleanup_service import get_cleanup_status

status = get_cleanup_status()
print(f"Service running: {status['running']}")
print(f"Interval: {status['interval_hours']} hours")
```

### Manual Cleanup
```python
from app.services.batch_cleanup_service import run_cleanup_now

deleted_count = run_cleanup_now()
print(f"Deleted {deleted_count} records")
```

## Security Considerations

- Uses parameterized queries to prevent SQL injection
- Database transactions ensure data consistency
- No external API calls or dependencies
- Runs with the same database permissions as your main application

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check your `DATABASE_URL` environment variable
   - Ensure database is accessible
   - Check network connectivity

2. **Permission Denied**
   - Ensure the application has DELETE permissions on the pending_users table
   - Check database user permissions

3. **Service Not Starting**
   - Check log files for error messages
   - Ensure no other instance is running
   - Verify Python path and dependencies

### Debug Mode

Enable debug logging by setting:
```bash
export LOG_LEVEL=debug
```

## Performance

- Uses database indexes for efficient querying
- Processes records in batches
- Minimal memory footprint
- Non-blocking operation (runs in separate thread)

## Maintenance

### Regular Tasks
- Monitor log files for errors
- Check cleanup statistics
- Verify database performance

### Backup Considerations
- The system only deletes from `pending_users` table
- Main user data is never modified
- Consider backing up pending_users table before first run

## Support

For issues or questions:
1. Check the log files first
2. Run the test script to verify functionality
3. Check database connectivity and permissions
4. Review the configuration settings
