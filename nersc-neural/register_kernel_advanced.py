import os
import json
import sys
from pathlib import Path

# --- Configuration ---
ENV_NAME = "nersc-neural"
DISPLAY_NAME = "NERSC Neural (Scratch + Secrets)"
ENV_PATH = "/pscratch/sd/b/bpb/python_envs/nersc-neural"
PYTHON_EXE = os.path.join(ENV_PATH, "bin", "python")
SECRETS_SCRIPT = os.path.join(os.getcwd(), "load_secrets.sh")

def install_kernel():
    # Standard NERSC Kernel Location
    kernel_dir = Path.home() / ".local/share/jupyter/kernels" / ENV_NAME
    kernel_dir.mkdir(parents=True, exist_ok=True)

    # Wrapper script to load secrets THEN python
    wrapper_script_path = kernel_dir / "kernel_wrapper.sh"
    with open(wrapper_script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"source {SECRETS_SCRIPT}\n") # Load tokens
        f.write(f"exec {PYTHON_EXE} \"$@\"\n") # Run Python
    
    os.chmod(wrapper_script_path, 0o755)

    # The Kernel Spec
    kernel_spec = {
        "argv": [
            str(wrapper_script_path),
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}"
        ],
        "display_name": DISPLAY_NAME,
        "language": "python"
    }

    with open(kernel_dir / "kernel.json", "w") as f:
        json.dump(kernel_spec, f, indent=2)

    print(f"✅ Kernel Registered: {kernel_dir}")

if __name__ == "__main__":
    install_kernel()
