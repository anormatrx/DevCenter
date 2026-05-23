$taskName = "DevCenter-Servers-247"
$scriptPath = "D:\DevCenter\run-servers-247.bat"
$username = $env:USERNAME

Write-Host "=== تثبيت DevCenter 24/7 ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "سيتم إنشاء مهمة في Task Scheduler لتشغيل السيرفرات:"
Write-Host "  - Ollama (الذكاء الاصطناعي)"
Write-Host "  - ChatApp Server (الدردشة)"
Write-Host "  - Telegram Bot"
Write-Host ""
Write-Host "عند تسجيل الدخول إلى ويندوز"
Write-Host ""

# حذف المهمة القديمة إن وجدت
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "⚠️  توجد مهمة سابقة. سيتم استبدالها..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# إنشاء المهمة
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`"" -WorkingDirectory "D:\DevCenter"
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $username
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -User $username -RunLevel Highest -Force

Write-Host ""
Write-Host "✅ تم التثبيت بنجاح!" -ForegroundColor Green
Write-Host ""
Write-Host "المهمة: $taskName"
Write-Host "التشغيل: عند تسجيل الدخول"
Write-Host "المسار: $scriptPath"
Write-Host ""
Write-Host "السيرفرات بتشتغل 24/7 وتعيد نفسها تلقائياً لو طفت"
Write-Host ""
Write-Host "للتشغيل اليدوي الآن:"
Write-Host " 双击 run-servers-247.bat"
Write-Host ""
Write-Host "لإلغاء التثبيت:"
Write-Host "  Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
