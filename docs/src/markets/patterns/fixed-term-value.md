# Fixed-term value positions

Some participants in a market want exposure to a reference value for a fixed period — a
merchant who must pay a supplier in ninety days, a provider hedging inventory — without holding
the asset itself. Today that means a stablecoin (an issuer's liability) or a broker. On BATHRON
it can be a bilateral contract: two parties, collateral in a covenant, and a payout selected at
expiry by a signed reference price. BATHRON does not mint a stablecoin, and this pattern is not
one.

## The contract

A professional counterparty quotes the contract, prices the risk and commits collateral in M1.
The other participant sees the quoted payoff and fees. At expiry, a price signature from the
designated signer — verified by `CSFS` — selects which branch of the covenant pays out;
`CSV`/`CLTV` bound the term and provide the fallback if no valid signature arrives.

```text
  participant ───┐                        ┌─── professional counterparty
                 ▼                        ▼
           both commit collateral in a covenant, term T
                              │
                              ▼  at T
           CSFS checks the signed reference price
                              │
              price above K          price below K
                    │                      │
                    ▼                      ▼
             pays one side          pays the other
```

Balances on the M1 side can stay confidential; the reference price and the payout rule are
explicit in the covenant.

## What this is not

It is not a stablecoin: nobody issues a unit that claims par against anything, and the other
participant is not invited to acquire network exposure. It is a bilateral position with real
signer, counterparty, liquidity and model risk. Collateralisation and a fixed expiry limit some
of those risks; they do not remove them. No implementation should be described as stable until
its payout rules, signer failure modes and liquidation assumptions have been reviewed — see
[Status & claims](../../consensus/status-and-claims.md).

**Primitives:** covenants · `CSFS` · `CSV` / `CLTV` · confidential internal balances

**See also:** [Hedging on Bitcoin facts](hedging.md) ·
[Why not an exchange, a bridge, or a stablecoin](../../problem/why-not-alternatives.md)
