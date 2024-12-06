import asyncio
import websockets
import time

async def monitor_websocket(uri):
    async with websockets.connect(uri) as websocket:
        previous_time = time.time()
        
        while True:
            message = await websocket.recv()
            if "<gr" in message or "<sm_lb" in message:
	            current_time = time.time()
	            latency = (current_time - previous_time) * 1000  # Latenza in millisecondi
	            previous_time = current_time
	            
	            print(f"Pacchetto ricevuto: {message} | Latenza: {latency:.2f} ms \n")


# Sostituisci l'URL con quello del WebSocket
uri = "wss://gs9.pragmaticplaylive.net/game?bcs=true&JSESSIONID=xalyHBVAKd8JLiOkAlfQcPXET0QwiLAVwXzGiBw44p90h5gvLYjU!-1415569409-c9915084&tableId=spacemanyxe123nh"
asyncio.run(monitor_websocket(uri))
