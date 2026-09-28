from __future__ import annotations

import re
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SITE_ROOT = Path(__file__).resolve().parent
INDEX = SITE_ROOT / "index.html"
STYLES = SITE_ROOT / "styles.css"
SCRIPT = SITE_ROOT / "site.js"


class SiteDocument(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.counts: Counter[str] = Counter()
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.resources: list[str] = []
        self.id_references: list[str] = []
        self.svg_without_hidden_state: list[dict[str, str]] = []
        self.buttons_without_type: list[dict[str, str]] = []
        self.text: list[str] = []

    def handle_starttag(
        self, tag: str, attributes: list[tuple[str, str | None]]
    ) -> None:
        attrs = {name: value or "" for name, value in attributes}
        self.counts[tag] += 1

        if identifier := attrs.get("id"):
            self.ids.append(identifier)

        if tag == "a" and (href := attrs.get("href")):
            self.hrefs.append(href)
        elif tag == "link" and (href := attrs.get("href")):
            self.resources.append(href)
        elif tag == "script" and (source := attrs.get("src")):
            self.resources.append(source)

        for name in ("aria-labelledby", "aria-describedby", "aria-controls"):
            self.id_references.extend(attrs.get(name, "").split())

        if tag == "svg" and attrs.get("aria-hidden") != "true":
            self.svg_without_hidden_state.append(attrs)
        if tag == "button" and not attrs.get("type"):
            self.buttons_without_type.append(attrs)

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if stripped:
            self.text.append(stripped)


class PublicDossierContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.css = STYLES.read_text(encoding="utf-8")
        cls.javascript = SCRIPT.read_text(encoding="utf-8")
        cls.document = SiteDocument()
        cls.document.feed(cls.html)
        cls.visible_text = " ".join(
            " ".join(fragment.split()) for fragment in cls.document.text
        )

    def test_semantic_landmarks_and_unique_ids(self) -> None:
        self.assertEqual(self.document.counts["h1"], 1)
        for landmark in ("header", "nav", "main", "footer"):
            self.assertGreaterEqual(self.document.counts[landmark], 1)
        self.assertEqual(len(self.document.ids), len(set(self.document.ids)))
        self.assertEqual(self.document.svg_without_hidden_state, [])
        self.assertEqual(self.document.buttons_without_type, [])
        self.assertIn('<main id="main-content" tabindex="-1">', self.html)

    def test_internal_references_resolve(self) -> None:
        identifiers = set(self.document.ids)
        for href in self.document.hrefs:
            if href.startswith("#"):
                self.assertIn(href.removeprefix("#"), identifiers)
            elif urlparse(href).scheme:
                self.assertEqual(urlparse(href).scheme, "https")
        self.assertLessEqual(set(self.document.id_references), identifiers)

    def test_runtime_assets_are_local_and_present(self) -> None:
        for resource in self.document.resources:
            self.assertFalse(urlparse(resource).scheme, resource)
            self.assertTrue((SITE_ROOT / resource).is_file(), resource)

        font_urls = re.findall(r"url\([\"']?([^\"')]+)", self.css)
        self.assertGreaterEqual(len(font_urls), 3)
        for resource in font_urls:
            self.assertFalse(urlparse(resource).scheme, resource)
            self.assertTrue((SITE_ROOT / resource).is_file(), resource)

        self.assertNotRegex(self.css, r"@import\s")
        for network_api in ("fetch(", "XMLHttpRequest", "WebSocket"):
            self.assertNotIn(network_api, self.javascript)

    def test_font_licenses_are_retained(self) -> None:
        for name in ("OFL-Newsreader.txt", "OFL-IBM-Plex-Mono.txt"):
            license_text = (SITE_ROOT / "assets/fonts" / name).read_text(
                encoding="utf-8"
            )
            self.assertIn("SIL OPEN FONT LICENSE", license_text.upper())

    def test_exact_scope_and_claim_limits_are_visible(self) -> None:
        expected = (
            "GQ55Q60TGUXZG",
            "T-NKLDEUC-2743.0",
            "uid=0(root) gid=0(root)",
            "Persistence mechanism modeled",
            "No reusable root shell installed",
            "Owner-reported helper remediation",
            "No affected-version range",
            "Keep the data. Remove the interpreter.",
            "Mount live · unmount source-validated",
            "This project is not affiliated with or endorsed by Samsung.",
        )
        for statement in expected:
            self.assertIn(statement, self.visible_text)

    def test_dossier_does_not_publish_private_or_live_inputs(self) -> None:
        for forbidden in (
            "TV_SERIAL=",
            "TV_ID_SHA256",
            "config/tv.env",
            "evidence/runs",
            "--live",
            "--confirm",
            "I-AUTHORIZE-",
            "payload.py",
            "serve.py",
            ".pre-root-sink-fix",
            "18080",
        ):
            self.assertNotIn(forbidden, self.html)

    def test_current_public_research_links_are_present(self) -> None:
        expected_paths = (
            "research/remotepc-cifs-root/reports/remote-pc-cifs-command-injection/remote-pc-cifs-command-injection.md",
            "research/remotepc-cifs-root/REMEDIATION.md",
            "research/remotepc-cifs-root/CANDIDATE-DEVICES.md",
            "research/remotepc-cifs-root/BOOT-PERSISTENCE.md",
        )
        for path in expected_paths:
            self.assertIn(path, self.html)

    def test_copy_control_contains_only_the_offline_check(self) -> None:
        self.assertIn(
            'id="safe-check-command">make -C research/remotepc-cifs-root syntax</code>',
            self.html,
        )
        self.assertEqual(self.html.count('data-copy-target="safe-check-command"'), 1)
        self.assertNotIn("button.disabled", self.javascript)
        self.assertIn('button.setAttribute("aria-busy", "true")', self.javascript)
        self.assertIn("previousFocus.focus({ preventScroll: true })", self.javascript)


if __name__ == "__main__":
    unittest.main()
