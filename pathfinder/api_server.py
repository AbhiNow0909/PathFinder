"""
PathFinder API — development server entrypoint.

Usage
-----
  python api_server.py                   # hot-reload enabled (default)
  python api_server.py --no-reload       # disable hot-reload (production-like)
  python api_server.py --port 9000       # custom port
  python api_server.py --host 127.0.0.1  # localhost-only binding
"""
from __future__ import annotations

import argparse
import os
import sys

# Ensure pathfinder/ is on sys.path so all internal package imports resolve.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn  # noqa: E402  (must come after sys.path fix)


def main() -> None:
    parser = argparse.ArgumentParser(description="PathFinder API server")
    parser.add_argument("--host",      default="0.0.0.0",  help="Bind host")
    parser.add_argument("--port",      type=int, default=8000, help="Port")
    parser.add_argument("--no-reload", action="store_true", help="Disable hot-reload")
    parser.add_argument("--workers",   type=int, default=1,
                        help="Worker processes (incompatible with --reload)")
    args = parser.parse_args()

    reload = not args.no_reload
    if reload and args.workers > 1:
        print("⚠️  --reload is incompatible with multiple workers. Disabling reload.")
        reload = False

    print(f"🚀  PathFinder API  →  http://{args.host}:{args.port}")
    print(f"📖  Swagger Docs    →  http://localhost:{args.port}/docs")
    print(f"🔄  Hot-reload: {reload}")

    uvicorn.run(
        "api.app:app",
        host=args.host,
        port=args.port,
        reload=reload,
        workers=args.workers if not reload else 1,
        log_level="info",
    )


if __name__ == "__main__":
    main()
