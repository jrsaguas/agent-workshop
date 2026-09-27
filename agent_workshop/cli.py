import argparse
from pathlib import Path
from .registry import AgentRegistry
from .resource_registries import ModelRegistry, ToolRegistry, MCPRegistry

def main():
    parser = argparse.ArgumentParser(prog="agent-workshop")
    sub = parser.add_subparsers(dest="command", required=True)
    ls = sub.add_parser("agents")
    ls.add_argument("--path", default="agents")
    for name in ("models", "tools", "mcp"):
        p = sub.add_parser(name)
        p.add_argument("--path", default=name)
    args = parser.parse_args()
    if args.command == "agents":
        for agent in AgentRegistry(Path(args.path)).list():
            print(f"{agent.id}\t{agent.version}\t{agent.name}")
    elif args.command == "models":
        for item in ModelRegistry(Path(args.path)).list():
            print(f"{item.id}\t{item.provider}\t{item.model}")
    elif args.command == "tools":
        for item in ToolRegistry(Path(args.path)).list():
            print(f"{item.id}\t{item.kind}\t{item.name}")
    elif args.command == "mcp":
        for item in MCPRegistry(Path(args.path)).list():
            print(f"{item.id}\t{item.transport}\t{item.name}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
