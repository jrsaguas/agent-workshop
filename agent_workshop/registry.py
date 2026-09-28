from pathlib import Path
import yaml
from .models import AgentDefinition

class AgentRegistry:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def load(self, path):
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        agent = data.get("agent") or {}
        required = ["id", "name", "version", "model", "instructions"]
        missing = [key for key in required if key not in agent]
        if missing:
            raise ValueError("Missing required fields: " + ", ".join(missing))
        return AgentDefinition(**agent)

    def list(self):
        return [self.load(path) for path in sorted(self.root.glob("*.agent.yaml"))]

    def get(self, identifier):
        for agent in self.list():
            if agent.id == identifier:
                return agent
        return None
