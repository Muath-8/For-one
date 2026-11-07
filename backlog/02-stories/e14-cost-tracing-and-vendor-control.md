# E14 · Cost tracing and vendor control

*Architecture domain 08. Budget $0.60 a session in the beta against an estimate of $0.66; scale target $0.35; stop line $1.00 with no costed plan.*

### E14-S01 · Price book
**As an** operator, **I want** `prices.yaml` with every vendor's unit prices, dated, and a `price_book` table, **so that** a price change is a commit and the January rises are already in the plan.
- **Given** a vendor call with no price row, **when** traced, **then** it is recorded as `unpriced` and alarms.
- Size: S · Priority: P0 · Week: W1 · Domain: 08 Cost · Depends on: none

### E14-S02 · Tracing middleware and `vendor_calls`
**As an** operator, **I want** every model, voice and speech call to pass through middleware that records unit usage, price, role, learner (tokenized), episode and cache hit, **so that** cost is a query from the first test render.
- **Given** the vendor tests in W1, **when** run, **then** every render is a priced `vendor_calls` row and "cost per 10 minutes of audio" is real before any episode exists.
- Size: M · Priority: P0 · Week: W1 · Domain: 08 Cost · Depends on: E14-S01, E01-S02

### E14-S03 · Session cost roll-up and the per-episode line
**As an** operator, **I want** `cost/rollup` into `session_costs` per role and vendor, feeding `episodes.cost_usd`, **so that** the cost report shows where the money goes.
- **Given** 20 test episodes, **when** rolled up, **then** teacher, writer, editor and voice lines are shown against the estimate ($0.08, $0.07, $0.03, $0.18).
- Size: M · Priority: P0 · Week: W2 · Domain: 08 Cost · Depends on: E14-S02, E04-S07

### E14-S04 · Spend caps and spend mode
**As an** operator, **I want** a daily spend cap, a per-learner daily cost guard, and `spend_mode` with conserve and halt wired into the pipeline and call configuration, **so that** a runaway night cannot bankrupt the beta.
- **Given** the cap is reached, **when** a new vendor call is attempted, **then** halt refuses non-live calls and conserve switches to the cheaper configuration first.
- Size: M · Priority: P0 · Week: W2 to W4 · Domain: 08 Cost · Depends on: E14-S02

### E14-S05 · Cost alarms
**As an** operator, **I want** alarms for kind ceilings, unpriced calls, low cache hit, a session over $1.00, p50 over $0.80 for 7 days and daily spend, **so that** the stop line is seen the day it is crossed.
- **Given** a session over $1.00, **when** rolled up, **then** `session_over_alert` fires with the role breakdown.
- Size: S · Priority: P0 · Week: W4 · Domain: 08 Cost, 09 Operations · Depends on: E14-S03, E15-S04

### E14-S06 · Call cost and the Haiku-host comparison
**As an** operator, **I want** per-call cost including LiveKit minutes, the host's cache hit rate, and the 50-call run repeated with a Haiku-class host, **so that** the cheapest host that passes the governor is known.
- **Given** the comparison, **when** done, **then** latency, governor violations and cost per call are in one table for both hosts.
- Size: M · Priority: P0 · Week: W4 · Domain: 08 Cost, 03 Live call · Depends on: E05-S02, E14-S02

### E14-S07 · Vendor health and the failover drill
**As an** operator, **I want** `/admin/vendors` with health and a drill that kills the primary voice key for an hour and still ships the night's episodes, **so that** a vendor outage is survivable.
- **Given** the drill, **when** run in W4, **then** every episode ships on the secondary and the report records the time to switch.
- Size: M · Priority: P0 · Week: W4 · Domain: 08 Cost, 02 Pipeline · Depends on: E02-S05, E04-S05

### E14-S08 · Weekly cost report and the exit document
**As an** operator, **I want** a weekly report (cost per session, per role, per vendor, cache hits, outliers, next week's prices) and, by 22 December, the exit document with the measured cost and the costed path to $0.35, **so that** the beta's gate on cost is a number.
- **Given** the pilot learners' production week, **when** reported, **then** measured cost per session is shown beside the $0.66 estimate and each lever to $0.35 has a measured first column.
- Size: M · Priority: P0 · Week: W5 · Domain: 08 Cost · Depends on: E14-S03, E06-S11
