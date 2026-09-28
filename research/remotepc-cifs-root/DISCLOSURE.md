# Remote PC/CIFS command injection disclosure

Samsung Smart TV model `GQ55Q60TGUXZG` running
`T-NKLDEUC-2743.0` was live-validated with a bounded Remote PC/CIFS proof:
credential text reached a privileged mount helper and executed one command as
UID 0. The same unsafe shell-evaluation pattern is present in the corresponding
unmount helper, although its disconnect-time reachability remains conditional.

The complete public report is
[Remote PC CIFS credential command injection](reports/remote-pc-cifs-command-injection/remote-pc-cifs-command-injection.md).
It separates four evidence classes that must not be conflated:

- **Live-validated:** the password-to-mount route executed a bounded identity
  marker as UID 0 on one owned TV.
- **Source-validated:** both retained helpers turn lower-trust CIFS data into
  root shell source.
- **Static and offline:** persistent `/opt` storage has enabled boot consumers,
  and a sandbox reproduced the sink-to-consumer mechanism. Exact on-device
  path replaceability and post-reboot execution were not demonstrated.
- **Owner-reported:** an authorized one-shot self-heal replaced existing
  helpers on the owned TV. This task has no independent post-change device
  readback, so the current device bytes are not claimed as verified here.

No reusable root shell, listener, key, service, implant, or malicious
persistence mechanism was installed or published. The original root proof and
the later defensive self-heal are separate events: the first changed only a
volatile marker; the second reportedly changed existing helper files to close
the sink.

See also:

- [Remediation architecture](REMEDIATION.md)
- [Boot-persistence evidence and limits](BOOT-PERSISTENCE.md)
- [Candidate devices for vendor triage](CANDIDATE-DEVICES.md)
- [Hardening portfolio](hardening/hardening.md)
- [Research harness and evidence contract](README.md)

Only the exact assessed firmware is within the verified affected scope. Other
models, earlier releases, backports, and a vendor-fixed release remain unknown.
