# Read request

#$url = "your_api_endpoint_url"
$url = "https://zhwfwtqyrb.execute-api.us-east-1.amazonaws.com/mp6-stage1"
$body = @{
    "USE_CACHE": "True",
    "REQUEST": "read",
    "SQLS": [1,2,3]
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Body $body -Headers $headers
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Response Content: $($response | ConvertTo-Json -Depth 10)"
} catch {
    Write-Host "Error occurred:"
    Write-Host $_.Exception.Message
}

# Write request

#$url = "your_api_endpoint_url"
$url = "https://zhwfwtqyrb.execute-api.us-east-1.amazonaws.com/mp6-stage1"
$body = @{
    "USE_CACHE": "True",
    "REQUEST": "write",
    "SQLS": [
		{
		  "hero": "yes",
		  "name": "fireman",
		  "power": "fire",
		  "color": "red",
		  "xp": "1000001"
		},
		{
		  "hero": "no",
		  "name": "dogman",
		  "power": "bark",
		  "color": "brown",
		  "xp": "1000002"
		}
	  ]
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Body $body -Headers $headers
    Write-Host "Status Code: $($response.StatusCode)"
    Write-Host "Response Content: $($response | ConvertTo-Json -Depth 10)"
} catch {
    Write-Host "Error occurred:"
    Write-Host $_.Exception.Message
}