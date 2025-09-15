import { FaClock, FaPercent, FaRedoAlt } from "react-icons/fa";
import "./Jokers.css";

function Jokers({ jokers, useExtraTime, useFiftyFifty, useDoubleAnswer }) {
  return (
    <div className="jokers">
      <button
        className="joker-button"
        onClick={useExtraTime}
        disabled={!jokers.extraTime}
      >
        <FaClock className="joker-icon" /> +30s
      </button>

      <button
        className="joker-button"
        onClick={useFiftyFifty}
        disabled={!jokers.fiftyFifty}
      >
        <FaPercent className="joker-icon" /> 50/50
      </button>

      <button
        className="joker-button"
        onClick={useDoubleAnswer}
        disabled={!jokers.doubleAnswer}
      >
        <FaRedoAlt className="joker-icon" /> Double
      </button>
    </div>
  );
}

export default Jokers;
