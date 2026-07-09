# Miner hedging

A miner's revenue is a bet on Bitcoin's difficulty. Hedging that bet normally requires a broker and a price feed — a counterparty and an oracle. Here, **the settlement condition is Bitcoin's own difficulty, read by consensus.**

```text
  miner ─────┐                       ┌───── counterparty
             ▼                       ▼
        both lock margin in a covenant
                       │
                       ▼
   at expiry: consensus reads Bitcoin difficulty
        from the in-consensus header chain
                       │
          difficulty rose        difficulty fell
                │                       │
                ▼                       ▼
         pays the miner        pays the counterparty
```

## Why this is different

Every difficulty derivative elsewhere trusts someone to *report* difficulty. On BATHRON the header chain — with its difficulty adjustments — **is consensus state**: the covenant reads the fact itself. No oracle to bribe, no publisher to go offline.

## The honest caveat

Difficulty is hedgeable oracle-free because Bitcoin publishes it. A full *hashprice* hedge also involves the BTC price — which is not an on-chain fact and needs a signed input (`CSFS`), with the trust that implies. The difficulty leg is the trustless core.

**Primitives:** in-consensus Bitcoin headers · difficulty introspection · covenants · `CSFS` (price leg only)
