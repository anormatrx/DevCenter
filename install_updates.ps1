try {
    $session = New-Object -ComObject Microsoft.Update.Session
    $searcher = $session.CreateUpdateSearcher()
    $result = $searcher.Search("IsInstalled=0")
    
    $updatesToDownload = New-Object -ComObject Microsoft.Update.UpdateColl
    foreach($u in $result.Updates) {
        $updatesToDownload.Add($u) | Out-Null
        Write-Host "Added: $($u.Title)"
    }
    
    if ($updatesToDownload.Count -gt 0) {
        Write-Host "Downloading $($updatesToDownload.Count) updates..."
        $downloader = $session.CreateUpdateDownloader()
        $downloader.Updates = $updatesToDownload
        $downloadResult = $downloader.Download()
        Write-Host "Download result: $($downloadResult.ResultCode)"
        
        Write-Host "Installing updates..."
        $installer = $session.CreateUpdateInstaller()
        $installer.Updates = $updatesToDownload
        $installResult = $installer.Install()
        Write-Host "Install result: $($installResult.ResultCode)"
        Write-Host "Reboot required: $($installResult.RebootRequired)"
    } else {
        Write-Host "No updates to install."
    }
} catch {
    Write-Host "Error: $_"
}
