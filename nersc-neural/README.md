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
* **Source Code:** `~/repos/python_envs/nersc-neural`
* **Environment:** `/pscratch/sd/b/bpb/python_envs/nersc-neural`
* **HF Cache:** `/pscratch/sd/b/bpb/python_envs/.hf_cache` (Shared across NERSC envs)
* **Secrets:** `/global/u2/b/bpb/secrets/nersc_hugging_face_token.txt` (Safe in Home)

## 🚀 Installation

Since NERSC uses modules, we use a build script to construct the environment on Scratch.

1.  **Login to Perlmutter:**
    ```bash
    ssh perlmutter.nersc.gov
    ```

2.  **Navigate to this repo:**
    ```bash
    cd ~/repos/python_envs/nersc-neural
    ```

3.  **Run the Build Script:**
    This loads the NERSC modules, creates the environment in scratch, and installs PyTorch (CUDA 12.1).
    ```bash
    bash build_env.sh
    ```

4.  **Register the Jupyter Kernel (Optional):**
    If you want to use this in NERSC Jupyter notebooks with secrets auto-loaded:
    ```bash
    bash activate_env.sh
    python register_kernel_advanced.py
    ```

## ⚡️ Verification & Testing (Fast Queues)

Do not submit to the `regular` queue for debugging. Use these methods to get instant access to GPU nodes.

### Pre-fetch Models (Login Node):
CRITICAL: Compute nodes do not have internet access. Run the test script on the login node first to download models to the cache.

```bash
source activate_env.sh
python test_specter.py
# Verify that models downloaded successfully (ignore "No GPU" warnings)
```

### Option A: Interactive Session (Instant Shell)
Use `salloc` to get a shell on a compute node immediately. This is best for exploring code or running `ipython`.

```bash
# Request 1 GPU node for 30 minutes in the "interactive" QOS
# Replace 'm1234' with your NERSC repo name (add '_g' if required for GPUs)
salloc -N 1 -C gpu -q interactive -t 30 -G 4 -A m2650_g

# Once the prompt returns (you are now on a compute node):
source activate_env.sh
python verify_nersc.py
python test_specter.py
exit # checking out
```

Option B: Debug Queue (Short Batch Job)
Use the debug QOS for testing submission scripts. It has a higher priority but a strictly enforced 30-minute limit.

1. Create a test script debug_test.slurm:

```bash
#!/bin/bash
#SBATCH -J neural-debug
#SBATCH -C gpu
#SBATCH -q debug
#SBATCH -t 00:10:00
#SBATCH -N 1
#SBATCH --gpus-per-node=4
#SBATCH -A m1234_g  # <--- REMEMBER YOUR ACCOUNT

source activate_env.sh
python verify_nersc.py
```

2. Submit it:

```bash
sbatch debug_test.slurm
```

3. Watch it run:

```bash
sq  # NERSC shortcut for 'squeue -u $USER'
cat neural-debug-*.out
```

Option C: Jupyter (Interactive Notebook)
Login to jupyter.nersc.gov.
Server Options: Select "GPU Shared" (Starts faster than Exclusive).
Create a new notebook.
Select Kernel: NERSC Neural (Scratch + Secrets).

Run:

```python
import torch
print(torch.cuda.is_available())
```

## 💻 Interactive Usage

To jump into the environment from a login node or interactive session, simply source the helper script. It handles modules, activation, and secrets automatically.

```bash
source activate_env.sh
````

## 💻 Slurm Batch Usage

Use `activate_env.sh` to simplify your submission scripts.

```bash
#!/bin/bash
#SBATCH -J neural-train
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -t 1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=4

# 1. Activate Environment (Modules + Conda + Secrets)
source ~/repos/python_envs/nersc-neural/activate_env.sh

# 2. Run Code
# (Example: Distributed training on 4 GPUs)
srun python train_script.py
```

## 🌐 Multi-GPU Note

Perlmutter GPU nodes have 4x A100 GPUs. The environment includes `torch` with CUDA support.

  * **Check visibility:** Run `python -c "import torch; print(torch.cuda.device_count())"` (Should output `4` on a GPU node).


