function GameOver({ score, questions }) {
  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>Game Over 🎉</h1>
      <p>
        Your score: {score} / {questions.length}
      </p>
    </div>
  );
}

export default GameOver;
