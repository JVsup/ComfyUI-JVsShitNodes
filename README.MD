# ComfyUI Shit Nodes - by AI, for AI

A collection of ai-slop utility nodes for ComfyUI, including workflow timing, setting extraction, universal name handling, model merging and other.

_Use at your own peril_

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

<img width="473" height="252" alt="{707D668A-0103-4D9D-B234-05D0CA645C6A}" src="https://github.com/user-attachments/assets/1697e35c-3363-4819-b095-8c0e49360302" />

**How to use:**
1. Download all model shards (e.g., `model-00001-of-00003.safetensors`) and the `model.safetensors.index.json` file into a folder.
2. **Source Dir**: Path to the folder containing the shards.
3. **Index Filename**: Usually `model.safetensors.index.json`.
4. **Dest Dir**: Where you want the final model saved.
5. **Output Filename**: Name of the resulting single file.

---

## ♾️ Universal Name Extractor
A smart node that extracts filenames or names from **any** connected node (Models, Loras, Checkpoints, Primitives, etc.) regardless of the input type.

<img width="686" height="225" alt="{17CCC2DE-25D9-490B-8F20-CDADA8C72194}" src="https://github.com/user-attachments/assets/4f824aef-9e96-4a6c-bf79-6280e4bf3461" />

### Features
- **Infinite Inputs:** Starts with one input, but automatically adds a new slot whenever you connect something.
- **Widget Aware:** Inspects the **previous node's settings** to find the actual filename (e.g., `v1-5-pruned.ckpt`) even if the model object passed down the link doesn't carry that name explicitly.
- **Universal Output:** Returns a clean list of names and a concatenated string.

---

## 📝 SettingsToText
Extracts basic settings from your workflow into a text string.
*Note: This node attempts to traverse the graph to find values. It may not work perfectly with complex subgraphed nodes.*

<img width="1465" height="888" alt="obrazek" src="https://github.com/user-attachments/assets/d9bdaa24-cd0c-4e7e-9b0f-7ffbf5255469" />

---

## ⏱️ Workflow Timer
A simple node that logs the execution time of your generation.
- Connect it to the end of your workflow.
- Prints the "Finished at" time and completion status to the console in green text.

<img width="212" height="126" alt="{6AEE0563-9CB7-4504-AD39-114B1C379854}" src="https://github.com/user-attachments/assets/eb60f4d4-c70c-424a-9e4e-b97eebb92eec" /><img width="664" height="150" alt="{6FBFC951-DD19-442F-A16C-E0BDE400E282}" src="https://github.com/user-attachments/assets/bce976c4-3354-4e4d-8c72-d77d963366e7" />

---

## 📊 System Monitor Overlay
A real-time overlay that appears in the bottom-right corner of your ComfyUI window.
* **Swap Memory:** Monitors usage to help detect when you are running out of VRAM/RAM and spilling to disk.
* **Disk Write:** Monitors write speed to visualize model saving or heavy paging operations.
* *No node required:* This is an automatic extension.

<img width="339" height="212" alt="{1AA20BCF-5B5A-4C5E-8F58-C76FB7708DE6}" src="https://github.com/user-attachments/assets/9349ef40-82d4-41b3-bd22-e100ee14c2c5" />

---

## 🧹 Tag Deduplicator
Efficiently cleans comma-separated strings by removing duplicates while intelligently prioritizing weighted tags over plain text. It ensures that a weighted entry like `(tag:1.5)` automatically replaces a standard `tag`, preserving your intended emphasis while keeping the prompt organized.

<img width="704" height="735" alt="{5B06E5E0-DBFF-42C7-824B-534A91668C76}" src="https://github.com/user-attachments/assets/5e2a0a9f-8843-46bf-8736-939b89a53cd6" />

---

## License

MIT



