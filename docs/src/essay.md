# Understanding BATHRON — a calm essay

> *Version française : [Comprendre BATHRON — essai](essai-fr.md).*

This text is meant to be read slowly — aloud, if you like. It explains the economic and
technical mechanism of BATHRON as it is understood today, while keeping three things
separate from beginning to end: **what already exists in code**, **what is a design
goal**, and **what remains an open market question**. It makes no promises, and it never
uses the word "trustless" without spelling out what still has to be trusted.

---

## 1. What Bitcoin does very well — and where it stops

Let us start by giving Bitcoin its due.

Bitcoin is remarkable at one precise thing: holding and transferring bitcoin. A person
owns bitcoin because they control a key. They sign a transaction, the network records it,
and once it is sufficiently confirmed it becomes extraordinarily hard to change. No bank
keeping a private ledger, no central operator deciding balances: public rules, verifiable
by anyone, upheld for more than fifteen years.

But that strength does not cover every settlement need.

An ordinary payment is simple: Alice sends bitcoin to Bob. A **conditional settlement** is
something else: Bob should only receive the money if a precise condition is met — and if
it is not met by a given date, Alice must be refunded, automatically, without depending on
anyone's goodwill.

Bitcoin can express some simple conditions: a signature, the revelation of a secret, a
delay. But as soon as you want a complete commercial logic — composed conditions,
verification of an event, coordination of several transactions, the case where one party
disappears — Bitcoin's small language runs out. It was deliberately restricted, long ago,
out of caution, and that restriction is defended by serious people with good arguments:
every capability added to a system protecting hundreds of billions is added risk.

Proposals to enrich this language have circulated for years. One of them even has, at the
time of writing, a *proposed* activation schedule — proposed, not adopted; nobody knows
whether it will succeed.

So BATHRON does not start from the idea that Bitcoin is deficient. It starts from the
opposite: Bitcoin is an excellent ownership-and-transfer layer, and certain conditional
operations are hard to organize directly on it — especially if you refuse to let an
intermediary hold clients' money.

---

## 2. Bridges: trusted by whom, for what, and for how long

Faced with this limit, the classic answer is to leave Bitcoin: lock bitcoin on one side,
create a representation of it on another system, do there what Bitcoin does not allow,
then — in theory — come back. That is called a bridge, and every bridge raises a single
question: *while you are on the other side, who holds your bitcoin?*

A **custodian** is a keeper: a company that holds the funds on behalf of users. The system
works as long as that keeper stays solvent, honest, available, and permitted to honor
withdrawals.

A **federation** is a group of keepers: several institutions must sign together to move
the funds. That is better — one compromised key is no longer enough. But the underlying
problem remains: the bitcoin still exists, in a reserve controlled by identifiable actors.
A majority of signers can move it; an authority can compel the members; keys can be lost.

The most recent constructions, the so-called optimistic bridges, do better still: it is
enough for *one* honest watcher to exist to prevent fraud. That is real progress — and it
still rests on an honest setup ceremony, operators designated in advance, and watchers who
remain alive and funded for the life of the bridge.

None of these systems is absurd. Some are well run and useful. But one should never call
them "trustless." One should say precisely **whom** the user trusts, **for what**, and
**for how long**. And in every case, the answer contains a keeper — because the original
bitcoin still exists, and somebody holds it.

---

## 3. Burning to enter

BATHRON's founding idea fits in one sentence: to enter the system, you do not hand over
your bitcoin — you destroy it.

Destroying has a precise technical meaning. It is possible to send bitcoin to a spending
condition designed to make it definitively unrecoverable. Not a lost key: a demonstrable
absence of any key. This act is called a *burn*, and it is recorded forever in Bitcoin's
public ledger.

On the other side, on the BATHRON chain, every satoshi proven burned brings into existence
exactly one satoshi of new money. One for one. And this issuance is not decided by any
counter clerk: the BATHRON chain verifies for itself, inside its own consensus rules, that
the burn happened on Bitcoin. **This exists in code today and runs on the test network**:
there was no initial allocation to founders, there is no block reward, and the only path
of monetary creation is the proven destruction of bitcoin.

What the burn removes is exactly the weakness of bridges: the recoverable reserve. No
vault to raid, no federation to compel, no custodian to subpoena, no exit to authorize.
There is nothing to seize, because there is nothing left.

What the burn freezes is the other side of the coin: **the path is one-way**. No
mechanism, anywhere in the protocol, turns BATHRON's money back into bitcoin. Whoever
burns exchanges a certainty for a bet: that the money received will be worth something
because others will want to use it. If the network fails, that capital is lost.

And let us say what remains to be trusted, since this text committed to doing so: reading
the burns rests on the assumption that the majority of Bitcoin's hashpower is honest; the
BATHRON chain has its own operators, a qualified majority of whom must be honest; and, as
always, you must trust the software you run. Real assumptions — different, and arguably
healthier, than "a company holds my money."

One last point, which governs everything that follows: **it is not the ordinary user who
burns**. Asking the general public to perform an irreversible act in order to use a
service would be bad experience and bad risk allocation. The one who burns is a
professional, knowingly, the way one ties up capital to open a business. We will meet them
in chapter six.

---

## 4. M0 and M1: the vault and the ticket

Two technical names run through the documentation: M0 and M1. One image is enough.

Think of a cloakroom. You hand in a coat; you receive a numbered ticket. The coat sleeps
in the wardrobe, the ticket circulates, and a strict rule binds them: as many tickets as
coats.

**M0 is the coat**: the base money, born from burns. When you want to use it for
settlement, you place it in a vault — kept not by a company, but by the chain's common
rule, the one every node enforces together.

**M1 is the ticket**: the receipt attesting that an amount sleeps in the vault, and it is
the ticket that circulates and enters contracts. The cloakroom rule is checked at every
block: the total of tickets equals exactly the total in the vault, one for one, freely
convertible in both directions. This equality is an *invariant* — a property the code
verifies permanently. **This exists in code today.**

Why two floors? To separate reserve from circulation: a rigid, boring base, and an active,
contractual layer. And let us be clear about what M1 is not: neither an investment token
nor a yield-bearing instrument. It is a settlement instrument, whose value ultimately
depends on the success of the whole system.

---

## 5. The client stays in bitcoin

Here is the ergonomic principle that governs the model — and it is a **design goal**, a
deliberate and coherent architecture, not yet a service in production.

In this model, the ordinary client lives entirely in bitcoin. They never hold M1, never
see a burn, never learn the vocabulary of this text. Their experience fits in one
sentence, displayed before anything starts: "you send this much BTC; the recipient will
receive this much, if this condition is met, within this delay; otherwise you are refunded
in full before this date; here are the fees." They pay in bitcoin; someone, at the other
end, receives bitcoin.

All the machinery works backstage, the way interbank systems work behind a payment card
without anyone knowing their names. One can picture the whole, by analogy, as a
**clearing house**: a discreet institution that records commitments, nets crossed debts,
and enforces the rules of settlement — except that here the rules are not enforced by an
institution that could fail, but by a chain's consensus.

But if the client burns nothing and holds nothing — who runs the backstage?

---

## 6. The Settlement Provider: the one who carries the risk

The central character of the economy is the **Settlement Provider**. They must immediately
be distinguished from a custodial intermediary: a custodial payment processor *receives*
the client's money and updates its database; the Settlement Provider, in the intended
model, *routes* a contract-bounded flow, without ever receiving the client's money as a
free deposit. They supply liquidity; they must have no arbitrary power over the outcome.

To operate, they keep two inventories. On one side, bitcoin, to pay out quickly to clients
who must receive it. On the other, M1, to run the contracts backstage — and to build that
stock, it is *they* who burn bitcoin. Their stake, their cost of entry into the trade.

Their revenue, in the model: a gap between entry and exit prices — a *spread* — and fees
on the conditional services that a simple payment cannot render. The spread also serves as
a rudder: when their M1 stock runs low, they quote better prices for flows that replenish
it and worse for flows that consume it; when it is their bitcoin stock, the reverse. Their
inventory breathes through their prices — the ordinary craft of market makers.

Their risks, stated plainly: the burned capital, to be amortized over years; price risk on
the stock; imbalance risk, if flows run durably one way; delay risk, when capital sits
locked in pending operations; and the opportunity cost of all that money. If they ever
want to reduce their position, they can only sell it to other professionals — if any
exist.

Their equation is brutally simple: revenues must exceed costs, durably. And it must be
said without evasion: **nobody knows today whether that equation can be positive.** It is
the project's central market hypothesis — to be measured with real professionals and their
real numbers, not assumed.

---

## 7. Alice and Bob, step by step

Here is the story that justifies everything. Alice buys a valuable item from Bob. They do
not know each other. Alice refuses to pay before receiving; Bob refuses to ship before
being paid. The oldest deadlock in commerce.

Let us walk through the BATHRON version — keeping in mind that this *complete* journey is
a design goal: the bricks exist, the assembly is not yet a product.

**The quote.** Alice goes to a Settlement Provider's service. She is shown, in plain
terms: amount to send, amount Bob will receive, release condition, deadline, fees — and
the guarantee being sought: automatic refund if nothing has happened by expiry.

**The lock.** Alice sends her bitcoin — not into someone's pocket, but into a contract.
From that second, this money has only two possible futures, written into the contract
itself: end up with Bob if the condition is met, or return to Alice after the deadline. No
third path; no "at the provider's discretion" clause.

**The backstage.** The provider sets up, on BATHRON, the mirror of the operation with its
own M1: the escrow, the condition, the delays. Alice sees none of it.

**The outcome.** Bob delivers, the condition occurs, the contract observes it — we will
see how — and releases the funds to Bob, in bitcoin, along the pre-committed path. Or Bob
does not deliver, disputes, disappears: then nobody decides anything; time passes, the
deadline falls, and Alice's refund executes.

At no point did an intermediary hold Alice's money with the power to do anything other
than the two planned outcomes. That is the service being sought.

---

## 8. The four gears: the padlock, the seal, the eye, and the clock

Four mechanisms carry this story.

**The secret padlock — the HTLC.** A sum is locked so that it opens either with a secret —
a cryptographic password — or, failing that, through a refund after a delay. The beauty of
the device: you can put *the same secret* on two locks, in two different worlds. Whoever
reveals the secret to collect on one side makes it, by that very act, usable on the other.
The two legs of the payment — Alice's going in, Bob's going out — become interlocked. An
old, battle-tested technique in the Bitcoin ecosystem.

**The seal on the futures — the covenant, including CTV.** At the moment money enters the
contract, the exhaustive list of its authorized exits is sealed cryptographically. "To Bob
if the condition holds, back to Alice otherwise" — nothing else, ever. This is one of the
capabilities Bitcoin has not activated to date; on BATHRON it exists and runs, along with
a whole family of sibling mechanisms. **Verifiable fact on the test network.** The
remaining assumption: that the covenant was built correctly and that the user — in
practice, their software — verifies what they sign. A very restrictive contract can still
be a bad one if its restrictions were badly chosen.

**The eye on Bitcoin — SPV.** The BATHRON chain follows Bitcoin's block headers and
verifies, *inside its consensus rules*, that a precise transaction is included and
confirmed — every node redoes the verification; nobody takes it on faith. A contract can
thus stipulate: "release when such-and-such Bitcoin transaction has so many
confirmations." No oracle, no attesting third party. **This capability exists in code
today** — and, to our knowledge, this precise combination exists nowhere else; we prefer
third parties to verify that claim rather than proclaim it. The remaining assumption: that
the Bitcoin chain being followed is the majority chain, and that the chosen confirmation
depth covers reorganization risk. The more confirmations you wait for, the safer — and the
slower.

**The clock — timelocks.** Every refund path opens at a date fixed in advance, and the
ordering of deadlines is no detail: Bob's window closes before Alice's opens, with margins
for the chains' slowness — otherwise an ambiguous moment would exist where both paths
overlap. Add the operational assumption everyone forgets: a refund right is only useful if
Alice's software watches the chain and publishes the transaction at the right time.

A padlock that interlocks the legs, a seal that freezes the exits, an eye that observes
the facts, a clock that guarantees the endgame. And the sentence of caution that must
follow immediately: the global guarantee — "Alice is settled per the quote or refunded, in
*all* cases, including failures at the worst moment" — is a **security objective**. The
flows have not been formally specified; no external review has taken place. Saying today
"the provider cannot steal the principal" would be a promise, not a fact — and we forbid
ourselves from saying it until that work is done.

---

## 9. The economics of the first entrant

One question decides a great deal: the first Settlement Provider — who will it be?

Put yourself in the shoes of a neutral, rational market maker. They will ask three
questions. How much does it earn? — spreads and fees on a volume that does not yet exist.
How much does it cost? — burned capital, unrecoverable through the protocol, to be
amortized over years. And above all: how do I exit? — by selling their M1 to other
professionals… who do not exist yet; or by consuming it slowly through the business; or by
losing it if the network dies. For the very first entrant, the exit market is empty by
definition.

A neutral market maker, facing that picture, says no — and by their criteria they are
right. The honest conclusion is therefore: **the first provider will probably be a
strategic sponsor**, not an arbitrageur. Someone whose interest exceeds the quarter's
return: a payment company seeking to differentiate through conditional settlement, a
trading desk wanting its own escrow rail, an actor buying the thesis and the
infrastructure at once. They might accept weak or zero profitability at first, to
bootstrap.

And the consequence for what proves what must be drawn: the arrival of the first will
prove that a sponsor believes. It is the *second* — independent, arriving uninvited — who
will prove that a market exists. The nuance matters: it prevents applauding at the wrong
moment.

---

## 10. The honest inventory of what is not proven

Let us list the gaps, as a chapter in its own right.

**No external audit.** The code has been reviewed and attacked repeatedly — by its own
team. In financial software, self-examination does not count as proof. Outside eyes, paid
to break things, are a prerequisite to any real value. That has not happened.

**A known, accepted vulnerability.** The test network opens to outside operators with a
near-free entry ticket; it follows that a malicious actor could, at little cost, create a
few fake identities and *freeze finalization* of blocks. Let us be precise about what this
does not allow: neither theft nor money creation — the accounting invariants hold no
matter what; that is in the code. Visible sabotage, reversible by restarting the test
network; accepted for the experimentation phase, to be hardened before any definitive
network.

**No real Settlement Provider.** Nobody has burned bitcoin to open shop. No real client
transaction has ever been routed. The economy described above is an architecture awaiting
its first inhabitant.

**Unproven economics.** The provider must earn enough; the client must accept the price;
both at once. Too small a spread does not pay for the capital; too large a spread drives
the client away. It will have to be measured, not reasoned.

**Client protection still to specify and review** — technically, and beyond. For
cryptographic protection does not replace commercial protection: what happens if the
delivered item is not as described? who defines that the condition is met? who answers for
an interface bug? is there any recourse? The protocol can guarantee that a secret was
revealed; it cannot guarantee that commercial reality matches the secret. Those questions
belong to the service built on top — and they remain open.

---

## 11. Against the alternatives: who wins what

A word of competitive fairness, for nothing discredits faster than claiming to beat
everything.

**Lightning** is better for simple, fast payments, no contest. It aims at transferring
bitcoin through pre-funded channels, with its own assumptions — channel liquidity, route
availability, chain monitoring. BATHRON does not compete on that ground; its subject
begins where rich conditions are needed.

**Liquid** brings fast, confidential transfers between institutions, with real liquidity —
at the price of its model: an identified federation holds custody, and the exit passes
through its members. A different trade-off, not an absurdity; one must simply know one has
signed it. BATHRON gives up the recoverable vault; in exchange, its exit liquidity must
come from providers and their inventory.

**A custodial payment processor** wins on simplicity: deposit, database, customer service
— against custody of your funds and the power to decide. BATHRON seeks to reduce that
power through pre-committed transactions; in exchange, the system is genuinely more
complex.

**Multisig with an arbiter and a legal contract**, finally, is the most honest alternative
for escrow — and its own strength must be acknowledged: a human arbiter can look at
photos, read messages, judge whether a product was as described. No cryptographic contract
can do that. The fair boundary is therefore this: **BATHRON targets objectively verifiable
conditions** — an elapsed delay, a signature, a confirmed transaction; **human arbitration
remains better when the condition requires interpretation**. This is not a decorative
concession: it is the product's boundary.

The real question is never "who is superior" — it is: what kind of trust, and what kind of
cost, does this particular client prefer?

---

## 12. The real market question — and the honest summary

Everything this text has described hangs on a question of disarming banality:

*How much would a real client pay to avoid custody and arbitration?*

Put yourself in Alice's place. For her escrow she has choices: the arbiter and their fees,
the processor and its terms, or this new rail. What price difference would make her choose
the rail? For a small ordinary payment, probably none. For a large transaction, an
international one, one exposed to freezing or to a custodian's bankruptcy — perhaps a lot.
Nobody knows that number. It cannot be computed in code; it is measured with real clients,
real offers, real refusals. And it governs everything: if it is comfortable, the
provider's equation can close and the system can live; if it is near zero, no technical
elegance will change anything.

Let us summarize, one last time, in the three registers.

**What exists.** A chain runs, on a public test network. It creates its money exclusively
through proven destruction of bitcoin — no premine, no block reward, one satoshi for one
satoshi. It verifies Bitcoin's state for itself, inside its rules. It maintains a vault
and receipts at strict parity, checked at every block. And it runs a family of
sealed-path contracts that Bitcoin, to date, declines to activate. All of it verifiable by
anyone who cares to look.

**What is aimed for.** A conditional-settlement engine behind an ordinary bitcoin
experience: clients who pay and receive BTC without seeing any machinery; professional
providers who carry inventory, prices, and risk; and one central guarantee — settled per
the quote, or refunded by the clock — governing every contract. This design is coherent,
written down, and unbuilt: neither formally specified, nor audited, nor inhabited by a
single real provider.

**What is hoped, and not yet known.** That clients exist whose pain is worth a price; that
this price pays for a professional's burned capital; that a first sponsor walks through
the door, and then that a second arrives uninvited.

BATHRON's proposition can thus be stated without exaggeration. It is not about removing
trust: it is about **moving** part of it — replacing a keeper's discretion with an
irreversible burn, Bitcoin proofs, pre-committed transactions, secrets, and delays. The
price of that move is real technical complexity and a vital need for liquidity providers.
What remains to be trusted is named; what remains to be proven is listed; and what would
prove the project wrong is written down in advance.

The code exists. The design is clear. The market is a question that has been asked — and
the only answer that counts will come from external audits, real trials, and real clients.
