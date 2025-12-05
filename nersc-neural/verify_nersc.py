import torch
import os
import sys

print(f"--- NERSC Environment Check: {os.environ.get('CONDA_DEFAULT_ENV', 'Unknown')} ---")

# 1. Check CUDA & GPUs
if torch.cuda.is_available():
    device_count = torch.cuda.device_count()
    print(f"✅ CUDA Available: Yes (Version {torch.version.cuda})")
    print(f"✅ GPU Count: {device_count} (Expected: 4 on Perlmutter GPU nodes)")
    
    # 2. Test Multi-GPU Visibility
    print("\n--- GPU Diagnostics ---")
    for i in range(device_count):
        props = torch.cuda.get_device_properties(i)
        print(f"   GPU {i}: {props.name} ({props.total_memory / 1e9:.2f} GB VRAM)")
    
    # 3. Simple Tensor Operation on GPU 0
    try:
        x = torch.ones(5, device="cuda:0")
        print(f"\n✅ Tensor Test: Created tensor on {x.device}")
    except Exception as e:
        print(f"❌ Tensor Test Failed: {e}")

else:
    print("❌ CUDA Not Available! (Are you on a CPU node?)")

# 4. Check Secrets
token = os.environ.get("HF_TOKEN")
if token:
    print(f"\n✅ Secrets Loaded: HF_TOKEN is set ({token[:4]}...)")
else:
    print("\n❌ Secrets Missing: HF_TOKEN is not set.")

print("------------------------------------------------")
