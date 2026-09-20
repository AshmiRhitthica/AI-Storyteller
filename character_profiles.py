import re
import ollama

FEMALE_WORDS = {
    "woman",
    "girl",
    "lady",
    "mother",
    "daughter",
    "sister",
    "wife",
    "queen",
    "princess",
    "actress",
    "female",
}

MALE_WORDS = {
    "man",
    "boy",
    "gentleman",
    "father",
    "son",
    "brother",
    "husband",
    "king",
    "prince",
    "actor",
    "male",
}

COMMON_FEMALE_NAMES = {
    "lily",
    "mira",
    "sarah",
    "emma",
    "olivia",
    "ava",
    "mia",
    "sophia",
    "isabella",
    "ella",
    "grace",
    "anna",
    "alice",
    "bella",
    "diana",
}

COMMON_MALE_NAMES = {
    "jack",
    "john",
    "james",
    "michael",
    "william",
    "daniel",
    "david",
    "alex",
    "adam",
    "lewis",
    "thomas",
    "robert",
    "henry",
    "charles",
    "samuel",
    "george",
}


def gender_from_description(character):

    description = (
        character.get("description")
        or ""
    ).lower()

    if any(
        word in description
        for word in FEMALE_WORDS
    ):
        return "female"

    if any(
        word in description
        for word in MALE_WORDS
    ):
        return "male"

    return None


def gender_from_story_description(
    name,
    story
):

    if not name:
        return None

    sentences = re.split(
        r'(?<=[.!?])\s+',
        story
    )

    name_lower = name.lower()

    for sentence in sentences:

        lower = sentence.lower()

        if not re.search(
            rf'\b{re.escape(name_lower)}\b',
            lower
        ):
            continue


        if re.search(
            rf'\b{re.escape(name_lower)}\b'
            r'.{0,50}\b(woman|girl|lady|female)\b',
            lower
        ):
            return "female"


        if re.search(
            r'\b(woman|girl|lady|female)\b'
            rf'.{{0,50}}\b{re.escape(name_lower)}\b',
            lower
        ):
            return "female"


        if re.search(
            rf'\b{re.escape(name_lower)}\b'
            r'.{0,50}\b(man|boy|gentleman|male)\b',
            lower
        ):
            return "male"


        if re.search(
            r'\b(man|boy|gentleman|male)\b'
            rf'.{{0,50}}\b{re.escape(name_lower)}\b',
            lower
        ):
            return "male"

    return None



def gender_from_dialogue_attribution(
    name,
    story
):
    """
    Detect strong evidence such as:

        "My name is Mira," she said.
        "Come here," he shouted.
        Mira said, "Come here."
        he said, "Hello."

    This is stronger evidence than a name-based guess.
    """

    if not name:
        return None

    name_pattern = re.escape(
        name
    )


    pattern_after_quote = re.compile(
        rf'"[^"]*"'
        rf'\s*,?\s*'
        rf'(she|her|he|him)'
        rf'\s+(?:{"|".join([
            "asked",
            "said",
            "replied",
            "answered",
            "whispered",
            "shouted",
            "cried",
            "exclaimed",
        ])})\b',
        re.IGNORECASE
    )


    matches = re.finditer(
        r'"([^"]*)"\s*,?\s*'
        r'(she|her|he|him)\s+'
        r'(?:asked|said|replied|answered|whispered|'
        r'shouted|cried|exclaimed)\b',
        story,
        re.IGNORECASE
    )

    for match in matches:

        dialogue = match.group(1)
        pronoun = match.group(2).lower()

        if not re.search(
            rf'\b{re.escape(name)}\b',
            dialogue,
            re.IGNORECASE
        ):
            continue

        if pronoun in {
            "she",
            "her"
        }:
            return "female"

        if pronoun in {
            "he",
            "him"
        }:
            return "male"


    name_said = re.search(
        rf'\b{re.escape(name_pattern)}\b'
        r'\s+(?:asked|said|replied|answered|'
        r'whispered|shouted|cried|exclaimed)\b',
        story,
        re.IGNORECASE
    )

    if name_said:

        pass


    sentences = re.split(
        r'(?<=[.!?])\s+',
        story
    )

    for index, sentence in enumerate(
        sentences
    ):

        if not re.search(
            rf'\b{re.escape(name)}\b',
            sentence,
            re.IGNORECASE
        ):
            continue

        lower = sentence.lower()

        if (
            "she said" in lower
            or "she asked" in lower
            or "she replied" in lower
            or "she whispered" in lower
        ):
            return "female"

        if (
            "he said" in lower
            or "he asked" in lower
            or "he replied" in lower
            or "he whispered" in lower
        ):
            return "male"

    return None



def gender_from_name(name):

    if not name:
        return None

    name_lower = name.lower()

    if name_lower in COMMON_FEMALE_NAMES:
        return "female"

    if name_lower in COMMON_MALE_NAMES:
        return "male"

    return None



def gender_from_pronoun(
    name,
    story
):

    if not name:
        return None

    sentences = re.split(
        r'(?<=[.!?])\s+',
        story
    )

    for index, sentence in enumerate(
        sentences
    ):

        if not re.search(
            rf'\b{re.escape(name)}\b',
            sentence,
            re.IGNORECASE
        ):
            continue


        if index + 1 >= len(
            sentences
        ):
            continue

        next_sentence = (
            sentences[index + 1]
            .strip()
            .lower()
        )

        # Only accept pronoun at the beginning.
        if re.match(
            r'^(she|her|hers)\b',
            next_sentence
        ):
            return "female"

        if re.match(
            r'^(he|him|his)\b',
            next_sentence
        ):
            return "male"

    return None


def infer_gender_with_qwen(
    name,
    story
):

    prompt = f"""
You are a fictional character profile classifier.

Determine the gender category associated with this
character using ONLY evidence in the story.

Character:
{name}

Story:
{story}

Allowed answers:
female
male
unknown

Rules:
- Return exactly one word.
- Do not explain.
- Do not infer from unrelated characters.
- If the story does not provide evidence,
  return unknown.

Answer:
"""

    try:

        response = ollama.chat(
            model="qwen2.5:1.5b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

    except Exception as error:

        print(
            f"Qwen gender inference failed "
            f"for {name}: {error}"
        )

        return None

    result = (
        response[
            "message"
        ][
            "content"
        ]
        .strip()
        .lower()
    )

    if re.search(
        r'\bfemale\b',
        result
    ):
        return "female"

    if re.search(
        r'\bmale\b',
        result
    ):
        return "male"

    return None


def infer_character_profiles(
    story,
    registry
):

    for character in registry.characters:

        if character.get(
            "gender"
        ):
            continue

        name = character.get(
            "name"
        )

        if not name:

            gender = (
                gender_from_description(
                    character
                )
            )

            if gender:

                character["gender"] = (
                    gender
                )

            continue


        gender = (
            gender_from_description(
                character
            )
        )

        if gender:

            character["gender"] = gender
            continue


        gender = (
            gender_from_dialogue_attribution(
                name,
                story
            )
        )

        if gender:

            character["gender"] = gender
            continue


        gender = (
            gender_from_story_description(
                name,
                story
            )
        )

        if gender:

            character["gender"] = gender
            continue

        
        gender = gender_from_name(
            name
        )

        if gender:

            character["gender"] = gender
            continue

        
        gender = gender_from_pronoun(
            name,
            story
        )

        if gender:

            character["gender"] = gender
            continue

       
        gender = (
            infer_gender_with_qwen(
                name,
                story
            )
        )

        if gender:

            character["gender"] = gender


    return registry


def print_character_profiles(
    registry
):

    print(
        "\n================ CHARACTER PROFILES ================\n"
    )

    for character in registry.characters:

        display_name = (
            character.get("name")
            or character.get("description")
            or "Unknown"
        )

        print(
            "Character :",
            display_name
        )

        print(
            "Gender    :",
            character.get(
                "gender",
                "unknown"
            )
        )

        print(
            "ID        :",
            character["id"]
        )

        print(
            "-" * 50
        )


if __name__ == "__main__":

    from story_parser import analyze_story

    TEST_STORY = """
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

    print(
        "\nAnalyzing story...\n"
    )

    segments, registry = analyze_story(
        TEST_STORY
    )

    registry = infer_character_profiles(
        TEST_STORY,
        registry
    )

    print_character_profiles(
        registry
    )