# LinkedIn AI Agent
🤖 Autonomous LinkedIn AI Content Agent

An autonomous AI-powered LinkedIn content agent built with LangChain, LangGraph, LLMs, Tavily, LinkedIn REST API, and GitHub Actions.

The system automatically discovers AI/ML topics, researches the subject, generates professional LinkedIn content, validates the generated post using AI guardrails, detects duplicate content, and can publish the final post to LinkedIn on a scheduled basis.

The goal of this project is to demonstrate how agentic AI, workflow orchestration, automated validation, API integration, persistent state, and scheduled cloud automation can be combined into a practical AI engineering system.

⸻

🚀 Project Overview

The agent is designed to automatically create and publish two AI/ML-focused LinkedIn posts per day.

Scheduled execution

* 🕘 09:00 AM IST
* 🌙 07:00 PM IST

The complete workflow runs automatically through GitHub Actions.

                         ┌──────────────────────┐
                         │   GitHub Actions     │
                         │  Scheduled Trigger   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ LangGraph Workflow   │
                         │    Orchestrator      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Topic Agent       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Research Agent     │
                         │       Tavily         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Writer Agent      │
                         │        LLM           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Validator /          │
                         │ AI Guardrails        │
                         └──────────┬───────────┘
                                    │
                              Validation
                              Passed?
                              /      \
                            No        Yes
                            │          │
                            ▼          ▼
                       Regenerate   Duplicate
                                    Detection
                                      │
                                Duplicate?
                                /       \
                              Yes        No
                              │           │
                              ▼           ▼
                         Regenerate    LinkedIn
                                      Publisher
                                          │
                                          ▼
                                   Persistent
                                     History

⸻

✨ Key Features

🧠 1. Autonomous Topic Generation

The Topic Agent selects relevant topics within the AI/ML ecosystem.

Supported areas include:

* Artificial Intelligence
* Machine Learning
* Generative AI
* Large Language Models
* RAG
* Agentic AI
* AI Agents
* LangChain
* LangGraph
* MCP
* MLOps
* AI Engineering
* Automation
* Data Engineering
* ML Engineering
* AI Architecture
* LLM Applications

The agent generates a topic, subtopic, and content angle before writing the post.

⸻

🔎 2. AI-Powered Research

The Research Agent gathers supporting information before content generation.

The research stage helps reduce generic content and gives the Writer Agent technical context.

Topic
  ↓
Research
  ↓
Research Synthesis
  ↓
Content Generation

The project uses Tavily for web research.

⸻

✍️ 3. AI LinkedIn Content Writer

The Writer Agent generates professional LinkedIn posts using an LLM.

The target audience includes:

* AI/ML Engineers
* Software Engineers
* Recruiters
* Technology Professionals
* Engineering Managers
* AI Engineering enthusiasts

The generated content is designed to be:

* Professional
* Technical
* Practical
* Easy to understand
* Useful
* LinkedIn-friendly
* Non-spammy
* Non-repetitive

⸻

🛡️ 4. AI Guardrails & Validation

Every generated post passes through an independent validation stage before publishing.

The Validator Agent evaluates:

✓ AI/ML relevance
✓ Technical soundness
✓ Professional quality
✓ Recruiter relevance
✓ Engineer relevance
✓ Grammar
✓ Overall quality

The validator returns a quality score.

Minimum quality threshold

0.85

A post is allowed to continue only when the required validation criteria are satisfied.

Example:

Quality Score: 0.92
AI/ML Relevant:       ✓
Technically Sound:    ✓
Professional:         ✓
Recruiter Relevant:   ✓
Engineer Relevant:    ✓
Grammar:              ✓
Result: PASSED

⸻

🔄 5. Automatic Regeneration

If a generated post fails validation, the LangGraph workflow automatically routes the state back to the Writer Agent.

Writer
  ↓
Validator
  ↓
Failed
  ↓
Regenerate
  ↓
Writer

The workflow supports a maximum of:

3 retries

If the post continues to fail validation, the workflow stops instead of publishing the content.

⸻

🔍 6. Duplicate Content Detection

The system checks the generated post against previously generated/published posts.

The current implementation uses:

* TF-IDF
* N-grams
* Cosine Similarity

New Post
   ↓
Normalize Text
   ↓
TF-IDF Vectorization
   ↓
Cosine Similarity
   ↓
Compare with History

The current duplicate threshold is:

0.85

If the similarity exceeds the threshold, the post is considered a duplicate and the workflow regenerates the content.

The current implementation is primarily a lexical similarity detector. It helps catch strongly similar wording but is not a complete semantic-duplicate detector.

⸻

🔐 7. Execution Idempotency

The system prevents the same scheduled execution from being processed multiple times.

Each execution receives a unique key.

Example:

2026-09-10-morning
2026-09-10-evening

Execution states include:

started
completed
failed

If an execution has already been completed, the workflow safely stops instead of generating and publishing another post for the same slot.

⸻

💾 8. Persistent History

The project stores generated/published post information in:

data/posts.json

The history can contain:

* Post content
* Topic
* Subtopic
* Content angle
* Quality score
* Duplicate score
* LinkedIn post ID
* Publishing status
* Execution information

This history is also used by the duplicate detector.

⸻

⏰ 9. Automated GitHub Actions Scheduling

GitHub Actions is used to run the agent automatically.

The workflow is located at:

.github/workflows/linkedin-agent.yml

The schedule is:

schedule:
  - cron: "30 3 * * *"
  - cron: "30 13 * * *"

Because GitHub Actions cron uses UTC:

03:30 UTC → 09:00 IST
13:30 UTC → 19:00 IST

The workflow also supports manual execution using:

workflow_dispatch

⸻

🔗 10. LinkedIn API Integration

The project integrates with the LinkedIn REST API for publishing posts.

The publishing flow is:

Validated Post
      ↓
Duplicate Check
      ↓
LinkedIn Publisher
      ↓
LinkedIn REST API
      ↓
Post ID
      ↓
History

The LinkedIn publishing functionality is isolated inside:

src/tools/linkedin.py

⸻

🧪 11. Dry-Run Mode

The project includes a safe dry-run mode.

Set:

DRY_RUN=true

When enabled, the agent executes the complete AI workflow but does not publish to LinkedIn.

Topic
  ↓
Research
  ↓
Writing
  ↓
Validation
  ↓
Duplicate Detection
  ↓
Save to History
  ↓
STOP

This is useful for testing the complete workflow before enabling real publishing.

⸻

🚀 Production Publishing

After validating the complete workflow, production publishing can be enabled using:

DRY_RUN=false

For GitHub Actions, DRY_RUN should be stored as a GitHub Actions secret.

Recommended approach

Development
     ↓
DRY_RUN=true
     ↓
Run Tests
     ↓
Test GitHub Actions
     ↓
Verify Generated Content
     ↓
Verify Guardrails
     ↓
Verify Duplicate Detection
     ↓
Enable DRY_RUN=false
     ↓
Real LinkedIn Publishing

⸻

🏗️ Project Architecture

linkedin-ai-agent/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── llm.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── workflow.py
│   │   └── router.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── topic_agent.py
│   │   ├── research_agent.py
│   │   ├── writer_agent.py
│   │   └── validator_agent.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── history.py
│   │   └── duplicate_detector.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   └── linkedin.py
│   │
│   └── models/
│       ├── __init__.py
│       └── schemas.py
│
├── data/
│   └── posts.json
│
├── tests/
│   ├── test_guardrails.py
│   ├── test_workflow_structure.py
│   ├── test_execution_lifecycle.py
│   ├── test_history.py
│   └── test_duplicate_detector.py
│
├── .github/
│   └── workflows/
│       └── linkedin-agent.yml
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md

⸻

🧩 Technology Stack

Technology	Purpose
Python 3.11	Application development
LangChain	LLM application framework
LangGraph	Agent/workflow orchestration
Groq	LLM inference
Tavily	AI/web research
Pydantic	Data validation
Scikit-learn	Duplicate detection
Requests	LinkedIn API integration
GitHub Actions	Scheduling and automation
uv	Dependency management
Docker	Containerization
Pytest	Automated testing

⸻

📦 Installation

1. Clone the repository

git clone https://github.com/arunrajselvarasu/linkedin-ai-agent-public.git
cd linkedin-ai-agent-public

⸻

2. Install uv

If uv is not already installed:

curl -LsSf https://astral.sh/uv/install.sh | sh

Restart your terminal if required.

Verify:

uv --version

⸻

3. Install dependencies

uv sync

⸻

🔑 Environment Configuration

Create:

.env

Add:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model
TAVILY_API_KEY=your_tavily_api_key
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_PERSON_URN=your_linkedin_person_urn
LINKEDIN_VERSION=your_linkedin_api_version
DRY_RUN=true

Never commit .env

The repository .gitignore already excludes:

.env

Never publish:

* API keys
* Access tokens
* Personal credentials
* Private configuration
* Secrets

⸻

▶️ Run Locally

Run the complete agent:

uv run python -m src.main

Example execution:

========================================
🚀 LINKEDIN AI AGENT
========================================
Topic selected
Research completed
Post generated
Validation passed
Duplicate check passed
💾 Dry-run post saved to history
✅ Execution completed
========================================
🏁 WORKFLOW FINISHED
========================================
Status: dry_run
Execution Status: completed

⸻

🧪 Testing

The project contains automated tests for the major reliability components.

Run:

uv run pytest -v

Current test coverage includes:

Guardrails

* Validation failure
* Retry routing
* Maximum retry handling
* Successful validation routing
* Duplicate routing

Workflow

* Graph compilation
* Required workflow nodes

Execution lifecycle

* Failure state handling

History

* Execution claiming
* Execution completion
* Post persistence
* Failed execution retry

Duplicate detection

* Empty history
* Similar content
* Different content
* Duplicate detection
* New-content detection

Current test suite:

18 tests

Expected result:

18 passed

⸻

🔬 Example LangGraph Flow

The workflow is implemented using LangGraph.

Conceptually:

START
  │
  ▼
Execution
  │
  ├── Already Processed ──────► END
  │
  ▼
Topic
  │
  ▼
Research
  │
  ▼
Writer
  │
  ▼
Validator
  │
  ├── Failed ──► Regenerate
  │                  │
  │                  └──► Writer
  │
  ▼
Duplicate Check
  │
  ├── Duplicate ──► Regenerate
  │                     │
  │                     └──► Writer
  │
  ▼
Publish
  │
  ▼
Execution Completed
  │
  ▼
 END

This provides explicit state transitions instead of relying on a simple sequential script.

⸻

🧠 Why LangGraph?

LangGraph is used because the application requires:

* Stateful workflows
* Conditional routing
* Retry loops
* Validation gates
* Duplicate detection
* Execution lifecycle management
* Failure handling
* Controlled publishing

This makes the system closer to a production-oriented agent workflow than a simple LLM API call.

⸻

🛡️ Reliability Design

The project includes multiple safety layers before publishing.

             Generated Content
                    │
                    ▼
             AI Validation
                    │
            ┌───────┴───────┐
            │               │
          Failed          Passed
            │               │
            ▼               ▼
        Regenerate     Duplicate Check
                            │
                     ┌──────┴──────┐
                     │             │
                  Duplicate      Unique
                     │             │
                     ▼             ▼
                 Regenerate     Publish

The intention is to make publishing a controlled final step, rather than allowing the LLM to directly publish generated content.

⸻

📈 Example Execution

A typical execution may look like:

Execution Key:
2026-09-10-morning
Topic:
RAG
Subtopic:
Hybrid Retrieval
Angle:
Practical AI Engineering
Research:
Completed
Generated Post:
Completed
Quality Score:
0.92
Duplicate Similarity:
0.10
Validation:
PASSED
Duplicate Check:
PASSED
Publishing:
DRY RUN
Execution:
COMPLETED

⸻

🔐 GitHub Actions Secrets

For scheduled cloud execution, configure these GitHub Actions secrets:

GROQ_API_KEY
GROQ_MODEL
TAVILY_API_KEY
LINKEDIN_ACCESS_TOKEN
LINKEDIN_PERSON_URN
LINKEDIN_VERSION
DRY_RUN

Do not hard-code any of these values inside the source code.

⸻

🐳 Docker

The project also includes a Dockerfile.

Build:

docker build -t linkedin-ai-agent .

Run:

docker run --env-file .env linkedin-ai-agent

⸻

📊 Production Workflow

The intended production workflow is:

GitHub Actions
      │
      ▼
Scheduled Trigger
      │
      ▼
LangGraph Agent
      │
      ├── Topic Selection
      │
      ├── Research
      │
      ├── Content Generation
      │
      ├── Validation
      │
      ├── Duplicate Detection
      │
      └── Publishing
      │
      ▼
LinkedIn
      │
      ▼
Persistent History
      │
      ▼
Git Commit
      │
      ▼
GitHub Repository

⸻

🔮 Future Improvements

Potential future enhancements include:

Semantic Duplicate Detection

Replace lexical TF-IDF similarity with embedding-based semantic similarity.

Advanced Content Evaluation

Introduce additional evaluation criteria such as:

* Factual grounding
* Research citation quality
* Readability
* Engagement potential
* Technical depth

AI Content Analytics

Analyze:

* Impressions
* Reactions
* Comments
* Engagement rate
* Post performance

Then use those metrics to improve future topic selection.

Trend Detection

Automatically identify trending AI/ML topics and prioritize them.

Content Memory

Use long-term semantic memory to prevent repeating the same ideas even when the wording is completely different.

Observability

Integrate tracing and monitoring for:

* Agent execution
* LLM calls
* Token usage
* Latency
* Validation failures
* Publishing failures

Database-backed State

Move persistent history from JSON to a production database.

⸻

🎯 What This Project Demonstrates

This project demonstrates practical experience with:

✓ Generative AI
✓ Agentic AI
✓ LangChain
✓ LangGraph
✓ LLM integration
✓ Prompt engineering
✓ AI guardrails
✓ RAG-style research workflows
✓ Tool integration
✓ API integration
✓ State management
✓ Retry mechanisms
✓ Duplicate detection
✓ Automated testing
✓ GitHub Actions
✓ CI/CD automation
✓ Docker
✓ Production-oriented AI engineering

⸻

💡 Key Engineering Principles

The project follows several important AI engineering principles:

1. LLMs should not directly control critical actions

The generated content passes through deterministic and AI-based validation before publishing.

2. Agents need state

LangGraph maintains workflow state between different stages.

3. Failures should be handled explicitly

Validation failures and duplicate content are routed through controlled retry paths.

4. Scheduled automation needs idempotency

Execution keys prevent duplicate processing of the same scheduled slot.

5. AI systems need guardrails

Content generation and content publishing are treated as separate stages.

⸻

👨‍💻 Author

Arunraj S

AI Engineer | Generative AI | Agentic AI | LangChain | LangGraph | RAG | AI Automation

Interested in building practical AI systems, autonomous agents, intelligent automation, and production-oriented GenAI applications.

⸻

⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐.

Feel free to explore the architecture, experiment with the agents, and extend the workflow with your own AI/ML use cases.

⸻

⚠️ Disclaimer

This project is intended for educational, experimental, and portfolio purposes.

When using automated LinkedIn publishing, ensure that your implementation complies with LinkedIn’s current API terms, developer policies, rate limits, and applicable platform rules.

Never expose API credentials, access tokens, or other secrets in a public repository.