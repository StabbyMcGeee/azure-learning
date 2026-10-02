"""AI-901 launch-course items (fresh originals).

Authored from the public AI-901 skills outline ("Skills measured as of
April 15, 2026", retrieved 2026-10-02) and standard Microsoft Learn facts.
AI-900 is retired; the current exam code is AI-901. No legacy wording or
recalled exam item was used.
"""

SRC = (
    "Original AI-fleet-authored content with publisher review (Dimitri Meier); "
    "facts from Microsoft Learn AI-901 study guide (2026-04-15) and docs, "
    "retrieved 2026-10-02"
)
BASIS = "original-human-ai-assisted"
COURSE = "ai-901"


def q(id_, text, options, ci, expl, diff):
    return {
        "id": id_,
        "text": text,
        "options": options,
        "correctOptionIndex": ci,
        "explanation": expl,
        "domain": "AI Concepts and Capabilities",
        "difficulty": diff,
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    }


def qf(id_, text, options, ci, expl, diff):
    """Microsoft Foundry domain item."""
    d = q(id_, text, options, ci, expl, diff)
    d["domain"] = "Microsoft Foundry"
    return d


QUESTIONS = [
    # ---- Responsible AI principles ----
    q("ai-901-001",
      "Which responsible AI principle requires an AI solution to avoid bias "
      "and treat all groups equitably?",
      ["fairness", "transparency", "accountability", "inclusiveness"],
      0,
      "Fairness requires AI solutions to avoid bias and treat all groups "
      "equitably.",
      "easy"),
    q("ai-901-002",
      "Which responsible AI principle requires an AI solution to behave "
      "safely and continue operating correctly under unexpected conditions?",
      ["reliability and safety", "fairness", "privacy and security",
       "transparency"],
      0,
      "Reliability and safety require an AI solution to behave safely and "
      "operate correctly, including under unexpected conditions.",
      "easy"),
    q("ai-901-003",
      "Which responsible AI principle focuses on protecting user data and "
      "securing the system against attack?",
      ["privacy and security", "fairness", "inclusiveness", "accountability"],
      0,
      "Privacy and security focus on protecting user data and securing the "
      "AI system.",
      "easy"),
    q("ai-901-004",
      "Which responsible AI principle requires solutions to be designed for "
      "and accessible to people of all abilities?",
      ["inclusiveness", "fairness", "transparency", "reliability and safety"],
      0,
      "Inclusiveness requires AI solutions to empower and be accessible to "
      "people of all abilities.",
      "easy"),
    q("ai-901-005",
      "Which responsible AI principle means users should understand how a "
      "system makes decisions?",
      ["transparency", "fairness", "privacy and security", "accountability"],
      0,
      "Transparency means users can understand how the AI system makes "
      "decisions and what data it uses.",
      "easy"),
    q("ai-901-006",
      "Which responsible AI principle holds people responsible for how an AI "
      "system behaves and its outcomes?",
      ["accountability", "inclusiveness", "fairness", "transparency"],
      0,
      "Accountability holds people responsible for the behavior and outcomes "
      "of an AI system.",
      "easy"),
    # ---- AI model components and configurations ----
    q("ai-901-007",
      "Which statement best describes how generative AI models work?",
      ["They generate new content by predicting the next token based on training data",
       "They only look up answers in a fixed database",
       "They copy training documents verbatim",
       "They require a human to write every response"],
      0,
      "Generative AI models produce new content by predicting the most "
      "likely next token based on patterns learned from training data.",
      "medium"),
    q("ai-901-008",
      "In a chat application, what is the role of the system prompt?",
      ["It provides instructions and context that guide the model's behavior",
       "It is the user's question typed at runtime",
       "It is the model's final answer",
       "It is an encryption key"],
      0,
      "The system prompt provides instructions and context that guide how "
      "the model behaves, while the user prompt is the user's request.",
      "medium"),
    q("ai-901-009",
      "Which configuration parameter controls the randomness of a generative "
      "model's output?",
      ["temperature", "max tokens", "system prompt", "endpoint URL"],
      0,
      "Temperature controls randomness: lower values produce more "
      "deterministic output, higher values produce more varied output.",
      "medium"),
    q("ai-901-010",
      "Which configuration parameter limits the length of a model's "
      "response?",
      ["max tokens", "temperature", "top_p", "the system prompt"],
      0,
      "The max tokens parameter limits the number of tokens the model can "
      "generate in its response.",
      "medium"),
    q("ai-901-011",
      "A developer needs to choose between deploying a model for real-time "
      "interactive use and batch scoring. What is this decision an example "
      "of?",
      ["A model deployment option",
       "A responsible AI principle",
       "A data visualization",
       "A speech synthesis technique"],
      0,
      "Choosing how and where to serve a model (real-time endpoint versus "
      "batch) is a model deployment option.",
      "medium"),
    # ---- AI workloads and techniques ----
    q("ai-901-012",
      "Which AI workload creates new content such as text, images, or code "
      "from a prompt?",
      ["generative AI", "text analysis", "computer vision",
       "information extraction"],
      0,
      "Generative AI creates new content such as text, images, or code from "
      "a prompt.",
      "easy"),
    q("ai-901-013",
      "Which AI workload describes systems that act autonomously to achieve "
      "goals, often using tools?",
      ["agentic AI", "sentiment analysis", "speech synthesis",
       "keyword extraction"],
      0,
      "Agentic AI describes systems (agents) that act autonomously to "
      "achieve goals, often by calling tools.",
      "medium"),
    q("ai-901-014",
      "Which text analysis technique identifies and categorizes named items "
      "such as people, places, and dates?",
      ["entity detection", "sentiment analysis", "summarization",
       "keyword extraction"],
      0,
      "Entity detection (named entity recognition) identifies and "
      "categorizes named items such as people, places, organizations, and "
      "dates.",
      "medium"),
    q("ai-901-015",
      "Which text analysis technique determines whether a review is "
      "positive, negative, or neutral?",
      ["sentiment analysis", "entity detection", "keyword extraction",
       "summarization"],
      0,
      "Sentiment analysis determines the tone of text as positive, negative, "
      "or neutral.",
      "easy"),
    q("ai-901-016",
      "Which text analysis technique extracts the most important terms and "
      "phrases from a document?",
      ["keyword extraction", "entity detection", "sentiment analysis",
       "speech synthesis"],
      0,
      "Keyword extraction identifies the most important terms and phrases in "
      "a document.",
      "medium"),
    q("ai-901-017",
      "Which text analysis technique produces a shorter version of a long "
      "document while keeping the main points?",
      ["summarization", "keyword extraction", "entity detection",
       "speech recognition"],
      0,
      "Summarization condenses a long document into a shorter version while "
      "keeping the main points.",
      "easy"),
    q("ai-901-018",
      "Which speech capability converts spoken audio into text?",
      ["speech recognition", "speech synthesis", "sentiment analysis",
       "image generation"],
      0,
      "Speech recognition (speech-to-text) converts spoken audio into text.",
      "easy"),
    q("ai-901-019",
      "Which speech capability converts text into spoken audio?",
      ["speech synthesis", "speech recognition", "entity detection",
       "keyword extraction"],
      0,
      "Speech synthesis (text-to-speech) converts text into spoken audio.",
      "easy"),
    q("ai-901-020",
      "Which computer vision capability identifies and locates objects "
      "within an image?",
      ["object detection", "speech synthesis", "summarization",
       "sentiment analysis"],
      0,
      "Object detection identifies and locates objects within an image, "
      "usually with bounding boxes.",
      "medium"),
    q("ai-901-021",
      "Which capability generates new images from a text description?",
      ["image-generation models", "speech recognition", "keyword extraction",
       "entity detection"],
      0,
      "Image-generation models create new images from a text description.",
      "medium"),
    q("ai-901-022",
      "Which information extraction task reads text from a scanned document "
      "image?",
      ["Extracting information from images using optical character recognition",
       "Speech recognition",
       "Sentiment analysis",
       "Image generation"],
      0,
      "Optical character recognition extracts text information from images "
      "such as scanned documents.",
      "medium"),
    # ---- Microsoft Foundry ----
    qf("ai-901-023",
       "What is Microsoft Foundry?",
       ["A platform for building, testing, and deploying AI solutions",
        "A relational database service",
        "A business intelligence tool",
        "A virtual machine service"],
       0,
       "Microsoft Foundry is a platform for building, testing, and deploying "
       "AI solutions, including generative AI apps and agents.",
       "easy"),
    qf("ai-901-024",
       "Which part of Microsoft Foundry provides a web interface for "
       "deploying and interacting with models?",
       ["The Foundry portal", "The Foundry SDK", "Azure Blob Storage",
        "Azure Cosmos DB"],
       0,
       "The Foundry portal is the web interface for deploying models and "
       "interacting with them.",
       "medium"),
    qf("ai-901-025",
       "Which tool do developers use to build lightweight client "
       "applications that call Microsoft Foundry models?",
       ["The Foundry SDK", "The Foundry portal", "A spreadsheet",
        "A virtual machine image"],
       0,
       "The Foundry SDK lets developers build lightweight client "
       "applications that call models deployed in Microsoft Foundry.",
       "medium"),
    qf("ai-901-026",
       "In Microsoft Foundry, what is a single-agent solution?",
       ["An AI agent that performs tasks, often by calling tools, within a solution",
        "A single virtual machine",
        "A database with one table",
        "A text analysis pipeline"],
       0,
       "A single-agent solution is an AI agent that acts to accomplish tasks, "
       "often by calling tools, built and tested in Microsoft Foundry.",
       "medium"),
    qf("ai-901-027",
       "Which type of model can process multiple input types such as text, "
       "images, and audio?",
       ["A multimodal model", "A speech synthesis model",
        "A sentiment analysis model", "A keyword extraction model"],
       0,
       "A multimodal model processes multiple input types, such as text, "
       "images, and audio, in a single model.",
       "medium"),
    qf("ai-901-028",
       "What is the purpose of the system prompt in a Foundry chat "
       "application?",
       ["To set the model's role, tone, and rules for the conversation",
        "To store the chat history in a database",
        "To encrypt the user's input",
        "To limit the number of users"],
       0,
       "The system prompt sets the model's role, tone, and rules, guiding how "
       "it responds to the user prompt.",
       "medium"),
    qf("ai-901-029",
       "A developer wants a model's responses to be highly consistent and "
       "predictable. Which configuration parameter should be lowered?",
       ["temperature", "max tokens", "the system prompt", "the endpoint URL"],
       0,
       "Lowering the temperature reduces randomness, making responses more "
       "consistent and predictable.",
       "medium"),
    qf("ai-901-030",
       "Which Foundry workflow step lets you test a model's responses "
       "directly through a chat interface in the portal?",
       ["Deploying the model and interacting with it in the Foundry portal",
        "Creating a storage account",
        "Writing a SQL query",
        "Configuring a virtual network"],
       0,
       "After deploying a model, you can interact with it through the chat "
       "interface in the Foundry portal to test its responses.",
       "medium"),
    qf("ai-901-031",
       "Which tool in Microsoft Foundry provides capabilities for speech "
       "recognition and speech synthesis?",
       ["Azure Speech in Foundry Tools", "Azure Content Understanding in Foundry Tools",
        "Azure Blob Storage", "Azure Files"],
       0,
       "Azure Speech in Foundry Tools provides speech recognition and speech "
       "synthesis capabilities.",
       "medium"),
    qf("ai-901-032",
       "Which tool in Microsoft Foundry extracts information from documents, "
       "forms, images, audio, and video?",
       ["Azure Content Understanding in Foundry Tools",
        "Azure Speech in Foundry Tools", "Azure Cosmos DB", "Azure Databricks"],
       0,
       "Azure Content Understanding in Foundry Tools extracts information "
       "from documents, forms, images, audio, and video.",
       "medium"),
    qf("ai-901-033",
       "What is Content Understanding?",
       ["A capability for extracting structured information from unstructured content",
        "A speech synthesis engine",
        "A relational database",
        "A data visualization tool"],
       0,
       "Content Understanding extracts structured information from "
       "unstructured content such as documents, images, audio, and video.",
       "medium"),
    qf("ai-901-034",
       "A developer builds an app that converts spoken audio to text and "
       "then reads the answer back aloud. Which Foundry tool provides these "
       "speech capabilities?",
       ["Azure Speech in Foundry Tools",
        "Azure Content Understanding in Foundry Tools",
        "A sentiment analysis model",
        "A keyword extraction model"],
       0,
       "Azure Speech in Foundry Tools provides speech recognition and speech "
       "synthesis for converting audio to text and text to speech.",
       "medium"),
    qf("ai-901-035",
       "Which Foundry capability lets a developer create new images from text "
       "descriptions?",
       ["Generative image models in Foundry",
        "Speech recognition",
        "Entity detection",
        "Data warehousing"],
       0,
       "Generative image models in Microsoft Foundry create new visual "
       "outputs from text descriptions.",
       "medium"),
    qf("ai-901-036",
       "A developer builds a lightweight application that extracts entities "
       "and sentiment from text. Which Microsoft Foundry capability supports "
       "this?",
       ["Text analysis in Foundry",
        "Speech synthesis",
        "Image generation",
        "Data warehousing"],
       0,
       "Microsoft Foundry supports building lightweight applications that "
       "perform text analysis such as entity detection and sentiment "
       "analysis.",
       "medium"),
    qf("ai-901-037",
       "Which model type interprets visual input supplied in a prompt, such "
       "as asking about an uploaded image?",
       ["A multimodal model",
        "A speech synthesis model",
        "A keyword extraction model",
        "A data model"],
       0,
       "A multimodal model can interpret visual input in prompts, such as "
       "reasoning about an uploaded image alongside text.",
       "medium"),
    qf("ai-901-038",
       "A developer must connect a client application to an agent deployed "
       "in Microsoft Foundry so the application can invoke the agent. Which "
       "component does the developer use?",
       ["The Foundry SDK",
        "A virtual machine image",
        "A storage account",
        "A SQL query"],
       0,
       "The Foundry SDK connects a lightweight client application to an agent "
       "or model deployed in Microsoft Foundry.",
       "medium"),
]
