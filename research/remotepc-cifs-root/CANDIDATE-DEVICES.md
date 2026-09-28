# Candidate device scope for vendor triage

Only `GQ55Q60TGUXZG` running `T-NKLDEUC-2743.0` has been live-validated. This
page is a research-based triage list, not an affected-products declaration.
Samsung should use its build manifest and source history to determine the real
range.

## Why firmware mapping is useful but not conclusive

Samsung's official support pages associate many 2020 model codes with one
download artifact. A model served the same `T-NKLDEUC.zip` version and download
path is a strong candidate to contain the same retained helpers. It still may
differ in feature flags, installed packages, Remote PC availability, caller
policy, regional configuration, or runtime reachability. A related firmware
family may share source without sharing the vulnerable bytes.

The minimum vendor check for every candidate is:

1. Does the image contain `mount.smb.sh` or `umount.smb.sh` with a constructed
   string passed to `bash -c`, `sh -c`, or `eval`?
2. Does the Remote PC launcher write lower-trust credential or share data to
   the file those helpers read?
3. Can the product's privileged policy route a legitimate Remote PC caller to
   either helper?
4. Which user action or lifecycle event reaches mount and unmount?
5. Does the release already contain a shell-free replacement?

## Tier 1: same public European firmware artifact

As observed on 2026-09-29, the following representative official support pages
offered `T-NKLDEUC.zip`; several exposed the same 2743.0 download path used for
the assessed family. Screen sizes and regional suffixes should be expanded from
Samsung's internal firmware-to-model manifest.

| Candidate family | Representative official model | Why it is a priority |
| --- | --- | --- |
| Q60T | [GQ55Q60TGUXZG](https://www.samsung.com/de/support/model/GQ55Q60TGUXZG/) | Exact validated model family and firmware identifier |
| Q64T | [GQ55Q64TGUXZG](https://www.samsung.com/de/support/model/GQ55Q64TGUXZG/) | Official page distributes `T-NKLDEUC.zip` |
| Q65T | [QE65Q65TAUXXU](https://www.samsung.com/ie/support/model/QE65Q65TAUXXU/) | Official page distributes `T-NKLDEUC.zip` |
| Q67T | [QE50Q67TASXXN](https://www.samsung.com/be/support/model/QE50Q67TASXXN/) | Official page distributes `T-NKLDEUC.zip` |
| TU8000 and regional TU80xx derivatives | [UE82TU8000KXXU](https://www.samsung.com/ie/support/model/UE82TU8000KXXU/), [GU55TU8079UXZG](https://www.samsung.com/cz/support/model/GU55TU8079UXZG/) | Official pages distribute `T-NKLDEUC.zip` |
| TU8305 | [UE55TU8305KXXC](https://www.samsung.com/dk/support/model/UE55TU8305KXXC/) | Official page distributes `T-NKLDEUC.zip` |
| TU8500 and regional TU85xx derivatives | [UE55TU8500UXXU](https://www.samsung.com/uk/support/model/UE55TU8500UXXU/), [UE50TU8505UXXC](https://www.samsung.com/es/support/model/UE50TU8505UXXC/), [GU55TU8509UXZG](https://www.samsung.com/de/support/model/GU55TU8509UXZG/) | Official pages distribute `T-NKLDEUC.zip` |

If these pages resolve to the byte-identical archive whose SHA-256 is
`cb717ed98daf9580eb5b84bccbad5adac82f75dd021ed028f1ee1bb6c4abde32`,
then the vulnerable helper bytes are expected to be identical as well. That
archive identity should be verified rather than inferred from filename and
version alone.

## Tier 2: regional or adjacent 2020 branches

These are source-lineage candidates. They should be searched and diffed, but
the public evidence does not show that they carry either sink.

| Candidate family | Official firmware signal | Vendor question |
| --- | --- | --- |
| North American Q60T and TU8000 | [QN85Q60TAFXZC](https://www.samsung.com/ca/support/model/QN85Q60TAFXZC/) and [UN55TU8000FXZC](https://www.samsung.com/ca_fr/support/model/UN55TU8000FXZC/) receive `T-NKLAKUC` 2743.0 | Does this regional branch share the privileged-service helpers and Remote PC call path? |
| Asia/MENA Q60T | [QA55Q60TAUXTW](https://www.samsung.com/levant/support/model/QA55Q60TAUXTW/) receives `T-NKLUABC` 2743.0 | Are the same helper sources, policies, and feature packages built into this branch? |
| European Q70T/Q80T/Q90T | [QE55Q70TATXXH](https://www.samsung.com/at/support/model/QE55Q70TATXXH/), [QE55Q80TATXXH](https://www.samsung.com/uk/support/model/QE55Q80TATXXH/), and [QE75Q90TALXXN](https://www.samsung.com/nl/support/model/QE75Q90TALXXN/) receive `T-NKMDEUC` 2743.0 | Was the CIFS helper source shared with `T-NKLDEUC`? |
| European TU7000 | [UE55TU7000KXXU](https://www.samsung.com/hu/support/model/UE55TU7000KXXU/) receives `T-KTSU2DEUC` 2743.0 | Does the lower branch ship Remote PC and either helper at all? |

The version number `2743.0` alone is not evidence of shared vulnerable code.
The same-family package mapping is the stronger lead; extracted helper hash,
call-path reachability, and product behavior are the deciding evidence.

## Public claim boundary

The project continues to claim one affected product/build only. Candidate
families are published so owners and Samsung can prioritize inspection, not so
the single-device result is generalized. A model should move into the affected
list only after Samsung or an authorized owner verifies the vulnerable helper
bytes and reachable Remote PC path on that exact firmware.
