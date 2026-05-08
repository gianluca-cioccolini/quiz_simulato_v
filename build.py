#!/usr/bin/env python3
"""
Script di build – genera l'eseguibile con PyInstaller.

Uso:
    python build.py

Produce:
    dist/QuizSimulator          (Linux)
    dist/QuizSimulator.exe      (Windows, se eseguito su Windows)
"""

import subprocess
import sys
import os

APP_NAME = "QuizSimulator"
MAIN     = "quiz_app.py"

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",          # nessuna console su Windows
    "--name", APP_NAME,
    "--clean",
    MAIN,
]

print("=" * 60)
print(f"  Build: {APP_NAME}")
print("=" * 60)

result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))

if result.returncode == 0:
    print("\n✅  Build completata!")
    print(f"   Eseguibile nella cartella: dist/")
else:
    print("\n❌  Build fallita. Controlla l'output sopra.")
    sys.exit(1)
