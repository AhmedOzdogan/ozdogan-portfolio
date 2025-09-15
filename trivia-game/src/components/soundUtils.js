import { Howl } from "howler";
import correctSound from "./sounds/correct.mp3";
import wrongSound from "./sounds/wrong.mp3";
import thirtysec from "./sounds/thirtysec.mp3";
import decisionSound from "./sounds/decision.mp3";

const correct = new Howl({ src: [correctSound] });
const wrong = new Howl({ src: [wrongSound] });
const thirtySec = new Howl({ src: [thirtysec], loop: true, volume: 0.5 });
const decision = new Howl({ src: [decisionSound] });

export const playCorrectSound = () => correct.play();
export const playWrongSound = () => wrong.play();
export const playDecisionSound = () => decision.play();

export const thirtySecSound = (input) => {
  if (input === "play") {
    if (!thirtySec.playing()) {
      thirtySec.play();
    }
  } else if (input === "stop") {
    thirtySec.stop();
  } else if (input === "pause") {
    thirtySec.pause();
  }
};
