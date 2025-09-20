const AnswerButton = ({
  answer,
  isSelected,
  isCorrect,
  isWrong,
  isDisabled,
  onClick,
}) => {
  return (
    <button
      onClick={() => onClick(answer)}
      disabled={isDisabled}
      className={`answer-button
        ${isSelected ? "selected" : ""}
        ${isCorrect ? "correct" : ""}
        ${isWrong ? "wrong" : ""}
        ${isDisabled ? "disabled-gray" : ""}
      `}
      dangerouslySetInnerHTML={{ __html: answer }}
    />
  );
};

export default AnswerButton;
