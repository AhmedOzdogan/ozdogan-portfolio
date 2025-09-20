import { useQuiz } from "../contexts/QuizContext";
import { FaVolumeUp, FaVolumeMute } from "react-icons/fa";

const SoundControls = () => {
  const { soundOn, setSoundOn } = useQuiz();

  const buttonStyle = {
    backgroundColor: "#282833ff",
    border: "none",
    borderRadius: "50%",
    width: "50px",
    height: "50px",
    fontSize: "1.5rem",
    cursor: "pointer",
    color: "#ffb703",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    transition: "all 0.2s ease-in-out",
  };

  const hoverStyle = {
    transform: "scale(1.1)",
    backgroundColor: "#2c2c40",
  };

  return (
    <div className="sound-controls">
      <button
        style={buttonStyle}
        onMouseEnter={(e) => {
          Object.assign(e.target.style, hoverStyle);
        }}
        onMouseLeave={(e) => {
          Object.assign(e.target.style, buttonStyle);
        }}
        onClick={() => setSoundOn(!soundOn)}
      >
        {soundOn ? <FaVolumeUp /> : <FaVolumeMute />}
      </button>
    </div>
  );
};

export default SoundControls;
