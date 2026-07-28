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
- The public testnet explorer (https://explorer.bathron.org/) is an
  experimental demonstrator served over HTTPS (publicly issued, auto-renewed
  certificate). It is a read-only display distinct from the Seed P2P
  endpoint; treat it as a view, never as an endpoint for secrets, and note
  that no availability is guaranteed.
