class AnyType(str):
    """A special type that equals anything. Bypasses ComfyUI validation."""
    def __ne__(self, __value: object) -> bool:
        return False
    def __eq__(self, __value: object) -> bool:
        return True

class UniversalNameInputs:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                # Start with input_1, the rest is handled by JavaScript
                "input_1": (AnyType("*"),)
            },
            # Hidden inputs for reading the graph (ID and Prompt)
            "hidden": {"unique_id": "UNIQUE_ID", "prompt": "PROMPT"},
        }

    RETURN_TYPES = ("STRING", "LIST",)
    RETURN_NAMES = ("concatenated_text", "raw_list",)
    FUNCTION = "process_inputs"
    CATEGORY = "💩 JVsShitNodes"

    def process_inputs(self, unique_id, prompt, **kwargs):
        # Keywords to look for in widgets (parent inputs)
        target_keys = ["name", "file", "ckpt", "lora", "model", "title", "text", "path"]
        
        extracted_names = []

        # Sort inputs by number (input_1, input_2...)
        sorted_keys = sorted(kwargs.keys(), key=lambda x: int(x.split('_')[-1]) if '_' in x else 0)

        for key in sorted_keys:
            # Process only our dynamic inputs
            if not key.startswith("input_"):
                continue
                
            input_data = kwargs[key]
            found_name = "None"
            
            # --- LOGIC 1: Graph Analysis (extract name from widget) ---
            # Look into the workflow JSON structure
            if unique_id in prompt and "inputs" in prompt[unique_id]:
                my_inputs = prompt[unique_id]["inputs"]
                
                # Check what is connected to this slot
                if key in my_inputs and isinstance(my_inputs[key], list):
                    parent_id = str(my_inputs[key][0])
                    
                    if parent_id in prompt:
                        parent_node = prompt[parent_id]
                        parent_inputs = parent_node.get("inputs", {})
                        
                        best_candidate = None
                        # Search parent node settings
                        for p_key, p_value in parent_inputs.items():
                            if isinstance(p_value, (str, int, float)):
                                k_lower = p_key.lower()
                                # If key contains target word (e.g. ckpt_name)
                                if any(t in k_lower for t in target_keys):
                                    if "name" in k_lower or "ckpt" in k_lower:
                                        best_candidate = str(p_value)
                                        break
                                    if best_candidate is None:
                                        best_candidate = str(p_value)
                        
                        if best_candidate:
                            found_name = best_candidate

            # --- LOGIC 2: Fallback (object inspection) ---
            # If the graph didn't yield results, try searching the data object itself
            if found_name == "None" and input_data is not None:
                found_name = self._inspect_object(input_data)
            
            extracted_names.append(found_name)

        # Output 1: String with newlines
        concat_string = "\n".join(extracted_names)
        
        # Output 2: List
        return (concat_string, extracted_names)

    def _inspect_object(self, obj):
        # Helper function to find a name inside an object/class
        if isinstance(obj, str): return obj
        search = ["name", "model_name", "ckpt_name", "filename"]
        
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(k, str) and any(s in k.lower() for s in search): return str(v)
        
        for s in search:
            if hasattr(obj, s): return str(getattr(obj, s))
            
        if hasattr(obj, "load_device"): return str(type(obj).__name__)
        
        return "Unknown"