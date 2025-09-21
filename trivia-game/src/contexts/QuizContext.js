import { createContext, useContext, useState } from "react";
import { setSoundEnabled } from "../utils/soundUtils";
import { useEffect } from "react";

const QuizContext = createContext();

export const QuizProvider = ({ children }) => {
  const [score, setScore] = useState(0);
  const [maxScore, setMaxScore] = useState(0);
  const [jokers, setJokers] = useState({
    extraTime: true,
    fiftyFifty: true,
    doubleAnswer: true,
  });
  const [soundOn, setSoundOn] = useState(() => {
    const saved = localStorage.getItem("soundOn");
    return saved ? JSON.parse(saved) : true;
  });

  useEffect(() => {
    setSoundEnabled(soundOn);
    localStorage.setItem("soundOn", JSON.stringify(soundOn));
  }, [soundOn]);

  return (
    <QuizContext.Provider
      value={{
        score,
        setScore,
        jokers,
        setJokers,
        maxScore,
        setMaxScore,
        soundOn,
        setSoundOn,
      }}
    >
      {children}
    </QuizContext.Provider>
  );
};

// custom hook for convenience
export const useQuiz = () => useContext(QuizContext);
