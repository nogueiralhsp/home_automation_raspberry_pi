import asyncio
import websockets

async def handle_websocket(websocket, path):
    try:
        print(f"Client connected from {websocket.remote_address}")
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected.")

if __name__ == "__main__":
    server = websockets.serve(handle_websocket, "localhost", 8765)

    print("WebSocket server is running. Waiting for connections...")
    try:
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("WebSocket server shutting down.")
