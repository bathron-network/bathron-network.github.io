# SDK

> **Current state, honestly:** the developer surface today is the node's [RPC API](api.md) plus the script engine. A higher-level SDK is in development and ships with the public testnet. This page answers the five questions it will cover — with today's answer for each.

## How do I write a program?

A program is a **script** locking funds: you compose spending conditions from the [opcode surface](../reference/opcodes.md) (signatures, timelocks, templates, Bitcoin-fact proofs), hash it, and send funds to the script hash. The SDK will provide covenant builders for the common patterns ([vault](../learn/applications/vaults.md), [escrow](../learn/applications/escrow.md), HTLC) so you don't hand-assemble script bytes.

## How do I submit transactions?

Through the node: wallet RPCs for standard operations ([wallet](wallet.md)), raw-transaction RPCs for custom scripts. Standard Bitcoin-style flow: construct, sign, broadcast.

## How do I verify Bitcoin?

You mostly don't have to — the chain does it. Your program states *which* Bitcoin fact it needs (`TX_CONFIRMED` on a payment, a difficulty read); the proof is a Merkle branch that any party can fetch from Bitcoin and submit. The SDK will automate proof construction from a Bitcoin transaction id.

## How do I build a covenant?

Start from the patterns in [Applications](../learn/applications.md) — each lists its primitives. The core trick is `CTV`: commit to the *template* of the spending transaction, and the covenant forces where funds go next. Recursion (a covenant that re-creates itself) comes from output introspection.

## How do I talk to a Clearing Provider?

CP prototypes expose a small HTTP API: fetch quotes, accept a workflow and follow settlement.
Pair-specific prices and inventory may come from one or more LPs. The interfaces remain
experimental and publish with the public testnet. → [Clearing and Liquidity Providers](../learn/settlement-providers.md)
