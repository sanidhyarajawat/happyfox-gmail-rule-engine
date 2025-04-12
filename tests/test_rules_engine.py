import pytest
from rules.rules_engine import match_condition
from rules.rule_schema import RuleCondition
from datetime import datetime, timedelta
from types import SimpleNamespace

# Simulate an Email object using SimpleNamespace
now = datetime.utcnow()

def make_email(**kwargs):
    return SimpleNamespace(
        sender=kwargs.get("sender", "john@example.com"),
        recipient=kwargs.get("recipient", "me@example.com"),
        subject=kwargs.get("subject", "Meeting with HappyFox"),
        message_snippet=kwargs.get("message_snippet", "Let’s discuss the HappyFox rule engine."),
        received_at=kwargs.get("received_at", now - timedelta(days=1))
    )

@pytest.mark.parametrize("cond,email,expected", [
    (RuleCondition(field="from", predicate="contains", value="example"), make_email(sender="john@example.com"), True),
    (RuleCondition(field="from", predicate="does_not_contain", value="gmail"), make_email(sender="john@example.com"), True),
    (RuleCondition(field="subject", predicate="equals", value="Meeting with HappyFox"), make_email(), True),
    (RuleCondition(field="subject", predicate="does_not_equal", value="Random Subject"), make_email(), True),
    (RuleCondition(field="received_at", predicate="less_than_days", value=2), make_email(received_at=now - timedelta(days=1)), True),
    (RuleCondition(field="received_at", predicate="greater_than_days", value=1), make_email(received_at=now - timedelta(days=2)), True),
    (RuleCondition(field="message", predicate="contains", value="HappyFox"), make_email(message_snippet="This is about HappyFox"), True),
    (RuleCondition(field="message", predicate="does_not_contain", value="error"), make_email(message_snippet="No issues"), True)
])
def test_match_condition(cond, email, expected):
    assert match_condition(email, cond) == expected
