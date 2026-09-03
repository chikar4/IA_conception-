import os
from pathlib import Path

HOME = Path.home()
SEARCH_ROOTS = [
    HOME / "Desktop",
    HOME / "Documents",
    HOME / "Downloads",
    HOME / "Pictures",
]

APP_ALIASES = {
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "bloc-notes": "notepad.exe",
    "calculatrice": "calc.exe",
    "calculator": "calc.exe",
    "explorateur": "explorer.exe",
    "explorer": "explorer.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "vscode": "code",
    "visual studio code": "code",
    "code": "code",
    "paint": "mspaint.exe",
    "edge": "msedge.exe",
}

TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".log", ".py", ".ini", ".yaml", ".yml"}
MAX_READ_CHARS = 8000
MAX_SEARCH_RESULTS = 5


def find_file(name_hint, max_results=MAX_SEARCH_RESULTS):
    """Searches common user folders (Desktop, Documents, Downloads, Pictures)
    for files whose name contains name_hint."""
    name_hint_low = name_hint.lower()
    matches = []
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and name_hint_low in path.name.lower():
                matches.append(path)
                if len(matches) >= max_results:
                    return matches
    return matches


def open_item(name_or_path):
    """Opens a file, folder, or application. Returns a status string."""
    path = Path(name_or_path).expanduser()
    if path.exists():
        os.startfile(str(path))
        return f"Ouverture de {path.name}."

    alias = APP_ALIASES.get(name_or_path.strip().lower())
    if alias:
        os.startfile(alias)
        return f"Lancement de {name_or_path}."

    matches = find_file(name_or_path, max_results=2)
    if len(matches) == 1:
        os.startfile(str(matches[0]))
        return f"Ouverture de {matches[0].name}."
    if len(matches) > 1:
        listing = ", ".join(m.name for m in matches)
        return f"Plusieurs fichiers correspondent : {listing}. Precise lequel."

    try:
        os.startfile(name_or_path)
        return f"Lancement de {name_or_path}."
    except OSError:
        return f"Impossible de trouver ou d'ouvrir '{name_or_path}'."


def read_text_file(name_or_path, max_chars=MAX_READ_CHARS):
    """Reads the text content of a file, resolving by name if needed."""
    path = Path(name_or_path).expanduser()
    if not path.exists():
        matches = find_file(name_or_path, max_results=1)
        if not matches:
            return f"Fichier introuvable : {name_or_path}"
        path = matches[0]

    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return f"Ce type de fichier ({path.suffix}) n'est pas lisible en texte brut."

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return f"Erreur de lecture : {exc}"

    if len(content) > max_chars:
        content = content[:max_chars] + "\n[...contenu tronque...]"
    return content
