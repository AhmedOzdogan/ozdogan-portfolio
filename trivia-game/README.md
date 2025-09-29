# 🧠 MindMaze

**MindMaze** is an interactive trivia quiz game built with **React**. Challenge yourself with dynamic multiple-choice questions, immersive sound effects, and strategic power-ups ("jokers")—all designed to test your knowledge under pressure in a fun, game-like experience.

---

## 🚀 Features

- 🎯 **Live Trivia API** – Fetches fresh questions from [The Trivia API](https://the-trivia-api.com/).
- 🎶 **Sound Effects** – Hear the ticking timer, correct/wrong answer cues, and suspenseful decisions.
- 🧩 **Jokers (Power-Ups):**
  - ⏱ **Extra Time** – Adds 30 seconds to the timer.
  - ➗ **50/50** – Removes two incorrect answers.
  - 🔁 **Double Answer** – Retry if your first answer is wrong.
- ⏳ **Countdown Timer** – 30 seconds per question, with a suspenseful tick.
- 🏆 **Score System** – +100 for correct, -50 for wrong (never below zero).
- 📊 **Max Score Tracking** – See your perfect score target.
- 📱 **Responsive UI** – Optimized for desktop and mobile.

---

## 🕹 How to Play

1. **Start the Game**

   - Select question count, difficulty, and category.
   - Click **Start**.

2. **Answer Questions**

   - You have **30 seconds** per question.
   - Click your answer.
   - Correct: +100 points. Wrong: -50 points.

3. **Use Jokers**

   - Click a joker for an advantage:
     - **Extra Time**: +30s to timer.
     - **50/50**: Only two options remain.
     - **Double Answer**: Retry once if wrong.

4. **Between Questions**

   - See feedback overlays ("Correct" or "Wrong").
   - Click **Next** to continue.

5. **Game Over**
   - View your final score on the **Game Over** screen.

---

## 🛠 Tech Stack

- **React 18**
- **Context API** – Global state (score, jokers, etc.)
- **Custom Hooks** – Game logic and refresh limits
- **Trivia API** – Question source
- **CSS Modules** – Component styling
- **Sound Management** – Custom `soundUtils.js`

---

## 📂 Project Structure

```
mindmaze/
├── src/
│   ├── components/
│   │   ├── Quiz.js           # Main game loop
│   │   ├── Welcome.js        # Start screen
│   │   ├── GameOver.js       # End screen
│   │   ├── Jokers.js         # Power-up buttons
│   │   ├── Timer.js          # Countdown timer
│   │   ├── MidQuestions.js   # Overlay feedback
│   │   ├── AnswerOptions.js  # Multiple choice answers
│   │   └── SoundControls.js  # Mute/Unmute buttons
│   ├── contexts/
│   │   └── QuizContext.js    # Global state provider
│   ├── utils/
│   │   ├── Api.js            # Fetches questions
│   │   └── soundUtils.js     # Plays/stops sounds
│   └── styles/
│       └── Quiz.css
└── README.md
```

---

## ⚙️ Installation & Setup

1. **Clone the repository:**

   ```bash
   https://github.com/AhmedOzdogan/ozdogan-portfolio.git
   cd trivia-game
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Run the development server:**

   ```bash
   npm start
   ```

   > Use this for local development and testing.

4. **Build for production:**

   ```bash
   npm run build
   ```

   > Run this after development to create an optimized production build.

---

## 🖼️ Screenshots

Below are 12 screenshots showcasing MindMaze's gameplay and features.  
All images are located in `public/img/screenshots/`.
