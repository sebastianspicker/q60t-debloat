# tiz0wn

An evidence-first security research workspace for a personally owned Samsung
GQ55Q60TGUXZG television running `T-NKLDEUC-2743.0`.

This began as a reversible debloating project. Firmware analysis eventually
exposed a much shorter path: Remote PC writes user-controlled SMB credentials,
the privileged CIFS helper substitutes them into a shell command, and the
shipped script executes that command as root. A bounded live validation on
2026-09-27 proved that path with only:

```text
$(/usr/bin/id>/tmp/<fresh-marker>)
```

A fresh two-push classifier proved that the resulting regular file was owned
by UID 0 and began with `uid=0(root) gid=0(root)`. This is a root-command proof
on the assessed build. Retained source also exposes the same shell-evaluation
root cause in the unmount helper. Static firmware evidence and an offline
sandbox establish the *mechanism* by which a root write to persistent `/opt`
content could meet an enabled boot consumer; they do not establish that an
exact boot path was replaceable or that malicious code ran after a TV reboot.

Read [From debloating to tiz0wn](docs/from-debloating-to-tiz0wn.md) for the
project story and
[the Remote PC/CIFS research](research/remotepc-cifs-root/README.md) for the
source trace, offline harness, and guarded reproduction contract. The
[detailed public disclosure](research/remotepc-cifs-root/reports/remote-pc-cifs-command-injection/remote-pc-cifs-command-injection.md)
separates live, source, static/offline, and owner-reported evidence. The
[remediation architecture](research/remotepc-cifs-root/REMEDIATION.md) removes
shell interpretation while preserving valid SMB inputs, and the
[boot-persistence analysis](research/remotepc-cifs-root/BOOT-PERSISTENCE.md)
classifies persistent boot consumers without publishing or installing a hook,
service, or shell.

The owner reports using the vulnerable path once as a self-healing bootstrap
to replace the existing helpers with defensive versions. No independent live
transcript or current device-byte readback is available in this task, so that
statement is not presented as verified device state or a Samsung-issued fix.
No reusable root shell, listener, key, service, implant, or malicious
persistence mechanism was installed or published.

For a concise, visual orientation to the result and its boundaries, preview the
[static public research dossier](site/README.md). It is a zero-dependency
reading layer over the canonical reports and does not contact a device.

## Current results

| Area | Result |
|---|---|
| Reversible debloating | Inventory and one-change-at-a-time tooling; no bulk uninstall list |
| Firmware analysis | Exact 2743.0 image decrypted and statically examined; proprietary firmware is not redistributed |
| Remote PC/CIFS | Password-to-mount command injection demonstrated as UID 0; an equivalent share-name sink is source-validated in unmount, with disconnect timing unresolved |
| One-shot harness | Offline audit and loopback lab complete; the fresh harness finished one terminal live run as `uid0-proof` on 2026-09-28 |
| Persistence research | Persistent `/opt` consumers and the abstract write-to-boot bridge are static/offline-confirmed; malicious post-reboot execution on the TV is not claimed |
| Defensive remediation | Owner reports a one-shot in-place helper replacement; current on-device bytes were not independently read back for this publication |
| Mali CVE-2022-46395 route | Target-specific research remains separate and inconclusive; no Mali root claim |

The [backdoor-risk assessment](docs/backdoor-risk-assessment.md) records which
parts of the persistence chain are proven, modeled, owner-reported, or still
unknown. Evidence classes are deliberately non-interchangeable; a source sink,
an offline mechanism, and a live post-reboot result are different claims.

Samsung support pages map the same public `T-NKLDEUC` package to additional
2020 Q60T/Q6xT and TU8xxx model codes. Those products are
[candidate devices for vendor triage](research/remotepc-cifs-root/CANDIDATE-DEVICES.md),
not claimed affected devices. Regional and adjacent firmware families are a
second, weaker source-lineage lead. Only extracted helper identity and a
reachable call path can expand the affected scope.

## Safe local checks

The Remote PC harness is offline by default. Its default command requires a
separately obtained copy of the exact rootfs tar at the documented private
path. It reads only that local archive and does not load TV configuration,
open a socket, invoke SDB, or start Docker:

```bash
make -C research/remotepc-cifs-root dry-run
make -C research/remotepc-cifs-root lab-test  # services bind to 127.0.0.1
```

The Docker build can download its pinned Debian base and Python dependency. A
fresh build from a frozen, allowlisted source snapshot is mandatory for each
run; the harness verifies source stability around the build, captures its
immutable image ID, checks the embedded snapshot digest, and runs that exact
ID. All lab service and self-test traffic is confined to the Mac. Neither local
mode contacts the TV.

Live mode is deliberately separate. It requires exact target identity and
firmware gates, three authorization phrases, an interactive terminal, two
visual form/session confirmations, one manual Shared Folder click, and one
non-retriable classification. Do not use it on a device you do not own and do
not expose RDP, SMB, SDB, or TV-control ports to the Internet.

## Repository map

| Path | Purpose |
|---|---|
| [`research/remotepc-cifs-root/`](research/remotepc-cifs-root/) | Validated Remote PC/CIFS finding and offline-first one-shot harness |
| [`research/remotepc-cifs-root/REMEDIATION.md`](research/remotepc-cifs-root/REMEDIATION.md) | Compatibility-preserving fix and verification contract |
| [`research/remotepc-cifs-root/CANDIDATE-DEVICES.md`](research/remotepc-cifs-root/CANDIDATE-DEVICES.md) | Official-firmware-based vendor triage candidates, not an affected list |
| [`research/remotepc-cifs-root/hardening/`](research/remotepc-cifs-root/hardening/) | Typed-boundary architectural options and tradeoffs |
| [`docs/firmware-analysis.md`](docs/firmware-analysis.md) | Exact firmware extraction and static-analysis findings |
| [`research/mali-cve-2022-46395/`](research/mali-cve-2022-46395/) | Separate, firmware-bound Mali research and guarded offline tooling |
| [`scripts/`](scripts/) | Explicit-target SDB inventory and one-package removal workflow |
| [`templates/`](templates/) | Baseline, rollback, compatibility, and change records |
| [`evidence/`](evidence/) | Private run output; identifying evidence is gitignored |
| [`site/`](site/) | Static public dossier for the result, evidence chain, and safe offline entry point |

The original research plan remains available at
[`docs/Samsung_Q60T_Debloating_Research_2026-09-25.md`](docs/Samsung_Q60T_Debloating_Research_2026-09-25.md).
Statements in dated checkpoints describe what was known at that time; the
table above is the current project status.

## Safety and scope

- Own device, trusted local network, explicit target only.
- Measure first; make one reversible change at a time.
- Persistence experiments are permitted only as separately authorized,
  target-bound lifecycles with recorded reboot, verification, and recovery
  phases. They must not be inferred from a volatile proof.
- Public material may explain the vulnerability and defensive mechanism, but
  must not publish owner-specific self-heal payloads or reusable privileged
  access.
- Treat IP addresses, DUID/device IDs, tokens, and raw evidence as private; the
  owned-device registry lives in gitignored `private/targets/`.
- Never infer a firmware range from one verified build.
- Do not confuse the disposable RDP host's `q60t` terminal with a TV shell.
- The proof harness leaves target markers and terminal evidence untouched; TV
  profile and allowed-device cleanup are manual and separately documented.

## License

MIT; see [`LICENSE`](LICENSE). Firmware and third-party tools are not
redistributed. Their attribution and licensing are described in
[`NOTICE.md`](NOTICE.md).
