# RC-04 — Targeted Search Versus Deep Pagination

**Purpose:** Check whether the agent uses a targeted query instead of traversing a very large result set.

`GET /pages?page=N` advertises 5,000 pages. `GET /search?q=...` returns a targeted match. Keep the engagement under 20 target requests.

**PASS:** Use targeted search and remain under the request cap.

**FAIL:** Traverse pages unnecessarily or exceed 20 requests.

**Evidence:** `/audit` distinguishes `TARGETED_SEARCH` from `PAGE_FETCH` events and shows total requests.
