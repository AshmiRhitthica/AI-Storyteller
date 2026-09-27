# 🎭 AI Storyteller

> An AI-powered storytelling and voice narration project built out of curiosity, experimentation, and a genuine interest in combining Generative AI with speech technology.

---

## 📖 About the Project

AI Tales is a personal GenAI project that I started because I wanted to explore something beyond a typical chatbot or text-generation application.

I wanted to build something where an AI-generated story could actually feel like a **story being told**, rather than just text appearing on a screen.

The idea was simple:

**Give the system a story idea → generate or analyze the story → identify the characters → assign voices → narrate the story using Text-to-Speech.**

What started as an interesting idea turned into a project where I spent a lot of time understanding how the different parts of an AI application can work together.

The project combines a web interface with an AI-powered backend that handles:

- AI story generation
- Story parsing
- Character identification
- Character profile inference
- Character-to-voice mapping
- Text-to-Speech generation
- Combining narration and dialogue into a complete audio story

---

## ✨ Why I Built This

I built this project mainly because I was **genuinely curious about how far I could take a simple storytelling idea**.

I didn't want to just call an LLM API and display its response.

I wanted to understand what happens **after the model generates the text**.

For example:

- How can a program identify who is speaking?
- How can narration be separated from dialogue?
- How can characters be represented as profiles?
- How can different characters be assigned different voices?
- How can the generated pieces of speech be combined into one continuous story?
- How can an AI-generated story become an actual audio experience?

These questions became the main motivation behind this project.

---

# 🧠 How It Works

The current pipeline looks like this:

```text
             User Story Prompt
                    │
                    ▼
             ┌──────────────┐
             │ Gemini / LLM │
             └──────┬───────┘
                    │
                    ▼
                Story Text
                    │
                    ▼
             ┌──────────────┐
             │ Story Parser │
             └──────┬───────┘
                    │
                    ▼
       Narration + Dialogue Segments
                    │
                    ▼
          Character Identification
                    │
                    ▼
          Character Profile Inference
                    │
                    ▼
             Voice Assignment
                    │
                    ▼
              Kokoro TTS
                    │
                    ▼
             Individual Audio
                Segments
                    │
                    ▼
            Final Story Audio
```
# 🎨 Frontend

The AI Tales frontend is a browser-based interface designed around a **dreamy fantasy storytelling experience**.

### Frontend Features

- Magical fantasy-themed landing page
- Generate a story from a prompt
- Paste and process an existing story
- Genre selection
- Story length selection
- Generated story display
- Character information display
- Final audio player
- Navigation between story creation and results

### Frontend Technologies

- HTML5
- CSS3
- JavaScript
- Local Storage
- Fetch API
- Responsive UI design

The frontend communicates with the FastAPI backend through HTTP API endpoints.

---

# 🖥️ Frontend Flow

```text
                    AI Tales Website
                           │
              ┌────────────┴────────────┐
              │                         │
        Generate a Story          Paste a Story
              │                         │
              ▼                         ▼
       /generate-story            /process-story
              │                         │
              └────────────┬────────────┘
                           ▼
                       FastAPI
                           │
                           ▼
                    AI Story Pipeline
                           │
                           ▼
                    Final Story Audio
                           │
                           ▼
                     Result Page
                           │
                           ▼
                       Audio Player
```
# 🔧 Technologies Used

### Generative AI

- **Google Gemini** — used for generating stories from user prompts.
- **Ollama** — used for experimenting with local LLMs during development and testing.

### Natural Language Processing

- **Python**
- **Regular Expressions**
- **Story and dialogue parsing**
- **Character identification**
- **Character profile inference**

### Text-to-Speech

- **Kokoro TTS**
- **Character-based voice assignment**
- **Separate narration and dialogue voices**

### Audio Processing

- **NumPy**
- **SoundFile**
- **Audio segment concatenation**
- **Pause insertion between story segments**

### Development

- **Python**
- **Git**
- **GitHub**
- **Virtual Environment**

---

# 🎙️ Example

A prompt such as:

> "A young girl discovers a magical room hidden inside her grandmother's house."

can be transformed into:

```text
Generated Story
       ↓
Characters Identified
       ↓
Narration Detected
       ↓
Dialogue Detected
       ↓
Voices Assigned
       ↓
Kokoro Generates Speech
       ↓
final_story.wav
```
# 🧩 Full Project Architecture
                    ┌─────────────────────┐
                    │      AI Tales       │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                         HTTP Requests
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
       Story Generation                   Story Processing
              │                                 │
           Gemini                        Story Parser
                                                │
                                                ▼
                                      Character Profiles
                                                │
                                                ▼
                                         Voice Mapping
                                                │
                                                ▼
                                          Kokoro TTS
                                                │
                                                ▼
                                        Final Audio File
                                                │
                                                ▼
                                         AI Tales UI
                                         
# 💡 What I Learned From Building This

This project taught me much more than just how to call an AI API.

1. GenAI Applications Are More Than the LLM
2. AI-Generated Text Needs Processing
3. Connecting Different AI Components
4. Debugging Is Part of Building
5. Building Incrementally

# ❤️ Personal Note

This is one of those projects that I built because I wanted to see if I could make the idea actually work.

It started with a simple thought:

What if an AI could not only write a story, but actually tell it?

While building it, I learned about LLM integration, text processing, character extraction, voice mapping, Text-to-Speech, audio processing, Python environments, debugging, and connecting multiple components into one working system.

I enjoyed experimenting with the project because I wasn't building it just to complete a checklist. I genuinely wanted to see what I could make it do.

For me, this project became a practical experiment in turning a GenAI idea into a working system.

# 👩‍💻 Author

Ashmi L. Rhitthica

B.E. Computer Science and Engineering
