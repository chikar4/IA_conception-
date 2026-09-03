# IA_conception

🦾 Ton propre Jarvis, sans le costume d'Iron Man.

Un assistant vocal personnel écrit en Python : tu parles, il te comprend, il te répond — à voix haute. Reconnaissance vocale locale avec Whisper, réflexion via l'API Claude d'Anthropic, réponse en synthèse vocale.

## Fonctionnement

1. Tu maintiens une touche enfoncée pour parler (push-to-talk).
2. Ta voix est transcrite en texte localement grâce à [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (aucune donnée audio envoyée sur internet à cette étape).
3. Le texte est envoyé à l'API Claude, qui génère une réponse en tenant compte de l'historique de la conversation.
4. La réponse est lue à voix haute avec `pyttsx3` (voix Windows SAPI5, hors-ligne).

## Structure du projet

| Fichier | Rôle |
|---|---|
| `main.py` | Boucle principale : orchestre écoute, réflexion et réponse |
| `voice_in.py` | Enregistrement micro (push-to-talk) + transcription Whisper |
| `brain.py` | Appel à l'API Claude et gestion de l'historique de conversation |
| `voice_out.py` | Synthèse vocale de la réponse |
| `requirements.txt` | Dépendances Python du projet |
| `.env` | Clés API et configuration (jamais versionné) |

## Installation

Prérequis : Python 3.10+ sur Windows, un micro fonctionnel.

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

## Configuration

Crée un fichier `.env` à la racine du projet (voir le modèle ci-dessous) :

```
ANTHROPIC_API_KEY=ta_cle_api
CLAUDE_MODEL=claude-sonnet-5
ANTHROPIC_WORKSPACE_ID=ton_workspace_id
```

- Récupère ta clé sur [console.anthropic.com](https://console.anthropic.com) → **Settings → API Keys**.
- `ANTHROPIC_WORKSPACE_ID` n'est nécessaire que si ta clé est de type "identity-linked" (l'API te le signalera explicitement le cas échéant).

## Utilisation

```bash
python main.py
```

- Maintiens **ESPACE** pour parler, relâche pour envoyer.
- Appuie sur **ÉCHAP** pour quitter.

## Statut

Projet personnel en cours de développement — minimal, ouvert, pensé pour Windows.
