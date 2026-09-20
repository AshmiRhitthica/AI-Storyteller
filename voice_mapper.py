
VOICE_CAST = {
    "narrator": {
        "voice": "bf_isabella",
        "lang": "b"
    },

    "female": {
        "voice": "af_bella",
        "lang": "a"
    },

    "male": {
        "voice": "am_adam",
        "lang": "a"
    }
}

class VoiceManager:

    def __init__(self, narrator_style="normal"):

        self.narrator_style = narrator_style

        self.character_voices = {}

        self.narrator_voice = VOICE_CAST["narrator"]


    def get_narrator(self):

        return self.narrator_voice


    def assign_voice(self, character, gender="female"):

        if not character:
            return self.get_narrator()

        # Already assigned
        if character in self.character_voices:
            return self.character_voices[character]

        gender = str(gender).lower().strip()

        if gender == "male":
            voice = VOICE_CAST["male"]

        elif gender == "female":
            voice = VOICE_CAST["female"]

        else:
            # Safe fallback
            voice = VOICE_CAST["female"]

        self.character_voices[character] = voice

        return voice


    def get_voice(self, segment, character_genders=None):

        if character_genders is None:
            character_genders = {}

        if segment.get("type") == "narration":
            return self.get_narrator()

        if segment.get("type") == "dialogue":

            character = segment.get("speaker")

            # Unknown speaker → narrator
            if not character:
                return self.get_narrator()

            gender = character_genders.get(
                character,
                "female"
            )

            return self.assign_voice(
                character,
                gender
            )

        return self.get_narrator()


_default_manager = VoiceManager()


def assign_voice(character, gender="female"):

    return _default_manager.assign_voice(
        character,
        gender
    )


def get_voice(character):

    if character is None:
        return _default_manager.get_narrator()

    return _default_manager.character_voices.get(
        character,
        VOICE_CAST["female"]
    )