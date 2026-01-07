# ComfyUI Shit Nodes - by AI, for AI

A collection of ai-slop utility nodes for ComfyUI, including workflow timing, setting extraction, universal name handling, model merging and other.

## 📦 Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   ```
2. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💾 Safetensors Merger (Shard to Single)
A utility node to merge multi-part (sharded) Safetensors models (often found on HuggingFace) into a single `.safetensors` file directly within ComfyUI.

**How to use:**
1. Download all model shards (e.g., `model-00001-of-00003.safetensors`) and the `model.safetensors.index.json` file into a folder.
2. **Source Dir**: Path to the folder containing the shards.
3. **Index Filename**: Usually `model.safetensors.index.json`.
4. **Dest Dir**: Where you want the final model saved.
5. **Output Filename**: Name of the resulting single file.

---

## ♾️ Universal Name Extractor
A smart node that extracts filenames or names from **any** connected node (Models, Loras, Checkpoints, Primitives, etc.) regardless of the input type.

### Features
- **Infinite Inputs:** Starts with one input, but automatically adds a new slot whenever you connect something.
- **Widget Aware:** Inspects the **previous node's settings** to find the actual filename (e.g., `v1-5-pruned.ckpt`) even if the model object passed down the link doesn't carry that name explicitly.
- **Universal Output:** Returns a clean list of names and a concatenated string.

---

## 📝 SettingsToText
Extracts basic settings from your workflow into a text string.
*Note: This node attempts to traverse the graph to find values. It may not work perfectly with complex subgraphed nodes.*

<img width="800" alt="SettingsToText Example" src="[https://github.com/user-attachments/assets/d9bdaa24-cd0c-4e7e-9b0f-7ffbf5255469](https://github.com/user-attachments/assets/d9bdaa24-cd0c-4e7e-9b0f-7ffbf5255469)" />

---

## ⏱️ Workflow Timer
A simple node that logs the execution time of your generation.
- Connect it to the end of your workflow.
- Prints the "Finished at" time and completion status to the console in green text.

---

## 📊 System Monitor Overlay
A real-time overlay that appears in the bottom-right corner of your ComfyUI window.
* **Swap Memory:** Monitors usage to help detect when you are running out of VRAM/RAM and spilling to disk.
* **Disk Write:** Monitors write speed to visualize model saving or heavy paging operations.
* *No node required:* This is an automatic extension.

---

## License
MIT