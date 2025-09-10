# Vibe for ComfyUI

A collection of utility nodes for ComfyUI that enhance workflow management and productivity.

> [!NOTE]
> This project was created with a [cookiecutter](https://github.com/Comfy-Org/cookiecutter-comfy-extension) template and enhanced with additional utility nodes.

## Quickstart

1. Install [ComfyUI](https://docs.comfy.org/get_started).
1. Install [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
1. Look up this extension in ComfyUI-Manager. If you are installing manually, clone this repository under `ComfyUI/custom_nodes`.
1. Restart ComfyUI.

## Features

### 🎯 Load LoRA With Prompt
- Apply LoRA models to base models with configurable strength
- Append custom prompts and notes
- Combine with existing prompt strings
- Automatic LoRA file discovery

### 📁 Open Folders
- Quick access to important ComfyUI directories
- One-click folder opening in Windows Explorer
- Supports multiple folder types:
  - LoRA models
  - Embeddings
  - Checkpoints
  - Workflows
  - Outputs

### 🔗 String List Joiner
- Dynamically combine multiple string inputs
- Automatic input slot management
- Filters out empty strings
- Perfect for prompt concatenation

### 🧪 Extended KSampler
- Wraps the built-in KSampler with extras
- Encodes prompts with CLIP inside the node (no external conditioning needed)
- Optionally decodes the result with a provided VAE and returns the decoded image

## Usage

### Load LoRA With Prompt
1. Add the "Load LoRA With Prompt" node from the "Vibe for Comfy" category
2. Connect your base model to the `model` input
3. Select a LoRA from the dropdown
4. Adjust the strength multiplier (default: 1.0)
5. Add your custom prompt text
6. Optionally connect an existing prompt to combine

### Open Folders
1. Add the "Open Folders" node from the "Vibe for Comfy" category
2. Click any of the five buttons to open the corresponding folder:
   - **LoRAs**: Opens the LoRA models directory
   - **Embeddings**: Opens the embeddings directory
   - **Checkpoints**: Opens the checkpoints directory
   - **Workflows**: Opens the workflows directory
   - **Outputs**: Opens the outputs directory

### String List Joiner
### Extended KSampler
1. Add the "Extended KSampler" node from the "Vibe for Comfy" category
2. Connect `model`, `clip`, `vae`, and an initial `latent_image`
3. Provide `positive_prompt` and `negative_prompt` (required)
4. Set sampling parameters: `seed`, `steps`, `cfg`, `sampler_name`, `scheduler`, `denoise`
5. Outputs include:
   - `image` (final decoded image)
   - passthrough settings: `positive_prompt`, `negative_prompt`, `steps`, `cfg`, `sampler_name`, `scheduler`
1. Add the "String List Joiner" node from the "Vibe for Comfy" category
2. Connect string inputs to the available slots
3. The node automatically creates new input slots as needed
4. Empty strings are automatically filtered out

## Configuration

The folder paths are configured in `src/vibe_for_comfy/constants.py`. You can modify the `FOLDER_MAP` dictionary to change the default paths:

```python
FOLDER_MAP = {
    "loras": r"C:\Users\cslil\Documents\ComfyUI\models\loras",
    "embeddings": r"C:\Users\cslil\Documents\ComfyUI\models\embeddings",
    # ... other paths
}
```

## Development

To install the dev dependencies and pre-commit (will run the ruff hook), do:

```bash
cd vibe_for_comfy
pip install -e .[dev]
pre-commit install
```

The `-e` flag above will result in a "live" install, in the sense that any changes you make to your node extension will automatically be picked up the next time you run ComfyUI.

### Code Structure
- `src/vibe_for_comfy/` - Main package source
- `src/vibe_for_comfy/nodes.py` - StringListJoiner node
- `src/vibe_for_comfy/open_folders.py` - Folder management node
- `src/vibe_for_comfy/constants.py` - Configuration constants
- `src/vibe_for_comfy/routes.py` - Backend API routes
- `js/app.js` - Frontend JavaScript extension

## Publish to Github

Install Github Desktop or follow these [instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) for ssh.

1. Create a Github repository that matches the directory name. 
2. Push the files to Git
```
git add .
git commit -m "project scaffolding"
git push
``` 

## Writing custom nodes

An example custom node is located in [node.py](src/vibe_for_comfy/nodes.py). To learn more, read the [docs](https://docs.comfy.org/essentials/custom_node_overview).


## Tests

This repo contains unit tests written in Pytest in the `tests/` directory. It is recommended to unit test your custom node.

- [build-pipeline.yml](.github/workflows/build-pipeline.yml) will run pytest and linter on any open PRs
- [validate.yml](.github/workflows/validate.yml) will run [node-diff](https://github.com/Comfy-Org/node-diff) to check for breaking changes

## Publishing to Registry

If you wish to share this custom node with others in the community, you can publish it to the registry. We've already auto-populated some fields in `pyproject.toml` under `tool.comfy`, but please double-check that they are correct.

You need to make an account on https://registry.comfy.org and create an API key token.

- [ ] Go to the [registry](https://registry.comfy.org). Login and create a publisher id (everything after the `@` sign on your registry profile). 
- [ ] Add the publisher id into the pyproject.toml file.
- [ ] Create an api key on the Registry for publishing from Github. [Instructions](https://docs.comfy.org/registry/publishing#create-an-api-key-for-publishing).
- [ ] Add it to your Github Repository Secrets as `REGISTRY_ACCESS_TOKEN`.

A Github action will run on every git push. You can also run the Github action manually. Full instructions [here](https://docs.comfy.org/registry/publishing). Join our [discord](https://discord.com/invite/comfyorg) if you have any questions!

