import pytest
from app.application.agents.architecture_review_agent import build_architecture_review_agent


@pytest.mark.asyncio
async def test_architecture_review_agent_execution():
    agent = build_architecture_review_agent()

    initial_state = {
        "repo_name": "acme/billing-microservice",
        "file_tree": ["src/main.py", "src/services/billing_monolith.py"],
        "dependencies": {"fastapi": "0.110.0", "sqlalchemy": "2.0.28"},
        "code_snippets": {
            "src/services/billing_monolith.py": "\n".join(["# line"] * 450)
        },
        "neo4j_session": None,
        "coupling_analysis": {},
        "circular_dependencies": [],
        "god_classes": [],
        "solid_violations": [],
        "clean_arch_compliance_score": 100.0,
        "tech_debt_score": 0.0,
        "architecture_report": "",
        "recommendations": []
    }

    final_state = await agent.ainvoke(initial_state)

    assert "tech_debt_score" in final_state
    assert isinstance(final_state["tech_debt_score"], float)
    assert len(final_state["god_classes"]) == 1
    assert final_state["god_classes"][0]["file_path"] == "src/services/billing_monolith.py"
    assert len(final_state["architecture_report"]) > 0
    assert len(final_state["recommendations"]) > 0
