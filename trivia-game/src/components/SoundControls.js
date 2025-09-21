import { useQuiz } from "../contexts/QuizContext";
import { FaVolumeUp, FaVolumeMute } from "react-icons/fa";

const SoundControls = () => {
  const { soundOn, setSoundOn } = useQuiz();

  const buttonStyle = {
    backgroundColor: "#ffe66d",
    border: "none",
    borderRadius: "50%",
    width: "50px",
    height: "50px",
    fontSize: "1.5rem",
    cursor: "pointer",
    color: "#333",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  };

  return (
    <div className="sound-controls">
      <button style={buttonStyle} onClick={() => setSoundOn(!soundOn)}>
        {soundOn ? <FaVolumeUp /> : <FaVolumeMute />}
      </button>
    </div>
  );
};

export default SoundControls;
