# Local web fonts

The public dossier self-hosts only the Latin subsets and weights it uses, so
the page does not contact a font CDN at runtime.

| Family | Files | Source | License |
|---|---|---|---|
| Newsreader | `newsreader-latin-variable.woff2` (200–800) | [Google Fonts](https://fonts.google.com/specimen/Newsreader) | SIL Open Font License 1.1; see `OFL-Newsreader.txt` |
| IBM Plex Mono | `ibm-plex-mono-latin-400.woff2`, `ibm-plex-mono-latin-500.woff2` | [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Mono) | SIL Open Font License 1.1; see `OFL-IBM-Plex-Mono.txt` |

The CSS uses `font-display: swap` and declares stable fallback families.
