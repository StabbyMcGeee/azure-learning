"""AI-901 Foundry-domain additions to align weighting to the study guide.

The AI-901 outline weights "Implement AI solutions by using Microsoft Foundry"
at 55-60%. These items deepen Foundry coverage to match that band.
"""

SRC = (
    "Original AI-fleet-authored content; publisher substantive review PENDING (Dimitri Meier); "
    "facts from Microsoft Learn AI-901 study guide (2026-04-15) and docs, "
    "retrieved 2026-10-02"
)
BASIS = "original-human-ai-assisted"
COURSE = "ai-901"


def qf(id_, text, options, ci, expl, diff="medium"):
    return {
        "id": id_,
        "text": text,
        "options": options,
        "correctOptionIndex": ci,
        "explanation": expl,
        "domain": "Microsoft Foundry",
        "difficulty": diff,
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    }


QUESTIONS = [
    qf("ai-901-039",
       "In a Foundry chat application, which prompt is the user's own request "
       "typed at runtime?",
       ["The user prompt", "The system prompt", "The temperature setting",
        "The endpoint URL"],
       0,
       "The user prompt is the user's request typed at runtime; the system "
       "prompt sets the model's role and rules.",
       "medium"),
    qf("ai-901-040",
       "Which configuration parameter controls how many of the most likely "
       "next tokens the model samples from?",
       ["top_p", "temperature", "max tokens", "the system prompt"],
       0,
       "top_p (nucleus sampling) limits sampling to the smallest set of most "
       "likely tokens whose combined probability reaches the threshold.",
       "medium"),
    qf("ai-901-041",
       "A developer deploys a model and wants a client application to send "
       "interactive requests to it over HTTP. What does the application "
       "call?",
       ["A real-time endpoint",
        "A storage account",
        "A virtual network",
        "A SQL database"],
       0,
       "A deployed model is served through a real-time endpoint that client "
       "applications call over HTTP for interactive requests.",
       "medium"),
    qf("ai-901-042",
       "Where can a developer create and test a single-agent solution before "
       "connecting a client application to it?",
       ["In the Foundry portal",
        "In a storage account",
        "In a virtual network",
        "In a SQL database"],
       0,
       "A single-agent solution is created and tested in the Foundry portal "
       "before a client application connects to it.",
       "medium"),
    qf("ai-901-045",
       "A developer builds an app that detects objects in photos. Which "
       "Foundry capability supports this?",
       ["Vision capabilities in Foundry",
        "Speech recognition",
        "Entity detection",
        "Data warehousing"],
       0,
       "Vision capabilities in Foundry include object detection for locating "
       "objects within images.",
       "medium"),
    qf("ai-901-049",
       "Which practice improves a generative model's output by writing clear, "
       "specific instructions and context in the prompt?",
       ["Creating effective prompts",
        "Lowering the endpoint URL",
        "Increasing the database size",
        "Disabling the model"],
       0,
       "Creating effective prompts (clear, specific instructions and context) "
       "improves a generative model's output.",
       "medium"),
]
