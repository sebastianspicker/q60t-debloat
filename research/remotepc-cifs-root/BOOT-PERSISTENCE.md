# Boot-persistence establishment and defense

Status: static firmware analysis identifies enabled consumers of persistent
`/opt` content, and an inert offline model composes an abstract root write with
a boot consumer. Exact on-device path replaceability and malicious post-reboot
execution remain unproven. No boot hook, service, shell, or executable canary is
published or installed by this work.

This document answers the open questions in
[`docs/backdoor-risk-assessment.md`](../../docs/backdoor-risk-assessment.md).
It is an analysis and establishment guide for the persistence surface. This
public document stops at static and offline evidence; any later device proof
requires separate authorization, exact target binding, and a tested recovery
procedure.

## The establishment question

Post-reboot execution requires more than the volatile `uid0-proof`: an exact
path on persistent storage must be replaceable from the sink's runtime context,
a boot consumer must execute or interpret that path, and the modified content
must pass DAC, SMACK, mount, UEP, and integrity controls. The evidence-shaped
question is therefore:

> Is there a replaceable path on a reboot-surviving mount whose **content** a
> boot-time consumer executes, sources, or injects as environment under the
> target's effective runtime controls?

If all of those links hold, the architecture can support reboot-persistent
execution because content at the referenced path is consumed by the firmware's
own boot logic. A static reference alone does not answer the replaceability or
runtime-policy questions. If no reviewed reference exists, persistence through
this route is not established for the reviewed surfaces.

The current static answer is “execution-shaped consumers exist.” Enabled units
name `/opt/etc/parseinfo.sh`, scripts and binaries below `/opt/usr/apps`, and
the `/opt/tizen-mobile-ui-sh` environment file. The current live answer is
still narrower: this publication has not established that the vulnerable
process could replace any exact consumer and has not observed malicious content
execute after reboot.

An independent retained-firmware sweep found three additional high-value
consumers. These are static sink inventory, not proof that their `/opt` targets
exist or can be replaced on the TV:

| Consumer | Persistent input | Privilege and trigger | Evidence boundary |
|---|---|---|---|
| `bm_init.sh` under PID 1 | `/opt/etc/BM/config_jbm` gates `/opt/data/BM/JBM/sys/init/jbm_init.sh` | Root during early boot | Both paths are named statically; runtime presence, ownership, label, and replaceability are unknown |
| `init.wrapper` | `/opt/data/DeviceTracker/Dlog_buffer.sh` | Root on normal boot | Direct boot execution is present in retained source; target state is unknown |
| joystick udev rule | `/opt/accessory/gamepad-service.sh` | Root on matching add/remove hotplug | Static root execution on the event; `/opt` writeability for the relevant context is unknown |

The same sweep found root-run setcap units and services that environment-load
other `/opt` content. Those are additional reasons to protect persistent data,
but they are not promoted here into live exploit findings.

The repository already records one ground-truth boot-processed writable path.
Firmware finding F15 (`docs/firmware-analysis.md`) shows
`com.samsung.tv.multiscreen.service` suppresses startup when
`/home/owner/share/multiviewnotsupport` exists, and that the directory is
writable by `sdk`. That is a writable, boot-processed survivor — but it is an
**existence condition**, not content execution. It proves user data reaches
boot logic; it does not by itself give execution.

## Read-only audit method

A bounded read-only survey would read `/proc/self/mounts`, keep only writable,
non-volatile survivor mounts, and inspect a reviewed list of boot surfaces for
references into those mounts. For this target, `/opt` is the candidate survivor;
because the rootfs also spells that partition `/home` through the
`/home -> /opt/usr/home` alias, both spellings must resolve to the same mount.
A bounded search should also cover file shapes a boot consumer can load
directly (`.profile`, `.bashrc`, `.bash_profile`, `.xprofile`, `.xsession`, user
`systemd` units, and XDG autostart `.desktop` files). A referenced path counts
as execution only when it is the command a boot consumer runs or sources; a
path that is merely an argument to a data command (`echo`, `find`, …) is a
read. Classify every reference:

| Classification | Meaning | Persistence value |
|---|---|---|
| `executes` | a boot consumer runs or sources the referenced file | **direct execution** |
| `environment-file` | a boot consumer loads the file as environment | **environment injection** (e.g. `LD_PRELOAD`, `PATH`) |
| `condition-exists` | an existence/writeability condition only | control (enable/disable, DoS), not execution |
| `reads-data` | the path is an argument or parsed data | data influence only |
| `unclassified` | a directive this analysis does not model | manual review required |

The reduced public release intentionally does not expose an owner-specific live
collector, authorization phrase, or canary action. A vendor or authorized
assessor can implement the method above as a read-only collector that never
creates, removes, or modifies a target file and stores its report outside the
public repository.

### Verdicts

| Verdict | Meaning | Defense action |
|---|---|---|
| `system-volume-writable` | a boot-relevant system mount (`/`, `/etc`, `/usr`, `/lib`, …) is writable at runtime | record the mount and vendor update/integrity policy; writeability alone does not establish an integrity bypass |
| `execution-reachable` | a boot consumer executes or environment-injects a file under a writable survivor | preserve evidence, escalate for vendor hardening, and avoid disruptive owner changes without a tested rollback |
| `unclassified-reference` | an unmodeled directive references a writable survivor | manual review before any conclusion |
| `no-execution-reference` | no reviewed surface executes or injects a writable survivor | persistence not established through this route; keep the referenced paths monitored |

`no-execution-reference` narrows the open question. It is **not** proof that no
persistence mechanism exists: the audit covers a fixed surface list, a bounded
`find` with a fixed name/glob set inside each survivor, and only paths the
target's own mount table marks writable and non-volatile.

## Relationship to a persistence proof

A non-executable root-written data file surviving one reboot would establish
only a persistent root-originated filesystem modification. The boot audit is
the execution-shaped companion: it finds the mechanism that could turn
surviving bytes into code execution.

If the audit returns `execution-reachable`, the finding already establishes the
mechanism from the firmware's own boot configuration; a marker confirmation is
a bounded follow-up, not a prerequisite. If the audit returns
`no-execution-reference`, there is no reviewed candidate for a marker canary and
none should be invented.

## Why the audit remains read-only

The audit does not alter the target because it is intended to establish the
mechanism before a separately authorized persistence proof. A persistent
canary, hook, or access mechanism must be evaluated against the exact target,
with explicit owner authorization, phase-bound evidence, and a tested recovery
path. The audit's read-only status is an action boundary, not a repository-wide
ban on persistence research.

## Research questions and status

These five questions bound continued authorized research. They are not
positive findings or permission to bypass exact-target, evidence, and recovery
gates.

| Question | Current status |
|---|---|
| 1. Persistent, reboot-surviving modification | Persistent `/opt` storage is static-confirmed. No persistent canary was run. The owner separately reports a defensive in-place helper replacement, without an independent current-byte readback here. |
| 2. Root code execution after reboot | Not proven on the TV; `/opt` execution-shaped consumers and the abstract bridge are static/offline-confirmed, while exact path replaceability is unresolved. |
| 3. Reusable root shell / SDB backdoor | Deliberately not installed, tested, or published. |
| 4. Firmware/system modification | No flash image was modified. Existing root-owned helpers were reportedly replaced for defense; that device state is not independently verified in this publication. |
| 5. Affected versions beyond 2743.0 | Unknown |

The owner-reported self-heal is not a persistence proof. It used the sink as a
one-shot maintenance bootstrap and reportedly replaced vulnerable files with
defensive files; it did not add an access mechanism. Conversely, its reported
success is evidence that “signed archive” must not be treated as proof of
runtime filesystem immutability without direct readback.

## Defense playbook

For the owner of an affected set:

1. Have Samsung or an authorized assessor apply the read-only audit method to
   the exact build and record the verdict.
2. If `execution-reachable`, preserve the evidence and treat the path as a
   vendor-hardening escalation. Do not remove a referenced file or disable a
   service solely from the audit result; either action can break normal TV
   behavior. Prefer a vendor image that relocates or integrity-protects the
   consumer. Any owner mitigation needs an exact backup, a tested rollback,
   and a post-change compatibility check before the audit is re-run.
3. Watch the writable survivors and any referenced path for unexpected files
   and permission changes, recording every exact path reviewed.
4. Keep the TV on a trusted, segmented LAN; keep SDB (26101), RDP (3389), SMB
   (445), and control ports off the Internet. Developer Mode is the confirmed
   SDB execution path — disable it when not in use.
5. Do not treat a factory reset as a proven fix for this mechanism. A reset may
   clear user-data state, but this work has not shown that it restores changed
   root-owned helpers or every surviving path. The
   `system-volume-writable` and `execution-reachable` verdicts help scope that
   question.
6. Re-run the audit after every firmware update; the result is bound to one
   exact build and says nothing about another.

## Offline validation

```bash
make -C research/remotepc-cifs-root syntax
make -C research/remotepc-cifs-root dry-run    # requires the pinned local rootfs
make -C research/remotepc-cifs-root lab-test   # loopback only; no TV
git diff --check
```

These commands validate the public harness syntax, pinned firmware anchors,
and loopback RDP/SMB behavior. They do not claim to run the conceptual boot
audit or contact the TV.
