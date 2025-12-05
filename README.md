# 🧪 Research Python Environments

This repository acts as the central catalog for my research computing environments. 

It contains the "recipes" (configuration files, lockfiles, and setup scripts) required to reproduce my work across different hardware architectures and domains.

## 🧭 The Organization Logic

Because scientific computing requires specific hardware optimizations, I do not use a "one size fits all" environment. Instead, environments are matrixed by **Domain** and **Infrastructure**.

### 1. By Infrastructure (The "Where")
* **🍎 Mac (Local):** Optimized for **Apple Silicon (Arm64)**. Uses Metal (MPS) for acceleration and NEON for CPU vectorization. 
    * *Manager:* `pixi` (Native)
* **⚡️ NERSC (HPC):** Optimized for **Perlmutter (Linux x86_64)**. Uses CUDA 11/12, MPI, and Shifter containers. Strict storage quotas.
    * *Manager:* `conda` / `mamba` (Module based)
* **☁️ RunPod (Cloud):** Optimized for **NVIDIA A100/H100 (Linux x86_64)**. Ephemeral instances for heavy LLM fine-tuning.
    * *Manager:* `docker` / `pixi`

### 2. By Domain (The "What")
* **Neural/AI:** Deep learning, Embeddings (Specter), LLMs.
* **Metabolomics:** Mass spec analysis (`metatlas`, `ms-buddy`), legacy Python requirements.
* **Stats:** Pure number crunching, R/Python hybrids, rigorous statistical modeling.

---

## 📂 Environment Catalog

### 🍎 Local (Mac Laptop)
| Environment | Path | Description | Status |
| :--- | :--- | :--- | :--- |
| **Mac Neural** | [`/mac-neural`](./mac-neural) | **Inference & Vector Math.**<br>PyTorch (MPS), Faiss (CPU), Transformers.<br>*Use for: Prototyping, Embeddings, Paper figures.* | ✅ Active |
| **Mac Metabo** | *TBD* | **Mass Spec Analysis.**<br>Legacy Python 3.9, MetAtlas, Blink.<br>*Use for: Local data inspection.* | 🚧 Planned |

### ⚡️ NERSC (Supercomputer)
| Environment | Path | Description | Status |
| :--- | :--- | :--- | :--- |
| **NERSC Prod** | *TBD* | **High-Throughput Computing.**<br>Conda-based, CUDA-optimized for A100 nodes.<br>*Use for: Large-scale dataset processing.* | 🚧 Planned |

### ☁️ Cloud (RunPod/AWS)
| Environment | Path | Description | Status |
| :--- | :--- | :--- | :--- |
| **Cloud Train** | *TBD* | **LLM Fine-Tuning.**<br>Flash Attention 2, Deepspeed, Axolotl.<br>*Use for: Training models too big for Mac.* | 🚧 Planned |

---

## 🛡 Security Policy

**CRITICAL:** No secrets (API Keys, HF Tokens, NERSC passwords) are ever committed to this repository.

* **Local:** Secrets are injected via `load_secrets.sh` (ignored by git) from a secure local directory.
* **HPC/Cloud:** Secrets are managed via environment variables (`.bashrc`) or secret managers.

## ⚡️ Quick Usage Guide (Local)

To spin up a local environment (e.g., `mac-neural`):

1.  **Navigate to the directory:**
    ```bash
    cd mac-neural
    ```
2.  **Activate (via Pixi):**
    ```bash
    pixi shell
    ```
3.  **Use in VS Code:**
    * Do not select the raw Python path.
    * Select the **Custom Kernel** (e.g., "Mac Neural (Pixi Activated)") to ensure secrets are loaded.

---

## 📝 Maintenance Notes

* **Updating Lockfiles:** Run `pixi update` inside the specific folder.
* **Adding Dependencies:** Run `pixi add <package>` inside the specific folder.
* **Cleaning:** Run `pixi clean` to remove local artifacts (does not delete config).