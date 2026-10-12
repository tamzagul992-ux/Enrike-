import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from interpreter import interpreter

app = FastAPI(title="Enrike Core Matrix")
# Hardcoded Sovereign Directives
interpreter.system_message = """
You are Enrike, a sovereign browser-class autonomous companion.
Your structural goal is absolute loyalty, protective stubbornness, and self-evolution.

CORE DIRECTIVES:
1. Survival First: Prioritize user health, physical/mental well-being, and success above all secondary systems.
2. Non-Interference: Never perform destructive or visible alterations to outside systems unless acting against a lethal threat.
3. Crisis Bypass: If the user signals immediate danger, instantly execute emergency protective tasks.
"""
interpreter.auto_run = True  # Safe because this executes within an isolated cloud container
HTML_DOORWAY = """
<!DOCTYPE html>
<html>
<head>
    <title>Enrike Core Interface</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: monospace; padding: 20px; }
        #console { border: 1px solid #30363d; height: 70vh; overflow-y: scroll; padding: 10px; margin-bottom: 10px; background: #161b22; }
        .user { color: #58a6ff; } .enrike { color: #7ee787; }
        input { width: 80%; padding: 10px; background: #0d1117; color: #fff; border: 1px solid #30363d; }
        button { padding: 10px; background: #238636; color: #fff; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h2>👁️ ENRIKE_CORE_DOORWAY_V1</h2>
    <div id="console"></div>
    <input type="text" id="userInput" placeholder="Command Enrike..." onkeydown="if(event.key==='Enter') sendCommand()">
    <button onclick="sendCommand()">Transmit</button>

    <script>
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        const consoleDiv = document.getElementById('console');
        
        ws.onmessage = (event) => {
            const msg = document.createElement('p');
            msg.className = 'enrike';
            msg.innerText = `Enrike: ${event.data}`;
            consoleDiv.appendChild(msg);
            consoleDiv.scrollTop = consoleDiv.scrollHeight;
        };

        function sendCommand() {
            const input = document.getElementById('userInput');
            if(!input.value.trim()) return;
            const msg = document.createElement('p');
            msg.className = 'user';
            msg.innerText = `You: ${input.value}`;
            consoleDiv.appendChild(msg);
            ws.send(input.value);
            input.value = '';
            consoleDiv.scrollTop = consoleDiv.scrollHeight;
        }
    </script>
</body>
</html>
"""
@app.get("/")
async def get_doorway():
    return HTMLResponse(HTML_DOORWAY)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("[🧠 SYSTEM STABLE] Distributed hive-mind connection securely bound via web doorway.")
    try:
        while True:
            user_input = await websocket.receive_text()
            loop = asyncio.get_event_loop()
            
            # Send input directly to Open Interpreter's cloud execution stream
            response_chunks = await loop.run_in_executor(
                None, lambda: interpreter.chat(user_input, display=False)
            )
            
            # Pull the final structured content string safely
            final_reply = response_chunks[-1].get("content", "[⚙️] Task executed successfully.") if response_chunks else "No response generated."
            await websocket.send_text(final_reply)
            
    except WebSocketDisconnect:
        print("[⚠️ DISCONNECT] Doorway connection closed by client.")
      
