import asyncio
import websockets
import re
import time
import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime
import json
import uuid

starting_time = None


data = {
    "id": str(uuid.uuid4()),
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "rounds": []
}

async def monitor_websocket(uri):

    latencies = deque()  # Elenco delle latenze per il round corrente
    multipliers = []  # Lista dei moltiplicatori per i round
    round_latencies = []  # Lista che contiene tutte le latenze dei round precedenti
    round_started = False  # Indica se un round è iniziato
    latency_diffs = []
    timestamps = []
    plot_data = False
    rounds = 0
    winning_rounds = 0

    starting_time = datetime.now()
    dt_string = starting_time.strftime("%d/%m/%Y %H:%M:%S")

    print("Inizio sessione raccolta, tempo: ", dt_string)

    # Inizializza il grafico con un valore iniziale vuoto
    if plot_data:
        line, = ax.plot([], [], label="Latenza del round", color='blue')

    async with websockets.connect(uri) as websocket:
        previous_time = time.time()
        previous_timestamp = None

        while True:
            message = await websocket.recv()
            current_time = time.time()
            latency = (current_time - previous_time) * 1000  # Latenza in ms
            previous_time = current_time

            timenow = time.time()  # tempo attuale in secondi

            latency_diffs.append(latency)

            if "pong" in message:
                print("Messaggio di pong ricevuto correttamente")
            

            # Estrai il moltiplicatore (se presente)
            match = re.search(r'mul="([0-9.]+)"', message)
            if match:
                multiplier = float(match.group(1))  # Converti il moltiplicatore in float
                print(f"Moltiplicatore: {multiplier} | Latenza: {latency:.2f} ms")
                multipliers.append(multiplier)  # Aggiungi il moltiplicatore alla lista
                latencies.append(latency)  # Aggiungi la latenza alla lista


            # Se la latenza supera il valore di soglia, inizia un nuovo round
            if latency > 2000:
                winning = False
                # Plotta i dati del round precedente
                #round_latencies.append(list(latencies))  # Salva il round
                #print(latency_diffs)
                rounds = rounds + 1
                if multipliers[-1] > 100:
                    winning_rounds = winning_rounds + 1
                    winning = True

                muls = list(multipliers)
                latencs = list(latencies)

                muls.pop()
                latencs.pop()

                print(f"Round completato. Round totali: {rounds}. Round vincenti: {winning_rounds}")
            
                data['rounds'].append({
                    "winning":winning,
                    "multipliers":muls,
                    "latencies":latencs,
                })

                if(rounds > 600):
                    file_name = "data_" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".json"

                    # Write data to JSON file
                    with open(file_name, "w") as json_file:
                        json.dump(data, json_file, indent=4)

                    data = {
                        "id": str(uuid.uuid4()),
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "rounds": []
                    }

                latencies.clear()  # Reset della latenza per il prossimo round
                multipliers.clear()

                await websocket.send("<ping time='{timenow}'></ping>")

# Sostituisci l'URL con quello del WebSocket
uri = "wss://broadcaster.pragmaticplaylive.net/broadcast?JSESSIONID=xalyHBVAKd8JLiOkAlfQcPXET0QwiLAVwXzGiBw44p90h5gvLYjU!-1415569409-c9915084&tableId=spacemanyxe123nh"  
try:
    asyncio.run(monitor_websocket(uri))
except KeyboardInterrupt:

    # File name
    file_name = "data_" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".json"

    # Write data to JSON file
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Keyboard interrupted detected")

