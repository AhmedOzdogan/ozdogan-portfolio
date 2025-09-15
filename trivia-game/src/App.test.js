import { render, screen, fireEvent, act } from "@testing-library/react";
import Quiz from "./components/Quiz";
import mockQuestions from "./components/MockData";

jest.useFakeTimers();

describe("Quiz Component", () => {
  test("renders loading and then first question", async () => {
    render(<Quiz numQuestions={1} difficulty="easy" />);

    expect(screen.getByText(/loading questions/i)).toBeInTheDocument();

    // Let effect resolve
    await screen.findByText(/Question 1/i);
    expect(screen.getByText(/Question 1/i)).toBeInTheDocument();
  });

  test("selecting an answer highlights it and freezes timer", async () => {
    render(<Quiz numQuestions={1} difficulty="easy" />);

    // Wait until question loads
    await screen.findByText(/Question 1/i);

    const firstAnswer = screen.getAllByRole("button")[0];
    fireEvent.click(firstAnswer);

    // Immediately should have "selected"
    expect(firstAnswer.className).toMatch(/selected/);

    // Timer should stop decreasing
    const timerBefore = screen.getByText("30");
    act(() => {
      jest.advanceTimersByTime(3000); // advance 3s
    });
    expect(screen.getByText("30")).toBe(timerBefore);
  });

  test("after 5s shows correct/wrong and after 10s goes next", async () => {
    render(<Quiz numQuestions={2} difficulty="easy" />);

    // Wait until question loads
    await screen.findByText(/Question 1/i);

    const firstAnswer = screen.getAllByRole("button")[0];
    fireEvent.click(firstAnswer);

    // After 5s → reveal
    act(() => {
      jest.advanceTimersByTime(5000);
    });

    expect(firstAnswer.className.match(/correct|wrong/)).not.toBeNull();

    // After 10s → move next question
    act(() => {
      jest.advanceTimersByTime(5000);
    });

    expect(screen.getByText(/Question 2/i)).toBeInTheDocument();
  });
});
