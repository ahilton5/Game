# Game
Simple game inspired by Paper.IO by VOODOO.

## Dependencies
bottle and requests.

## Instructions
The command-line usage for the server is as follows:
```
usage: server.py [-h] [--nseconds NSECONDS]

optional arguments:
  -h, --help           show this help message and exit
  --nseconds NSECONDS  The number of seconds between turns. Defaults to 0.2.
```

The AI takes no arguments. Simply call `python3 ai_client.py` to start it.

To play the AI, open http://localhost:8088 in a web browser. The space bar starts/pauses the game, the arrows moves your player, and esc resets the game.
