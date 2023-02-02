from server.main import app
from main import game

@app.get("/")
async def read_root():
    player_ship = game.PLAYER_SHIP