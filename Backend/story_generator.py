import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL = "gemini-3.5-flash"

OUTPUT_DIR = "output"
STORY_FILE = os.path.join(
    OUTPUT_DIR,
    "story.txt"
)


llm_model = ChatGoogleGenerativeAI(
    model=MODEL,
    api_key=os.environ["GOOGLE_GEMINI_API_KEY"],
    temperature=0.7,
)


# STORY GENERATION

def generate_story(user_prompt):

    prompt = f"""
You are a simple short-story writer.

Write ONE complete story based on this idea:

{user_prompt}

Rules:

- Write approximately 300-400 words.
- Use simple and natural English.
- Give the main characters names.
- Include a beginning, middle, problem, climax and ending.
- Use normal paragraphs.
- Use dialogue when appropriate.
- Keep the events connected.
- Do not repeat scenes.
- Do not repeat paragraphs.
- Do not repeat sentences.
- Do not use headings.
- Do not write an outline.
- Do not explain anything.
- Do not say "to be continued".
- Do not leave the story unfinished.
- The final paragraph must be the actual ending.

Output ONLY the story.
"""

    response = llm_model.invoke(prompt)

    content = response.content
    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):

                text_parts.append(item)

            elif isinstance(item, dict):

                if "text" in item:

                    text_parts.append(
                        item["text"]
                    )

        content = "\n".join(
            text_parts
        )

    content = str(content).strip()

    return content

def clean_story(story):

    story = story.strip()

    # Remove accidental markdown code fences
    story = re.sub(
        r"^```(?:text)?\s*",
        "",
        story,
        flags=re.IGNORECASE
    )

    story = re.sub(
        r"\s*```$",
        "",
        story
    )

    # Remove accidental "Story:" prefix
    prefixes = [
        "Story:",
        "STORY:",
        "Here is the story:",
        "Here is a story:"
    ]

    for prefix in prefixes:

        if story.lower().startswith(
            prefix.lower()
        ):

            story = story[len(prefix):].strip()

    return story


def word_count(text):

    return len(
        re.findall(
            r"\b[\w'-]+\b",
            text
        )
    )


def save_story(story):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    with open(
        STORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(story)

    print()
    print("Story saved to:")
    print(STORY_FILE)



def main():

    print()
    print("================ STORY GENERATOR ================")
    print()

    user_prompt = input(
        "What kind of story do you want?\n> "
    ).strip()

    if not user_prompt:

        print("No prompt provided.")
        return

    print()
    print("Generating story...")
    print()

    try:

        story = generate_story(
            user_prompt
        )

        story = clean_story(
            story
        )

        print(
            "================ GENERATED STORY ================"
        )

        print()
        print(story)

        print()
        print("==================================================")
        print()

        print(
            f"Word count: {word_count(story)}"
        )

        save_story(story)

    except Exception as error:

        print()
        print("================ ERROR ================")
        print()
        print(error)


if __name__ == "__main__":
    main()