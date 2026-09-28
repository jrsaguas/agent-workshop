from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .execution import Execution
from .execution_store import ExecutionStore
from .builtin_tools import filesystem_handlers
from .process_tools import process_tool_handlers
from .tool_executor import ToolExecutor
from .permissions import PermissionPolicy
from .providers import ProviderRegistry
from .registry import AgentRegistry
from .resource_registries import MCPRegistry, ModelRegistry, ToolRegistry


@dataclass
class ResolvedAgent:
    definition: Any
    model: Any
    tools: list[Any]
    mcp: list[Any]
    permissions: PermissionPolicy


class AgentResolver:
    def __init__(self, root: Path = Path(".")) -> None:
        self.root = root

    def resolve(self, agent_id: str) -> ResolvedAgent:
        definition = AgentRegistry(self.root / "agents").get(agent_id)
        if definition is None:
            raise KeyError(f"agent not found: {agent_id}")
        model_ref = definition.model.get("id") or definition.model.get("model")
        model = ModelRegistry(self.root / "models").get(model_ref)
        if model is None:
            raise KeyError(f"model not found: {model_ref}")
        tools = []
        for ref in definition.tools:
            tool = ToolRegistry(self.root / "tools").get(ref)
            if tool is None:
                raise KeyError(f"tool not found: {ref}")
            tools.append(tool)
        mcps = []
        for ref in definition.mcp:
            server = MCPRegistry(self.root / "mcp").get(ref)
            if server is None:
                raise KeyError(f"mcp server not found: {ref}")
            mcps.append(server)
        return ResolvedAgent(definition, model, tools, mcps, PermissionPolicy(definition.permissions))


class AgentRuntime:
    def __init__(self, root: Path = Path("."), providers: ProviderRegistry | None = None, execution_store: ExecutionStore | None = None):
        self.root = root
        self.resolver = AgentResolver(root)
        self.providers = providers or ProviderRegistry()
        self.execution_store = execution_store or ExecutionStore(root / "executions")
        handlers = {}
        handlers.update(filesystem_handlers(root))
        handlers.update(process_tool_handlers(root))
        self.tool_executor = ToolExecutor(handlers)

    def _persist(self, execution: Execution) -> None:
        self.execution_store.save(execution)

    def prepare(self, agent_id: str) -> Execution:
        resolved = self.resolver.resolve(agent_id)
        execution = Execution(agent_id)
        execution.start()
        execution.record("agent.resolved", model=resolved.model.id, tools=[t.id for t in resolved.tools], mcp=[m.id for m in resolved.mcp])
        execution.record("permissions.loaded", default=resolved.permissions.default)
        self._persist(execution)
        return execution

    def authorize(self, execution: Execution, agent_id: str, operation: str, resource: str = "*") -> bool:
        resolved = self.resolver.resolve(agent_id)
        allowed = resolved.permissions.allows(operation, resource)
        execution.record("permission.checked", operation=operation, resource=resource, allowed=allowed)
        self._persist(execution)
        return allowed

    def generate(self, agent_id: str, prompt: str, **options: Any) -> tuple[Execution, str]:
        resolved = self.resolver.resolve(agent_id)
        execution = self.prepare(agent_id)
        execution.record("model.requested", provider=resolved.model.provider, model=resolved.model.model)
        self._persist(execution)
        try:
            provider = self.providers.get(resolved.model.provider)
            response = provider.generate(resolved.model.model, prompt, **options)
            execution.record("model.completed")
            execution.complete()
            self._persist(execution)
            return execution, response
        except Exception as exc:
            execution.fail(str(exc))
            self._persist(execution)
            raise
