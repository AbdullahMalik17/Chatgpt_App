# Direct HTTP Test for MCP Server
Write-Host "Testing MCP Server Directly..." -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8001"

$testCode = @"
function getUserData(userId) {
  const query = 'SELECT * FROM users WHERE id = ' + userId;
  const apiKey = 'hardcoded-secret-key';
  return db.query(query);
}
"@

Write-Host "Test Code:" -ForegroundColor Yellow
Write-Host $testCode
Write-Host ""

# Test 1: List tools
Write-Host "[1] Listing available tools..." -ForegroundColor Green

$listBody = @{
    jsonrpc = "2.0"
    id = 1
    method = "tools/list"
} | ConvertTo-Json

try {
    $toolsResponse = Invoke-RestMethod `
        -Uri "$baseUrl/messages" `
        -Method POST `
        -ContentType "application/json" `
        -Body $listBody

    Write-Host "Available Tools:" -ForegroundColor Green
    $toolsResponse.result.tools | ForEach-Object {
        Write-Host "  - $($_.name): $($_.description)" -ForegroundColor White
    }
    Write-Host ""
} catch {
    Write-Host "Could not list tools: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 2: Analyze code
Write-Host "[2] Analyzing code..." -ForegroundColor Green

$analyzeBody = @{
    jsonrpc = "2.0"
    id = 2
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
    $analysisResponse = Invoke-RestMethod `
        -Uri "$baseUrl/messages" `
        -Method POST `
        -ContentType "application/json" `
        -Body $analyzeBody

    Write-Host "Analysis Result:" -ForegroundColor Green
    Write-Host $analysisResponse.result.content[0].text
    Write-Host ""

    if ($analysisResponse.result.structuredContent) {
        $data = $analysisResponse.result.structuredContent
        Write-Host "Statistics:" -ForegroundColor Cyan
        Write-Host "  Total Issues: $($data.total_issues)"
        Write-Host "  Errors: $($data.errors)"
        Write-Host "  Warnings: $($data.warnings)"
        Write-Host "  Suggestions: $($data.suggestions)"
    }
} catch {
    Write-Host "Analysis failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Test Complete!" -ForegroundColor Cyan
