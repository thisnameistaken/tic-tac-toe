import pytest
from app import app, get_db_connection

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def client_with_empty_game():
    app.config["TESTING"] = True
    with app.test_client() as client:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create a new empty game
        cur.execute("""
            INSERT INTO games (board, current_turn, status)
            VALUES ('---------', 'X', 'ongoing')
            RETURNING id;
        """)
        game_id = cur.fetchone()[0]
        conn.commit()

        yield client, game_id

        # Cleanup
        cur.execute("DELETE FROM games WHERE id = %s", (game_id,))
        conn.commit()
        cur.close()
        conn.close()

def test_create_game(client):
    """Test creating a new game."""
    response = client.post("/create_game")
    data = response.get_json()
    print("\n data , ", data)
    
    assert response.status_code == 201
    assert "game_id" in data
    assert data["board"] == ['-', '-', '-', '-', '-', '-', '-', '-', '-']
    assert data["current_turn"] == "X"
    assert data["status"] == "ongoing"

    # Cleanup
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM games WHERE id = %s", (data["game_id"],))
    conn.commit()
    cur.close()
    conn.close()

def test_invalid_move(client_with_empty_game):
    """Test making an invalid move"""
    client, game_id = client_with_empty_game

    response = client.post(f"/update_game/{game_id}/10")
    data = response.get_json()
    
    assert response.status_code == 400
    assert data["error"] == "Invalid placement"

def test_update_game_valid_move(client_with_empty_game):
    """Test making a single valid move"""
    client, game_id = client_with_empty_game

    # Make valid move
    response = client.post(f"/update_game/{game_id}/0")

    data = response.get_json()
    print("\n data   ", data)

    assert response.status_code == 200
    assert data["game_id"] == game_id
    assert data["board"][0] == "X"
    assert data["current_turn"] == "O"
    assert data["status"] == "ongoing"

def test_win_condition(client_with_empty_game):
    """Test a game where a player wins."""
    client, game_id = client_with_empty_game

    moves = [0,3,1,4]
    for move in moves:
      client.post(f"/update_game/{game_id}/{move}")

    response = client.post(f"/update_game/{game_id}/2") # X move, should win

    data = response.get_json()
    assert response.status_code == 200
    assert data["status"] == "X_wins"

def test_draw_condition(client_with_empty_game):
    """Test a game that results in a draw."""
    client, game_id = client_with_empty_game

    moves = [0, 1, 2, 4, 3, 5, 7, 6]
    for move in moves:
        client.post(f"/update_game/{game_id}/{move}")

    response = client.post(f"/update_game/{game_id}/8")  # Last move
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "draw"

def test_game_not_found(client):
    """Test updating a non-existent game."""
    response = client.post("/update_game/9983478/4")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Game not found"

def test_get_game(client_with_empty_game):
    """Test get game returns valid data"""
    client, game_id = client_with_empty_game

    # Make valid move
    client.post(f"/update_game/{game_id}/0")
    response = client.get(f"/get_game/{game_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["game_id"] == game_id
    assert data["board"] == ['X', '-', '-', '-', '-', '-', '-', '-', '-']
    assert data["current_turn"] == "O"
    assert data["status"] == "ongoing"

def test_get_game_invalid(client_with_empty_game):
    """Test get game returns an error when finding invalid game"""
    client, game_id = client_with_empty_game

    response = client.get(f"/get_game/789302450092358")
    assert response.status_code == 404

def test_reset_game(client_with_empty_game):
    """Test reset game resets game"""
    client, game_id = client_with_empty_game

    client.post(f"/update_game/{game_id}/0")
    response = client.post(f"/reset_game/{game_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["game_id"] == game_id
    assert data["board"] == ['-', '-', '-', '-', '-', '-', '-', '-', '-']
    assert data["current_turn"] == "X"
    assert data["status"] == "ongoing"
