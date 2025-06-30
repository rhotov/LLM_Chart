
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from data_provider import get_historical_data, generate_new_candle
from llm_service import get_llm_analysis

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory data store
kline_data = get_historical_data(400)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/api/history")
async def get_history():
    """Provide historical k-line data."""
    return kline_data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # The server will push data, so we just wait here
            await websocket.receive_text() 
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def background_data_task():
    """Simulates real-time data updates and LLM analysis."""
    global kline_data
    while True:
        await asyncio.sleep(5)  # Wait for 5 seconds
        
        # 1. Generate a new candle
        new_candle = generate_new_candle(kline_data[-1])
        kline_data.append(new_candle)
        if len(kline_data) > 500: # Keep the list from growing indefinitely
            kline_data.pop(0)
        
        # Broadcast the new candle
        update_message = json.dumps({"type": "kline", "data": new_candle})
        await manager.broadcast(update_message)
        
        # 2. Trigger LLM analysis
        # Use the last 20 candles for context
        analysis_result = get_llm_analysis(kline_data[-20:])
        llm_message = json.dumps({"type": "llm_analysis", "data": analysis_result})
        await manager.broadcast(llm_message)

@app.on_event("startup")
async def startup_event():
    # Start the background task when the server starts
    asyncio.create_task(background_data_task())

if __name__ == "__main__":
    import uvicorn
    # Note: Running this directly is for testing. 
    # Use `uvicorn main:app --reload` for development.
    uvicorn.run(app, host="0.0.0.0", port=8000)
