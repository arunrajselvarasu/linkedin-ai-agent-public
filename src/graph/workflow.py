import os

from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from src.agents.research_agent import (
    research_topic,
    synthesize_research,
)

from src.agents.topic_agent import (
    select_topic,
)

from src.agents.validator_agent import (
    validate_post,
)

from src.agents.writer_agent import (
    generate_post,
)

from src.graph.router import (
    route_after_duplicate_check,
    route_after_validation,
)

from src.graph.state import (
    LinkedInState,
)

from src.services.duplicate_detector import (
    check_duplicate,
)

from src.services.history import (
    claim_execution,
    save_post,
    update_execution_status,
)

from src.tools.linkedin import (
    publish_to_linkedin,
)

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

MAX_RETRIES = 3
MIN_QUALITY_SCORE = 0.85


# ============================================================
# EXECUTION LIFECYCLE
# ============================================================

def mark_execution_completed(
    state: LinkedInState,
):
    """
    Mark execution as completed.
    """

    execution_key = state.get(
        "execution_key"
    )

    if execution_key:
        update_execution_status(
            execution_key,
            "completed",
        )

    print(
        f"✅ Execution completed: "
        f"{execution_key}"
    )

    return {
        "execution_status": "completed",
    }


def mark_execution_failed(
    state: LinkedInState,
):
    """
    Mark execution as failed.
    """

    execution_key = state.get(
        "execution_key"
    )

    if execution_key:
        update_execution_status(
            execution_key,
            "failed",
        )

    print(
        f"❌ Execution failed: "
        f"{execution_key}"
    )

    return {
        "execution_status": "failed",
        "status": "failed",
    }


# ============================================================
# EXECUTION / IDEMPOTENCY
# ============================================================

def execution_node(
    state: LinkedInState,
):
    """
    Create a unique execution key
    for morning/evening scheduling.

    Example:

    2026-09-10-morning
    2026-09-10-evening
    """

    print("\n==============================")
    print("🔐 IDEMPOTENCY CHECK")
    print("==============================")

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    if now.hour < 12:
        slot = "morning"
    else:
        slot = "evening"

    execution_key = (
        f"{now.strftime('%Y-%m-%d')}-{slot}"
    )

    print(
        f"Execution Key: {execution_key}"
    )

    is_new_execution = (
        claim_execution(
            execution_key
        )
    )

    if not is_new_execution:

        print(
            "⚠️ This execution has already "
            "been processed."
        )

        return {
            "execution_key": execution_key,
            "execution_status":
                "already_processed",
            "status":
                "already_processed",
        }

    print(
        "✅ New execution claimed"
    )

    return {
        "execution_key": execution_key,
        "execution_status": "started",
        "status":
            "execution_started",
    }


def route_after_execution(
    state: LinkedInState,
):
    """
    Decide whether execution should continue.
    """

    if (
        state.get(
            "execution_status"
        )
        == "already_processed"
    ):
        return "stop"

    return "continue"


# ============================================================
# 1. TOPIC NODE
# ============================================================

def topic_node(
    state: LinkedInState,
):
    """
    Select a fresh AI/ML topic.
    """

    print("\n==============================")
    print("🤖 TOPIC AGENT")
    print("==============================")

    selection = select_topic()

    print(
        f"Topic     : {selection.topic}"
    )

    print(
        f"Subtopic  : {selection.subtopic}"
    )

    print(
        f"Angle     : {selection.angle}"
    )

    return {
        "topic":
            selection.topic,

        "subtopic":
            selection.subtopic,

        "angle":
            selection.angle,

        "retry_count":
            0,

        "status":
            "topic_selected",
    }


# ============================================================
# 2. RESEARCH NODE
# ============================================================

def research_node(
    state: LinkedInState,
):
    """
    Research the selected topic.
    """

    print("\n==============================")
    print("🔎 RESEARCH AGENT")
    print("==============================")

    topic = state["topic"]
    subtopic = state["subtopic"]
    angle = state["angle"]

    print(
        f"Researching: "
        f"{topic} → {subtopic}"
    )

    raw_research = research_topic(
        topic=topic,
        subtopic=subtopic,
        angle=angle,
    )

    research = synthesize_research(
        topic=topic,
        subtopic=subtopic,
        angle=angle,
        raw_research=raw_research,
    )

    print(
        "✅ Research completed"
    )

    return {
        "research":
            research,

        "status":
            "research_completed",
    }


# ============================================================
# 3. WRITER NODE
# ============================================================

def writer_node(
    state: LinkedInState,
):
    """
    Generate LinkedIn content.
    """

    print("\n==============================")
    print("✍️ WRITER AGENT")
    print("==============================")

    retry_count = state.get(
        "retry_count",
        0,
    )

    if retry_count > 0:

        print(
            f"♻️ Regeneration attempt: "
            f"{retry_count}"
        )

    post = generate_post(
        topic=state["topic"],
        subtopic=state["subtopic"],
        angle=state["angle"],
        research=state["research"],

        validation_feedback=
            state.get(
                "validation_feedback",
                "",
            ),

        duplicate_score=
            state.get(
                "duplicate_score",
                0.0,
            ),

        retry_count=
            retry_count,
    )

    print("\nGenerated Post:")
    print(
        "------------------------------"
    )

    print(post)

    print(
        "------------------------------"
    )

    return {
        "generated_post":
            post,

        "retry_count":
            retry_count,

        "status":
            "post_generated",
    }


# ============================================================
# 4. VALIDATOR NODE
# ============================================================

def validator_node(
    state: LinkedInState,
):
    """
    Validate the generated post.
    """

    print("\n==============================")
    print("🛡️ VALIDATOR AGENT")
    print("==============================")

    result = validate_post(
        post=state[
            "generated_post"
        ],

        research=state.get(
            "research",
            "",
        ),
    )

    print(
        f"AI/ML             : "
        f"{result['is_ai_ml']}"
    )

    print(
        f"Technical         : "
        f"{result['technically_sound']}"
    )

    print(
        f"Professional      : "
        f"{result['professional']}"
    )

    print(
        f"Recruiter         : "
        f"{result['recruiter_relevant']}"
    )

    print(
        f"Engineer          : "
        f"{result['engineer_relevant']}"
    )

    print(
        f"Grammar           : "
        f"{result['grammar_ok']}"
    )

    print(
        f"Quality Score     : "
        f"{result['quality_score']}"
    )

    print(
        f"Feedback          : "
        f"{result['feedback']}"
    )

    return {
        "is_ai_ml":
            result["is_ai_ml"],

        "technically_sound":
            result[
                "technically_sound"
            ],

        "professional":
            result[
                "professional"
            ],

        "recruiter_relevant":
            result[
                "recruiter_relevant"
            ],

        "engineer_relevant":
            result[
                "engineer_relevant"
            ],

        "grammar_ok":
            result[
                "grammar_ok"
            ],

        "quality_score":
            result[
                "quality_score"
            ],

        "validation_feedback":
            result[
                "feedback"
            ],

        "status":
            "validated",
    }


# ============================================================
# 5. DUPLICATE DETECTION
# ============================================================

def duplicate_node(
    state: LinkedInState,
):
    """
    Check semantic similarity against
    previously generated/published posts.
    """

    print("\n==============================")
    print("🔍 DUPLICATE DETECTOR")
    print("==============================")

    post = state[
        "generated_post"
    ]

    is_duplicate, similarity = (
        check_duplicate(post)
    )

    print(
        f"Similarity Score : "
        f"{similarity:.4f}"
    )

    print(
        f"Duplicate        : "
        f"{is_duplicate}"
    )

    if is_duplicate:
        print(
            "⚠️ Duplicate detected"
        )
    else:
        print(
            "✅ Post is unique"
        )

    return {
        "is_duplicate":
            is_duplicate,

        "duplicate_score":
            similarity,

        "status":
            (
                "duplicate_detected"
                if is_duplicate
                else "unique_post"
            ),
    }


# ============================================================
# 6. REGENERATE
# ============================================================

def regenerate_node(
    state: LinkedInState,
):
    """
    Increment retry count.

    Writer receives the new retry count,
    validation feedback and duplicate score.
    """

    retry_count = (
        state.get(
            "retry_count",
            0,
        )
        + 1
    )

    print("\n==============================")
    print("♻️ REGENERATION")
    print("==============================")

    print(
        f"Retry attempt: "
        f"{retry_count}/{MAX_RETRIES}"
    )

    return {
        "retry_count":
            retry_count,

        "status":
            "regenerating",
    }


# ============================================================
# 7. PUBLISH
# ============================================================

def publish_node(
    state: LinkedInState,
):
    """
    Final safety gate and publishing.
    """

    print("\n==============================")
    print("🚀 PUBLISH NODE")
    print("==============================")

    post = state[
        "generated_post"
    ]

    # --------------------------------------------------------
    # FINAL VALIDATION GATE
    # --------------------------------------------------------

    validation_passed = (
        state.get(
            "is_ai_ml",
            False,
        )
        and state.get(
            "technically_sound",
            False,
        )
        and state.get(
            "professional",
            False,
        )
        and state.get(
            "recruiter_relevant",
            False,
        )
        and state.get(
            "engineer_relevant",
            False,
        )
        and state.get(
            "grammar_ok",
            False,
        )
        and state.get(
            "quality_score",
            0.0,
        ) >= MIN_QUALITY_SCORE
    )

    if not validation_passed:

        print(
            "❌ FINAL VALIDATION FAILED"
        )

        print(
            "Post will NOT be published."
        )

        return {
            "status":
                "publish_blocked_validation"
        }

    # --------------------------------------------------------
    # FINAL DUPLICATE GATE
    # --------------------------------------------------------

    if state.get(
        "is_duplicate",
        True,
    ):

        print(
            "❌ FINAL DUPLICATE CHECK FAILED"
        )

        print(
            "Post will NOT be published."
        )

        return {
            "status":
                "publish_blocked_duplicate"
        }

    # --------------------------------------------------------
    # DRY RUN
    # --------------------------------------------------------

    dry_run = (
        os.getenv(
            "DRY_RUN",
            "true",
        ).lower()
        == "true"
    )

    print(
        f"🔥 DRY_RUN: {dry_run}"
    )

    if dry_run:

        print(
            "\n🧪 DRY RUN MODE"
        )

        print(
            "LinkedIn publishing "
            "is disabled."
        )

        print(
            "\nPost that would be published:"
        )

        print(
            "--------------------------------"
        )

        print(post)

        print(
            "--------------------------------"
        )

        save_post(
            {
                "content":
                    post,

                "topic":
                    state.get(
                        "topic"
                    ),

                "subtopic":
                    state.get(
                        "subtopic"
                    ),

                "angle":
                    state.get(
                        "angle"
                    ),

                "linkedin_post_id":
                    None,

                "quality_score":
                    state.get(
                        "quality_score"
                    ),

                "duplicate_score":
                    state.get(
                        "duplicate_score"
                    ),

                "status":
                    "dry_run",
            }
        )

        print(
            "💾 Dry-run post saved "
            "to history"
        )

        return {
            "status":
                "dry_run"
        }

    # --------------------------------------------------------
    # REAL PUBLISH
    # --------------------------------------------------------

    print(
        "📤 Publishing to LinkedIn..."
    )

    linkedin_post_id = (
        publish_to_linkedin(
            post
        )
    )

    print(
        "✅ LinkedIn post published!"
    )

    print(
        f"Post ID: "
        f"{linkedin_post_id}"
    )

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    save_post(
        {
            "content":
                post,

            "topic":
                state.get(
                    "topic"
                ),

            "subtopic":
                state.get(
                    "subtopic"
                ),

            "angle":
                state.get(
                    "angle"
                ),

            "linkedin_post_id":
                linkedin_post_id,

            "quality_score":
                state.get(
                    "quality_score"
                ),

            "duplicate_score":
                state.get(
                    "duplicate_score"
                ),

            "status":
                "published",
        }
    )

    print(
        "💾 Post saved to history"
    )

    return {
        "linkedin_post_id":
            linkedin_post_id,

        "status":
            "published",
    }


# ============================================================
# 8. FAILED NODE
# ============================================================

def failed_node(
    state: LinkedInState,
):
    """
    Logical failure after maximum retries.
    """

    print("\n==============================")
    print("❌ WORKFLOW FAILED")
    print("==============================")

    retry_count = state.get(
        "retry_count",
        0,
    )

    print(
        f"Retries used: "
        f"{retry_count}/{MAX_RETRIES}"
    )

    print(
        "The post was NOT published."
    )

    return {
        "status":
            "failed",
    }


# ============================================================
# LANGGRAPH
# ============================================================

builder = StateGraph(
    LinkedInState
)


# ============================================================
# NODES
# ============================================================

builder.add_node(
    "execution",
    execution_node,
)

builder.add_node(
    "topic",
    topic_node,
)

builder.add_node(
    "research",
    research_node,
)

builder.add_node(
    "writer",
    writer_node,
)

builder.add_node(
    "validator",
    validator_node,
)

builder.add_node(
    "duplicate",
    duplicate_node,
)

builder.add_node(
    "regenerate",
    regenerate_node,
)

builder.add_node(
    "publish",
    publish_node,
)

builder.add_node(
    "failed",
    failed_node,
)

builder.add_node(
    "execution_completed",
    mark_execution_completed,
)

builder.add_node(
    "execution_failed",
    mark_execution_failed,
)


# ============================================================
# START
# ============================================================

builder.add_edge(
    START,
    "execution",
)


# ============================================================
# IDEMPOTENCY ROUTING
# ============================================================

builder.add_conditional_edges(
    "execution",
    route_after_execution,
    {
        "continue":
            "topic",

        "stop":
            END,
    },
)


# ============================================================
# MAIN PIPELINE
# ============================================================

builder.add_edge(
    "topic",
    "research",
)

builder.add_edge(
    "research",
    "writer",
)

builder.add_edge(
    "writer",
    "validator",
)


# ============================================================
# VALIDATION ROUTING
# ============================================================

builder.add_conditional_edges(
    "validator",
    route_after_validation,
    {
        "duplicate_check":
            "duplicate",

        "regenerate":
            "regenerate",

        "failed":
            "execution_failed",
    },
)


# ============================================================
# DUPLICATE ROUTING
# ============================================================

builder.add_conditional_edges(
    "duplicate",
    route_after_duplicate_check,
    {
        "publish":
            "publish",

        "regenerate":
            "regenerate",

        "failed":
            "execution_failed",
    },
)


# ============================================================
# REGENERATION LOOP
# ============================================================

builder.add_edge(
    "regenerate",
    "writer",
)


# ============================================================
# SUCCESS
# ============================================================

builder.add_edge(
    "publish",
    "execution_completed",
)

builder.add_edge(
    "execution_completed",
    END,
)


# ============================================================
# FAILURE
# ============================================================

builder.add_edge(
    "execution_failed",
    END,
)


# ============================================================
# COMPILE
# ============================================================

graph = builder.compile()