from src.graph.workflow import graph


def test_workflow_is_compiled():
    assert graph is not None


def test_workflow_has_required_nodes():
    nodes = graph.nodes

    required_nodes = {
        "execution",
        "topic",
        "research",
        "writer",
        "validator",
        "duplicate",
        "regenerate",
        "publish",
        "failed",
        "execution_completed",
        "execution_failed",
    }

    for node in required_nodes:
        assert node in nodes