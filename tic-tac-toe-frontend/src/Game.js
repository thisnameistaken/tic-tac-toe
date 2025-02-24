import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
const API_URL = process.env.REACT_APP_API_URL;

function Game() {
  const { gameId } = useParams();
  const [game, setGame] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/get_game/${gameId}`)
      .then((res) => res.json())
      .then((data) => setGame(data))
      .catch((err) => console.error("Error fetching game:", err));
  }, [gameId]);

  if (!game) return <p>Loading game...</p>;

  const boardArray = Array.isArray(game.board) ? game.board : [];

  const handleMove = (index) => {
    if (!game || game.board[index] !== "-") return; // Prevent playing on an occupied cell

    fetch(`${API_URL}/update_game/${gameId}/${index}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((data) => setGame(data))
      .catch((err) => console.error("Error updating game:", err));
  };

  const resetGame = () => {
    setGame(null);
    fetch(`${API_URL}/reset_game/${gameId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((data) => setGame(data))
      .catch((err) => console.error("Error resetting game:", err));
  };

  return (
    <div  style={{ margin: "20px auto", width: "fit-content" }}>
      <h1>Game Id - {gameId}</h1>
      <button onClick={() => resetGame()}> Reset Game </button>
      <p>Status: {game.status}</p>
      <p>Current Turn: {game.current_turn}</p>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 60px)",
          gap: "5px",
        }}
      >
        {boardArray.map((cell, index) => (
          <BoardButton
            key={index}
            value={cell}
            onClick={() => {handleMove(index)}}
            disabled={cell !== "-" || game.status !== "ongoing"}
          />
        ))}
      </div>
      
    </div>
  );
}

export default Game;

const BoardButton = ({ value, onClick, disabled }) => {
  return (
    <button
      style={{
        width: "60px",
        height: "60px",
        fontSize: "24px",
        textAlign: "center",
        cursor: disabled ? "not-allowed" : "pointer",
        backgroundColor: disabled ? "#ddd" : "#fff",
        border: "1px solid #000",
      }}
      disabled={disabled}
      onClick={onClick}
    >
      {value === "-" ? "" : value}
    </button>
  );
};
