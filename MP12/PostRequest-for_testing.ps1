$uri = "http://54.145.200.192:5000/img-classification/free"
$body = @{
    dataset = "mnist"
} | ConvertTo-Json
$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -Headers $headers
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Response Content:"
    $response | ConvertTo-Json
} catch {
    Write-Host "Error occurred:"
    Write-Host $_.Exception.Message
}

$uri = "http://54.145.200.192:5000/img-classification/premium"
$body = @{
    dataset = "kmnist"
} | ConvertTo-Json
$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -Headers $headers
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Response Content:"
    $response | ConvertTo-Json
} catch {
    Write-Host "Error occurred:"
    Write-Host $_.Exception.Message
}

# References
# https://www.google.com/search?q=send+a+post+response+powershell&rlz=1C1CHBF_enUS1071US1071&oq=send+a+post+response+powershell&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRigATIHCAQQIRifBTIHCAUQIRifBTIHCAYQIRifBTIHCAcQIRifBTIHCAgQIRiPAtIBCDY1MzVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8