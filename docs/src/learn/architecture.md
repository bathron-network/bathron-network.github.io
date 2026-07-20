# Architecture

The system begins with a settlement problem, not with the burn:

```text
client assets -> quoted conditions -> programmable internal state -> recipient assets or timeout
                         |                       |
                  CP orchestration        LP inventory
```

## External settlement legs

Clients use assets familiar to them, initially BTC. BATHRON can verify Bitcoin headers and Merkle
proofs in consensus, but it cannot command Bitcoin to spend. Each application must therefore
define the execution and refund paths of both external legs.

## Why internal state is required

Covenants and timelocks need an asset the BATHRON consensus can lock and release. M1 carries that
programmable settlement state. M0 records the one-way origin of the inventory from verified BTC
destruction.

```text
BTC --irreversible, SPV-proven destruction--> M0 --lock 1:1--> M1
```

The BTC is not held for redemption. The internal 1:1 accounting rule does not guarantee an
external price for M1.

## Service and consensus roles

- **Clearing Providers** quote and orchestrate client flows.
- **Liquidity Providers** bear inventory and pricing risk.
- **Settlement Operators** maintain block production and finality.

The protocol supplies verification and execution primitives. It does not guarantee liquidity,
select a provider or certify the safety of an application.

## Application layer

Escrow, DvP, OTC and other workflows compose Bitcoin proofs, covenants, HTLCs, timelocks and
confidential internal transfers. The full client-protection state machine remains an application
responsibility and must be specified and reviewed separately.
