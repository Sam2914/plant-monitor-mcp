1. 🪴 Smart Plant Monitor & Waterer (MCP Server)

An Model Context Protocol (MCP) server built with Python and FastAPI that enables AI assistants (like Alexa+) to remotely query plant soil moisture levels and trigger automated watering systems.



   Overview

The Smart Plant Monitor MCP bridges the gap between smart home AI agents and real-world IoT plant care systems. By exposing standardized Model Context Protocol (MCP) endpoints, AI agents can dynamically query real-time sensor data, interpret environmental status, and take autonomous actions—like activating a water pump when soil moisture drops below critical thresholds.



2. ✨ Features

- MCP Protocol Integration: Implements standard JSON-RPC `tools/list` and `tools/call` endpoints for seamless AI agent interoperability.
- Real-Time Sensor Polling (`get_plant_status`): Returns live soil moisture percentages, plant health statuses, and last-watered timestamps.
- Automated Actuation (`water_plant`): Triggers simulated or hardware pump mechanisms for specified durations.
- Interactive Streamlit UI: Provides a clean visual test dashboard for demonstration and manual control.
- Cloud Tunnels: Publicly accessible via Ngrok / Pinggy for remote webhooks and voice assistant integration.



3. 🛠️ Tech Stack

- Backend: Python 3.12+, FastAPI, Uvicorn
- Protocol: Model Context Protocol (MCP), JSON-RPC 2.0
- Frontend / Dashboard: Streamlit
- Tunneling: Ngrok / Pinggy

