@echo off
REM Batch Cleanup Runner for Windows
REM This script provides easy access to the batch cleanup functionality

echo ========================================
echo ONE-QLICK BATCH CLEANUP SYSTEM
echo ========================================
echo.

if "%1"=="demo" (
    echo Running demo...
    python demo_batch_cleanup.py
    goto :end
)

if "%1"=="test" (
    echo Running test...
    python test_batch_cleanup.py
    goto :end
)

if "%1"=="once" (
    echo Running one-time cleanup...
    python batch_cleanup.py --run-once
    goto :end
)

if "%1"=="daemon" (
    echo Starting daemon mode...
    python batch_cleanup.py --daemon --interval 1
    goto :end
)

echo Usage:
echo   run_batch_cleanup.bat demo    - Run demonstration
echo   run_batch_cleanup.bat test    - Run test (dry run)
echo   run_batch_cleanup.bat once    - Run cleanup once
echo   run_batch_cleanup.bat daemon  - Start daemon mode
echo.
echo Examples:
echo   run_batch_cleanup.bat demo
echo   run_batch_cleanup.bat test
echo   run_batch_cleanup.bat once
echo   run_batch_cleanup.bat daemon

:end
pause
