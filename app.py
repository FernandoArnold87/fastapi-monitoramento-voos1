from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Bem-vindo ao monitoramento de voos! Use /docs para acessar a API."}
fake_flights_db = [
    {"origin": "FRA", "destination": "FLN", "price": 600, "date": "2026-02-10"},
    {"origin": "FRA", "destination": "FLN", "price": 550, "date": "2026-02-15"},
    {"origin": "FRA", "destination": "FLN", "price": 580, "date": "2026-03-01"},
]

class FlightSearch(BaseModel):
    origin: str
    destination: str
    max_price: float
    date_range: Optional[List[str]] = None
    stay_days: Optional[int] = 21

users_searches = []

def monitor_search(search: FlightSearch):
    print(f"[Monitoramento iniciado] {search}")
    for attempt in range(1, 6):
        print(f"[Busca #{attempt}]")
        for flight in fake_flights_db:
            if (flight["origin"] == search.origin and
                flight["destination"] == search.destination and
                flight["price"] <= search.max_price):
                print(f"✨ Oferta encontrada! {flight}")
        time.sleep(10)
    print(f"[Monitoramento finalizado] {search}")

@app.post("/search")
def add_search(search: FlightSearch, background_tasks: BackgroundTasks):
    users_searches.append(search)
    background_tasks.add_task(monitor_search, search)
    return {"message": "Busca cadastrada. Monitoramento iniciado."}

@app.get("/searches")
def get_searches():
    return users_searches
