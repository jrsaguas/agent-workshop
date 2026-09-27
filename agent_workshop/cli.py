import argparse
from pathlib import Path
from .registry import AgentRegistry
def main():
    parser = argparse.ArgumentParser(prog="agent-workshop")
    sub = parser.add_subparsers(dest="command", required=True)
    ls = sub.add_parser("agents")
    ls.add_argument("--path", default="agents")
    args = parser.parse_args()
    if args.command == "agents":
        for agent in AgentRegistry(Path(args.path)).list():
            print(f"{agent.id}\t{agent.version}\t{agent.name}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
