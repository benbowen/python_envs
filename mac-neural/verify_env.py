import os
import torch
import faiss
import transformers
from adapters import AutoAdapterModel

print(f"--- Environment Check: {os.environ.get('CONDA_PREFIX', 'Pixi Env')} ---")

# 1. Check Hugging Face Token
token = os.environ.get("HF_TOKEN")
if token:
    print(f"✅ HF Token Detected: {token[:4]}... (Loaded from secrets)")
else:
    print(f"❌ HF Token MISSING. Check load_secrets.sh")

# 2. Check Mac GPU (MPS)
if torch.backends.mps.is_available():
    print(f"✅ Mac GPU (MPS) Available: Yes")
    # Test a small tensor move
    x = torch.ones(5, device="mps")
    print(f"   Tensor on device: {x.device}")
else:
    print(f"❌ Mac GPU Not Detected (Using CPU)")

# 3. Check Faiss (CPU Optimized for Arm64)
index = faiss.IndexFlatL2(128)
print(f"✅ Faiss Version: {faiss.__version__} (Index created successfully)")

# 4. Check Specter/Adapters Compatibility
print(f"✅ Transformers Version: {transformers.__version__}")
try:
    # Just try to load the config to prove libs are talking
    model = AutoAdapterModel.from_pretrained("allenai/specter2_base")
    print("✅ Adapters & Transformers are compatible (Model loaded)")
except Exception as e:
    print(f"❌ Version Conflict: {e}")

print("------------------------------------------------")
