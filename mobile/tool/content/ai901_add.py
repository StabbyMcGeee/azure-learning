"""AI-901 Foundry-domain additions to align weighting to the study guide.

The AI-901 outline weights "Implement AI solutions by using Microsoft Foundry"
at 55-60%. These items deepen Foundry coverage to match that band.
"""

SRC = (
    "Original AI-fleet-authored content with publisher review (Dimitri Meier); "
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
       "A developer must choose how to serve a model: a real-time endpoint "
       "for interactive requests or a batch job for large scoring runs. What "
       "is this choice an example of?",
       ["A model deployment option",
        "A responsible AI principle",
        "A text analysis technique",
        "A data visualization"],
       0,
       "Choosing how to serve a model, such as a real-time endpoint versus "
       "batch scoring, is a model deployment option.",
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
    qf("ai-901-043",
       "A developer builds a lightweight application that extracts the main "
       "terms from customer feedback. Which Foundry capability does this?",
       ["Text analysis in Foundry",
        "Speech synthesis",
        "Image generation",
        "Data warehousing"],
       0,
       "Text analysis in Foundry includes keyword extraction for finding the "
       "main terms in text such as customer feedback.",
       "medium"),
    qf("ai-901-044",
       "A developer builds an app that answers spoken questions by using a "
       "model that processes both audio and text. Which model type is "
       "required?",
       ["A multimodal model",
        "A keyword extraction model",
        "A sentiment analysis model",
        "A table model"],
       0,
       "Responding to spoken prompts uses a deployed multimodal model that "
       "processes both audio and text.",
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
    qf("ai-901-046",
       "Which tool extracts fields from documents and forms in Microsoft "
       "Foundry?",
       ["Azure Content Understanding in Foundry Tools",
        "Azure Speech in Foundry Tools",
        "Azure Blob Storage",
        "Azure Cosmos DB"],
       0,
       "Azure Content Understanding in Foundry Tools extracts structured "
       "information from documents and forms.",
       "medium"),
    qf("ai-901-047",
       "A developer needs to extract spoken words and visual text from a "
       "video recording. Which Foundry capability handles audio and video "
       "content?",
       ["Content Understanding",
        "Speech synthesis",
        "Sentiment analysis",
        "Keyword extraction"],
       0,
       "Content Understanding extracts information from audio and video, "
       "including spoken words and visual text.",
       "medium"),
    qf("ai-901-048",
       "A developer wants to interact with a deployed model through a web "
       "interface without writing code. Which surface should they use?",
       ["The Foundry portal",
        "The Foundry SDK",
        "A command-line shell",
        "A database client"],
       0,
       "The Foundry portal is the web interface for deploying and interacting "
       "with models without writing code.",
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
