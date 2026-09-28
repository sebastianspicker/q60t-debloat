# Backdoor risk assessment — GQ55Q60TGUXZG / T-NKLDEUC 2743.0

Defensive assessment updated 2026-09-29. It asks what the validated Remote
PC/CIFS root command could lead to, what the firmware and offline models now
show, and what still lacks live evidence. No new device operation was performed
for this assessment.

## Bottom line

- The password-to-mount route executed one bounded command as **UID 0** on the
  exact assessed TV. That is a root-level compromise primitive during the
  configured Shared Folder workflow.
- Retained `mount.smb.sh` and `umount.smb.sh` both turn lower-trust CIFS data
  into root shell source. Mount/password is live-validated. Unmount/share-name
  is source-validated, but its disconnect-time trigger and credential-file
  lifetime remain unresolved.
- Persistent `/opt` storage has enabled services that execute scripts or
  binaries or load environment data from it. The sink-to-consumer bridge works
  in an inert offline model. Exact path replaceability and malicious execution
  after a TV reboot remain unproven.
- The owner reports using the sink once to replace existing helpers with
  defensive versions. There is no separate live transcript or independent
  current-byte readback in this publication. That status is not a Samsung fix
  and is not used as proof that the device is currently remediated.
- No reusable root shell, listener, key, service, implant, or malicious boot
  payload was installed or published.

## Evidence ledger

| Claim | Status | Source |
| --- | --- | --- |
| Password-to-mount command ran as UID 0 | Live-validated once | [Detailed disclosure](../research/remotepc-cifs-root/reports/remote-pc-cifs-command-injection/remote-pc-cifs-command-injection.md) |
| Mount helper contains root command injection | Source-validated and reproduced offline | [Disclosure index](../research/remotepc-cifs-root/DISCLOSURE.md) |
| Unmount helper contains equivalent share-name sink | Source-validated; lifecycle trigger conditional | [Detailed disclosure](../research/remotepc-cifs-root/reports/remote-pc-cifs-command-injection/remote-pc-cifs-command-injection.md) |
| Persistent `/opt` has execution-shaped boot consumers | Static firmware evidence | [Boot-persistence analysis](../research/remotepc-cifs-root/BOOT-PERSISTENCE.md) |
| Sink and boot consumer compose | Inert offline sandbox | [Boot-persistence analysis](../research/remotepc-cifs-root/BOOT-PERSISTENCE.md) |
| Exact boot-consumed path is replaceable on the TV | Unresolved | Runtime DAC, SMACK, mount, integrity, and UEP facts needed |
| Malicious root code ran after TV reboot | Not demonstrated | No live evidence |
| Defensive helper self-heal was applied | Owner-reported | No independent live transcript/current readback |
| Other models are affected | Unknown | [Candidate list](../research/remotepc-cifs-root/CANDIDATE-DEVICES.md) is for triage only |

## Attack chain and preconditions

The demonstrated chain is:

1. A person configures a Remote PC profile using RDP and credentials containing
   shell syntax.
2. The TV connects to an RDP endpoint and an authenticated SMB service.
3. The in-session Shared Folder action causes Remote PC to write credential and
   share values to a temporary file and request a privileged CIFS mount.
4. `mount.smb.sh` substitutes those values into one command string.
5. Root `/bin/bash -c` parses the string before the mount result is known.

These preconditions make the demonstrated route local, configured, and
user-assisted. They do not make shell evaluation safe. A saved-profile
automatic replay, passive network injection, and Internet-reachable trigger
were not established.

The unmount path is separate. Static evidence connects Disconnect to
`umount.smb.sh`, which evaluates the share name through root Bash. Whether a
real session close invokes it while the original file exists is still an open
runtime question. The inspected unmount helper does not substitute the
password, so this is not described as password replay.

## Capability during the session

Root shell evaluation is more powerful than the bounded proof. It can invoke
installed programs, change anything its process label and runtime controls
allow, or stage a larger script. A short input can load longer content, so UI
length limits are not a reliable security boundary. SMB authentication failure
also does not help because command substitution occurs when Bash parses the
command.

The live work deliberately stopped after a fresh identity marker and terminal
classification. Saying “no root shell was installed” describes the experiment,
not a limitation of the vulnerability.

## Reboot persistence: mechanism supported, exploit not demonstrated

A reboot-persistent implant needs both halves:

```text
root write capability + replaceable content consumed at boot
```

The first half exists in the command primitive. Static firmware evidence now
shows the second half in architectural form:

- `/opt` is the persistent data partition, and `/home` aliases into it;
- an enabled root service names `/opt/etc/parseinfo.sh` in `ExecStart`;
- enabled owner services execute scripts or binaries below `/opt/usr/apps`;
- an enabled service loads `/opt/tizen-mobile-ui-sh` as environment data; and
- additional boot logic reads control/data files below
  `/opt/usr/home/owner/share`.

An offline sandbox connected an inert root write to a modeled boot consumer.
That answers “can these two mechanisms compose?” It does not answer whether
the exact TV permits the vulnerable process to replace a named path or whether
the resulting content passes every runtime control.

The missing device facts are path and ancestor ownership/mode, SMACK labels,
effective mount flags, file presence and type, UEP behavior, package integrity,
service enablement, and a fresh boot observation. Until those are collected in
a separately authorized and recoverable lifecycle, persistent attacker
execution remains unproven.

## System-image and runtime integrity nuance

The official archive is signed and its extracted image provides valuable
static integrity evidence. That does not prove the live root filesystem is
immutable after boot. The retained configuration and private remediation
analysis indicate an ext4 root layout used by vendor update mechanics, while
earlier notes described signed/VDFS image constraints. The owner-reported
in-place helper replacement is another reason not to state “root cannot modify
the system” without a current readback.

UEP and SMACK remain meaningful boundaries. UID 0 does not automatically prove
that arbitrary new binaries execute, that every label can write every path, or
that a modified firmware image can be forged. Those controls must be tested at
the exact file and process boundary; they do not erase an already demonstrated
root shell injection.

## Defensive self-heal status

The owner reports that the vulnerable route was used once to install reviewed
replacements over existing privileged helpers. The design was hash-pinned,
reversible, and avoided a new service, listener, key, shell, or boot hook.
Inert root-owned rollback copies may remain.

The available deployment JSON records are from a fake-device test harness, not
a live transcript. The publication therefore does not assert the current TV
hashes. A read-only check should compare the on-device helper hashes with the
reviewed replacements, verify owner/mode/labels and rollback-copy state, reboot
under observation, and confirm ordinary Shared Folder compatibility. That is a
verification task, not permission to redeploy the private payload.

## Residual risk after helper replacement

If the reported replacement is present and correct, the observed mount and
unmount shell sinks are closed on that device. Residual risk still includes:

- compatibility loss from an emergency narrow input allowlist;
- equivalent privileged shell construction elsewhere in the image;
- boot consumers of mutable `/opt` content exposed to another root primitive;
- unknown Samsung update behavior for locally changed helpers and backups; and
- lack of an authoritative vendor-fixed image and version matrix.

The long-term fix is a Samsung firmware update using a typed/direct-argv CIFS
boundary and protected credential handling. The
[remediation architecture](../research/remotepc-cifs-root/REMEDIATION.md) and
[hardening portfolio](../research/remotepc-cifs-root/hardening/hardening.md)
describe that design without narrowing valid SMB character support.

## Owner mitigations

- Disable or avoid Remote PC when it is not needed.
- Remove profiles you did not create and use only trusted RDP/SMB endpoints.
- Keep the TV on a trusted, segmented LAN. Do not forward SMB, RDP, SDB, or TV
  control ports from the Internet.
- Disable Developer Mode when it is not actively required.
- Apply Samsung firmware updates, but do not assume a release fixes this issue
  until Samsung identifies it as fixed or the helper bytes are verified.
- If compromise is suspected, preserve evidence and seek vendor guidance. A
  factory reset may clear user data but is not proven to restore changed system
  helpers or every persistent path.
- Monitor helper hashes and boot-consumed `/opt` content where a safe,
  read-only owner workflow is available.

## Honest limits

One owned device and one exact build were live-tested. Candidate Q6xT/TU8xxx
models share an official firmware signal but have not been independently
validated. The first affected version, complete model range, Samsung-fixed
version, disconnect trigger, exact persistent-path replaceability, and current
post-self-heal device bytes remain unknown.
