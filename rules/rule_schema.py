from typing import List, Literal, Union
from pydantic import BaseModel
from datetime import datetime


# Supported predicates
StringPredicate = Literal[
    "contains", "does_not_contain", "equals", "does_not_equal"
]

DatePredicate = Literal[
    "less_than_days", "greater_than_days", "less_than_months", "greater_than_months"
]

FieldName = Literal["from", "subject", "message", "received_at"]

ActionType = Literal["mark_as_read", "mark_as_unread", "move"]


class RuleCondition(BaseModel):
    field: FieldName
    predicate: Union[StringPredicate, DatePredicate]
    value: Union[str, int]


class RuleAction(BaseModel):
    type: ActionType
    label: Union[str, None] = None  # Needed for move action


class Rule(BaseModel):
    predicate: Literal["all", "any"]
    rules: List[RuleCondition]
    actions: List[RuleAction]


class RuleSet(BaseModel):
    rules: List[Rule]