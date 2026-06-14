"""Regression tests for real-world public rewarded issue patterns."""

import pytest
from vrp.parser import build_issue

from tests.fixtures import make_raw_metadata, make_raw_updates


@pytest.mark.parametrize(
    ("issue_id", "amount"),
    [
        ("351327767", 20000.0),
        ("384186547", 20000.0),
        ("386565144", 50000.0),
        ("481074858", 11000.0),
    ],
)
def test_metadata_reward_regression_cases(issue_id, amount):
    issue = build_issue(
        issue_id,
        make_raw_updates(bounty_text="No public award text."),
        make_raw_metadata(bounty_amount=amount),
    )
    assert issue is not None
    assert issue.public_issue is True
    assert issue.bounty_amount == amount
    assert issue.reward_amount_meta == amount
    assert issue.inclusion_reason == "reward_amount_meta"
    assert issue.award_text_found is False


# --- Denial emails must NOT be mistaken for awards (false-positive guard) ---

DENIAL_TEXT = (
    "*NOTE: This is an automatically generated email* Hello, Chrome "
    "Vulnerability Rewards Program (VRP) Panel has decided that the security "
    "impact of this issue does not meet the criteria to qualify for a reward. "
    "Rationale for this decision: Controlled assertion failure."
)


def test_panel_denial_email_is_not_a_bounty():
    """The panel's denial email shares the 'VRP Panel' header with grant emails;
    it must not be flagged as a confirmed bounty (regression for ~22 false
    positives)."""
    issue = build_issue(
        "999000001",
        make_raw_updates(bounty_text=DENIAL_TEXT),
        make_raw_metadata(bounty_amount=0),
    )
    assert issue is None


@pytest.mark.parametrize(
    ("text", "amount"),
    [
        ("The VRP Panel has decided to award you $5,000. Congratulations!", 5000.0),
        ("The VRP Panel has decided to award $500 for reporting this issue.", 500.0),
        ("The Chrome VRP panel has decided to award the parent bug a VRP reward of $20,000.", 20000.0),
        ("Congratulations! We awarded $1,337 for this report.", 1337.0),
    ],
)
def test_award_phrasings_detected_with_amount(text, amount):
    issue = build_issue(
        "999000002",
        make_raw_updates(bounty_text=text),
        make_raw_metadata(bounty_amount=0),
    )
    assert issue is not None
    assert issue.bounty_amount == amount
    assert issue.award_text_found is True
    assert issue.inclusion_reason == "award_text"
