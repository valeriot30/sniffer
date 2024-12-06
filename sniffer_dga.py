import asyncio
import websockets
import time

async def monitor_websocket(uri):
    async with websockets.connect(uri) as websocket:
        previous_time = time.time()
        
        while True:
            message = await websocket.recv()
            current_time = time.time()
            latency = (current_time - previous_time) * 1000  # Latenza in millisecondi
            previous_time = current_time
                
            print(f"Pacchetto ricevuto: {message} | Latenza: {latency:.2f} ms \n")


# Sostituisci l'URL con quello del WebSocket
uri = "wss://dga.pragmaticplaylive.net/ws"
asyncio.run(monitor_websocket(uri))
