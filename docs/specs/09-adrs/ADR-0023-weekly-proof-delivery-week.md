# ADR-0023 — Weekly Proof assessment and delivery weeks

**Status:** Accepted

## Context

FR-433 rates a complete user-local Monday-through-Sunday assessment week at 03:00 on the following Monday. A Proof cannot truthfully consume that complete assessment and also be delivered inside the already-ended assessed week. Earlier prose used “same assessment week” for late delivery while the runtime and data contracts scheduled the Proof in the following week, leaving expiry and cost-resume behavior ambiguous.

## Decision

Assessment week W remains the completed user-local Monday 00:00 through Sunday 23:59:59 interval owned by FR-433. Its Proof has a distinct delivery week: the immediately following user-local Monday-through-Sunday interval W+1.

After the W assessment commits, the system computes the FR-507 preferred weekday and freezes `delivery_due_at` at 09:00 local on that weekday in W+1. It freezes `delivery_expires_at` at the following Monday 00:00 local, exclusive. A Proof not ready at its preferred slot may appear on the next app open before that exclusive expiry. At or after expiry, incomplete, parked, failed, or losing publication work becomes a silent omission and MUST NOT surface in a later week.

The Proof continues to display and archive the assessed W dates. Due and expiry are delivery-control metadata and are not progress data. The timezone used to convert the slot is frozen when the Proof row is created; a later timezone refresh does not move an existing Proof.

## Consequences

- Assessment input is complete before Proof generation starts.
- “This week” delivery behavior has one exact interval for polling, cost admission, late readiness, and expiry.
- A played Proof remains in Archive after delivery expiry; an unplayed stale Proof does not surface later.
- No notification is added. FR-501 and FR-629 remain unchanged.

## Rejected alternatives

1. **Deliver inside W before W closes.** Rejected because the Proof would rate an incomplete week and could fabricate a final comparison.
2. **Move the assessment earlier.** Rejected because FR-433 intentionally measures the complete Monday-through-Sunday interval.
3. **Allow delivery at any later time.** Rejected because stale Proofs would collide with a newer assessment and turn the surface into a progress feed.
