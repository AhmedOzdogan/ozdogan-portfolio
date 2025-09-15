import axios from "axios";

export const fetchQuestions = async (amount = 10, difficulty = "easy") => {
  const url = `https://opentdb.com/api.php?amount=${amount}&difficulty=${difficulty}&type=multiple`;
  const { data } = await axios.get(url);
  return data.results;
};
