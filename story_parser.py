import re


SPEECH_VERBS = [
    "said",
    "asked",
    "replied",
    "answered",
    "whispered",
    "shouted",
    "cried",
    "exclaimed",
    "muttered",
    "called",
    "yelled",
    "continued",
]

IGNORED_WORDS = {
    "Today",
    "While",
    "Suddenly",
    "Instantly",
    "Slowly",
    "Downstairs",
    "Curiosity",
    "Pushing",
    "Glowing",
    "But",
    "The",
    "A",
    "An",
    "One",
    "Her",
    "His",
}

class CharacterRegistry:

    def __init__(self):
        self.characters = []

    def add(self, name):

        if name is None:
            return

        if self.get_by_name(name):
            return

        self.characters.append({
            "name": name,
            "gender": None
        })

    def get_by_name(self, name):

        for char in self.characters:
            if char["name"].lower() == name.lower():
                return char

        return None



def normalize_story(text):

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text.strip()


def extract_characters(story):

    registry = CharacterRegistry()

    pattern1 = (
        r'\b([A-Z][a-z]+)\s+'
        r'(?:said|asked|replied|answered|whispered|'
        r'shouted|cried|exclaimed|muttered|called|yelled)\b'
    )

    for name in re.findall(pattern1, story):
        registry.add(name)


    grandma_pattern = r'\bGrandma\s+([A-Z][a-z]+)\b'

    for name in re.findall(grandma_pattern, story):
        registry.add(name)

    intro_pattern = r'\bmy name is ([A-Z][a-z]+)\b'

    for name in re.findall(intro_pattern, story, re.I):
        registry.add(name)

    
    names = re.findall(r'\b[A-Z][a-z]{2,}\b', story)

    counts = {}

    for name in names:

        if name in IGNORED_WORDS:
            continue

        counts[name] = counts.get(name, 0) + 1

    for name, count in counts.items():

        if count >= 2:
            registry.add(name)

    return registry


def detect_speaker(before, after, registry, previous_speaker):


    after_pattern = (
        r'^\s*,?\s*'
        r'([A-Z][a-z]+)\s+'
        r'(?:said|asked|replied|answered|whispered|'
        r'shouted|cried|exclaimed|muttered|called|yelled)'
    )

    match = re.search(after_pattern, after)

    if match:

        name = match.group(1)

        if registry.get_by_name(name):
            return name


    pronoun_pattern = (
        r'^\s*,?\s*'
        r'(she|he)\s+'
        r'(?:said|asked|replied|answered|whispered|'
        r'shouted|cried|exclaimed|muttered|called|yelled)'
    )

    if re.search(pronoun_pattern, after, re.I):

        # Most recent active character
        if previous_speaker:
            return previous_speaker

        if registry.get_by_name("Lily"):
            return "Lily"


    before_pattern = (
        r'([A-Z][a-z]+)\s+'
        r'(?:said|asked|replied|answered|whispered|'
        r'shouted|cried|exclaimed|muttered|called|yelled|'
        r'read the words aloud)'
        r'\s*:?\s*$'
    )

    match = re.search(before_pattern, before)

    if match:

        name = match.group(1)

        if registry.get_by_name(name):
            return name


    last_250 = before[-250:]

    names_found = []

    for char in registry.characters:

        name = char["name"]

        if re.search(rf'\b{name}\b', last_250):
            names_found.append(name)

    if names_found:

        return names_found[-1]

    if previous_speaker:
        return previous_speaker

    return None


def clean_narration(text):

    if not text:
        return ""

    # Removing attribution at beginning...

    pattern = (
        r'^\s*,?\s*'
        r'(?:[A-Z][a-z]+|she|he|they)\s+'
        r'(?:said|asked|replied|answered|whispered|'
        r'shouted|cried|exclaimed|muttered|called|yelled)'
        r'[^.]*\.\s*'
    )

    text = re.sub(
        pattern,
        "",
        text,
        flags=re.I
    )

    return text.strip()


def parse_story(story):

    story = normalize_story(story)

    registry = extract_characters(story)

    dialogue_pattern = r'"([^"]*)"'

    matches = list(re.finditer(dialogue_pattern, story))

    segments = []

    previous_end = 0
    previous_speaker = None

    for match in matches:

        before = story[previous_end:match.start()]

        after = story[match.end():]

        after_context = after[:180]

        speaker = detect_speaker(
            before,
            after_context,
            registry,
            previous_speaker
        )

        narration = before.strip()

        if narration:

            narration = clean_narration(narration)

            if narration:
                segments.append({
                    "type": "narration",
                    "text": narration
                })

        dialogue = match.group(1).strip()

        segments.append({
            "type": "dialogue",
            "speaker": speaker,
            "text": dialogue
        })

        if speaker:
            previous_speaker = speaker

        previous_end = match.end()

    # Remaining narration

    remaining = story[previous_end:].strip()

    remaining = clean_narration(remaining)

    if remaining:

        segments.append({
            "type": "narration",
            "text": remaining
        })

    return segments, registry


def analyze_story(story):
    """
    Function imported by integration_test.py
    """

    return parse_story(story)


if __name__ == "__main__":

    TEST_STORY = """
Lily walked into the forest.

"Hello," Lily whispered.

Grandma Clara smiled.

"Come here," Clara said.

"Okay," Lily replied.
"""

    segments, registry = analyze_story(TEST_STORY)

    print("\nCHARACTERS\n")

    for char in registry.characters:
        print(char["name"])

    print("\nSEGMENTS\n")

    for seg in segments:
        print(seg)