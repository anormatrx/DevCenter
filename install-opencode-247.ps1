# تثبيت OpenCode 24/7 كـ Task Scheduler (يشتغل عند startup)
# شغّل هذا السكريبت كـ Administrator

$taskName = "OpenCode247"
$scriptPath = "D:\DevCenter\run-opencode-247.bat"

# إزالة المهمة القديمة إن وجدت
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# إنشاء المهمة الجديدة
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory "D:\DevCenter"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1)

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -RunLevel Highest -LogonType Interactive

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

Write-Host "تم تثبيت OpenCode 24/7 بنجاح!" -ForegroundColor Green
Write-Host "المهمة: $taskName"
Write-Host "السكريبت: $scriptPath"
Write-Host ""
Write-Host "OpenCode يشتغل تلقائياً عند تشغيل الويندوز"
Write-Host "ويضل شغال 24/7 مع إعادة تشغيل تلقائية"