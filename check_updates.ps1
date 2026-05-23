try {
    $session = New-Object -ComObject Microsoft.Update.Session
    $searcher = $session.CreateUpdateSearcher()
    $result = $searcher.Search("IsInstalled=0")
    Write-Host "Windows Updates found: $($result.Updates.Count)"
    foreach($u in $result.Updates) {
        Write-Host "- $($u.Title)"
    }
    if ($result.Updates.Count -eq 0) {
        Write-Host "No pending Windows updates."
    }
} catch {
    Write-Host "Error: $_"
}
