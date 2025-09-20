const Loading = () => {
  {
    /* Simple CSS spinner for loading state */
  }

  const spinnerStyle = {
    width: "120px",
    height: "120px",
    border: "15px solid #ffb703",
    borderTop: "15px solid #ffffffff",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  };

  const spinnerContainerStyle = {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    flexGrow: 1,
    height: "100%",
  };

  const textStyle = {
    marginTop: "20px",
    fontSize: "2rem",
    color: "#ffffffff",
    fontWeight: "bold",
    textAlign: "center",
  };

  const styleSheet = document.styleSheets[0];
  const keyframes = `
    @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
    }`;

  styleSheet.insertRule(keyframes, styleSheet.cssRules.length);

  return (
    <main>
      <div className="spinner-container" style={spinnerContainerStyle}>
        <div className="spinner" style={spinnerStyle}></div>
        <p style={textStyle}>Loading questions...</p>
      </div>
    </main>
  );
};

export default Loading;
