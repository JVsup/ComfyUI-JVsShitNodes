from .workflow_timer import TimerEndNode
from .SettingsToText import SettingsToText
from .universal_name_node import UniversalNameInputs
from .safetensors_merger import SafetensorsMerger
from .deduplicator import TagDeduplicator

# Import the monitor to register the API route (no node class needed)
from . import system_monitor

# Merge all mappings into one dictionary
NODE_CLASS_MAPPINGS = {
    "TimerEndNode": TimerEndNode,
    "SettingsToText": SettingsToText,
    "UniversalNameInputs": UniversalNameInputs,
    "SafetensorsMerger": SafetensorsMerger,
    "TagDeduplicator": TagDeduplicator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TimerEndNode": "⏱️ Timer End",
    "SettingsToText": "Settings To Text",
    "UniversalNameInputs": "♾️ Universal Name (Infinite Inputs)",
    "SafetensorsMerger": "💾 Safetensors Merger (Shard to Single)",
    "TagDeduplicator": "🧹 String Tag Deduplicator"
}

# Explicitly tell ComfyUI where the web files (JS) are located
WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
