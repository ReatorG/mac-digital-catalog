"""
Usage:
    python rundev.py
"""

import uvicorn
import os
import sys
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    app_path = "src.app.main:app"

    if len(sys.argv) > 1:
        app_path = sys.argv[1]

    print(f"Starting development server for: {app_path}")

    uvicorn.run(
        app_path,
        host="127.0.0.1",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
