# Public research dossier

This directory is a static orientation layer for the repository's already
published research. It does not read private evidence, contact a device, run a
proof, or replace the package-specific procedures.

The dossier now presents the live UID-0 mount proof, the source-validated
unmount sink, the static/offline persistence mechanism, the owner-reported
defensive self-heal, the shell-free remediation design, and candidate device
scope as separate evidence classes. It deliberately does not publish the
self-heal delivery payload, target identity, live authorization inputs, or a
reusable privileged-access mechanism.

Preview it from the repository root:

```sh
python3 -m http.server 4173 --directory site
```

Then open <http://127.0.0.1:4173/>. The page needs no build step, package
manager, network request, or JavaScript to expose its content. JavaScript only
enhances the mobile navigation and the clean-checkout
`make -C research/remotepc-cifs-root syntax` copy control.

The typefaces are self-hosted, Latin-subset WOFF2 files under the SIL Open Font
License 1.1. Their provenance and license copies are in `assets/fonts/`.

Keep detailed procedures and current classifications in their canonical
README or report. The dossier should summarize and link to them; it must never
duplicate private identifiers, raw evidence, authorization phrases, or a live
execution path.

The primary reading flow is: bounded result → vulnerable chain → “From sink to
fix” evidence ledger → detailed disclosure/remediation/candidate links → safe
offline check. Run
`python3 -m unittest discover -s site -p 'test_*.py'` after copy or link
changes.
