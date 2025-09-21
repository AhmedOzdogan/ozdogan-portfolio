import axios from "axios";

export const fetchQuestions = async (
  limit = 10,
  difficulty = "easy",
  categorySlug = ""
) => {
  let url = `https://the-trivia-api.com/v2/questions?limit=${limit}&difficulties=${difficulty}`;
  if (categorySlug) {
    url += `&categories=${categorySlug}`;
  }
  const { data } = await axios.get(url);

  return data.map((q) => ({
    question: q.question.text,
    correct_answer: q.correctAnswer,
    incorrect_answers: q.incorrectAnswers,
  }));
};
