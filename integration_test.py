from story_generator import generate_story, clean_story
from story_parser import analyze_story
from character_profiles import infer_character_profiles
from voice_mapper import VoiceManager
from tts_engine import TTSEngine

user_prompt = input(
    "\nWhat kind of story do you want?\n> "
).strip()

if not user_prompt:
    raise ValueError("Story prompt cannot be empty.")


print("\nGenerating story...\n")

story = generate_story(user_prompt)
story = clean_story(story)


print("\n================ STORY ================\n")
print(story)



print("\n================ ANALYZING ================\n")

segments, registry = analyze_story(story)



registry = infer_character_profiles(
    story,
    registry
)


character_genders = {}

for character in registry.characters:

    name = (
        character.get("name")
        or character.get("description")
    )

    gender = character.get("gender")

    if name and gender:
        character_genders[name] = gender


print("\n================ CHARACTERS ================\n")

for character in registry.characters:

    name = (
        character.get("name")
        or character.get("description")
        or "Unknown"
    )

    print(
        f"{name:<20} → "
        f"{character.get('gender') or 'unknown'}"
    )


voice_manager = VoiceManager(
    narrator_style="normal"
)


print("\n================ FINAL SEGMENTS ================\n")

for index, segment in enumerate(
    segments,
    start=1
):

    try:

        voice = voice_manager.get_voice(
            segment,
            character_genders
        )

        # Store voice directly inside segment
        segment["voice"] = voice

    except ValueError as error:

        print(
            f"Segment {index}: Voice mapping error"
        )
        print(error)
        print("-" * 60)

        continue


    print(f"Segment {index}")
    print("Type    :", segment["type"])

    if segment["type"] == "dialogue":

        print(
            "Speaker :",
            segment.get("speaker")
            or "Unknown"
        )

    print("Text    :", segment["text"])
    print("Voice   :", voice["voice"])
    print("Language:", voice["lang"])

    print("-" * 60)


print("\n================ VOICE CAST ================\n")

narrator = voice_manager.get_narrator()

print(
    "Narrator".ljust(20),
    "→",
    narrator["voice"]
)

for character, voice in (
    voice_manager.character_voices.items()
):

    print(
        character.ljust(20),
        "→",
        voice["voice"]
    )


print("\n================ TEXT TO SPEECH ================\n")

tts = TTSEngine()

audio_path = tts.generate_story_audio(
    segments,
    output_path="output/final_story.wav"
)


print("\n================================================")
print("STORYTELLER COMPLETE!")
print("================================================")

print(
    f"\nFinal audio:\n{audio_path}"
)