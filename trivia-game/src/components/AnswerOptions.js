import AnswerButton from "./AnswerButton";

const AnswerOptions = ({
  answers,
  selectedAnswer,
  revealResult,
  currentQuestion,
  wrongAttempts,
  onAnswerClick,
}) => {
  return (
    <div className="answers">
      {answers.map((answer, index) => {
        const isSelected = selectedAnswer === answer && !revealResult;
        const isCorrect =
          revealResult && answer === currentQuestion.correct_answer;
        const isWrong =
          revealResult &&
          selectedAnswer === answer &&
          answer !== currentQuestion.correct_answer;
        const isDisabled =
          (selectedAnswer !== answer &&
            selectedAnswer !== null &&
            !revealResult) ||
          wrongAttempts.includes(answer);

        return (
          <AnswerButton
            key={index}
            answer={answer}
            isSelected={isSelected}
            isCorrect={isCorrect}
            isWrong={isWrong}
            isDisabled={isDisabled}
            onClick={onAnswerClick}
          />
        );
      })}
    </div>
  );
};

export default AnswerOptions;
