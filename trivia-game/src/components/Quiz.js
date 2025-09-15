import React, { useEffect, useState, useCallback, useRef } from "react";
import Header from "./Header";
import GameOver from "./GameOver";
import Jokers from "./Jokers";
import MidQuestions from "./MidQuestions";
import mockQuestions from "./MockData";
import "./Quiz.css";

//Sounds Import

import {
  playCorrectSound,
  playWrongSound,
  thirtySecSound,
  playDecisionSound,
} from "./soundUtils";

/**
 * Quiz Component
 *
 * Main game loop:
 *  - Loads questions (mocked for now)
 *  - Tracks score, timer, jokers, and current question
 *  - Shows feedback overlay (MidQuestions) after each answer
 */

function Quiz({ questions: initialQuestions, numQuestions, difficulty }) {
  // Core state
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);

  // Answer/result state
  const [selectedAnswer, setSelectedAnswer] = useState(null); // chosen option
  const [revealResult, setRevealResult] = useState(false); // whether to color buttons

  // Timer state
  const [timer, setTimer] = useState(30);
  const [maxTime, setMaxTime] = useState(30);
  const [isFrozen, setIsFrozen] = useState(false); // pause countdown when locked

  // Answer buttons
  const [shuffledAnswers, setShuffledAnswers] = useState([]);

  // Jokers (power-ups)
  const [doubleActive, setDoubleActive] = useState(false);
  const [wrongAttempts, setWrongAttempts] = useState([]);
  const [tries, setTries] = useState(0);
  const [jokers, setJokers] = useState({
    extraTime: true,
    fiftyFifty: true,
    doubleAnswer: true,
  });

  // Overlay (between questions)
  const [showMidQuestions, setShowMidQuestions] = useState(false);
  const [midAnswer, setMidAnswer] = useState(null);

  /**
   * Move to the next question
   */
  const handleNext = () => {
    setSelectedAnswer(null);
    setWrongAttempts([]); // reset
    setCurrentIndex((prev) => prev + 1);
    setTimer(30);
    setMaxTime(30);
    setTries(0);
    thirtySecSound("play");
  };

  /**
   * Reveal answer and update score
   * If timedOut is true, treat as wrong answer
   */

  const revealAnswer = useCallback(
    (answer, timedOut = false) => {
      setSelectedAnswer(answer);
      setIsFrozen(true);
      thirtySecSound("stop");
      playDecisionSound();

      setTimeout(() => {
        const correct = questions[currentIndex].correct_answer;

        if (!timedOut && answer === questions[currentIndex].correct_answer) {
          setScore((prev) => prev + 100);
          setMidAnswer("correct");
          playCorrectSound();
        } else {
          setScore((prev) => (prev >= 50 ? prev - 50 : 0));
          setMidAnswer("wrong");
          playWrongSound();
        }
        setShowMidQuestions(true);
        setRevealResult(true);
      }, 5000);
    },
    [questions, currentIndex, score] // dependencies to keep it stable
  );

  /**
   * Load mock questions when game starts
   */
  useEffect(() => {
    async function loadQuestions() {
      setLoading(true);
      //const sliced = mockQuestions.slice(0, numQuestions);
      const sliced = initialQuestions.slice(0, numQuestions);
      setQuestions(sliced);
      setCurrentIndex(0);
      setScore(0);
      setSelectedAnswer(null);
      setTimer(30);
      setMaxTime(30);
      setLoading(false);
      thirtySecSound("play");
    }
    loadQuestions();
  }, [numQuestions, difficulty]);

  /**
   * Shuffle answers for current question
   */
  useEffect(() => {
    if (questions.length > 0 && currentIndex < questions.length) {
      const q = questions[currentIndex];
      const answers = [...q.incorrect_answers, q.correct_answer].sort(
        () => Math.random() - 0.5
      );
      setShuffledAnswers(answers);
    }
  }, [currentIndex, questions]);

  /**
   * Timer countdown
   */
  useEffect(() => {
    if (loading || questions.length === 0 || isFrozen) return;

    if (timer === 0) {
      thirtySecSound("stop");
      revealAnswer(null, true);
      return;
    }

    const countdown = setInterval(() => {
      setTimer((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(countdown);
  }, [timer, loading, questions.length, isFrozen, revealAnswer]); // ✅ include revealAnswer

  /**
   * Joker actions
   */
  const useExtraTime = () => {
    setTimer((prev) => prev + 30);
    setMaxTime((prev) => prev + 30);
    setJokers((prev) => ({ ...prev, extraTime: false }));
  };

  const useFiftyFifty = () => {
    const q = questions[currentIndex];
    const incorrect = [...q.incorrect_answers];
    const toRemove = incorrect.sort(() => Math.random() - 0.5).slice(0, 2);

    const reduced = [
      q.correct_answer,
      ...incorrect.filter((ans) => !toRemove.includes(ans)),
    ].sort(() => Math.random() - 0.5);

    setShuffledAnswers(reduced);
    setJokers((prev) => ({ ...prev, fiftyFifty: false }));
  };

  const useDoubleAnswer = () => {
    // Activate joker and disable button
    setDoubleActive(true);
    setJokers((prev) => ({ ...prev, doubleAnswer: false }));
  };

  /**
   * Handle when player clicks an answer
   */
  const handleAnswer = (answer) => {
    if (doubleActive) {
      // First wrong attempt
      if (answer !== questions[currentIndex].correct_answer && tries === 0) {
        setSelectedAnswer(answer); // highlight the button
        thirtySecSound("pause");
        playDecisionSound();
        setTries(1);

        // After 2s → gray it out & let them retry
        setTimeout(() => {
          setWrongAttempts((prev) => [...prev, answer]);
          setSelectedAnswer(null); // clear so they can pick again
          thirtySecSound("play");
        }, 5000);

        return;
      }

      // Second wrong → reveal fully
      if (answer !== questions[currentIndex].correct_answer && tries === 1) {
        setDoubleActive(false);
        revealAnswer(answer, false);
        return;
      }

      // Correct (on first or second try) → reveal
      setDoubleActive(false);
      revealAnswer(answer, false);
      return;
    }

    // Normal mode
    revealAnswer(answer, false);
  };

  const currentQuestion = questions[currentIndex];

  if (loading) return <h2>Loading questions...</h2>;
  if (!currentQuestion) return <h2>No question available</h2>;

  return (
    <main>
      {/* Score + question counter */}
      <Header score={score} currentIndex={currentIndex} questions={questions} />

      <div className="question">
        {/* Joker buttons */}
        <Jokers
          jokers={jokers}
          useExtraTime={useExtraTime}
          useFiftyFifty={useFiftyFifty}
          useDoubleAnswer={useDoubleAnswer}
        />

        {/* Timer */}
        <div className="timer-bar">
          <div
            className="timer-fill"
            style={{
              width: `${(timer / maxTime) * 100}%`,
              backgroundColor: timer > 10 ? "green" : "red",
              transition: "width 1s linear, background-color 0.5s ease",
            }}
          >
            {timer}
          </div>
        </div>

        {/* Question */}
        <h2 dangerouslySetInnerHTML={{ __html: currentQuestion.question }} />

        {/* Answer options */}
        <div className="answers">
          {shuffledAnswers.map((answer, index) => (
            <button
              key={index}
              onClick={() => handleAnswer(answer)}
              disabled={selectedAnswer !== null}
              className={`answer-button
              ${selectedAnswer === answer && !revealResult ? "selected" : ""}
              ${
                revealResult &&
                answer === questions[currentIndex].correct_answer
                  ? "correct"
                  : ""
              }
              ${
                revealResult &&
                selectedAnswer === answer &&
                answer !== questions[currentIndex].correct_answer
                  ? "wrong"
                  : ""
              }
              ${
                selectedAnswer !== answer &&
                selectedAnswer !== null &&
                !revealResult
                  ? "disabled-gray"
                  : ""
              }
            `}
              dangerouslySetInnerHTML={{ __html: answer }}
            />
          ))}
        </div>
      </div>

      {/* Overlay feedback after answering */}
      {showMidQuestions && (
        <div className="overlay">
          <MidQuestions
            answer={midAnswer}
            onNext={() => {
              handleNext();
              setRevealResult(false);
              setIsFrozen(false);
              setShowMidQuestions(false);
            }}
          />
        </div>
      )}
    </main>
  );
}

export default Quiz;
