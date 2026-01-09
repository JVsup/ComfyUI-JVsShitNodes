import re

class TagDeduplicator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "process_tags"
    CATEGORY = "💩 JVsShitNodes"

    def process_tags(self, text):
        if not text:
            return ("",)

        # Split text by commas
        tags = [t.strip() for t in text.split(',')]
        
        # Dictionary to store unique tags
        # Key = "core" tag (cleaned text), Value = dict with original tag and weight info
        seen_tags = {}
        
        # List to preserve order (storing keys only)
        ordered_keys = []

        for tag in tags:
            if not tag:
                continue

            # Get "core" text for comparison and check if the tag is weighted
            core_text, is_weighted = self.analyze_tag(tag)

            if core_text not in seen_tags:
                # If we haven't seen this tag yet, add it
                seen_tags[core_text] = {"original": tag, "weighted": is_weighted}
                ordered_keys.append(core_text)
            else:
                # If it already exists, check priorities
                current_entry = seen_tags[core_text]
                
                # If the new tag IS weighted and the old one IS NOT, replace it
                if is_weighted and not current_entry["weighted"]:
                    seen_tags[core_text] = {"original": tag, "weighted": True}
                
                # In all other cases (both unweighted, both weighted, old one weighted)
                # keep the original one (preserve first occurrence or the one with better weight status)

        # Build the result string
        result_list = [seen_tags[key]["original"] for key in ordered_keys]
        result_string = ", ".join(result_list)

        return (result_string,)

    def analyze_tag(self, tag):
        """
        Returns tuple (clean_text, is_weighted_bool)
        Removes parentheses and weights for comparison purposes.
        E.g.: "(screaming:1.5)" -> "screaming", True
              "blue light"      -> "blue light", False
        """
        # Weight detection (simplified heuristic: contains colon and number or bracket structure)
        # Looks for pattern :number or :number.number at the end of string (before potential bracket)
        is_weighted = bool(re.search(r':\d+(\.\d+)?\)*$', tag)) or ( "(" in tag and ")" in tag and ":" in tag)

        # Clean text for comparison
        # 1. Remove weights (e.g. :1.5)
        clean = re.sub(r':\d+(\.\d+)?', '', tag)
        # 2. Remove all parentheses
        clean = clean.replace('(', '').replace(')', '')
        # 3. Remove multiple spaces and strip
        clean = re.sub(r'\s+', ' ', clean).strip()

        return clean, is_weighted
