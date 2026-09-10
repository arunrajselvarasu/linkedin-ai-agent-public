from src.graph.workflow import graph
from src.services.history import update_execution_status


def main():
    """
    Application entry point.
    """

    print("\n")
    print("========================================")
    print("🚀 LINKEDIN AI AGENT")
    print("========================================")
    print("\n")

    try:

        result = graph.invoke({})

        print("\n")
        print("========================================")
        print("🏁 WORKFLOW FINISHED")
        print("========================================")

        print(
            f"Status: "
            f"{result.get('status')}"
        )

        print(
            f"Execution Status: "
            f"{result.get('execution_status')}"
        )

        print("\n")

        return result

    except Exception as exc:

        print("\n")
        print("========================================")
        print("💥 WORKFLOW EXCEPTION")
        print("========================================")

        print(
            f"Error: {exc}"
        )

        print("\n")

        # ----------------------------------------------------
        # Mark execution as failed
        # ----------------------------------------------------

        try:

            execution_key = (
                result_execution_key()
            )

            if execution_key:

                update_execution_status(
                    execution_key,
                    "failed",
                )

        except Exception as lifecycle_error:

            print(
                "⚠️ Could not update "
                "execution failure status:"
            )

            print(
                lifecycle_error
            )

        raise


def result_execution_key():
    """
    Read the currently claimed execution key
    from the persisted execution history.

    This is intentionally kept simple.
    The execution key is based on the current
    IST morning/evening slot.
    """

    from datetime import datetime
    from zoneinfo import ZoneInfo

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    if now.hour < 12:
        slot = "morning"
    else:
        slot = "evening"

    return (
        f"{now.strftime('%Y-%m-%d')}-{slot}"
    )


if __name__ == "__main__":
    main()