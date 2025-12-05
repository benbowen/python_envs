# NERSC Neural Environment (Perlmutter)

**⚠️ FILESYSTEM WARNING: PURGE POLICY** This environment is installed on `$SCRATCH` (`/pscratch/sd/b/bpb/python_envs`).  
Files on scratch not accessed for **8 weeks** are **permanently deleted**.  
*You must touch or use this environment regularly, or it will vanish.*

---

## ⚡️ Overview
This environment is designed for **Perlmutter GPU (A100)** and **CPU (Milan)** nodes.
* **Architecture:** Linux x86_64
* **Acceleration:** CUDA 12.x (NVIDIA A100)
* **Manager:** Standard Conda (via `module load python`)

## 📂 Locations
* **Environment:** `/pscratch/sd/b/bpb/python_envs/nersc-neural`
* **HF Cache:** `/pscratch/sd/b/bpb/python_envs/.hf_cache` (Shared across NERSC envs)
* **Secrets:** `/global/u2/b/bpb/secrets/nersc_hugging_face_token.txt` (Safe in Home)

## 🚀 Installation
Since NERSC uses modules, we use a build script instead of Pixi.

1.  **Login to Perlmutter:**
    ```bash
    ssh perlmutter.nersc.gov
    ```

2.  **Navigate to this repo:**
    ```bash
    cd ~/repos/python_envs/nersc-neural
    ```

3.  **Run the Build Script:**
    This will load the NERSC python module, create the env in scratch, and install PyTorch.
    ```bash
    bash build_env.sh
    ```

## 💻 Usage (Jupyter)
1.  Go to [https://jupyter.nersc.gov](https://jupyter.nersc.gov)
2.  Start a server (CPU or GPU Shared).
3.  Select Kernel: **`NERSC Neural (Scratch)`**

## 💻 Usage (Slurm Batch Scripts)
To use this in a batch job (`sbatch`), you must load the environment manually:

```bash
#!/bin/bash
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -t 1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1

# 1. Load NERSC Python
module load python

# 2. Activate your scratch environment
source activate /pscratch/sd/b/bpb/python_envs/nersc-neural

# 3. Inject Secrets (Critical!)
source load_secrets.sh

# 4. Run Code
srun python my_training_script.py
