from rules.actions import execute_actions
from rules.rule_schema import RuleAction
from types import SimpleNamespace
import pytest

def test_execute_mark_as_read(mocker):
    service = mocker.Mock()
    email = SimpleNamespace(gmail_id="abc123")

    action = RuleAction(type="mark_as_read")
    execute_actions(service, email, [action])

    service.users().messages().modify.assert_called_with(
        userId='me',
        id='abc123',
        body={'removeLabelIds': ['UNREAD']}
    )

def test_mark_as_read_does_not_call_if_wrong_action_type(mocker):
    service = mocker.Mock()
    email = SimpleNamespace(gmail_id="no_action")
    
    # No 'mark_as_read' in actions
    execute_actions(service, email, [])
    
    # Should not call modify at all
    service.users().messages().modify.assert_not_called()

def test_execute_mark_as_unread(mocker):
    service = mocker.Mock()
    email = SimpleNamespace(gmail_id="def456")

    action = RuleAction(type="mark_as_unread")
    execute_actions(service, email, [action])

    service.users().messages().modify.assert_called_with(
        userId='me',
        id='def456',
        body={'addLabelIds': ['UNREAD']}
    )

def test_execute_move_existing_label(mocker):
    service = mocker.Mock()
    email = SimpleNamespace(gmail_id="move123")
    label_name = "TestLabel"

    service.users().labels().list.return_value.execute.return_value = {
        "labels": [{"id": "Label_1", "name": label_name}]
    }

    action = RuleAction(type="move", label=label_name)
    execute_actions(service, email, [action])

    service.users().messages().modify.assert_called_with(
        userId='me',
        id='move123',
        body={'addLabelIds': ['Label_1'], 'removeLabelIds': ['INBOX']}
    )

def test_execute_move_label_not_created_and_no_existing_label(mocker):
    service = mocker.Mock()
    email = SimpleNamespace(gmail_id="no_label")
    label_name = "UncreatableLabel"

    # Simulate no existing labels and failure to create
    service.users().labels().list.return_value.execute.return_value = {"labels": []}
    service.users().labels().create.side_effect = Exception("Label creation failed")

    action = RuleAction(type="move", label=label_name)

    # Expect action to raise but not call message.modify
    with pytest.raises(Exception, match="Label creation failed"):
        execute_actions(service, email, [action])

    service.users().messages().modify.assert_not_called()

def test_execute_move_create_label(mocker):
    service = mocker.Mock()
    email = SimpleNamespace(gmail_id="move456")
    label_name = "NewLabel"

    # No label matches, so new one is created
    service.users().labels().list.return_value.execute.return_value = {"labels": []}
    service.users().labels().create.return_value.execute.return_value = {"id": "Label_New"}

    action = RuleAction(type="move", label=label_name)
    execute_actions(service, email, [action])

    service.users().labels().create.assert_called_with(userId='me', body={
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    })

    service.users().messages().modify.assert_called_with(
        userId='me',
        id='move456',
        body={'addLabelIds': ['Label_New'], 'removeLabelIds': ['INBOX']}
    )