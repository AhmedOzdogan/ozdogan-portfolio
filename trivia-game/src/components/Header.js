function Header({ score, currentIndex, questions }) {
  return (
    <header className="quiz-header">
      <h1>MindMaze</h1>
      <div className="score-board">
        <h2>Score: {score}</h2>
        <h2>
          Question {currentIndex + 1} / {questions.length}
        </h2>
      </div>
    </header>
  );
}

export default Header;
