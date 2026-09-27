from pathlib import Path
from .resource_models import ModelDefinition, ToolDefinition, MCPServerDefinition
from .resource_registry import ResourceRegistry

def _model(data): return ModelDefinition(id=data["id"], name=data["name"], provider=data["provider"], model=data["model"], kind=data.get("kind","chat"), capabilities=tuple(data.get("capabilities", [])), context_window=data.get("context_window"), config=data.get("config", {}))
def _tool(data): return ToolDefinition(id=data["id"], name=data["name"], kind=data["kind"], description=data.get("description",""), capabilities=tuple(data.get("capabilities", [])), input_schema=data.get("input_schema", {}), permission=data.get("permission"))
def _mcp(data): return MCPServerDefinition(id=data["id"], name=data["name"], transport=data["transport"], command=data.get("command"), args=tuple(data.get("args", [])), url=data.get("url"), env=data.get("env", {}), tools=tuple(data.get("tools", [])))

class ModelRegistry(ResourceRegistry[ModelDefinition]):
    def __init__(self, root: Path = Path("models")): super().__init__(root, _model, "model")
class ToolRegistry(ResourceRegistry[ToolDefinition]):
    def __init__(self, root: Path = Path("tools")): super().__init__(root, _tool, "tool")
class MCPRegistry(ResourceRegistry[MCPServerDefinition]):
    def __init__(self, root: Path = Path("mcp")): super().__init__(root, _mcp, "mcp")
