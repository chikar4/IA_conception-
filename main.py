from brain import Brain
from voice_in import record_audio, transcribe, wait_for_push_to_talk
from voice_out import speak

QUIT_KEY = "esc"


def main():
    print("=== Assistant vocal ===")
    print(f"Maintiens SPACE pour parler, ou {QUIT_KEY.upper()} pour quitter.\n")

    try:
        brain = Brain()
    except RuntimeError as exc:
        print(f"Erreur: {exc}")
        return

    while True:
        started = wait_for_push_to_talk(cancel_key=QUIT_KEY)
        if not started:
            print("A bientot.")
            break

        print("[Ecoute...]")
        audio = record_audio()
        text = transcribe(audio)
        if not text:
            continue

        print(f"Toi: {text}")
        reply = brain.ask(text)
        print(f"Assistant: {reply}")
        speak(reply)


if __name__ == "__main__":
    main()
