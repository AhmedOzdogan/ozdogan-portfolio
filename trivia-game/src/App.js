import React, { useState } from "react";
import Welcome from "./components/Welcome";
import Quiz from "./components/Quiz";
import { fetchQuestions } from "./components/Api";

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [numQuestions, setNumQuestions] = useState(5);
  const [difficulty, setDifficulty] = useState("easy");
  const [questions, setQuestions] = useState([]); // store fetched questions
  const [loading, setLoading] = useState(false);

  const startGame = async (questionsCount, level) => {
    setNumQuestions(questionsCount);
    setDifficulty(level);
    setLoading(true);

    console.log(
      `Starting game with ${questionsCount} questions at ${level} difficulty.`
    );
    try {
      const data = await fetchQuestions(questionsCount, level);
      setQuestions(data);
      setGameStarted(true);
    } catch (error) {
      console.error("Error fetching questions:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <h2>Loading questions...</h2>;

  return (
    <div>
      {!gameStarted ? (
        <Welcome startGame={startGame} />
      ) : (
        <Quiz
          questions={questions}
          numQuestions={numQuestions}
          difficulty={difficulty}
        />
      )}
    </div>
  );
}

export default App;
