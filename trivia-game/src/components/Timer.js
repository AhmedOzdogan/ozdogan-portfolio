const Timer = ({ timer, maxTime }) => {
  return (
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
  );
};

export default Timer;
