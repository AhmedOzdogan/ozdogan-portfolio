function HowToPlay() {
  const buttonStyle = {
    width: "200px",
    backgroundColor: "#282833ff",
    border: "none",
    borderRadius: "16px",
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
    <div>
      <button style={buttonStyle}>How To Play</button>
    </div>
  );
}
export default HowToPlay;
