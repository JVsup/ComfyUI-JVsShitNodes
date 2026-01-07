import time
import datetime

class AnyType(str):
    """A special type that equals anything. Bypasses ComfyUI validation."""
    def __ne__(self, __value: object) -> bool:
        return False
    def __eq__(self, __value: object) -> bool:
        return True

class TimerEndNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                # Connect the final output of your workflow here
                "final_input": (AnyType("*"),)
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True # Ensures this node executes
    FUNCTION = "end_timer"
    CATEGORY = "💩 JVsShitNodes"

    # Force the node to run every time
    @classmethod
    def IS_CHANGED(s, **kwargs):
        return float("NaN")

    def end_timer(self, final_input=None, unique_id=None, extra_pnginfo=None):
        current_time = time.time()
        formatted_time = datetime.datetime.fromtimestamp(current_time).strftime('%H:%M:%S')

        # Green success log
        print(f"\n\033[92m{'='*60}")
        print(f" ⏱️  WORKFLOW COMPLETE")
        print(f"    Finished at: {formatted_time}")
        print(f"{'='*60}\033[0m\n")

        return {"ui": {"text": "done"}}