Write-Host "========================================" -ForegroundColor Green
Write-Host "    تشغيل OpenCode - DevCenter" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# التأكد من المسار
Set-Location -LiteralPath "D:\DevCenter" -ErrorAction Stop

# تشغيل Ollama server (إذا مو شغال)
$ollama = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if (-not $ollama) {
    Write-Host "[1/3] تشغيل Ollama server..." -ForegroundColor Yellow
    Start-Process -WindowStyle Hidden -FilePath "C:\Users\anorm\AppData\Local\Programs\Ollama\ollama.exe" -ArgumentList "serve"
    Start-Sleep -Seconds 3
} else {
    Write-Host "[1/3] Ollama server شغال بالفعل" -ForegroundColor Green
}

Write-Host "[2/3] المسار: $(Get-Location)" -ForegroundColor Cyan
Write-Host ""

# تشغيل OpenCode
Write-Host "[3/3] تشغيل OpenCode..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   اكتب أوامرك بالعربية" -ForegroundColor Cyan
Write-Host "   Ctrl+V للصق | F2 للنماذج" -ForegroundColor Cyan
Write-Host "   Ctrl+Z تراجع | Ctrl+Y إعادة" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& "C:\Users\anorm\.opencode\bin\opencode.exe"

# بعد الخروج
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    تم إغلاق OpenCode" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Read-Host "اضغط Enter للخروج"
