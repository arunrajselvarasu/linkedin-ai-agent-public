from src.graph.workflow import graph


def main():
    print("\n")
    print("========================================")
    print("🤖 AUTONOMOUS LINKEDIN AI CONTENT AGENT")
    print("========================================")
    print("Starting workflow...")
    print("========================================")

    try:
        final_state = graph.invoke({})

        print("\n========================================")
        print("🏁 WORKFLOW COMPLETED")
        print("========================================")

        print(f"Status: {final_state.get('status')}")

        if final_state.get("topic"):
            print(f"Topic: {final_state['topic']}")

        if final_state.get("subtopic"):
            print(f"Subtopic: {final_state['subtopic']}")

        if final_state.get("quality_score") is not None:
            print(
                f"Quality Score: "
                f"{final_state['quality_score']}"
            )

        if final_state.get("duplicate_score") is not None:
            print(
                f"Duplicate Score: "
                f"{final_state['duplicate_score']:.4f}"
            )

        if final_state.get("linkedin_post_id"):
            print(
                f"LinkedIn Post ID: "
                f"{final_state['linkedin_post_id']}"
            )

        print("========================================")

    except Exception as exc:
        print("\n========================================")
        print("❌ WORKFLOW ERROR")
        print("========================================")
        print(str(exc))
        print("========================================")

        raise


if __name__ == "__main__":
    main()