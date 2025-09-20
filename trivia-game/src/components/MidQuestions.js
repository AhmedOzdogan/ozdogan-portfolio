import "../styles/Quiz.css";

function MidQuestions({ answer, onNext }) {
  const isCorrect = answer === "correct";

  return (
    <div className={`mid-questions ${isCorrect ? "correct" : "wrong"}`}>
      <p className="mid-title">{isCorrect ? "Correct!" : "Wrong!"}</p>
      <p className="mid-points">
        {isCorrect ? "+100 points 🎉" : "-50 points ❌"}
      </p>
      <button className="mid-button" onClick={onNext}>
        Next Question →
      </button>
    </div>
  );
}

export default MidQuestions;
