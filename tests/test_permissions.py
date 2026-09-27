from agent_workshop.permissions import PermissionPolicy

def test_permissions_deny_by_default():
    assert PermissionPolicy().allows("filesystem.write", "C:/x") is False

def test_permissions_match_operation_and_resource():
    policy = PermissionPolicy({"default": "deny", "rules": [{"operation": "filesystem.read", "resource": "workspace/*", "effect": "allow"}]})
    assert policy.allows("filesystem.read", "workspace/file.txt") is True
    assert policy.allows("filesystem.write", "workspace/file.txt") is False
    assert policy.allows("filesystem.read", "other/file.txt") is False

def test_deny_rule_overrides_default_allow_for_matching_rule():
    policy = PermissionPolicy({"default": "allow", "rules": [{"operation": "terminal.*", "resource": "*", "effect": "deny"}]})
    assert policy.allows("terminal.execute", "*") is False
    assert policy.allows("filesystem.read", "*") is True
