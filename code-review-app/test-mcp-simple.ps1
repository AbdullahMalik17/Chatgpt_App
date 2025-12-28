# MCP Server Quick Test
Write-Host "Code Review MCP Server - Quick Test" -ForegroundColor Cyan
Write-Host ""

$ngrokUrl = "https://0c0109b4e456.ngrok-free.app"

# Test code with security issues
$testCode = 'function getUserData(userId) { const query = "SELECT * FROM users WHERE id = " + userId; return db.query(query); }'

Write-Host "Testing analyze_code tool..." -ForegroundColor Yellow

# Generate session ID
$sessionId = [guid]::NewGuid().ToString("N").Substring(0,32)

# Call analyze_code
$body = @{
    jsonrpc = "2.0"
    id = 1
    method = "tools/call"
    params = @{
        name = "analyze_code"
        arguments = @{
            code = $testCode
            language = "javascript"
        }
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod `
        -Uri "$ngrokUrl/messages/?session_id=$sessionId" `
        -Method POST `
        -ContentType "application/json" `
        -Headers @{"ngrok-skip-browser-warning"="true"} `
        -Body $body

    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Result:" -ForegroundColor Cyan
    $response.result.content[0].text
    Write-Host ""

    # Show structured data if available
    if ($response.result.structuredContent) {
        Write-Host "Issues Found: $($response.result.structuredContent.total_issues)" -ForegroundColor Yellow
        Write-Host "Errors: $($response.result.structuredContent.errors)" -ForegroundColor Red
        Write-Host "Warnings: $($response.result.structuredContent.warnings)" -ForegroundColor Yellow
        Write-Host "Suggestions: $($response.result.structuredContent.suggestions)" -ForegroundColor Cyan
    }

} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Response: $($_.ErrorDetails.Message)" -ForegroundColor Red
}
