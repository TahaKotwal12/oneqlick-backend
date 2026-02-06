# Update .env with Upstash Redis Configuration
# Run this script to automatically update your Redis settings

$envFile = ".env"
$backupFile = ".env.backup"

# Create backup
Write-Host "Creating backup of .env file..." -ForegroundColor Yellow
Copy-Item $envFile $backupFile -Force
Write-Host "✓ Backup created: $backupFile" -ForegroundColor Green

# Read current .env content
$content = Get-Content $envFile

# Upstash Redis credentials
$upstashHost = "still-opossum-21235.upstash.io"
$upstashPort = "6379"
$upstashPassword = "AVLzAAIncDJiZWYxMzFiYjVmOTg0NjVmYTM3YmQ2OGY2ZjJjYTQwMXAyMjEyMzU"

Write-Host "`nUpdating Redis configuration..." -ForegroundColor Yellow

# Update Redis configuration
$newContent = $content | ForEach-Object {
    if ($_ -match "^REDIS_HOST=") {
        "REDIS_HOST=$upstashHost"
    }
    elseif ($_ -match "^REDIS_PORT=") {
        "REDIS_PORT=$upstashPort"
    }
    elseif ($_ -match "^REDIS_PASSWORD=") {
        "REDIS_PASSWORD=$upstashPassword"
    }
    elseif ($_ -match "^REDIS_USE_TLS=") {
        "REDIS_USE_TLS=true"
    }
    else {
        $_
    }
}

# Check if REDIS_USE_TLS exists, if not add it after REDIS_PASSWORD
if ($newContent -notmatch "REDIS_USE_TLS=") {
    $updatedContent = @()
    foreach ($line in $newContent) {
        $updatedContent += $line
        if ($line -match "^REDIS_PASSWORD=") {
            $updatedContent += "REDIS_USE_TLS=true"
        }
    }
    $newContent = $updatedContent
}

# Write updated content
$newContent | Set-Content $envFile

Write-Host "✓ Redis configuration updated!" -ForegroundColor Green
Write-Host "`nNew Redis settings:" -ForegroundColor Cyan
Write-Host "  REDIS_HOST=$upstashHost" -ForegroundColor White
Write-Host "  REDIS_PORT=$upstashPort" -ForegroundColor White
Write-Host "  REDIS_PASSWORD=$upstashPassword" -ForegroundColor White
Write-Host "  REDIS_USE_TLS=true" -ForegroundColor White

Write-Host "`n✓ Configuration complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Review the changes in .env file" -ForegroundColor White
Write-Host "  2. Test locally: docker-compose up" -ForegroundColor White
Write-Host "  3. Deploy to EC2: git push origin main" -ForegroundColor White
Write-Host "`nTo rollback: Copy-Item .env.backup .env -Force" -ForegroundColor Gray
