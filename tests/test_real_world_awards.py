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
