import { app } from "/scripts/app.js";
import { api } from "/scripts/api.js";

// refer. https://github.com/ltdrdata/ComfyUI-Impact-Pack/blob/Main/js/impact-pack.js
app.registerExtension({
    name: "Comfy.VibeForComfy.app",
    setup() {
        const refreshButton = document.getElementById('comfy-refresh-button');
        refreshButton.addEventListener('click', async function () {
            await fetch('/vibe_for_comfy/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            }).then(response => { }).catch(error => {
                console.error('Error:', error);
            });
        });
    },
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === 'StringListJoiner') {
            let input_name = 'arg';

            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
                if (!link_info)
                    return;

                // If action is disconnecting, remove disconnected slots
                if (!connected && (this.inputs.length > 1)) {
                    const stackTrace = new Error().stack;
                    if (
                        !stackTrace.includes('LGraphNode.prototype.connect') && // for touch device
                        !stackTrace.includes('LGraphNode.connect') && // for mouse device
                        !stackTrace.includes('loadGraphData')) {
                        this.removeInput(index);
                    }
                }

                // Re-arrange the arg names in case a middle slot is removed
                let slot_i = 1;
                for (let i = 0; i < this.inputs.length; i++) {
                    let input_i = this.inputs[i];
                    input_i.name = `${input_name}${slot_i}`
                    slot_i++;
                }

                // Ensure there is always one more slot than the number of inputs
                let last_slot = this.inputs[this.inputs.length - 1];
                if (last_slot.link != undefined) {
                    this.addInput(`${input_name}${slot_i}`, this.outputs[0].type);
                }
            }
        } else if (nodeData.name === 'OpenFolders') {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                if (onNodeCreated) onNodeCreated.apply(this, arguments);

                const buttons = [
                    { label: 'LoRAs', key: 'loras' },
                    { label: 'Embeddings', key: 'embeddings' },
                    { label: 'Checkpoints', key: 'checkpoints' },
                    { label: 'Workflows', key: 'workflows' },
                    { label: 'Outputs', key: 'outputs' },
                    { label: 'Logs', key: 'logs' },
                ];

                for (const btn of buttons) {
                    const w = this.addWidget("button", `Open ${btn.label}`, null, async () => {
                        try {
                            await fetch('/vibe_for_comfy/open_folder', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ key: btn.key })
                            });
                        } catch (err) {
                            console.error(`Failed to open ${btn.label}`, err);
                        }
                    });
                    w.serialize = false;
                }
            }
        }
    },

    nodeCreated(node) {
        if (node.comfyClass == "StringListJoiner") {
            if (node.widgets) {
                node.widgets = node.widgets.filter(w => !node.inputs.some((input) => w.name === input.name));
            }
        }
    }
});

// refer. https://github.com/ltdrdata/ComfyUI-Impact-Pack/blob/Main/js/common.js
function nodeFeedbackHandler(event) {
    let nodes = app.graph._nodes_by_id;
    let node = nodes[event.detail.node_id];
    if (node) {
        const w = node.widgets.find((w) => event.detail.widget_name === w.name);
        if (w) {
            w.value = event.detail.value;
        }
    }
}

api.addEventListener("vibe-for-comfy-feedback", nodeFeedbackHandler);