import os
import json
import sys
from pathlib import Path

# --- Configuration ---
KERNEL_NAME = "mac-neural-activated"
DISPLAY_NAME = "Mac Neural (Pixi Activated)"
# Path to your pixi executable (usually ~/.pixi/bin/pixi)
PIXI_PATH = os.path.expanduser("~/.pixi/bin/pixi")
# Path to your project
PROJECT_DIR = os.getcwd()

def install_kernel():
    # 1. Determine where to save the kernel spec (standard Jupyter location on Mac)
    kernel_dir = Path.home() / "Library/Jupyter/kernels" / KERNEL_NAME
    kernel_dir.mkdir(parents=True, exist_ok=True)

    # 2. Create the kernel.json
    # This acts as a wrapper: VS Code calls Pixi -> Pixi loads secrets -> Pixi calls Python
    kernel_spec = {
        "argv": [
            PIXI_PATH,
            "run",
            "--manifest-path",
            str(Path(PROJECT_DIR) / "pixi.toml"),
            "python",
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}"
        ],
        "display_name": DISPLAY_NAME,
        "language": "python",
        "env": {}  # Pixi handles the env vars, so we leave this empty
    }

    # 3. Write file
    with open(kernel_dir / "kernel.json", "w") as f:
        json.dump(kernel_spec, f, indent=2)

    print(f"✅ Success! Kernel registered at: {kernel_dir}")
    print(f"   Name: {DISPLAY_NAME}")
    print("\n👉 Restart VS Code, open a notebook, and select this new kernel!")

if __name__ == "__main__":
    if not os.path.exists(PIXI_PATH):
        print(f"❌ Error: Pixi not found at {PIXI_PATH}. Run 'which pixi' to find it.")
    else:
        install_kernel()
