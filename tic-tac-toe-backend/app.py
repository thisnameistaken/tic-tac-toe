from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS
from db_values import DB_CONNECTION_PARAMS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(**DB_CONNECTION_PARAMS)

def check_winner(board):
    winning_combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
        (0, 4, 8), (2, 4, 6) # Diagonals
    ]

    for a, b, c in winning_combos:
        if board[a] == board[b] == board[c] and board[a] in ('X', 'O'):
            return board[a]  # Return the winner

    return None

# Create a new game
@app.route('/create_game', methods=['POST'])
def create_game():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert a new game row into DB
        cur.execute("""
            INSERT INTO games (board, current_turn, status)
            VALUES ('---------', 'X', 'ongoing')
            RETURNING id, board, current_turn, status;
        """)
        game_id, board, current_turn, status = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Game created successfully",
            "game_id": game_id,
            "board": list(board),  # Convert board string into a list
            "current_turn": current_turn,
            "status": status
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a game board with the current marker
@app.route('/update_game/<int:game_id>/<int:placement>', methods=['POST'])
def update_game(game_id, placement):
    try:
        # Validate placement is between 0-8
        if placement < 0 or placement > 8:
            return jsonify({"error": "Invalid placement"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT board, current_turn, status FROM games WHERE id = %s", (game_id,))
        cur_game = cur.fetchone()

        # Return error if game doesn't exist
        if not cur_game:
            return jsonify({"error": "Game not found"}), 404

        board, current_turn, status = list(cur_game[0]), cur_game[1], cur_game[2]

        # Check if the game is completed
        if status != 'ongoing':
            return jsonify({"error": "Game is already completed"}), 400

        # Check if move is valid
        if board[placement] != '-':
            return jsonify({"error": "Invalid move"}), 400

        # Update the board
        board[placement] = current_turn
        winner = check_winner(board)

        # Determine next player or if the game ends
        if winner:
            new_status = "X_wins" if winner == 'X' else "O_wins"
        elif '-' not in board:
            new_status = 'draw'
        else:
            new_status = 'ongoing'
            next_turn = 'O' if current_turn == 'X' else 'X'

        # Update the database
        cur.execute("""
            UPDATE games
            SET board = %s, current_turn = %s, status = %s
            WHERE id = %s
        """, (
            ''.join(board),
            next_turn if new_status == 'ongoing' else current_turn,
            new_status,
            game_id
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "game_id": game_id,
            "board": board,
            "current_turn": next_turn if new_status == 'ongoing' else current_turn,
            "status": new_status,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get game state
@app.route('/get_game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT board, current_turn, status FROM games WHERE id = %s", (game_id,))
    cur_game = cur.fetchone()
    cur.close()
    conn.close()

    if cur_game:
        board, current_turn, status = list(cur_game[0]), cur_game[1], cur_game[2]
        return jsonify({"game_id": game_id, "board": board, "current_turn": current_turn, "status": status}), 200
    else:
        return jsonify({"error": "Game not found"}), 404

@app.route('/reset_game/<int:game_id>', methods=['POST'])
def reset_game(game_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Check if the game exists
        cur.execute("SELECT id FROM games WHERE id = %s", (game_id,))
        cur_game = cur.fetchone()
        if not cur_game:
            return jsonify({"error": "Game not found"}), 404
        
        # Reset the game
        cur.execute("""
            UPDATE games
            SET board = '---------', current_turn = 'X', status = 'ongoing'
            WHERE id = %s
            RETURNING board, current_turn, status;
        """, (game_id,))
        updated_game = cur.fetchone()
        conn.commit()

        board, current_turn, status = list(updated_game[0]), updated_game[1], updated_game[2]
        return jsonify({"game_id": game_id, "board": board, "current_turn": current_turn, "status": status}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
