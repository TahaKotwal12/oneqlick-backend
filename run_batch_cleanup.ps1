# Batch Cleanup Runner for PowerShell
# This script provides easy access to the batch cleanup functionality

param(
    [Parameter(Position=0)]
    [ValidateSet("demo", "test", "once", "daemon")]
    [string]$Action = "help"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ONE-QLICK BATCH CLEANUP SYSTEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

switch ($Action) {
    "demo" {
        Write-Host "Running demo..." -ForegroundColor Yellow
        python demo_batch_cleanup.py
    }
    "test" {
        Write-Host "Running test..." -ForegroundColor Yellow
        python test_batch_cleanup.py
    }
    "once" {
        Write-Host "Running one-time cleanup..." -ForegroundColor Yellow
        python batch_cleanup.py --run-once
    }
    "daemon" {
        Write-Host "Starting daemon mode..." -ForegroundColor Yellow
        python batch_cleanup.py --daemon --interval 1
    }
    default {
        Write-Host "Usage:" -ForegroundColor Green
        Write-Host "  .\run_batch_cleanup.ps1 demo    - Run demonstration" -ForegroundColor White
        Write-Host "  .\run_batch_cleanup.ps1 test    - Run test (dry run)" -ForegroundColor White
        Write-Host "  .\run_batch_cleanup.ps1 once    - Run cleanup once" -ForegroundColor White
        Write-Host "  .\run_batch_cleanup.ps1 daemon  - Start daemon mode" -ForegroundColor White
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Green
        Write-Host "  .\run_batch_cleanup.ps1 demo" -ForegroundColor White
        Write-Host "  .\run_batch_cleanup.ps1 test" -ForegroundColor White
        Write-Host "  .\run_batch_cleanup.ps1 once" -ForegroundColor White
        Write-Host "  .\run_batch_cleanup.ps1 daemon" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
