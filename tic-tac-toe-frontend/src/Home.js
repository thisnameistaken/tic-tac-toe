import React from "react";
import { useNavigate } from "react-router-dom";
const API_URL = process.env.REACT_APP_API_URL;

function Home() {
  const navigate = useNavigate();

  const createGame = () => {
    fetch(`${API_URL}/create_game`, {method: "POST", headers: { "Content-Type": "application/json" }})
      .then((res) => res.json())
      .then((data) => {
        if (data.game_id) {
          navigate(`/game/${data.game_id}`); // Navigate to the game page
        } else {
          console.error("Error creating game:", data.error);
        }
      })
      .catch((err) => console.error("Error creating game:", err));
  };

  return (
    <div>
      <h1>Tic-Tac-Toe</h1>
      <button onClick={createGame}>Start New Game</button>
    </div>
  );
}

export default Home;
