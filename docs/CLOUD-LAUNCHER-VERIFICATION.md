# Cloud launcher preparation receipt — 14 November 2026

Base: `ed82d0032d19c453c422ae10716716e1d74f9959` (`main`).

Prepared in the existing managed Codex Cloud runtime, provider `cloud`, actual
Linux executor; no owner's computer or real model invocation was used.
The change retains the single-story `CLAUDE.md` prompt and appends the Cloud
execution/release contract. The launcher retains normal tool permissions and
propagates a failed invocation before looking for its completion marker.

## Measured checks

- `bash -n ralph.sh`: exit 0, 0.002 seconds.
- `python3 -B -m unittest discover -s tests -v`: exit 0, 0.107 seconds.
- `git diff --check`: exit 0, 0.014 seconds.

Five offline tests cover both prompt paths/default permissions, immediate failure
without retry (even if failed output contains the completion marker), invalid
selector and missing selector. These are mock launcher checks, not proof of a
working subscription, live model, deployment or persistent sweep.

## Checked source hashes (SHA-256)

- `ralph.sh`: `bceb351b55a3ef98ff97a0ef890b966eeaeef13572fd2471d80df3320a291bd8`
- `AGENTS.md`: `8c632345992230010961d8c99185a4fa86f0c2a4375321613ffe7e898bb1c075`
- `CLAUDE.md`: `5ead133b8e50c5d60969353c0acac9f89f87b79d14a327290042f33f4cf695a7`
- `README.md`: `6fa00072321b4d7a1b31f1048491859e30551a367a1576bc9bca2a3d7d7dc105`
- `tests/test_launcher.py`: `2130fd39cf07712ed73bff88945c530a1b87407b94bc0e6346ccce35b1518f1f`

## Release gate and rollback

A fresh different-family review is still required. Same-family preparation does
not satisfy it. No sensitive packet was transferred for this change. Keep this
normal PR unmerged until required review and scoped checks pass. The existing
push-to-main deployment workflow was neither modified nor dispatched; a branch
push does not match its main-only event. Its account-level enabled setting could
not be read: GitHub returned HTTP 403 Resource not accessible by integration.

Any later approved merge must preserve the repository's protected merge and
release contract, verify the exact resulting tree and applicable deployment,
and record live evidence. Roll back through a normal revert PR if needed; do not
remove protections or reactivate a dormant deployment to make a receipt green.
