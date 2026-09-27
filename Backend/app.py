from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from story_generator import generate_story, clean_story
from story_parser import analyze_story
from character_profiles import infer_character_profiles
from voice_mapper import VoiceManager
from tts_engine import TTSEngine

app = FastAPI(
    title="AI Tales API",
    description="Backend API for AI Tales",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StoryRequest(BaseModel):
    story: str


class GenerateStoryRequest(BaseModel):
    prompt: str
    genre: str = "Fantasy"
    length: str = "Short"


@app.get("/")
def home():
    return {
        "message": "AI Tales API is running!",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

def process_story_pipeline(story):

    print("\n========================================")
    print("PROCESSING STORY")
    print("========================================")

    print("\n[1/5] Analyzing story...")

    segments, registry = analyze_story(story)


    print("[2/5] Inferring character profiles...")

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


    print("[3/5] Assigning voices...")

    voice_manager = VoiceManager(
        narrator_style="normal"
    )

    for segment in segments:

        segment["voice"] = voice_manager.get_voice(
            segment,
            character_genders
        )


    print("[4/5] Generating audio with Kokoro...")

    output_path = "output/final_story.wav"

    tts = TTSEngine()

    audio_path = tts.generate_story_audio(
        segments,
        output_path=output_path
    )


    print("[5/5] Story processing complete.")

    print(
        f"\nAudio created at: {audio_path}"
    )

    characters = []

    for character in registry.characters:

        name = (
            character.get("name")
            or character.get("description")
            or "Unknown"
        )

        characters.append({
            "name": name,
            "gender": character.get("gender")
        })


    return {
        "status": "success",
        "message": "Story processed successfully.",
        "story": story,
        "characters": characters,
        "audio_url": "/audio"
    }


@app.post("/process-story")
def process_story(request: StoryRequest):

    story = request.story.strip()

    if not story:

        raise HTTPException(
            status_code=400,
            detail="Story cannot be empty."
        )

    try:

        return process_story_pipeline(story)

    except Exception as error:

        print("\n========================================")
        print("ERROR")
        print("========================================")

        print(error)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/generate-story")
def generate_story_endpoint(
    request: GenerateStoryRequest
):

    prompt = request.prompt.strip()

    if not prompt:

        raise HTTPException(
            status_code=400,
            detail="Story prompt cannot be empty."
        )

    try:

        print("\n========================================")
        print("GENERATING NEW STORY")
        print("========================================")

        print("\nPrompt :", prompt)
        print("Genre  :", request.genre)
        print("Length :", request.length)


        generation_prompt = f"""
Write a {request.length.lower()} {request.genre.lower()} story.

Story idea:
{prompt}

Requirements:
- Include a narrator.
- Include characters with clear names.
- Include dialogue between characters when appropriate.
- Make the story engaging and coherent.
- Keep the story suitable for text-to-speech narration.
"""

        print("\nGenerating story with Gemini...")

        story = generate_story(
            generation_prompt
        )

        story = clean_story(story)


        if not story:

            raise RuntimeError(
                "Story generation returned empty text."
            )


        print("\n================ GENERATED STORY ================\n")

        print(story)

        result = process_story_pipeline(
            story
        )
        result["prompt"] = prompt
        result["genre"] = request.genre
        result["length"] = request.length

        return result

    except Exception as error:

        print("\n========================================")
        print("GENERATION ERROR")
        print("========================================")

        print(error)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/audio")
def get_audio():

    audio_path = Path(
        "output/final_story.wav"
    )


    if not audio_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Audio file not found."
        )


    return FileResponse(
        audio_path,
        media_type="audio/wav",
        filename="final_story.wav"
    )