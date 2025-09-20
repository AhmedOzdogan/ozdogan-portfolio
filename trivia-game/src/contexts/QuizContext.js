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
  const [soundOn, setSoundOn] = useState(true);

  useEffect(() => {
    setSoundEnabled(soundOn); // mute/unmute globally
    console.log("Sound setting changed:", soundOn);
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
