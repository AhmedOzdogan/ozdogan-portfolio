// src/mockQuestions.js
const mockQuestions = [
  {
    category: "General Knowledge",
    type: "multiple",
    difficulty: "easy",
    question: "What is the capital of France?",
    correct_answer: "Paris",
    incorrect_answers: ["Berlin", "Madrid", "Rome"],
  },
  {
    category: "Science & Nature",
    type: "multiple",
    difficulty: "medium",
    question: "Which planet is known as the Red Planet?",
    correct_answer: "Mars",
    incorrect_answers: ["Venus", "Jupiter", "Saturn"],
  },
  {
    category: "Entertainment: Video Games",
    type: "multiple",
    difficulty: "hard",
    question:
      "In 'The Legend of Zelda: Ocarina of Time', what is the name of Link's fairy companion?",
    correct_answer: "Navi",
    incorrect_answers: ["Tatl", "Ezlo", "Midna"],
  },
];

export default mockQuestions;
