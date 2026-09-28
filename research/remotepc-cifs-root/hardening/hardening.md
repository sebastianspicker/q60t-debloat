# Security Hardening Review: Remote PC/CIFS privileged boundary

## Evidence Basis

I reviewed the public live-proof record, the retained 2743.0 mount and unmount
helpers, the static `/opt` consumer analysis, the offline behavioral checks,
and the owner-reported self-heal status. The collection is bound in
[`hardening.json`](hardening.json); [`context.md`](context.md) records its
evidence IDs and drift note.

The strongest facts are narrow but decisive: the mount route executed one
credential-derived command as UID 0, and both retained helpers independently
pass constructed text to a root shell. Static and offline evidence supports a
persistence mechanism, but not malicious post-reboot execution on the TV. The
owner reports applying a defensive one-shot replacement, but this analysis did
not independently read back the current device bytes.

## Constraints

We must close mount and disconnect without shrinking legitimate SMB
functionality. Valid spaces, Unicode, and punctuation need to remain data; a
shell-character blacklist is not a sound product contract. Private target
identity, authorization phrases, and the self-heal payload are outside the
public artifact. No performance or memory measurements were available, so the
proposal names measurement plans instead of presenting estimates as results.

## Opportunity Portfolio

| Opportunity | Evidence | Options | Recommendation | Proposal |
| --- | --- | --- | --- | --- |
| Make privileged CIFS operations typed and shell-free | Live UID-0 mount proof, two retained root shell sinks, static/offline `/opt` bridge (`E1`–`E4`) | Direct-argv helpers; typed privileged API; isolated broker | Ship the direct-argv repair immediately, then adopt the typed API; use a broker only if broader containment warrants its cost | [Typed CIFS boundary](proposals/typed-cifs-boundary.md) |

## Recommendation Summary

I recommend Option 2, a typed privileged API, as the durable vendor design.
It puts schema validation, canonical target policy, credential lifetime,
process creation, and disconnect state under one owner. That eliminates the
structural gap in which one component validates a template and another later
turns file contents into code.

Option 1 remains necessary as the tactical repair and is proportionate for an
emergency update. It should preserve credentials out of band and execute a
fixed utility directly, not reject broad character classes. Option 3 is the
strongest containment design, but a resident broker and mount namespace add
recovery, policy, resource, and rollout work. It becomes preferable if Samsung
finds other risky privileged CIFS parsers or needs to contain a compromise
beyond this injection class.

The `/opt` consumer issue is complementary: closing the Remote PC sink removes
this entry point, while integrity and label controls keep a different future
root primitive from converting persistent data into boot execution.

## Next Decisions

- Confirm the supported SMB character, length, and normalization contract.
- Select the protected credential interface available in the shipped CIFS
  stack.
- Establish disconnect timing and one owner for temporary-file deletion.
- Decide whether the typed API replaces the old method in one image or through
  a short, instrumented compatibility window.
- Measure representative mount latency, resource use, and failure recovery for
  the selected option.
- Audit runtime ownership, labels, writeability, and integrity of enabled
  `/opt` consumers on representative devices.
