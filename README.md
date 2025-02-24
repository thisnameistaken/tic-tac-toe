# Tic-Tac-Toe Full Stack App  

This is a full-stack Tic-Tac-Toe game with a **Flask backend**, a **React frontend**, and **PostgreSQL** for data storage.  

## Requirements  

### Backend  
- **Python 3**  
- **PostgreSQL**  
- A virtual environment is recommended  

### Frontend  
- **Node.js** and **npm**

## Setup  

### Backend  
1. **Create a virtual environment**  
   ```sh
   python -m venv venv
   source venv/bin/activate
2. **Create a .env based off the example**
3. **Run migrations**
   ```sh
   python3 migrate.py
4. **Run the app**
   ```sh
   python3 app.py

### Frontend  
1. **Create a .env based off the example**
2. **Install dependencies**
   ```sh
   npm install
3. **Run Frontend**
   ```sh
   npm start

## API Endpoints
### /create_game
Creates a new game with a blank board. Returns the game ID, game board, current turn (X), and the game status (ongoing).

### /update_game/game_id/placement
Updates a game with the current active marker. Placement should be an int from 0-8 and game_id should be the id of a currently active game. The API checks for a winner after each placement and returns the game ID, game board, current turn (X or O), and the game status (ongoing, X_wins, O_wins, or draw).

### /get_game/game_id
Gets all information for a game with that specific game_id. Returns the game ID, game board, current turn (X or O), and the game status (ongoing, X_wins, O_wins, or draw).

### /reset_game/game_id
Resets a game to a the starting state. Can be called regardless of the current state of the game. Returns the game ID, game board, current turn (X), and the game status (ongoing).