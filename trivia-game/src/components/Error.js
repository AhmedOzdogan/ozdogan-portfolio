const Error = () => {
  const textStyle = {
    marginTop: "20px",
    fontSize: "2rem",
    color: "#ffffffff",
    fontWeight: "bold",
    textAlign: "center",
  };

  const buttonStyle = {
    color: "#1e1e2f",
    fontWeight: "bold",
    display: "block",
    margin: "20px auto",
    padding: "10px 20px",
    fontSize: "16px",
    border: "none",
    borderRadius: "12px",
    backgroundColor: "#ffb703",
    cursor: "pointer",
  };

  const wrapperStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
  };

  return (
    <main>
      <div className="wrapper" style={wrapperStyle}>
        <h2 style={textStyle}>
          Oops! Something unexpected happened. Please restart the game.
        </h2>
        <button onClick={() => window.location.reload()} style={buttonStyle}>
          Restart Game
        </button>
      </div>
    </main>
  );
};

export default Error;
