import { useState } from "react";
import "../styles/HowToPlay.css";

function HowToPlay() {
  const [showRules, setShowRules] = useState(false);
  const [closing, setClosing] = useState(false);

  const handleClose = () => {
    setClosing(true);
    setTimeout(() => {
      setShowRules(false);
      setClosing(false);
    }, 500);
  };

  return (
    <div>
      <button className="howto-btn" onClick={() => setShowRules(true)}>
        How To Play
      </button>

      {showRules && (
        <div className={`rules-overlay ${closing ? "closing" : ""}`}>
          <div className="rules-content">
            <h2 className="rules-title">📜 How to Play</h2>

            <div className="rules-section">
              <h3>🎯 Scoring</h3>
              <table className="rules-table">
                <tbody>
                  <tr>
                    <td className="correct">✔ Correct</td>
                    <td>+100 points</td>
                  </tr>
                  <tr>
                    <td className="wrong">✘ Wrong</td>
                    <td>-50 points</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="rules-section">
              <h3>⏳ Timer</h3>
              <p>
                You have <strong>30 seconds</strong> to answer each question.
              </p>
            </div>

            <div className="rules-section">
              <h3>🃏 Jokers</h3>
              <table className="rules-table">
                <tbody>
                  <tr>
                    <td>+30 Sec</td>
                    <td>Adds 30 seconds to your timer.</td>
                  </tr>
                  <tr>
                    <td>Double Answer</td>
                    <td>Get a second chance if your first choice is wrong.</td>
                  </tr>
                  <tr>
                    <td>50/50</td>
                    <td>Eliminates two incorrect answers.</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <button className="close-btn" onClick={handleClose}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default HowToPlay;
