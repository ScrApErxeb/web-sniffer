import pytest
from core.reporting import Reporter

def test_generate_report_creates_dict(tmp_path):
    data = [{"title": "t1"}, {"title": "t2"}]

    reporter = Reporter(output_dir=tmp_path)  # tmp_path est un répertoire temporaire
    reporter.add_query_results(
        "test_query",
        data,
        {"mock_source": {"count": len(data), "status": "OK"}}
    )

    assert "queries" in reporter.data
    assert "test_query" in reporter.data["queries"]
    assert len(reporter.data["queries"]["test_query"]["results"]) == 2
