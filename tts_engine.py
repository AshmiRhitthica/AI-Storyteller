import os
import numpy as np
import soundfile as sf
from kokoro import KPipeline


class TTSEngine:

    def __init__(self):

        print("\nLoading Kokoro...")

        self.pipeline_a = KPipeline(lang_code="a")
        self.pipeline_b = KPipeline(lang_code="b")

        print("Kokoro loaded.")



    def generate_segment(self, text, voice, lang):

        if not text.strip():
            return np.array([], dtype=np.float32)

        pipeline = (
            self.pipeline_a
            if lang == "a"
            else self.pipeline_b
        )

        audio_parts = []

        generator = pipeline(
            text,
            voice=voice
        )

        for _, _, audio in generator:

            if audio is not None:
                audio_parts.append(
                    np.asarray(audio, dtype=np.float32)
                )

        if not audio_parts:
            return np.array([], dtype=np.float32)

        return np.concatenate(audio_parts)



    def generate_story_audio(
        self,
        segments,
        output_path="output/final_story.wav"
    ):

        print("\n================ GENERATING AUDIO ================\n")

        all_audio = []

        for index, segment in enumerate(
            segments,
            start=1
        ):

            text = segment.get("text", "").strip()

            if not text:
                continue

            voice_info = segment.get("voice")

            if not voice_info:
                print(
                    f"Skipping segment {index}: "
                    "no voice assigned."
                )
                continue

            voice = voice_info["voice"]
            lang = voice_info["lang"]

            print(
                f"Segment {index}: "
                f"{voice} → {text[:60]}..."
            )

            audio = self.generate_segment(
                text,
                voice,
                lang
            )

            if len(audio) > 0:

                all_audio.append(audio)

                #pause between segments
                pause = np.zeros(
                    int(24000 * 0.25),
                    dtype=np.float32
                )

                all_audio.append(pause)


        if not all_audio:

            raise RuntimeError(
                "No audio was generated."
            )


        final_audio = np.concatenate(
            all_audio
        )


        # Make sure output directory exists
        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )


        sf.write(
            output_path,
            final_audio,
            24000
        )


        print(
            f"\nAudio saved to:\n{output_path}"
        )

        return output_path