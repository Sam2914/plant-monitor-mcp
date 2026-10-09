import json
import uvicorn
from fastapi import FastAPI, Request, Response

app = FastAPI(title="Alexa+ Smart Plant Monitor MCP")

# Simulated database/sensor state for your plants
PLANT_DATABASE = {
    "monstera": {
        "name": "Monstera Deliciosa",
        "moisture": 28,  # percentage
        "status": "Needs Water",
        "last_watered": "3 days ago"
    },
    "succulent": {
        "name": "Jade Plant",
        "moisture": 65,
        "status": "Healthy",
        "last_watered": "Yesterday"
    }
}

# 1. Define the tools your MCP server exposes to Alexa+
TOOLS_MANIFEST = [
    {
        "name": "get_plant_status",
        "description": "Checks the current soil moisture level, overall status, and last watered time for a specific plant.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "plant_id": {
                    "type": "string",
                    "description": "The plant to check (e.g., 'monstera' or 'succulent')."
                }
            },
            "required": ["plant_id"]
        }
    },
    {
        "name": "water_plant",
        "description": "Triggers the automatic watering pump for a specific plant for a given duration in seconds.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "plant_id": {
                    "type": "string",
                    "description": "The plant to water (e.g., 'monstera' or 'succulent')."
                },
                "duration_seconds": {
                    "type": "integer",
                    "description": "Duration to run the water pump in seconds (default is 5)."
                }
            },
            "required": ["plant_id"]
        }
    }
]

@app.post("/mcp")
async def handle_mcp(request: Request):
    """MCP Streamable HTTP Endpoint (2025-11-25 Spec)."""
    body = await request.json()
    method = body.get("method")
    req_id = body.get("id")

    # Handshake / Initialization
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-11-25",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "PlantWatererMCP", "version": "1.0.0"}
            }
        }

    # Expose tools list to Alexa+ LLM agent
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS_MANIFEST}
        }

    # Execute tool actions when triggered
    elif method == "tools/call":
        params = body.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        plant_id = args.get("plant_id", "").lower()

        if plant_id not in PLANT_DATABASE:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Plant '{plant_id}' not found in system."}]
                }
            }

        # Handle Action 1: Get Status
        if tool_name == "get_plant_status":
            info = PLANT_DATABASE[plant_id]
            text_result = (
                f"Plant: {info['name']}\n"
                f"Soil Moisture: {info['moisture']}%\n"
                f"Status: {info['status']}\n"
                f"Last Watered: {info['last_watered']}"
            )

        # Handle Action 2: Water Plant
        elif tool_name == "water_plant":
            duration = args.get("duration_seconds", 5)
            # Update simulated state
            PLANT_DATABASE[plant_id]["moisture"] = 85
            PLANT_DATABASE[plant_id]["status"] = "Healthy & Hydrated"
            PLANT_DATABASE[plant_id]["last_watered"] = "Just now"

            text_result = (
                f"Success! Water pump activated for {duration} seconds on {PLANT_DATABASE[plant_id]['name']}. "
                f"New moisture level is 85%."
            )

        else:
            text_result = "Unknown tool action requested."

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": text_result}]
            }
        }

    return Response(status_code=400, content=json.dumps({"error": "Method not found"}))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)