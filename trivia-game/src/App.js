import React, { useState } from "react";
import Welcome from "./components/Welcome";
import Quiz from "./components/Quiz";
import { fetchQuestions } from "./utils/Api";
import Loading from "./components/Loading";
import Error from "./components/Error";
import GameOver from "./components/GameOver";
import { QuizProvider } from "./contexts/QuizContext";

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [numQuestions, setNumQuestions] = useState(5);
  const [difficulty, setDifficulty] = useState("easy");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [gameOver, setGameOver] = useState(false);

  const startGame = async (questionsCount, level) => {
    setNumQuestions(questionsCount);
    setDifficulty(level);
    setLoading(true);
    setError(false);

    try {
      const data = await fetchQuestions(numQuestions, level);
      setQuestions(data);
      setGameStarted(true);
    } catch (error) {
      console.error("Error fetching questions:", error);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error) return <Error />;

  return (
    <QuizProvider>
      {!gameStarted ? (
        <Welcome startGame={startGame} />
      ) : gameOver ? (
        <GameOver questions={questions} />
      ) : (
        <Quiz
          questions={questions}
          numQuestions={numQuestions}
          difficulty={difficulty}
          setGameOver={setGameOver}
        />
      )}
    </QuizProvider>
  );
}

export default App;
