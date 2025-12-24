# MCP Server Deployment Configuration

## Overview
This document provides the deployment configuration for the Todo MCP (Model Context Protocol) server, enabling integration with ChatGPT and other MCP-compatible clients.

## Server Status

### Local Server
- **Status**: Running
- **Port**: 8787
- **Local URL**: `http://localhost:8787`
- **MCP Endpoint**: `http://localhost:8787/mcp`
- **Health Check**: `http://localhost:8787/` → Returns "Todo MCP server"

### Public Tunnel (ngrok)
- **Status**: Active
- **Public URL**: `https://e3e3af3d8f8d.ngrok-free.app`
- **MCP Endpoint**: `https://e3e3af3d8f8d.ngrok-free.app/mcp`
- **Protocol**: HTTPS
- **CORS**: Enabled (Access-Control-Allow-Origin: *)

## ChatGPT Integration

### Connector Configuration
To integrate this MCP server with ChatGPT, use the following URL:

```
https://e3e3af3d8f8d.ngrok-free.app/mcp
```

### Steps to Add Connector
1. Navigate to ChatGPT settings
2. Select "Custom Connectors" or "MCP Connectors"
3. Click "Add New Connector"
4. Enter the MCP endpoint URL: `https://e3e3af3d8f8d.ngrok-free.app/mcp`
5. Save the configuration

### Important: Browser Access Behavior

**Expected Error When Accessing via Browser**:
When navigating to the MCP endpoint (`/mcp`) directly in a web browser, you will encounter the following error:

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Not Acceptable: Client must accept text/event-stream"
  },
  "id": null
}
```

**This is normal and expected behavior.** Web browsers do not send the required `Accept` headers for MCP protocol communication. The endpoint requires:
- `Accept: application/json, text/event-stream`
- `Content-Type: application/json`

**Verification**: The MCP endpoint is functioning correctly when ChatGPT or other MCP clients connect with proper protocol headers. The error message confirms the server is running and enforcing correct communication protocols.

**Testing the Endpoint Properly**:
```bash
# Test MCP initialization
curl -X POST https://e3e3af3d8f8d.ngrok-free.app/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-client","version":"1.0.0"}},"id":1}'

# Expected response:
# {"result":{"protocolVersion":"2024-11-05","capabilities":{"resources":{"listChanged":true},"tools":{"listChanged":true}},"serverInfo":{"name":"todo-app","version":"0.1.0"}},"jsonrpc":"2.0","id":1}

# List available tools
curl -X POST https://e3e3af3d8f8d.ngrok-free.app/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":2}'
```

## Available Resources and Tools

### Resources
- **todo-widget** (`ui://widget/todo.html`)
  - **Type**: HTML Widget with Skybridge support
  - **MIME Type**: `text/html+skybridge`
  - **Metadata**: Border preference enabled (`openai/widgetPrefersBorder: true`)
  - **Purpose**: Visual representation of todo list state

### Tools

#### 1. add_todo
- **Title**: Add todo
- **Description**: Creates a todo item with the given title
- **Input Schema**:
  ```json
  {
    "title": "string (minimum length: 1)"
  }
  ```
- **Output**: Structured content with updated tasks array
- **Metadata**:
  - Output Template: `ui://widget/todo.html`
  - Invoking Message: "Adding todo"
  - Invoked Message: "Added todo"

#### 2. complete_todo
- **Title**: Complete todo
- **Description**: Marks a todo as done by id
- **Input Schema**:
  ```json
  {
    "id": "string (minimum length: 1)"
  }
  ```
- **Output**: Structured content with updated tasks array
- **Metadata**:
  - Output Template: `ui://widget/todo.html`
  - Invoking Message: "Completing todo"
  - Invoked Message: "Completed todo"

## Technical Specifications

### HTTP Endpoints

#### GET /
- **Purpose**: Health check and server identification
- **Response**: Plain text "Todo MCP server"
- **Status Code**: 200

#### OPTIONS /mcp
- **Purpose**: CORS preflight handling
- **Headers**:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Methods: POST, GET, OPTIONS`
  - `Access-Control-Allow-Headers: content-type, mcp-session-id`
  - `Access-Control-Expose-Headers: Mcp-Session-Id`
- **Status Code**: 204

#### POST/GET/DELETE /mcp
- **Purpose**: MCP protocol communication
- **Transport**: StreamableHTTPServerTransport
- **Session Mode**: Stateless (sessionIdGenerator: undefined)
- **JSON Response**: Enabled

### Server Architecture
- **Framework**: Node.js HTTP Server (native `node:http`)
- **MCP SDK**: `@modelcontextprotocol/sdk` v1.20.2
- **Validation**: Zod v3.25.76
- **State Management**: In-memory (non-persistent)
- **Session Handling**: Stateless per-request instantiation

## Data Persistence
**Important**: The current implementation utilizes in-memory storage. Todo items are **not persisted** across server restarts. All todos will be lost when the server process terminates.

## Monitoring and Logs

### Server Logs
- **Location**: `/tmp/claude/-mnt-f-Chatgpt-App/tasks/bb0655d.output`
- **View Command**: `cat /tmp/claude/-mnt-f-Chatgpt-App/tasks/bb0655d.output`

### ngrok Logs
- **Location**: `/tmp/claude/-mnt-f-Chatgpt-App/tasks/baccba3.output`
- **View Command**: `cat /tmp/claude/-mnt-f-Chatgpt-App/tasks/baccba3.output`

### ngrok Web Interface
- **URL**: `http://127.0.0.1:4040`
- **Features**: Real-time request inspection, replay functionality, traffic statistics

## Maintenance Commands

### Check Server Status
```bash
curl http://localhost:8787/
```
Expected output: `Todo MCP server`

### Check Public Endpoint
```bash
curl https://e3e3af3d8f8d.ngrok-free.app/
```
Expected output: `Todo MCP server`

### Test MCP Endpoint CORS
```bash
curl -X OPTIONS -i https://e3e3af3d8f8d.ngrok-free.app/mcp
```
Expected: HTTP 204 with CORS headers

### View Active Processes
```bash
ps aux | grep -E "node|ngrok"
```

## Security Considerations

### Current Configuration
- **CORS**: Unrestricted (`Access-Control-Allow-Origin: *`)
- **Authentication**: None
- **Rate Limiting**: None
- **Input Validation**: Zod schema validation only

### Recommendations for Production
1. Implement authentication middleware (OAuth 2.0, API keys)
2. Restrict CORS to specific origins
3. Add rate limiting to prevent abuse
4. Implement request logging and monitoring
5. Use persistent storage (database) instead of in-memory state
6. Enable HTTPS on local server (ngrok provides this in tunnel)
7. Implement session management for stateful interactions
8. Add request validation and sanitization beyond schema checks

## Troubleshooting

### Server Not Responding
```bash
# Check if server process is running
ps aux | grep "node server.js"

# Restart server if needed
cd /mnt/f/Chatgpt_App/public
node server.js &
```

### ngrok Tunnel Disconnected
```bash
# Restart ngrok
export PATH="$HOME/bin:$PATH"
ngrok http 8787 --log=stdout &
```

### Port Already in Use
```bash
# Find process using port 8787
lsof -i :8787

# Kill the process if necessary
kill -9 <PID>
```

## Environment Variables

### Supported Variables
- **PORT**: Server listening port (default: 8787)
  ```bash
  PORT=3000 node server.js
  ```

### ngrok Configuration
- **Config File**: `/home/abdullah/.config/ngrok/ngrok.yml`
- **Authtoken**: Configured and saved

## Versioning
- **MCP Server**: v0.1.0
- **MCP SDK**: v1.20.2
- **ngrok**: v3.34.1
- **Node.js**: v18.19.1

## Next Steps

1. **Test Integration**: Add connector to ChatGPT and verify functionality
2. **Monitor Usage**: Track requests via ngrok web interface (http://127.0.0.1:4040)
3. **Consider Persistence**: Evaluate database integration for production use
4. **Security Hardening**: Implement authentication and authorization
5. **Documentation**: Create user guide for ChatGPT interaction patterns

---

**Last Updated**: 2025-12-24
**Deployment Status**: Active
**MCP Endpoint**: `https://e3e3af3d8f8d.ngrok-free.app/mcp`
