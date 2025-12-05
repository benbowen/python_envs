import os
import torch
from transformers import AutoTokenizer
from adapters import AutoAdapterModel
def test_specter():
    print(f"==================================================")
    print(f"🧪 NERSC Specter & Cache Test")
    print(f"==================================================")

    # 1. Verify Cache Location (Critical for NERSC)
    # We want to ensure models are landing in SCRATCH, not HOME
    hf_home = os.environ.get("HF_HOME")
    print(f"📂 HF_HOME: {hf_home}")
    if not hf_home or "pscratch" not in hf_home:
        print("⚠️  WARNING: HF_HOME is not set to a scratch directory!")
        print("   You risk hitting your HOME quota. Check activate_env.sh.")
    else:
        print("✅ Cache location looks correct (Scratch).")

    # 2. Check GPU Availability
    if torch.cuda.is_available():
        device = "cuda"
        gpu_name = torch.cuda.get_device_name(0)
        print(f"✅ GPU Detected: {gpu_name}")
    else:
        print("❌ No GPU detected! This script should be run on a GPU node.")
        return

    # 3. Download & Load Specter 2.0
    print("\n⬇️  Downloading/Loading Model (AllenAI Specter 2.0)...")
    try:
        # Load Base Model
        model_id = "allenai/specter2_base"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoAdapterModel.from_pretrained(model_id)
        
        # Load Adapter (This enables the embedding capability)
        # requires 'adapters' library installed via pip
        model.load_adapter("allenai/specter2", source="hf", load_as="specter2", set_active=True)
        
        model.to(device)
        print("✅ Model loaded and moved to GPU.")
    except Exception as e:
        print(f"❌ Model Load Failed: {e}")
        print("   (Did you source activate_env.sh to load the HF token?)")
        return

    # 4. Run Inference
    print("\n🧠 Running Encoding Test...")
    papers = [
        {'title': 'BERT', 'abstract': 'We introduce a new language representation model called BERT'},
        {'title': 'Attention is all you need', 'abstract': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks'}
    ]

    # Prepare inputs: Title + Sep + Abstract
    text_batch = [d['title'] + tokenizer.sep_token + (d.get('abstract') or '') for d in papers]

    inputs = tokenizer(
        text_batch, 
        padding=True, 
        truncation=True, 
        return_tensors="pt", 
        max_length=512
    ).to(device)

    with torch.no_grad():
        output = model(**inputs)
        # Take the first token (CLS token) as the embedding
        embeddings = output.last_hidden_state[:, 0, :]

    print(f"✅ Encoding Successful!")
    print(f"   Input Batch Size: {len(text_batch)}")
    print(f"   Output Embedding Shape: {embeddings.shape} (Expected: [2, 768])")
    print(f"   Device Used: {embeddings.device}")

    print("\n==================================================")
    print("🎉 Test Complete. Your environment is ready for science.")
    print("==================================================")

if __name__ == "__main__":
    test_specter()
