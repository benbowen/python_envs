#!/bin/bash

SECRET_FILE="/global/u2/b/bpb/secrets/nersc_hugging_face_token.txt"

# 1. Load Secrets
if [ -f "$SECRET_FILE" ]; then
    export HF_TOKEN=$(cat "$SECRET_FILE" | xargs)
    export HUGGINGFACE_HUB_TOKEN="$HF_TOKEN"
    echo "✅ Secrets loaded."
else
    echo "⚠️  Warning: Token file not found at $SECRET_FILE"
fi

# 2. Set Cache to Scratch (Crucial for NERSC!)
export HF_HOME="/pscratch/sd/b/bpb/python_envs/.hf_cache"
echo "✅ HF Cache set to: $HF_HOME"
