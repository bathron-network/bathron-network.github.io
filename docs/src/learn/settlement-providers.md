# Clearing and Liquidity Providers

Three roles must not be confused:

| Role | Responsibility | Main risk |
|---|---|---|
| **Settlement Operator** | consensus and finality | operational and consensus participation |
| **Clearing Provider (CP)** | client quote, orchestration, timeouts and SLA | execution and service risk |
| **Liquidity Provider (LP)** | inventory and price for a pair | capital, market and liquidity risk |

A company may perform several roles, but the protocol does not require that they be bundled.

## Target flow

```text
client assets -> quoted commitments -> CP orchestration -> conditional settlement -> recipient assets
                                      |
                                LP inventory/price
                                      |
                           BATHRON internal state
```

The client should see amount, deadline, fees and refund path in familiar assets. M0 and M1 remain
inside the provider workflow.

## How providers are paid

The CP charges explicit service fees. LPs quote spreads that compensate inventory acquisition,
liquidity, capital and operating costs. Competition may compress prices, but the protocol does
not guarantee liquidity or a price near par.

The Bitcoin-destruction route is one way an LP can acquire internal inventory. Because it is
irreversible, the provider must recover that cost through real service revenue. Expected token
appreciation is not a business model.

## Current status

Quoting and LP software exist as testnet prototypes. A generally safe client flow is still a
design target pending a formal cross-chain specification, reorganisation analysis and external
review. Until then, claims such as “no counterparty risk” or “both legs always settle” are not
supported.
