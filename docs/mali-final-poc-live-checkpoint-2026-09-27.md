# Q60T Mali final-PoC live checkpoint — 2026-09-27

## Outcome

The owner explicitly acknowledged disposable/recoverable-target risk while the
assessed GQ55Q60TGUXZG TV was running. The bounded CVE-2021-44828 validator and
the CVE-2022-46395 credential PoC were each given a fresh, target-bound signed
WGT transport and a fail-closed device-free prerequisite.

Neither active Mali mode ran. Both final transports installed and attested
their exact managed payloads, but `/usr/bin/dotnet-launcher-inhouse` returned
zero with empty redirected output and did not create the required exclusive
preflight proof. Each host runner stopped at that proof gate, before its sole
detached active-launch gate. There is therefore no observed root access and no
`vulnerable` or `not_observed` classification for CVE-2021-44828.

## CVE-2021-44828 managed validator

- Candidate archive:
  `q60t-jit-write-netcoreapp2.2-candidate-run-v2-20260927.tar.gz`
- Archive SHA-256:
  `de2c4a866e5123940de01157890f0a8fd66d4cb3b4fb98a33d3a9f0e21f17a91`
- Managed DLL SHA-256:
  `9b1cb9e463e363707ad99b85b38c8b1f2e9b30d86a40214a910d6b0120b7791b`
- Package/application: `q60t04482n` / `q60t04482n.transport`
- Signed WGT SHA-256:
  `5acf2dbc0cd0c829b1bdf8f1568e36dd64ec7ce3b008f59b163b1e1cee6c9836`
- Retained stage:
  `/home/owner/share/tmp/sdk_tools/q60t-jm-5acf2dbc0cd0c829-v4`

The package-absence, target-profile, install transcript, installed-member,
copied-member, and launcher-completion gates passed. Read-only postmortem
predicates established:

- `preflight-completed` exists;
- `preflight-exit.txt` is exactly `0`;
- `preflight.txt` is a regular empty file;
- `Q60T.JitWriteProbe.selftest-started`, `.selftest-validated`, and
  `.selftest-ok` are all absent; and
- the active `completed` directory and `Q60T.JitWriteProbe.result` are absent.

Thus the host never launched `--probe-jit-write-proof`, and this route did not
open `/dev/mali0` or issue a Mali ioctl. Package `q60t04482n` and the stage are
terminal retained state. The earlier managed package `q60t04482m` and native
package `q60t044828` are also retained and must not be retried or automatically
removed.

## CVE-2022-46395 final credential PoC

- Candidate archive:
  `q60t-mali-poc-netcoreapp2.2-candidate-durable-proof-20260927.tar.gz`
- Archive SHA-256:
  `da9ae11ccec1750d6a28e894e1ffd3900323253e37bc4a052c19759479acfd8d`
- Managed DLL SHA-256:
  `103c205dd1b6ba19ba11ae621f442608e7d7aa9a841e117ffd52eead48a1a5f3`
- Package/application: `q60t046395` / `q60t046395.transport`
- Signed WGT SHA-256:
  `6214cbb6eabe647af0306b4a0739076044924431e760f51f75429bdd0a813b56`
- Retained credential stage:
  `/home/owner/share/tmp/sdk_tools/q60t-m-6214cbb6eabe647a-c-v1`

The package-absence, install transcript, installed-member, copied-member, and
launcher-completion gates passed. Read-only postmortem predicates established:

- `preflight-completed` exists;
- `preflight-exit.txt` is exactly `0`;
- `preflight.txt` is a regular empty file;
- `Q60T.MaliChain.preflight-ok` is absent; and
- `completed`, `Q60T.MaliChain.result`, `Q60T.MaliChain.attempted`, and
  `Q60T.MaliChain.entered` are all absent.

The permanent attempt marker is written by the managed supervisor before its
fork. Its absence, together with the host launch gate never being reached,
establishes that the credential supervisor was not invoked. No EGL setup,
Mali open, race, reclaim, PTE operation, physical scan, credential mutation,
or transient UID/GID/capability proof ran.

## Artifact and tool boundary

Both deployed WGTs were signed through the pinned Tizen Studio
`tools/tizen-core/tz` executable, SHA-256
`fc88160a1e2d7ee0ce6d2fd821d821bf4c421c698c53ba1534b7643ba6034cb2`.
An earlier host-only signing diagnostic used the incompatible legacy
`tools/ide/bin/tizen` front end; that WGT was never supplied to a live runner
and its persistent artifact is explicitly marked superseded. A subsequent
live command using that legacy executable failed its local SHA-256 gate before
creating a TV stage or installing a package.

The TV's Developer Mode identity, configured host IP, exact SDB serial/model,
kernel, driver, library, launcher hashes, and `/dev/mali0` type were guarded as
documented by the deployers. Device-private identifiers are intentionally not
recorded here.

## Retention rule

Do not rerun either live command, reuse either stage, delete those stages, or
uninstall the retained packages automatically. A missing proof is terminal by
design because launcher/process state cannot be inferred safely from its zero
status. Cleanup, if ever desired, is a separate manually authorized operation.
