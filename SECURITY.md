# Security policy

This repository holds the BATHRON website and documentation
(https://bathron.org). The canonical security policy for the BATHRON
project lives in the node repository:

https://github.com/bathron-network/bathron-core/blob/main/SECURITY.md

**Report vulnerabilities to security@bathron.org.** Please do not open
public issues for security-sensitive reports — this applies to the website,
the documentation, the explorer and the node software alike.

Notes specific to this site:
- https://bathron.org is served by GitHub Pages with HTTPS enforced
  (HTTP requests are redirected). GitHub Pages does not allow setting a
  Strict-Transport-Security header on custom domains — a known limitation.
- The public testnet explorer (linked from the docs) is an experimental
  demonstrator currently served over plain HTTP; treat it as untrusted
  display, never as an endpoint for secrets. Its HTTPS migration is tracked
  separately.
