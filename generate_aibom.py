import json
import os
import importlib.metadata
import subprocess
import hashlib
import sys
sys.stdout.reconfigure(encoding='utf-8')

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--model-path", required=True, help="Path to the model directory")
args = parser.parse_args()

# Get local_path from environment variables (pipeline parameters)
file_path = __file__
local_path = os.path.join(os.path.dirname(file_path) , "reports")


# Use --model-path directly from CLI args
args = parser.parse_args()
model_path = args.model_path

if not model_path or not os.path.exists(model_path):
    print("❌ Error: Model path is not set or does not exist.")
    exit(1)
print(f"✅ Using model path: {model_path}")


def calculate_file_hash(file_path):
    if not os.path.exists(file_path):
        return "N/A"
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def read_requirements(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            packages = [line.strip() for line in f.readlines() if line.strip()]
        return {pkg: importlib.metadata.version(pkg) for pkg in packages if pkg in {d.metadata["Name"].lower() for d in importlib.metadata.distributions()}}
    return {}

def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def extract_model_metadata(model_file):
    return {
        "File Path": model_file,
        "Size (KB)": os.path.getsize(model_file) / 1024 if os.path.exists(model_file) else "N/A",
        "SHA-256 Hash": calculate_file_hash(model_file)
    }

def generate_aibom(input_folder, reports_folder):
    """Generate AIBOM.json inside the reports folder."""
    requirements_file = os.path.join(input_folder, "requirements.txt")
    model_info_file = os.path.join(input_folder, "model_info.json")
    dataset_file = os.path.join(input_folder, "dataset.json")
    model_file = os.path.join(input_folder, "model.py")
    aibom = {
        "Model Information": read_json(model_info_file),
        "Dataset Information": read_json(dataset_file),
        "Dependencies": read_requirements(requirements_file),
        "Model Metadata": extract_model_metadata(model_file),
    }

    aibom_file = os.path.join(reports_folder, "aibom.json")
    with open(aibom_file, "w", encoding="utf-8") as f:
        json.dump(aibom, f, indent=2)

    print(f"✅ AIBOM saved to {aibom_file}")
    return aibom_file

def main():

    if not os.path.exists(local_path):
        print(f"❌ Error: Model directory does not exist - {local_path}")
        return
    # Generate AIBOM
    generate_aibom(model_path, local_path)

if __name__ == "__main__":
     main()
