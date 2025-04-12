from rules.rules_engine import apply_rules
from rules.rule_schema import RuleSet
from types import SimpleNamespace
from datetime import datetime, timedelta
from db.models import Email

def make_email(**kwargs):
    return Email(
        sender=kwargs.get("from_email", "john@example.com"),
        # recipient=kwargs.get("recipient", "me@example.com"),
        subject=kwargs.get("subject", "Offer Letter"),
        message_snippet=kwargs.get("message", "Welcome to HappyFox"),
        received_at=kwargs.get("received_at", datetime.utcnow() - timedelta(days=1))
    )

def test_rule_with_all_predicates_matching():
    email = make_email(sender="hr@happyfox.com", subject="Welcome")
    rule_data = {
        "rules": [
            {
                "predicate": "all",
                "rules": [
                    {"field": "from", "predicate": "contains", "value": "happyfox"},
                    {"field": "subject", "predicate": "contains", "value": "welcome"}
                ],
                "actions": [{"type": "mark_as_read"}]
            }
        ]
    }
    rs = RuleSet(**rule_data)
    db = SimpleNamespace(query=lambda model: SimpleNamespace(all=lambda: [email]))
    matches = apply_rules(db, rs)
    assert len(matches) == 0

def test_rule_with_any_predicate_matching():
    email = make_email(sender="no-reply@random.com", subject="Offer")
    rule_data = {
        "rules": [
            {
                "predicate": "any",
                "rules": [
                    {"field": "from", "predicate": "contains", "value": "happyfox"},
                    {"field": "subject", "predicate": "contains", "value": "offer"}
                ],
                "actions": [{"type": "mark_as_unread"}]
            }
        ]
    }
    rs = RuleSet(**rule_data)
    db = SimpleNamespace(query=lambda model: SimpleNamespace(all=lambda: [email]))
    matches = apply_rules(db, rs)
    assert len(matches) == 1
    assert matches[0][1][0].type == "mark_as_unread"

def test_rule_no_match():
    email = make_email(sender="support@abc.com", subject="Billing Issue")
    rule_data = {
        "rules": [
            {
                "predicate": "all",
                "rules": [
                    {"field": "from", "predicate": "contains", "value": "xyz"},
                    {"field": "subject", "predicate": "equals", "value": "Something Else"}
                ],
                "actions": [{"type": "mark_as_unread"}]
            }
        ]
    }
    rs = RuleSet(**rule_data)
    db = SimpleNamespace(query=lambda model: SimpleNamespace(all=lambda: []))
    matches = apply_rules(db, rs)
    assert len(matches) == 0
