@echo off
echo ========================================
echo ONE-QLICK BACKEND SERVER WITH BATCH CLEANUP
echo ========================================
echo.
echo Starting server on port 8001...
echo.
echo Server URLs:
echo   Main: http://localhost:8001
echo   Health: http://localhost:8001/health
echo   API Docs: http://localhost:8001/docs
echo   Batch Cleanup Status: http://localhost:8001/api/v1/batch-cleanup/status
echo.
echo Batch cleanup service will run automatically every hour.
echo Press Ctrl+C to stop the server.
echo.

python start_server.py

pause
