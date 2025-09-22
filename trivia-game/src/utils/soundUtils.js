import { Howl, Howler } from "howler";
import correctSound from "../assets/sounds/correct.mp3";
import wrongSound from "../assets/sounds/wrong.mp3";
import thirtysecSound from "../assets/sounds/thirtysec.mp3";
import decisionSound from "../assets/sounds/decision.mp3";

// Shared sound instances
const sounds = {
  correct: new Howl({ src: [correctSound] }),
  wrong: new Howl({ src: [wrongSound] }),
  thirty: new Howl({ src: [thirtysecSound], loop: true }),
  decision: new Howl({ src: [decisionSound] }),
};

export const unlockAudio = () => {
  if (Howler.ctx && Howler.ctx.state === "suspended") {
    Howler.ctx.resume();
  }
};

// Enforce mute/unmute globally
export const setSoundEnabled = (enabled) => {
  Howler.mute(!enabled);
  Howler.volume(enabled ? 1 : 0);
};

// Safe wrapper to play a sound if not muted
const safePlay = (sound) => {
  if (!Howler._muted) {
    try {
      sound.stop(); // reset to beginning
      sound.play();
    } catch (e) {
      console.warn("Sound play failed:", e);
    }
  }
};

// Wrappers for each effect
export const playCorrectSound = () => safePlay(sounds.correct);
export const playWrongSound = () => safePlay(sounds.wrong);
export const playDecisionSound = () => safePlay(sounds.decision);

// Special case: ticking sound with commands
export const thirtySecSound = (cmd) => {
  const h = sounds.thirty;

  if (cmd === "play") {
    if (!Howler._muted && !h.playing()) {
      h.play();
    }
  } else if (cmd === "pause") {
    if (h.playing()) h.pause();
  } else if (cmd === "stop") {
    if (h.playing()) h.stop();
  }
};
