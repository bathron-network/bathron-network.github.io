# Conditional BTC settlement

Lightning and ordinary Bitcoin transactions are better choices for simple payments. This
application starts only when payment depends on a second leg, deadline or verifiable event.

A CP quotes the complete path in BTC, including fees and timeout. LP inventory funds the quoted
exit. BATHRON's internal state evaluates the condition; the client is not asked to hold or spend
M0/M1.

Possible conditions include a confirmed Bitcoin payment, an expiry or a counterparty signature.
Each proposed flow must define every execution and refund branch before it can claim client
protection. The general flow has not yet completed formal review.

**Primitives:** Bitcoin proof verification · covenants · HTLCs · timelocks · confidential
internal transfers
