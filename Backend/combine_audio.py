import os

import numpy as np
import soundfile as sf

from story_parser import parse_story


INPUT_FOLDER = "output/multivoice"

OUTPUT_FILE = os.path.join(
    INPUT_FOLDER,
    "story.wav"
)

SAMPLE_RATE = 24000

NARRATION_TO_NARRATION = 0.20
NARRATION_TO_DIALOGUE = 0.35
DIALOGUE_TO_NARRATION = 0.30
DIALOGUE_TO_DIALOGUE = 0.45

START_SILENCE = 0.10
END_SILENCE = 0.50

FADE_IN_SECONDS = 0.015
FADE_OUT_SECONDS = 0.025



story = """
Lily walked into the forest with Jack beside her.

"Are we going the right way?" Lily asked.

Jack looked around carefully.

"Yes. The old house should be just ahead."

A woman suddenly stepped out from behind a tree.

"My name is Mira," she said.

Lily took a step back.

"Who are you?"

Mira smiled mysteriously.

"You really shouldn't be here."

A second man appeared behind Mira.

"We need to leave," he said.

Jack reached for Lily's hand.

"Come on. We're going."

The forest became silent again.
"""


def create_silence(seconds):

    samples = int(
        SAMPLE_RATE * seconds
    )

    return np.zeros(
        samples,
        dtype=np.float32
    )

def apply_fade(audio):

    audio = audio.astype(
        np.float32,
        copy=True
    )

    fade_in_samples = int(
        SAMPLE_RATE * FADE_IN_SECONDS
    )

    fade_out_samples = int(
        SAMPLE_RATE * FADE_OUT_SECONDS
    )

    if (
        fade_in_samples > 0
        and len(audio) > fade_in_samples
    ):

        fade_in = np.linspace(
            0.0,
            1.0,
            fade_in_samples,
            dtype=np.float32
        )

        audio[:fade_in_samples] *= fade_in


    if (
        fade_out_samples > 0
        and len(audio) > fade_out_samples
    ):

        fade_out = np.linspace(
            1.0,
            0.0,
            fade_out_samples,
            dtype=np.float32
        )

        audio[-fade_out_samples:] *= fade_out

    return audio

def get_segment_files():

    files = [
        file
        for file in os.listdir(INPUT_FOLDER)
        if (
            file.startswith("segment_")
            and file.endswith(".wav")
        )
    ]

    files.sort(
        key=lambda filename: int(
            filename
            .replace("segment_", "")
            .replace(".wav", "")
        )
    )

    return files


def get_pause(previous_type, current_type):

    if (
        previous_type == "narration"
        and current_type == "narration"
    ):

        return NARRATION_TO_NARRATION

    if (
        previous_type == "narration"
        and current_type == "dialogue"
    ):

        return NARRATION_TO_DIALOGUE

    if (
        previous_type == "dialogue"
        and current_type == "narration"
    ):

        return DIALOGUE_TO_NARRATION

    if (
        previous_type == "dialogue"
        and current_type == "dialogue"
    ):

        return DIALOGUE_TO_DIALOGUE

    return 0.30



def combine_audio():

    print(
        "\n================ COMBINING AUDIO ================\n"
    )
    segments = parse_story(story)

    files = get_segment_files()

    if not files:

        print(
            "No segment WAV files found."
        )

        return

    if len(files) != len(segments):

        raise ValueError(
            f"Number of audio segments ({len(files)}) "
            f"does not match parsed story segments "
            f"({len(segments)})."
        )

    print("Segments found:\n")

    for index, file in enumerate(files):

        print(
            f"- {file} "
            f"→ {segments[index]['type']}"
        )

    print(
        "\nCombining...\n"
    )

    all_audio = []

    all_audio.append(
        create_silence(
            START_SILENCE
        )
    )

    previous_type = None


    for index, file in enumerate(files):

        path = os.path.join(
            INPUT_FOLDER,
            file
        )

        current_type = segments[index]["type"]

        print(
            f"Adding: {file} "
            f"({current_type})"
        )



        if previous_type is not None:

            pause = get_pause(
                previous_type,
                current_type
            )

            all_audio.append(
                create_silence(pause)
            )

            print(
                f"  Pause: {pause:.2f}s"
            )


        audio, sample_rate = sf.read(
            path,
            dtype="float32"
        )

        if sample_rate != SAMPLE_RATE:

            raise ValueError(
                f"{file} has sample rate "
                f"{sample_rate}, expected "
                f"{SAMPLE_RATE}."
            )

        if audio.ndim > 1:

            audio = audio.mean(
                axis=1
            )
        audio = apply_fade(
            audio
        )

        all_audio.append(
            audio
        )

        previous_type = current_type



    all_audio.append(
        create_silence(
            END_SILENCE
        )
    )

    
    # Combine

    final_audio = np.concatenate(
        all_audio
    )


    sf.write(
        OUTPUT_FILE,
        final_audio,
        SAMPLE_RATE
    )


    duration = (
        len(final_audio)
        / SAMPLE_RATE
    )

    print(
        "\n================ SUCCESS ================\n"
    )

    print(
        "Final story saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        f"\nDuration: "
        f"{duration:.2f} seconds"
    )

if __name__ == "__main__":

    combine_audio()