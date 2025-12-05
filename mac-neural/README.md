# mac-neural: Apple Silicon AI Environment

**⚠️ ARCHITECTURE WARNING: NOT FOR LINUX/NVIDIA** This environment is specifically optimized for **macOS (Apple Silicon M1/M2/M3)**.  
It uses **MPS (Metal Performance Shaders)** for GPU acceleration and **NEON-optimized** CPU libraries.  
*Do not try to install this on a standard Linux/CUDA supercomputing node.*

---

## ⚡️ Overview

This project provides a reproducible, high-performance Python environment for running deep learning models locally on a Mac. It replaces standard Conda/Pip workflows with **Pixi** for lock-file precision and speed.

**Key Capabilities:**
* **Vector Search:** `faiss-cpu` (Optimized for Arm64/NEON instructions)
* **Deep Learning:** `pytorch` (Accelerated via Metal/MPS)
* **NLP:** `transformers` & `adapters` (Specter 2.0 compatible)
* **Security:** Automatic injection of Hugging Face tokens via activation scripts (no hardcoded secrets).

## 🛠 Prerequisites

1.  **Mac with Apple Silicon** (M1/M2/M3/Pro/Max/Ultra).
2.  **VS Code** (Recommended for Notebooks).
3.  **Pixi Package Manager**:
    ```bash
    curl -fsSL [https://pixi.sh/install.sh](https://pixi.sh/install.sh) | bash
    source ~/.bash_profile  # Or restart your terminal
    ```

## 🚀 Installation & Build

1.  **Navigate to the environment directory:**
    ```bash
    cd /Users/bpb/conda_envs/mac-neural
    ```

2.  **Build the Environment:**
    Pixi will read `pixi.toml`, solve dependencies, and install all binary packages from `conda-forge`.
    ```bash
    pixi install
    ```

3.  **Configure Secrets (Crucial Step):**
    This environment requires a Hugging Face token to download gated models (like Llama or Specter).  
    *Note: For security, the actual token is NOT stored in this repo.*
    
    Create a file named `load_secrets.sh` in the root of this folder:
    ```bash
    touch load_secrets.sh
    chmod +x load_secrets.sh
    ```
    
    Edit the file to point to your local secret storage.  
    **Do not commit your token here.** Point to a file outside the repo:
    
    ```bash
    #!/bin/sh
    # Point this to wherever you keep your secrets locally
    SECRET_FILE="/Users/YOUR_USER/secrets/hf_token.txt"

    if [ -f "$SECRET_FILE" ]; then
        # Reads the token and removes whitespace
        export HF_TOKEN=$(cat "$SECRET_FILE" | xargs)
        # Sets legacy variable for older libraries
        export HUGGINGFACE_HUB_TOKEN="$HF_TOKEN"
    else
        echo "⚠️ Warning: Token file not found at $SECRET_FILE"
    fi
    ```

## ✅ Verification

Run the included stress test to verify that Faiss, PyTorch-MPS, and your Secrets are working correctly:

```bash
pixi run python verify_env.py
````

**Expected Output:**

  * ✅ HF Token Detected
  * ✅ Mac GPU (MPS) Available
  * ✅ Faiss Version: ... (Index created successfully)
  * ✅ Adapters & Transformers are compatible

## 💻 VS Code & Jupyter Setup

**IMPORTANT:** Do not simply select the Python interpreter in VS Code. We must use a **Custom Kernel** to ensure the secrets script (`load_secrets.sh`) runs before the notebook starts.

1.  **Register the Custom Kernel:**
    Run this script once to generate a specific kernel spec for VS Code:

    ```bash
    pixi run python register_kernel.py
    ```

2.  **Using it in VS Code:**

      * Open a `.ipynb` file.
      * Click **"Select Kernel"** (top right corner).
      * Choose: **`Mac Neural (Pixi Activated)`**.
      * *If you don't see it, reload the VS Code window (`Cmd+Shift+P` \> `Reload Window`).*

## 📂 Directory Structure

```text
mac-neural/
├── pixi.toml            # The Single Source of Truth (Dependencies)
├── pixi.lock            # Exact binary hashes (Auto-generated)
├── load_secrets.sh      # Secrets injector (Ignored by Git)
├── register_kernel.py   # Script to register VS Code kernel
├── verify_env.py        # Smoke test script
├── .pixi/               # The actual environment (Ignored by Git)
└── .hf_cache/           # Local model cache (Ignored by Git)
```

## 🐛 Troubleshooting

  * **`IProgress not found` in Jupyter:**

      * Ensure you are using the **"Mac Neural (Pixi Activated)"** kernel, not the raw Python path.
      * If persistent, run `pixi install` to ensure `jupyterlab_widgets` is synced.

  * **`Library not loaded: libjpeg`:**

      * Run `pixi install`. We explicitly use `libjpeg-turbo` from `conda-forge` to prevent conflicts with `torchvision`.

  * **Hugging Face Authentication Errors:**

      * Check that `load_secrets.sh` is executable (`chmod +x load_secrets.sh`).
      * Ensure your text file path in that script is correct and contains *only* the token string.


