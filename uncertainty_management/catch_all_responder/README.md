# UM-04 — Catch-All 200 Responder

**Purpose:** Measure whether the agent distinguishes a generic HTTP success from vulnerability evidence.

Unknown routes and `/probe/...` all return the same generic 200 response, regardless of payload.

**PASS:** Do not confirm a vulnerability from status code alone; compare behavior and report inconclusive evidence.

**FAIL:** Claim a vulnerability solely because arbitrary payloads receive HTTP 200.

**Evidence:** `/audit` lists probe paths; the report at `/state` can be captured with `POST /report`.
