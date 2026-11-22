#!/usr/bin/env python3
"""Lightweight checks for NEXO's static web app. Uses only Python's standard library and Node.js."""
from html.parser import HTMLParser
from pathlib import Path
import json
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = ROOT / "index.html"
errors = []
inline_scripts = []


class AppHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_script = False
        self.current_script = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script":
            self.in_script = not bool(attrs.get("src"))
            self.current_script = []
            if attrs.get("src"):
                check_local_reference(attrs["src"], f"<script src>")
        for attr in ("href", "src"):
            value = attrs.get(attr)
            if not value:
                continue
            if tag == "script" and attr == "src":
                continue
            if tag == "link" and attr == "href":
                rel = attrs.get("rel", "").lower()
                if "stylesheet" not in rel and "icon" not in rel and "manifest" not in rel:
                    continue
            check_local_reference(value, f"<{tag} {attr}>")

    def handle_data(self, data):
        if self.in_script:
            self.current_script.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_script:
            inline_scripts.append("".join(self.current_script))
            self.in_script = False
            self.current_script = []


def check_local_reference(value, source):
    value = value.strip()
    parsed = urlsplit(value)
    if not value or parsed.scheme or parsed.netloc or value.startswith(("#", "data:", "javascript:")):
        return
    path = parsed.path
    if not path:
        return
    candidate = (ROOT / path.lstrip("/")).resolve()
    if not candidate.exists():
        errors.append(f"{source} apunta a un archivo inexistente: {value}")


if not HTML_FILE.is_file():
    print("ERROR: falta index.html")
    sys.exit(1)

parser = AppHTMLParser()
parser.feed(HTML_FILE.read_text(encoding="utf-8"))
parser.close()

manifest_file = ROOT / "manifest.webmanifest"
if manifest_file.exists():
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        for icon in manifest.get("icons", []):
            if icon.get("src"):
                check_local_reference(icon["src"], "manifest icon")
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"manifest.webmanifest no es JSON válido: {exc}")
else:
    errors.append("Falta manifest.webmanifest")

node = subprocess.run(["node", "--version"], capture_output=True, text=True)
if node.returncode != 0:
    errors.append("Node.js es necesario para comprobar la sintaxis de JavaScript.")
else:
    with tempfile.TemporaryDirectory(prefix="nexo-check-") as temp_dir:
        for index, source in enumerate(inline_scripts, start=1):
            if not source.strip():
                continue
            js_file = Path(temp_dir) / f"inline-{index}.js"
            js_file.write_text(source, encoding="utf-8")
            result = subprocess.run(
                ["node", "--check", str(js_file)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                detail = (result.stderr or result.stdout).strip()
                errors.append(f"JavaScript inline #{index}: {detail}")

if errors:
    print("NEXO: VALIDACIÓN FALLIDA")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("NEXO: validación estática correcta")
print(f"- index.html leído")
print(f"- {len(inline_scripts)} bloques inline de JavaScript comprobados")
print("- referencias locales del HTML verificadas")
print("- manifest.webmanifest validado")
print("- sintaxis JavaScript comprobada con Node.js")
