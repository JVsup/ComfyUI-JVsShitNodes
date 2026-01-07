import os
import json
import torch
from safetensors.torch import load_file, save_file
import comfy.utils

class SafetensorsMerger:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source_dir": ("STRING", {"default": "C:\\models\\source", "multiline": False}),
                "index_filename": ("STRING", {"default": "model.safetensors.index.json", "multiline": False}),
                "dest_dir": ("STRING", {"default": "C:\\models\\output", "multiline": False}),
                "output_filename": ("STRING", {"default": "merged_model.safetensors", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "merge_safetensors"
    OUTPUT_NODE = True
    CATEGORY = "💩 JVsShitNodes"

    def merge_safetensors(self, source_dir, index_filename, dest_dir, output_filename):
        # 1. Check and prepare paths
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
        
        if not os.path.exists(dest_dir):
            print(f"Destination directory does not exist, creating: {dest_dir}")
            os.makedirs(dest_dir, exist_ok=True)

        if not output_filename.endswith(".safetensors"):
            output_filename += ".safetensors"
            
        output_file_path = os.path.join(dest_dir, output_filename)
        
        # Use the specified index filename
        index_path = os.path.join(source_dir, index_filename)

        # 2. Load Index
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}. Check the filename and path.")

        print(f"Loading index: {index_path}")
        with open(index_path, 'r') as f:
            index = json.load(f)

        weight_map = index.get("weight_map", {})
        shard_files = set(weight_map.values())
        total_shards = len(shard_files)
        
        if total_shards == 0:
             raise ValueError("Index file contains no shard references (weight_map is empty or missing).")

        print(f"Found {total_shards} files to merge.")

        # 3. Initialize Progress Bar for ComfyUI
        # Steps = shards + 1 step for saving
        pbar = comfy.utils.ProgressBar(total_shards + 1)

        all_tensors = {}
        
        # 4. Iterate over shards and load into memory
        for i, shard_file in enumerate(sorted(shard_files)):
            shard_path = os.path.join(source_dir, shard_file)
            print(f"[{i+1}/{total_shards}] Loading {shard_file}...")
            
            if not os.path.exists(shard_path):
                 raise FileNotFoundError(f"Missing shard file: {shard_path}")

            # Load tensors
            tensors = load_file(shard_path)
            all_tensors.update(tensors)
            
            # Release reference to local variable
            del tensors
            
            # Update UI progress bar
            pbar.update(1)

        print(f"All tensors loaded. Total keys: {len(all_tensors)}")
        print(f"Saving merged model to: {output_file_path}...")
        
        # 5. Save
        save_file(all_tensors, output_file_path)
        
        # Final progress update
        pbar.update(1)

        file_size_gb = os.path.getsize(output_file_path) / (1024**3)
        result_msg = f"Done! Model saved ({file_size_gb:.2f} GB)"
        print(result_msg)

        return (output_file_path,)