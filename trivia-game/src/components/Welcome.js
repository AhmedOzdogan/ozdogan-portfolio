import React, { useState } from "react";
import "../styles/Welcome.css";
import SoundControls from "./SoundControls";
import HowToPlay from "./HowToPlay";

function Welcome({ startGame }) {
  const [selectedNum, setSelectedNum] = useState(5);
  const [selectedDifficulty, setSelectedDifficulty] = useState("easy");

  return (
    <main className="welcome-container">
      <header className="welcome-header-top">
        <SoundControls />
        <HowToPlay />
      </header>
      <div className="app-name">MindMaze</div>

      <div className="welcome-header">
        <h2>Welcome to the Trivia Challenge!</h2>
      </div>

      <div className="welcome-text">
        <p>Are you ready for the challenge?</p>
        <p>Can you score 100%?</p>
      </div>

      <div className="welcome-footer">
        <label htmlFor="numQuestions">Select Number of Questions:</label>
        <select
          id="numQuestions"
          value={selectedNum}
          onChange={(e) => setSelectedNum(Number(e.target.value))}
        >
          <option value="5">5</option>
          <option value="10">10</option>
          <option value="15">15</option>
          <option value="20">20</option>
        </select>

        <label htmlFor="difficulty">Select Difficulty:</label>
        <select
          id="difficulty"
          value={selectedDifficulty}
          onChange={(e) => setSelectedDifficulty(e.target.value)}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      <button
        className="welcome-button"
        onClick={() => startGame(selectedNum, selectedDifficulty)}
      >
        BEGIN
      </button>
    </main>
  );
}

export default Welcome;
