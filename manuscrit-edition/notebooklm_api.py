#!/usr/bin/env python3
"""
notebooklm_api.py
═════════════════
Injecte « La paix, on peut l'éviter » dans Google NotebookLM via l'API v1beta.

Chaque section H1 du manuscrit devient une source texte indépendante dans le
notebook, ce qui permet à NotebookLM de répondre avec précision aux questions
par chapitre et de générer un Audio Overview structuré.

━━ PRÉREQUIS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    pip install requests

━━ OBTENIR UNE CLÉ API ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    1. Ouvrir Google AI Studio : https://aistudio.google.com/apikey
    2. Cliquer « Create API key »  → copier la clé
    3. Exporter : export NOTEBOOKLM_API_KEY="AIzaSy..."
       (ou passer --api-key à la commande)

    Note : l'API NotebookLM v1beta est distincte de l'API Gemini — la même clé
    Google AI Studio fonctionne pour les deux si elle est associée à un projet
    Cloud ayant activé l'API « Notebook LM API ».

━━ USAGE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # Analyse du manuscrit sans appel API
    python notebooklm_api.py --dry-run

    # Créer un notebook et injecter tous les chapitres
    python notebooklm_api.py --api-key AIzaSy...

    # Injecter dans un notebook existant
    python notebooklm_api.py --notebook-id abc123def456

    # Tester sur les 3 premières sections uniquement
    python notebooklm_api.py --dry-run --limit 3

    # Créer le notebook + déclencher l'Audio Overview
    python notebooklm_api.py --audio-overview

    # Lister les notebooks existants
    python notebooklm_api.py --list-notebooks

━━ VARIABLES D'ENVIRONNEMENT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    NOTEBOOKLM_API_KEY   Clé API Google (obligatoire hors --dry-run)
    NOTEBOOKLM_NB_ID     ID notebook par défaut (optionnel)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("ERREUR : module 'requests' introuvable — pip install requests")
    sys.exit(1)

# ── Chemins ──────────────────────────────────────────────────────────────────────
HERE       = Path(__file__).parent
MANUSCRIPT = HERE / "LIVRE-FINAL.md"

# ── Métadonnées du livre ─────────────────────────────────────────────────────────
BOOK_TITLE  = "La paix, on peut l'éviter — enquête AES (BEN-H2O)"
BOOK_LANG   = "fr"

# ── API ──────────────────────────────────────────────────────────────────────────
BASE_URL   = "https://notebooklm.googleapis.com/v1beta"
MAX_SOURCE = 200_000   # limite chars par source NotebookLM (~200 ko)
RATE_DELAY = 0.6       # secondes entre appels (politesse API)


# ══════════════════════════════════════════════════════════════════════════════════
# PARSING DU MANUSCRIT
# ══════════════════════════════════════════════════════════════════════════════════

def clean_markdown(text: str) -> str:
    """Nettoie les marqueurs internes avant d'envoyer à NotebookLM."""
    text = re.sub(r'^---(?:ENCADRE|FIN)---\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^-{3,}\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'★★★', '* * *', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_sections(md_text: str) -> list[dict]:
    """
    Découpe le manuscrit en sections H1.
    Retourne une liste de dicts { title, content, kind }.
    kind ∈ { 'partie', 'chapitre', 'annexe', 'frontmatter' }
    """
    sections: list[dict] = []
    current_title: str   = "Préambule"
    current_lines: list  = []
    current_kind: str    = "frontmatter"

    PARTIE_RE   = re.compile(r'^PARTIE\s', re.IGNORECASE)
    CHAPITRE_RE = re.compile(r'^Chapitre\s', re.IGNORECASE)
    ANNEX_KEYS  = {"Conclusion", "Chronologie", "Glossaire", "Index", "Notes",
                   "Sommaire", "Avant-propos", "Prologue", "Introduction"}

    def detect_kind(title: str) -> str:
        bare = title.split("—")[0].strip()
        if PARTIE_RE.match(bare):
            return "partie"
        if CHAPITRE_RE.match(bare):
            return "chapitre"
        if any(bare.startswith(k) for k in ANNEX_KEYS):
            return "annexe" if bare not in {"Avant-propos", "Prologue", "Introduction"} else "frontmatter"
        return "frontmatter"

    for raw_line in md_text.splitlines(keepends=True):
        if raw_line.startswith("# ") and not raw_line.startswith("## "):
            if current_lines:
                content = clean_markdown("".join(current_lines))
                sections.append({
                    "title":   current_title,
                    "content": content,
                    "kind":    current_kind,
                    "chars":   len(content),
                })
            current_title = raw_line[2:].strip()
            current_lines = [raw_line]
            current_kind  = detect_kind(current_title)
        else:
            current_lines.append(raw_line)

    if current_lines:
        content = clean_markdown("".join(current_lines))
        sections.append({
            "title":   current_title,
            "content": content,
            "kind":    current_kind,
            "chars":   len(content),
        })

    return sections


def chunk_section(section: dict, max_size: int = MAX_SOURCE) -> list[dict]:
    """
    Si une section dépasse max_size, la découpe en sous-blocs sur double-saut.
    Retourne une liste de dicts prêts à être envoyés comme sources.
    """
    text  = section["content"]
    title = section["title"]
    if len(text) <= max_size:
        return [{"title": title, "content": text}]

    chunks = []
    part   = 1
    while text:
        # Découpe propre sur un double saut de ligne
        cut = text[:max_size].rfind("\n\n")
        if cut <= 0:
            cut = max_size
        chunk_text = text[:cut].strip()
        chunks.append({
            "title":   f"{title} ({part})",
            "content": chunk_text,
        })
        text = text[cut:].strip()
        part += 1

    return chunks


# ══════════════════════════════════════════════════════════════════════════════════
# CLIENT API
# ══════════════════════════════════════════════════════════════════════════════════

class NotebookLMClient:
    """Client minimaliste pour l'API NotebookLM v1beta."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._s = requests.Session()
        self._s.headers.update({
            "Content-Type":   "application/json",
            "x-goog-api-key": api_key,
        })

    def _url(self, path: str) -> str:
        return f"{BASE_URL}/{path.lstrip('/')}"

    def _raise(self, resp: requests.Response) -> None:
        if not resp.ok:
            try:
                err = resp.json()
                msg = err.get("error", {}).get("message", resp.text[:300])
            except Exception:
                msg = resp.text[:300]
            raise requests.HTTPError(
                f"HTTP {resp.status_code} — {msg}",
                response=resp,
            )

    # ── Notebooks ────────────────────────────────────────────────────────────────

    def list_notebooks(self) -> list[dict]:
        resp = self._s.get(self._url("notebooks"))
        self._raise(resp)
        return resp.json().get("notebooks", [])

    def create_notebook(self, title: str) -> dict:
        resp = self._s.post(self._url("notebooks"), json={"title": title})
        self._raise(resp)
        return resp.json()

    def get_notebook(self, notebook_id: str) -> dict:
        resp = self._s.get(self._url(f"notebooks/{notebook_id}"))
        self._raise(resp)
        return resp.json()

    # ── Sources ──────────────────────────────────────────────────────────────────

    def list_sources(self, notebook_id: str) -> list[dict]:
        resp = self._s.get(self._url(f"notebooks/{notebook_id}/sources"))
        self._raise(resp)
        return resp.json().get("sources", [])

    def add_text_source(self, notebook_id: str, title: str, content: str) -> dict:
        payload = {
            "source": {
                "displayName": title,
                "content": {
                    "type": "TEXT",
                    "text": content,
                },
            }
        }
        resp = self._s.post(
            self._url(f"notebooks/{notebook_id}/sources"),
            json=payload,
        )
        self._raise(resp)
        return resp.json()

    def delete_source(self, notebook_id: str, source_id: str) -> None:
        resp = self._s.delete(
            self._url(f"notebooks/{notebook_id}/sources/{source_id}")
        )
        self._raise(resp)

    # ── Audio Overview ────────────────────────────────────────────────────────────

    def generate_audio_overview(self, notebook_id: str,
                                 custom_prompt: Optional[str] = None) -> dict:
        body: dict = {}
        if custom_prompt:
            body["customization"] = {"style": custom_prompt}
        resp = self._s.post(
            self._url(f"notebooks/{notebook_id}:generateAudio"),
            json=body,
        )
        self._raise(resp)
        return resp.json()

    def get_audio_overview(self, notebook_id: str) -> dict:
        resp = self._s.get(self._url(f"notebooks/{notebook_id}/audio"))
        self._raise(resp)
        return resp.json()

    def poll_audio_overview(self, notebook_id: str,
                             timeout: int = 300, interval: int = 10) -> dict:
        """Attend la fin de la génération Audio Overview (max timeout secondes)."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            data = self.get_audio_overview(notebook_id)
            state = data.get("state", "")
            if state == "SUCCEEDED":
                return data
            if state in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"Audio Overview {state}: {data}")
            print(f"    Audio Overview : {state or '…'}  (attente {interval}s)", end="\r")
            time.sleep(interval)
        raise TimeoutError("Audio Overview non terminé dans le délai imparti.")


# ══════════════════════════════════════════════════════════════════════════════════
# COMMANDES
# ══════════════════════════════════════════════════════════════════════════════════

def cmd_dry_run(sections: list[dict], limit: Optional[int]) -> None:
    """Affiche l'analyse du manuscrit sans appel API."""
    if limit:
        sections = sections[:limit]
    total_chars  = sum(s["chars"] for s in sections)
    total_chunks = sum(len(chunk_section(s)) for s in sections)

    print(f"\n{'─'*72}")
    print(f"  MANUSCRIT : {MANUSCRIPT.name}")
    print(f"  Sections  : {len(sections)}")
    print(f"  Chunks    : {total_chunks}  (sources NotebookLM)")
    print(f"  Total     : {total_chars:,} chars  (~{total_chars // 1000} Ko)")
    print(f"{'─'*72}")
    print(f"  {'#':>3}  {'TYPE':<12}  {'CHARS':>7}  TITRE")
    print(f"  {'─'*3}  {'─'*12}  {'─'*7}  {'─'*44}")
    for i, s in enumerate(sections, 1):
        flag = " ✂" if s["chars"] > MAX_SOURCE else ""
        print(f"  {i:>3}  {s['kind']:<12}  {s['chars']:>7,}  {s['title'][:50]}{flag}")
    print(f"{'─'*72}\n")


def cmd_list_notebooks(client: NotebookLMClient) -> None:
    print("Récupération des notebooks…")
    nbs = client.list_notebooks()
    if not nbs:
        print("  Aucun notebook trouvé.")
        return
    print(f"\n  {'ID':<28}  TITRE")
    for nb in nbs:
        nb_id    = nb.get("name", "?").split("/")[-1]
        nb_title = nb.get("title", "—")
        print(f"  {nb_id:<28}  {nb_title}")
    print()


def cmd_inject(client: NotebookLMClient,
               sections: list[dict],
               notebook_id: Optional[str],
               limit: Optional[int],
               skip_existing: bool) -> str:
    """Crée ou réutilise un notebook, injecte les sources."""

    if limit:
        sections = sections[:limit]

    # ── Notebook ──────────────────────────────────────────────────────────────────
    if notebook_id:
        nb = client.get_notebook(notebook_id)
        print(f"Notebook existant : {nb.get('title', notebook_id)}")
    else:
        print(f"Création du notebook « {BOOK_TITLE} »…")
        nb          = client.create_notebook(BOOK_TITLE)
        notebook_id = nb.get("name", "").split("/")[-1] or nb.get("id", "")
        print(f"  → ID : {notebook_id}")

    # ── Sources existantes (pour dédoublonnage) ──────────────────────────────────
    existing_titles: set[str] = set()
    if skip_existing:
        print("  Récupération des sources existantes…")
        existing = client.list_sources(notebook_id)
        existing_titles = {s.get("displayName", "") for s in existing}
        if existing_titles:
            print(f"  {len(existing_titles)} source(s) déjà présente(s) — ignorées.")

    # ── Injection ────────────────────────────────────────────────────────────────
    all_chunks: list[dict] = []
    for s in sections:
        all_chunks.extend(chunk_section(s))

    n = len(all_chunks)
    ok = err = skip = 0

    print(f"\nInjection de {n} source(s) dans le notebook {notebook_id}…\n")
    for i, chunk in enumerate(all_chunks, 1):
        title = chunk["title"]
        pad   = f"[{i:>3}/{n}]"

        if title in existing_titles:
            print(f"  {pad}  ⏭  {title[:56]}")
            skip += 1
            continue

        print(f"  {pad}  ↑  {title[:56]}", end="  ", flush=True)
        try:
            client.add_text_source(notebook_id, title, chunk["content"])
            print("✓")
            ok += 1
        except requests.HTTPError as exc:
            code = exc.response.status_code if exc.response is not None else "?"
            body = (exc.response.text[:120] if exc.response is not None else str(exc))
            print(f"✗  [{code}] {body}")
            err += 1

        time.sleep(RATE_DELAY)

    print(f"\n  Résultat : {ok} ajoutée(s), {skip} ignorée(s), {err} erreur(s).")
    return notebook_id


# ══════════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ══════════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Injecte le manuscrit dans Google NotebookLM (API v1beta)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    auth = p.add_argument_group("Authentification")
    auth.add_argument("--api-key",   default=os.getenv("NOTEBOOKLM_API_KEY"),
                      metavar="KEY", help="Clé API Google AI Studio")

    nb = p.add_argument_group("Notebook")
    nb.add_argument("--notebook-id", default=os.getenv("NOTEBOOKLM_NB_ID"),
                    metavar="ID",  help="ID notebook existant (sinon : crée)")
    nb.add_argument("--list-notebooks", action="store_true",
                    help="Liste les notebooks disponibles et quitte")
    nb.add_argument("--skip-existing", action="store_true", default=True,
                    help="Ne réinjecte pas les sources déjà présentes (défaut)")
    nb.add_argument("--no-skip-existing", dest="skip_existing", action="store_false")

    inj = p.add_argument_group("Injection")
    inj.add_argument("--manuscript", default=str(MANUSCRIPT),
                     metavar="PATH", help="Chemin vers le fichier Markdown")
    inj.add_argument("--limit", type=int, metavar="N",
                     help="Injecter seulement les N premières sections (test)")
    inj.add_argument("--dry-run", action="store_true",
                     help="Analyse le manuscrit sans appeler l'API")

    ao = p.add_argument_group("Audio Overview")
    ao.add_argument("--audio-overview", action="store_true",
                    help="Déclenche la génération Audio Overview après injection")
    ao.add_argument("--audio-prompt", metavar="TEXTE",
                    default=(
                        "Réalisez un podcast en français de 10 minutes sur ce livre. "
                        "Présentez les thèses principales, les preuves les plus "
                        "frappantes et les enjeux géopolitiques du Sahel pour un "
                        "grand public cultivé mais non spécialiste."
                    ),
                    help="Consigne de style pour l'Audio Overview")
    ao.add_argument("--audio-wait", action="store_true",
                    help="Attend la fin de la génération et affiche le lien de téléchargement")

    return p


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    # ── Manuscrit ────────────────────────────────────────────────────────────────
    manuscript = Path(args.manuscript)
    if not manuscript.exists():
        print(f"ERREUR : manuscrit introuvable — {manuscript}")
        sys.exit(1)

    print(f"Lecture de {manuscript}…")
    text     = manuscript.read_text(encoding="utf-8")
    sections = split_sections(text)
    print(f"  {len(sections)} section(s) détectée(s).")

    # ── Dry-run ──────────────────────────────────────────────────────────────────
    if args.dry_run:
        cmd_dry_run(sections, args.limit)
        return

    # ── Clé API requise pour tout le reste ───────────────────────────────────────
    if not args.api_key:
        print(
            "ERREUR : clé API manquante.\n"
            "  → Exporter : export NOTEBOOKLM_API_KEY='AIzaSy...'\n"
            "  → Ou passer : --api-key AIzaSy...\n"
            "  → Obtenir une clé : https://aistudio.google.com/apikey"
        )
        sys.exit(1)

    client = NotebookLMClient(args.api_key)

    # ── Lister les notebooks ──────────────────────────────────────────────────────
    if args.list_notebooks:
        cmd_list_notebooks(client)
        return

    # ── Injection ────────────────────────────────────────────────────────────────
    notebook_id = cmd_inject(
        client      = client,
        sections    = sections,
        notebook_id = args.notebook_id,
        limit       = args.limit,
        skip_existing = args.skip_existing,
    )

    # ── Audio Overview ────────────────────────────────────────────────────────────
    if args.audio_overview:
        print(f"\nDéclenchement de l'Audio Overview…")
        print(f"  Prompt : {args.audio_prompt[:80]}…")
        try:
            ao = client.generate_audio_overview(notebook_id, args.audio_prompt)
            print(f"  → Démarré : {json.dumps(ao, ensure_ascii=False)[:200]}")

            if args.audio_wait:
                print("  Attente de la génération (max 5 min)…")
                result = client.poll_audio_overview(notebook_id)
                audio_url = result.get("audioUrl") or result.get("url", "—")
                print(f"\n  ✓ Audio Overview prêt : {audio_url}")

        except requests.HTTPError as exc:
            print(f"  ✗ Erreur Audio Overview : {exc}")

    # ── Récapitulatif ─────────────────────────────────────────────────────────────
    print(f"\n{'━'*72}")
    print(f"  Notebook ID : {notebook_id}")
    print(f"  URL         : https://notebooklm.google.com/notebook/{notebook_id}")
    print(f"{'━'*72}\n")


if __name__ == "__main__":
    main()
