# Fixed-term value position

BATHRON does not mint a stablecoin. A possible application is a bilateral, fixed-term contract
whose payout depends on a signed reference price.

A professional counterparty quotes the contract, prices the risk and commits collateral. At
expiry, a CSFS-verified price signature selects the covenant payout. The other participant sees
the quoted payoff and fees, not an invitation to acquire leveraged network exposure.

This design introduces real oracle, counterparty, liquidity and model risk. Collateralisation and
expiry limit some risks but do not remove them. No implementation should be described as stable
until its payout rules, oracle failure modes and liquidation assumptions have been reviewed.

**Primitives:** covenants · CSFS · CSV/CLTV · confidential internal balances
