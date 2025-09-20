import { useQuiz } from "../contexts/QuizContext";

function GameOver() {
  const { score, maxScore } = useQuiz();

  const percentage = maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;

  const wrapperStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "100vh",
    backgroundColor: "#1e1e2f", // dark background for contrast
    color: "#ffffff",
    textAlign: "center",
    padding: "20px",
  };

  const headingStyle = {
    fontSize: "2.5rem",
    fontWeight: "bold",
    marginBottom: "1rem",
    color: "#ffb703",
  };

  const scoreStyle = {
    fontSize: "1.5rem",
    marginBottom: "1.5rem",
  };

  const progressWrapper = {
    width: "80%",
    maxWidth: "400px",
    background: "#333",
    borderRadius: "20px",
    overflow: "hidden",
    marginBottom: "2rem",
  };

  const progressBar = {
    width: `${percentage}%`,
    height: "20px",
    backgroundColor: percentage >= 50 ? "#06d6a0" : "#ef476f",
    transition: "width 0.5s ease",
  };

  const buttonStyle = {
    backgroundColor: "#ffb703",
    color: "#1e1e2f",
    fontWeight: "bold",
    padding: "12px 24px",
    fontSize: "16px",
    border: "none",
    borderRadius: "12px",
    cursor: "pointer",
    transition: "all 0.2s ease",
  };

  const handleRestart = () => {
    window.location.reload();
  };

  return (
    <main style={wrapperStyle}>
      <h2 style={headingStyle}>🎉 Game Over 🎉</h2>
      <p style={scoreStyle}>
        You scored <strong>{score}</strong> out of <strong>{maxScore}</strong> (
        {percentage}%)
      </p>

      {/* Progress Bar */}
      <div style={progressWrapper}>
        <div style={progressBar}></div>
      </div>

      <button style={buttonStyle} onClick={handleRestart}>
        Play Again
      </button>
    </main>
  );
}

export default GameOver;
