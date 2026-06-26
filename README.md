# CinePrompt Studio

A dependency-free prompt builder for cinematic still images. It combines subject, action, camera look, composition, lighting, color, grade, texture, and unified image-prompt formatting into a prompt ready for image generation.

The full local app supports optional Ollama-based prompt refinement. The public GitHub Pages site deliberately excludes Ollama controls and makes no calls to a local model server.

## Live Demo

[Open the GitHub Pages version](https://sh4d0wbu7n.github.io/cineprompt-studio/)

## Features

- Unified model-agnostic image prompt output.
- Camera-look, lens, framing, angle, motivated light source, light direction, exposure, palette, grade, physical realism, texture, art-direction, and quality controls.
- Cinematic look recipes for grounded spy thriller, cyber-noir, neo-noir action, war documentary, desert sci-fi, urban noir, and wasteland action looks.
- Optional Anti AI Gloss constraints targeting fake HDR, waxy skin, CGI/render artifacts, plastic reflections, oversaturation, and overprocessed contrast.
- `None` bypasses for every builder setting.
- Local preset storage, JSON export/import, prompt QA, and generated visual reference assets.
- Optional local Ollama model selection and prompt enhancement in the local app only.

## Run Locally

### Install Node.js

Install a current Node.js LTS release from [nodejs.org](https://nodejs.org/en/download). Node is used only to serve the static app locally; there are no package dependencies to install.

Verify the installation:

```powershell
node --version
```

### Start the App

Clone the repository, open a terminal in its directory, and run:

```powershell
git clone https://github.com/sh4d0wbu7n/cineprompt-studio.git
cd cineprompt-studio
```

Then start the app:

```powershell
node serve-local.mjs
```

On Windows, you can also double-click [start-local.bat](start-local.bat).

Open [http://localhost:8787](http://localhost:8787). Keep the terminal open while using the app. Stop the server with `Ctrl+C`.

## Optional: Ollama Prompt Enhancement

Ollama is required only for the local **Enhance** feature. The builder and GitHub Pages version both work without it.

### Install Ollama

Download Ollama for your operating system from [ollama.com/download](https://ollama.com/download). For installation and platform-specific service instructions, see the [official Ollama documentation](https://docs.ollama.com/).

After installation, download at least one local text model. For example:

```powershell
ollama pull qwen3.6:27b
```

You can use any locally installed chat model. If the Ollama service is not already running, start it with:

```powershell
ollama serve
```

Then open the local app at `http://localhost:8787`, select **Refresh** in the Ollama panel, choose a model, and use **Enhance**. The app calls only your configured local endpoint, which defaults to `http://127.0.0.1:11434`.

## GitHub Pages

GitHub Pages deploys the workflow-generated `dist/` artifact. The build script strips the Ollama UI, client code, and local endpoint settings before deployment.

To reproduce the Pages build locally:

```powershell
node scripts/build-pages.mjs
```

The generated `dist/` folder is ignored by Git. It is validated during the build and fails if an Ollama reference remains.

## Origin and License

CinePrompt Studio is based on [yedp123/yedp123.github.io](https://github.com/yedp123/yedp123.github.io). The original project's MIT license and copyright notice are preserved in [LICENSE](LICENSE).

## Project Layout

```text
assets/                 Visual reference images used by the builder
Prompting_Guides/       Local prompting guides used to shape model profiles
index.html              Full local app, including optional Ollama enhancement
serve-local.mjs         Dependency-free local static server
scripts/build-pages.mjs GitHub Pages build without Ollama
.github/workflows/      GitHub Pages deployment workflow
```

## License

See [LICENSE](LICENSE).
