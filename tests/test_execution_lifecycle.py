from unittest.mock import patch

from src.graph.workflow import mark_execution_failed


def test_execution_failure_updates_status():
    execution_key = "test-execution-failure"

    with patch(
        "src.graph.workflow.update_execution_status"
    ) as mock_update:

        result = mark_execution_failed(
            {
                "execution_key": execution_key,
            }
        )

    mock_update.assert_called_once_with(
        execution_key,
        "failed",
    )

    assert result["execution_status"] == "failed"
    assert result["status"] == "failed"