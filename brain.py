import os

from anthropic import Anthropic
from dotenv import load_dotenv

import pc_control

load_dotenv()

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")
SYSTEM_PROMPT = (
    "Tu es un assistant vocal personnel, dans l'esprit de Jarvis, qui vit sur le PC "
    "Windows de l'utilisateur. Reponds de maniere concise et naturelle, adaptee a une "
    "lecture a voix haute. Tu peux ouvrir des fichiers, dossiers ou applications, et "
    "lire le contenu de fichiers texte via tes outils. N'utilise ces outils que quand "
    "l'utilisateur te le demande explicitement."
)

TOOLS = [
    {
        "name": "open_item",
        "description": (
            "Ouvre un fichier, un dossier ou lance une application sur le PC de "
            "l'utilisateur, par nom ou chemin (ex: 'mon CV', 'chrome', "
            "'C:/Users/moi/Documents/notes.txt')."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name_or_path": {
                    "type": "string",
                    "description": "Nom ou chemin du fichier, dossier ou application a ouvrir.",
                }
            },
            "required": ["name_or_path"],
        },
    },
    {
        "name": "read_text_file",
        "description": (
            "Lit le contenu texte d'un fichier (txt, md, csv, json, py, log...) sur le "
            "PC de l'utilisateur, par nom ou chemin, pour pouvoir le resumer ou repondre "
            "a son sujet."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name_or_path": {
                    "type": "string",
                    "description": "Nom ou chemin du fichier a lire.",
                }
            },
            "required": ["name_or_path"],
        },
    },
]

TOOL_FUNCTIONS = {
    "open_item": pc_control.open_item,
    "read_text_file": pc_control.read_text_file,
}


class Brain:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY manquante. Ajoute-la dans le fichier .env."
            )
        workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID")
        default_headers = {"anthropic-workspace-id": workspace_id} if workspace_id else None
        self.client = Anthropic(api_key=api_key, default_headers=default_headers)
        self.history = []

    def ask(self, user_text):
        self.history.append({"role": "user", "content": user_text})

        while True:
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=self.history,
            )
            self.history.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                return "".join(block.text for block in response.content if block.type == "text")

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": self._run_tool(block.name, block.input),
                        }
                    )
            self.history.append({"role": "user", "content": tool_results})

    def _run_tool(self, name, tool_input):
        func = TOOL_FUNCTIONS.get(name)
        if func is None:
            return f"Outil inconnu : {name}"
        try:
            return func(**tool_input)
        except Exception as exc:
            return f"Erreur lors de l'execution de l'outil {name} : {exc}"

