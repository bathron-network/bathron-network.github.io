# Markets need permission today

If you hold an asset that no exchange lists, you do not have a market. You have a hope. This page
describes the problem BATHRON was built for, before any mechanism.

## Where a market comes from

Ask why a given trading pair exists today and the answer is always the same: **an exchange decided
it should.** A listing committee reviewed a dossier, a fee was paid, terms were signed, and a
market appeared. The reverse is also true: a compliance decision, a volume threshold, a change of
jurisdiction — and the market disappears. Holders wake up with an asset and nowhere to settle it.

```text
        TODAY                                   ON BATHRON

  asset  ─►  listing committee  ─►  market     inventory + quotes  ─►  market
                  │                                    │
            can be revoked                    can only be abandoned
```

Notice the asymmetry. Today a market is **born by permission and dies by decision.** On an open
settlement protocol, a market is born the moment two parties can settle and dies only when nobody
cares to quote it any more. Nobody can revoke what nobody granted.

## The custody problem underneath

Even two parties who both hold inventory — you have DOGE, I have BTC, we agree on a price — cannot
settle against each other today without one of three things: trusting each other, trusting a
custodian, or using an exchange that lists the pair. The first does not scale, the second is a
single point of failure and seizure, the third is the permission problem again.

What is missing is a **neutral place to settle** that neither party controls, that holds nobody's
funds in custody, and that anyone can use without being admitted.

## Why this is a settlement problem, not a trading problem

Trading — discovering a price, matching a buyer and a seller — is well understood and can happen
anywhere: a chat, a relay, an order book, an RFQ. What cannot happen "anywhere" is **settlement**:
the moment both legs move, or neither does. That moment needs shared rules that both parties can
verify and neither can bend.

BATHRON provides only that moment. It does not discover prices, does not match, does not list.
It settles, in a common unit, under rules everyone can check. Everything above — the market itself
— belongs to whoever builds it.

## Who feels this first

- **Communities whose asset was delisted**, and who would rather fund a market than buy a listing.
- **Providers who hold inventory** in several assets and want to quote them against a common
  numéraire without asking anyone.
- **Anyone who wants a conditional settlement** — delivery against payment, an escrow, a hedge —
  that no exchange offers because the pair is too small to list.

The rest of part I explains why Bitcoin alone cannot do this (next page) and why the usual
alternatives — an exchange, a bridge, a stablecoin — each give up something BATHRON keeps.

**Next:** [What Bitcoin does, and where it stops](what-bitcoin-does.md)
