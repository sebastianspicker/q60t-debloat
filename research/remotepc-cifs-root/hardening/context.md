# Hardening analysis context

Analysis ID: `hardening_20260929_remotepc_cifs`
Source root: repository root
Collection SHA-256:
`26820c6c2533ff06e5a7f6f788e4338ba60f9d55be6fe8e54724d9ae02a7c18b`

The collection digest covers eight inputs selected before the public analysis
was written: the then-current public disclosure, the two retained vulnerable
helpers, the private persistence and hardening analyses, and three offline JSON
manifests. The disclosure subsequently changed as an output of this work, so
`sourceDrift` is recorded as `present`. The retained helper hashes and offline
results used for the diagnosis did not change.

The completed standard security scan was
`5fb49241-83a9-4e8f-a718-a56a41097f3f`. It validated the mount-helper finding
and the separate unmount-helper sink. This proposal treats them as one
structural opportunity because both arise from the same stringly privileged
boundary.

## Evidence registry

| ID | Kind | Evidence | Claim boundary |
| --- | --- | --- | --- |
| `E1` | Live validation | Bounded Remote PC password-to-mount run | One credential-derived command executed as UID 0; no shell or persistence was installed. |
| `E2` | Retained source | `mount.smb.sh` SHA-256 `37aaf2f05bf714332a6bf8f14b543ac9584a1b9a051341674a74fc0dd753c57e` | Credential and share data are substituted into a root `bash -c` command. |
| `E3` | Retained source | `umount.smb.sh` SHA-256 `d0dffdaedd33243445a85019cbfadb8d281ab48d29b7a68d7eedec7f13ccc782` | Share data reaches an independent root `bash -c`; disconnect timing is unverified. |
| `E4` | Static analysis and offline experiment | Persistent `/opt` consumers and sandbox reproduction | A root-write-to-boot-consumer mechanism exists in the model; exact on-device replaceability and post-reboot execution are unresolved. |
| `E5` | Owner report | One-shot defensive helper replacement | The self-heal was reportedly applied; there is no independent live transcript or current byte readback in this task. |

## Constraints used in the analysis

- Preserve the supported SMB username, password, share-name, dialect, and
  lifecycle behavior rather than treating shell punctuation as invalid by
  default.
- Fix mount and unmount together and define credential-file lifetime across
  disconnect.
- Keep private target identity, authorization phrases, and remediation payload
  out of distributable artifacts.
- Do not infer an affected-version range or a vendor-fixed release.
- Treat `/opt` hardening as defense in depth unless runtime path replaceability
  is separately established.
- No latency, memory, availability, or compatibility measurements were supplied;
  resource effects below are source-derived or hypothetical and include plans
  to measure them.
