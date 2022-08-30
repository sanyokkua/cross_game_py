from crossgame.api.controller import Controller
from crossgame.api.persistance import GameStateInMemoryPersistence

GAME_PERSISTENCE: GameStateInMemoryPersistence = GameStateInMemoryPersistence()
GAME_CONTROLLER: Controller = Controller(GAME_PERSISTENCE)
