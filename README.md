# 🧠 AI Command Line Assistant

A smart AI-powered CLI agent that converts natural language tasks into executable shell commands.

> "Install Node.js and set up a React app" ➜ `sudo apt install nodejs`, `npx create-react-app my-app`

Built using Hugging Face Inference API + Python + Shell.

### Features
- Converts tasks to shell commands
- Filters unsafe/redundant steps
- Optional auto-execution

### Tech Stack
- Hugging Face Mistral-7B-Instruct
- Python (requests, subprocess)
- Command filtering logic
