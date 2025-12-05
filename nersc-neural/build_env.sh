#!/bin/bash
set -e  # Exit on error

# --- Configuration ---
ENV_NAME="nersc-neural"
INSTALL_BASE="/pscratch/sd/b/bpb/python_envs"
ENV_PATH="$INSTALL_BASE/$ENV_NAME"
CACHE_DIR="$INSTALL_BASE/.hf_cache"

echo "================================================="
echo "🏗  Building NERSC Environment: $ENV_NAME"
echo "📍 Location: $ENV_PATH"
echo "================================================="

# 1. Load NERSC Base Modules
echo "-> Loading module python..."
module load python

# 2. Setup Directories
mkdir -p "$INSTALL_BASE"
mkdir -p "$CACHE_DIR"

# 3. Create Conda Environment
if [ -d "$ENV_PATH" ]; then
    echo "⚠️  Environment exists. Updating..."
else
    echo "-> Creating fresh conda environment..."
    # We use basic python 3.10 as a stable base for PyTorch 2.x
    conda create -y --prefix "$ENV_PATH" python=3.10 pip
fi

# 4. Activate
echo "-> Activating environment..."
source activate "$ENV_PATH"

# 5. Install PyTorch (CUDA 12.1 for A100s)
# Note: We use pip inside conda to get the specific CUDA wheels efficiently
echo "-> Installing PyTorch (CUDA 12.1)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 6. Install Hugging Face & Science Stack
echo "-> Installing HF Transformers & Science tools..."
pip install transformers \
            datasets \
            accelerate \
            huggingface_hub \
            scikit-learn \
            pandas \
            numpy \
            scipy \
            adapters \
	    tqdm \
            ipykernel \
            faiss-gpu   # NERSC has GPUs, so we use the GPU version if possible

# 7. Register Kernel for Jupyter
echo "-> Registering Jupyter Kernel..."
python -m ipykernel install --user --name "$ENV_NAME" --display-name "NERSC Neural (Scratch)"

# 8. Create Activation Helper (Optional but handy)
echo "-> Creating 'load_secrets.sh' helper..."
cat <<EOF > load_secrets.sh
#!/bin/bash
SECRET_FILE="/global/u2/b/bpb/secrets/nersc_hugging_face_token.txt"

# 1. Load Secrets
if [ -f "\$SECRET_FILE" ]; then
    export HF_TOKEN=\$(cat "\$SECRET_FILE" | xargs)
    export HUGGINGFACE_HUB_TOKEN="\$HF_TOKEN"
    echo "✅ Secrets loaded."
else
    echo "⚠️  Warning: Token file not found at \$SECRET_FILE"
fi

# 2. Set Cache to Scratch (Crucial for NERSC!)
export HF_HOME="$CACHE_DIR"
echo "✅ HF Cache set to: \$HF_HOME"
EOF

chmod +x load_secrets.sh

echo "================================================="
echo "✅ Build Complete!"
echo "To use via CLI: source activate $ENV_PATH && source load_secrets.sh"
echo "To use via Jupyter: Select 'NERSC Neural (Scratch)' kernel."
echo "================================================="
