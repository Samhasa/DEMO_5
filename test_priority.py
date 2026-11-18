import pytest

from priority_score import calculate_priority_score


@pytest.mark.parametrize(
    ("severity", "metric_value", "expected_score"),
    [
        ("critical", 125.0, 70),
        ("warning", 150.0, 50),
        ("info", 110.0, 14),
    ],
)
def test_calculate_priority_score_above_threshold(
    severity: str,
    metric_value: float,
    expected_score: int,
) -> None:
    score = calculate_priority_score(severity, metric_value, 100.0)

    assert score == expected_score
    assert isinstance(score, int)


# --- Edge cases added manually ---
def test_unknown_severity_raises_value_error():
    with pytest.raises(ValueError, match="Unsupported severity"):
        calculate_priority_score("emergency", 100, 90)


def test_zero_threshold_raises_value_error():
    with pytest.raises(ValueError, match="threshold must not be zero"):
        calculate_priority_score("critical", 50, 0)


def test_metric_below_threshold_gets_no_bonus():
    assert calculate_priority_score("warning", -20, 10) == 30


def test_metric_at_threshold_gets_no_bonus():
    assert calculate_priority_score("warning", 100, 100) == 30


def test_large_breach_caps_score_at_100():
    assert calculate_priority_score("critical", 1000, 100) == 100