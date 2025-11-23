# Vercel Deployment Script for Windows PowerShell

Write-Host "🚀 Vercel Deployment Script" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Write-Host "❌ Vercel CLI not found!" -ForegroundColor Red
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
    Write-Host "✅ Vercel CLI installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Choose deployment option:" -ForegroundColor Yellow
Write-Host "1. Deploy Backend only"
Write-Host "2. Deploy Frontend only"
Write-Host "3. Deploy Both"
Write-Host ""
$choice = Read-Host "Enter choice (1-3)"

if ($choice -eq "1" -or $choice -eq "3") {
    Write-Host ""
    Write-Host "📦 Deploying Backend..." -ForegroundColor Cyan
    Set-Location "backend (3)\backend"
    vercel
    Set-Location ..\..\..
    Write-Host "✅ Backend deployment initiated" -ForegroundColor Green
}

if ($choice -eq "2" -or $choice -eq "3") {
    Write-Host ""
    Write-Host "📦 Deploying Frontend..." -ForegroundColor Cyan
    Set-Location "frontend (2)\frontend"
    
    # Check if .env.production exists
    if (-not (Test-Path ".env.production")) {
        Write-Host "⚠️  .env.production not found!" -ForegroundColor Yellow
        $backendUrl = Read-Host "Enter your backend Vercel URL (e.g., https://memory-decay-backend.vercel.app)"
        "VITE_API_BASE_URL=$backendUrl" | Out-File -FilePath ".env.production" -Encoding utf8
        Write-Host "✅ Created .env.production" -ForegroundColor Green
    }
    
    vercel
    Set-Location ..\..\..
    Write-Host "✅ Frontend deployment initiated" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Deployment process started!" -ForegroundColor Green
Write-Host "Check Vercel dashboard for deployment status: https://vercel.com/dashboard" -ForegroundColor Cyan

