import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "UniversalName.DynamicSlots",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Check if this is our node (must match NODE_CLASS_MAPPINGS in Python)
        if (nodeData.name === "UniversalNameInputs") {
            
            // Log to verify the script has loaded
            console.log("UniversalName: Dynamic Inputs Extension Loaded for", nodeData.name);

            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
                // Call the original function if it exists
                const r = onConnectionsChange ? onConnectionsChange.apply(this, arguments) : undefined;

                // type 1 = Input, type 2 = Output. We only care about inputs.
                if (type !== 1) return r;

                // Get the list of inputs
                const inputs = this.inputs;
                if (!inputs) return r;

                const lastIndex = inputs.length - 1;
                const lastInput = inputs[lastIndex];

                // If the LAST input is connected (link is not null), add a new one
                if (lastInput.link !== null && lastInput.link !== undefined) {
                    
                    // Calculate the name for the new input (e.g., input_2, input_3...)
                    const nextIndex = inputs.length + 1;
                    const newName = `input_${nextIndex}`;

                    console.log(`UniversalName: Adding new slot ${newName}`);
                    
                    // Add new input of type "*" (universal)
                    this.addInput(newName, "*");
                }

                return r;
            };
        }
    },
});