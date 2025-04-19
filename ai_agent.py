# import os
# import sys
# import re
# import platform
# import subprocess
# import webbrowser
# import requests
# from rich import print
# from dotenv import load_dotenv

# load_dotenv()

# HF_API_TOKEN = os.getenv("HF_API_TOKEN")
# MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
# HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# def query_huggingface(prompt: str):
#     payload = {
#         "inputs": prompt,
#         "parameters": {"max_new_tokens": 300}
#     }
#     response = requests.post(MODEL_URL, headers=HEADERS, json=payload)
#     if response.status_code == 200:
#         full_output = response.json()[0]["generated_text"]
#         # Strip prompt from AI echo
#         if "Task:" in full_output:
#             return full_output.split("Task:")[1].strip()
#         return full_output.strip()
#     else:
#         print(f"[red]❌ Error {response.status_code}[/red]: {response.text}")
#         return None


# def extract_commands(text: str):
#     commands = []
#     for line in text.strip().splitlines():
#         line = line.strip()

#         # Filter out noise
#         if (
#             not line
#             or "rule" in line.lower()
#             or line.startswith("-")
#             or len(line.split()) > 20
#         ):
#             continue

#         # Remove bullet points, numbering, backticks
#         line = re.sub(r"^\d+\.\s*", "", line)
#         line = line.strip("` ")

#         # Accept basic shell commands and file commands
#         if any(cmd in line for cmd in ["start", "open", "xdg-open", "npm", "npx", "echo", "touch"]):
#             commands.append(line)

#     return commands


# def save_to_file(content: str, filename="ai_task_output.txt"):
#     with open(filename, "w") as f:
#         f.write(content.strip())
#     print(f"\n[green]✅ Saved to {filename}[/green]")


# def execute_command(command: str):
#     os_name = platform.system()
#     try:
#         if "youtube.com" in command:
#             print(f"\n[cyan]→ Opening YouTube in browser...[/cyan]")
#             webbrowser.open("https://youtube.com")
#         elif os_name == "Windows":
#             subprocess.run(command, shell=True)
#         elif os_name == "Darwin":
#             subprocess.run(["open"] + command.split())
#         elif os_name == "Linux":
#             subprocess.run(command.split())
#         else:
#             print("[red]❌ Unsupported OS[/red]")
#     except Exception as e:
#         print(f"[red]❌ Command failed:[/red] {e}")


# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("[red]⚠️  Please provide a task in quotes.[/red]")
#         sys.exit(1)

#     task = " ".join(sys.argv[1:])
#     print("[cyan]🧠 Thinking...[/cyan]\n")

#     prompt = f"""
# You are a helpful AI assistant. Your job is to output a list of clean, executable shell commands only.

# Task: {task}

# Rules:
# - Only return shell commands that work in a terminal (e.g., start, open, xdg-open, npm, npx, echo, touch)
# - One command per line
# - No explanations, no extra text, just shell commands
# - Do not repeat any command or install the same package more than once
# - Return each step only once in the correct order

# Instructions:
# - Create a Next.js app with Tailwind CSS
# - Only install necessary dependencies for Tailwind CSS (no Webpack, Babel, or other tools needed for Next.js)
# - Do not install any unnecessary development tools
# - Build the app
# - Run the app inside the project folder
# """

#     result = query_huggingface(prompt)

#     if result:
#         print("\n[yellow]📋 AI-Generated Response:[/yellow]\n")
#         print(result)

#         commands = extract_commands(result)

#         # Filter out unnecessary dependencies like Webpack, Babel
#         commands = [cmd for cmd in commands if "webpack" not in cmd and "babel" not in cmd]

#         if commands:
#             save_to_file("\n".join(commands))

#             feedback = input("\n🤖 Do you find the commands useful? [y/n]: ").strip().lower()
#             if feedback == "y":
#                 execute = input("🚀 Do you want to execute them now? [y/n]: ").strip().lower()
#                 if execute == "y":
#                     for cmd in commands:
#                         print(f"\n⚙️ Executing Command: [bold]{cmd}[/bold]\n")
#                         execute_command(cmd)
#                 else:
#                     print("❎ Skipped execution.")
#             else:
#                 print("👍 Okay, not executing.")
#         else:
#             print("[red]❌ No valid shell command found.[/red]")
import os
import subprocess
import webbrowser
import json
from rich import print
import requests
from dotenv import load_dotenv
import sys
import re

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def query_huggingface(prompt: str):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300}
    }
    response = requests.post(MODEL_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        full_output = response.json()[0]["generated_text"]
        # Strip prompt from AI echo
        if "Task:" in full_output:
            return full_output.split("Task:")[1].strip()
        return full_output.strip()
    else:
        print(f"[red]❌ Error {response.status_code}[/red]: {response.text}")
        return None


def extract_commands(text: str):
    commands = []
    for line in text.strip().splitlines():
        line = line.strip()

        # Filter out noise
        if (
            not line
            or "rule" in line.lower()
            or line.startswith("-")
            or len(line.split()) > 20
        ):
            continue

        # Remove bullet points, numbering, backticks
        line = re.sub(r"^\d+\.\s*", "", line)
        line = line.strip("` ")

        # Accept basic shell commands and file commands
        if any(cmd in line for cmd in ["start", "open", "xdg-open", "npm", "npx", "echo", "touch"]):
            commands.append(line)

    return commands


def save_to_file(content: str, filename="ai_task_output.txt"):
    with open(filename, "w") as f:
        f.write(content.strip())
    print(f"\n[green]✅ Saved to {filename}[/green]")


def add_missing_scripts(package_json_path: str):
    try:
        with open(package_json_path, 'r+') as f:
            data = json.load(f)

            # Add missing scripts
            if 'scripts' not in data:
                data['scripts'] = {}

            if 'dev' not in data['scripts']:
                data['scripts']['dev'] = 'next dev'

            if 'build' not in data['scripts']:
                data['scripts']['build'] = 'next build'

            if 'start' not in data['scripts']:
                data['scripts']['start'] = 'next start'

            # Move file pointer to the beginning
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

            print("[green]✅ Missing scripts added to package.json[/green]")

    except Exception as e:
        print(f"[red]❌ Error updating package.json: {e}[/red]")


def execute_command(command: str):
    try:
        if "youtube.com" in command:
            print(f"\n[cyan]→ Opening YouTube in browser...[/cyan]")
            webbrowser.open("https://youtube.com")
        else:
            subprocess.run(command, shell=True)
    except Exception as e:
        print(f"[red]❌ Command failed: {e}[/red]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[red]⚠️  Please provide a task in quotes.[/red]")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    print("[cyan]🧠 Thinking...[/cyan]\n")

    prompt = f"""
You are a helpful AI assistant. Your job is to output a list of clean, executable shell commands only.

Task: {task}

Rules:
- Only return shell commands that work in a terminal (e.g., start, open, xdg-open, npm, npx, echo, touch)
- One command per line
- No explanations, no extra text, just shell commands
- Do not repeat any command or install the same package more than once
- Return each step only once in the correct order

Instructions:
- Create a Next.js app with Tailwind CSS
- Only install necessary dependencies for Tailwind CSS (no Webpack, Babel, or other tools needed for Next.js)
- Add the correct `dev`, `build`, and `start` scripts to the `package.json` file
- Do not install any unnecessary development tools
- Build the app
- Run the app inside the project folder
"""

    result = query_huggingface(prompt)

    if result:
        print("\n[yellow]📋 AI-Generated Response:[/yellow]\n")
        print(result)

        commands = extract_commands(result)

        # Filter out unnecessary dependencies like Webpack, Babel
        commands = [cmd for cmd in commands if "webpack" not in cmd and "babel" not in cmd]

        if commands:
            save_to_file("\n".join(commands))

            feedback = input("\n🤖 Do you find the commands useful? [y/n]: ").strip().lower()
            if feedback == "y":
                execute = input("🚀 Do you want to execute them now? [y/n]: ").strip().lower()
                if execute == "y":
                    for cmd in commands:
                        print(f"\n⚙️ Executing Command: [bold]{cmd}[/bold]\n")
                        execute_command(cmd)

                    # Check and add missing scripts in package.json
                    add_missing_scripts("package.json")

                    # Navigate into the correct project folder (if needed)
                    project_name = "your_project_name"  # Replace this with your actual project folder name
                    os.chdir(os.path.join(os.getcwd(), project_name))
                    print(f"\n[cyan]→ Navigated to project folder: {os.getcwd()}[/cyan]")

                    # Now execute the commands inside the project folder
                    for cmd in ["npm run dev", "npm run build", "npm run start"]:
                        print(f"\n⚙️ Executing Command: {cmd}\n")
                        execute_command(cmd)
                else:
                    print("❎ Skipped execution.")
            else:
                print("👍 Okay, not executing.")
        else:
            print("[red]❌ No valid shell command found.[/red]")
