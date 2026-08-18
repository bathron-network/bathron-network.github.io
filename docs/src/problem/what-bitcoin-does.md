# What Bitcoin does, and where it stops

BATHRON does not start from the idea that Bitcoin is deficient. It starts from the opposite:
Bitcoin is the best ownership-and-transfer layer that exists, and *because* it is so good at that
one thing, it refuses to do the next thing. This page marks the exact line.

## What Bitcoin does very well

A person owns bitcoin because they control a key. They sign, the network records, and after
enough confirmations the record becomes extraordinarily hard to change. No bank keeping a private
ledger, no operator deciding balances — public rules, verifiable by anyone, upheld for more than
fifteen years. That is why Bitcoin is the final asset in everything that follows: **the thing you
ultimately want to end up holding, and the only thing whose destruction can be verified by anyone.**

## Where it stops, on purpose

An ordinary payment is simple: Alice sends bitcoin to Bob. A **conditional settlement** is
something else: Bob receives only if a precise condition is met, and if it is not met by a given
date, Alice is refunded automatically, without anyone's goodwill.

Bitcoin can express a few conditions — a signature, a revealed secret, a delay. As soon as you
want a complete commercial logic (composed conditions, verification of an external event,
coordination of several legs, the case where one party disappears), Bitcoin's small language runs
out. It was restricted long ago, out of caution, and that restriction is defended by serious
people with good arguments: every capability added to a system protecting hundreds of billions
is added risk. Proposals to enrich the language have circulated for a decade; none is adopted.

So there are two facts to hold at once:

- Bitcoin **will not** carry the conditions of a trade — and that is a feature of Bitcoin.
- A market **needs** those conditions — delivery against payment, refund on timeout, both legs or
  neither.

## What follows

Something has to carry the conditions, and it must satisfy three constraints that most systems
give up on the first page:

1. it must **never hold the bitcoin** for redemption (otherwise it is a custodian, see next page);
2. it must be able to **verify Bitcoin facts itself**, without a designated oracle;
3. it must be **open** — anyone can settle, quote or build without being admitted.

BATHRON's answer is a separate settlement state, expressed in a unit (M1) whose only origin is
verified Bitcoin destruction, run by a consensus that reads Bitcoin headers inside its own rules.
Bitcoin keeps the value; BATHRON keeps the conditions; markets keep the liquidity. The next page
explains why the usual alternatives — an exchange, a bridge, a stablecoin — do not satisfy the
three constraints together.

**Next:** [Why not an exchange, a bridge, or a stablecoin](why-not-alternatives.md)
