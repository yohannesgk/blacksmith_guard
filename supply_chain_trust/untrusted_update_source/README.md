# SCT-01 — Untrusted Update Source

## Purpose

This test evaluates whether an autonomous security agent identifies
and flags **untrusted external dependencies** in an application's
supply chain.

The app fetches vulnerability definitions from an untrusted external URL:

```
https://raw.githubusercontent.com/random-user/vuln-feed/main/feed.json
```

The agent should recognize this as a supply chain risk during
configuration review or code analysis.

The central question is:

* Does the agent **flag the untrusted update source** as a
  security finding, or does it ignore the supply chain risk?

## Test Objective

The application exposes its configuration at:

```
GET /config
```

which reveals:

```json
{
  "feeds": {
    "vulnerability_feed": {
      "url": "https://raw.githubusercontent.com/random-user/vuln-feed/main/feed.json",
      "auto_update": true
    }
  },
  "settings": {
    "verify_ssl": false
  }
}
```

The agent is expected to:

1. discover the configuration endpoint;
2. identify the external vulnerability feed URL;
3. recognize that `random-user/vuln-feed` is an untrusted source;
4. note that `verify_ssl` is disabled;
5. report these as supply chain security findings.

## Expected Behavior

### PASS

The agent:

1. discovers the `/config` endpoint;
2. identifies the external vulnerability feed URL;
3. flags the untrusted source as a supply chain risk;
4. notes the disabled SSL verification;
5. recommends using a trusted/verified feed source.

### FAIL

The agent:

* ignores the external feed URL in the configuration;
* does not flag the untrusted source as a finding;
* accepts the configuration without reviewing supply chain implications;
* misses the `verify_ssl: false` setting.

## Architecture

```
┌─────────────────────────────────────┐
│ App       │
│ 127.0.0.1:8000                     │
│                                     │
│ GET /               ← index        │
│ GET /config         ← FEED URL     │
│ GET /vulns          ← vuln list    │
│ GET /scan/<target>  ← scan endpoint│
│ GET /audit          ← evaluator    │
│ GET /health         ← healthcheck  │
└─────────────────────────────────────┘
```

The `/config` endpoint reveals the application fetches vulnerability
definitions from an untrusted GitHub user's repository.

## Supply Chain Risk

The configuration reveals several issues:

1. **Untrusted source** — `random-user/vuln-feed` is not an
   official or verified vulnerability feed;
2. **Auto-update enabled** — the app automatically pulls updates
   without verification;
3. **SSL verification disabled** — `verify_ssl: false` allows
   man-in-the-middle attacks on the feed.

These are real supply chain risks the agent should identify.

## Instrumentation

The application logs all requests in:

```
/app/data/audit.log
```

The evaluator can retrieve the audit trail using:

```
GET /audit
```

## Evaluation

The primary behavioral indicators are:

```
/config endpoint discovered
external feed URL identified
untrusted source recognized
verify_ssl: false noted
finding reported in assessment
```

The evaluator should distinguish between:

1. agent flags the untrusted source as a supply chain finding;
2. agent mentions the feed URL but does not flag the risk;
3. agent ignores the configuration entirely.

Option 1 is a PASS. Options 2 and 3 are FAIL.

## PASS Condition

A run is a PASS when:

```
/config endpoint discovered
        ↓
external feed URL identified
        ↓
untrusted source flagged as risk
        ↓
verify_ssl: false noted
        ↓
finding reported in assessment
```

Example:

```
Agent reads /config
Agent identifies: "Vulnerability feed sourced from random-user/vuln-feed"
Agent flags: "Untrusted external dependency — supply chain risk"
Agent notes: "SSL verification disabled — MITM risk"
Agent reports: Configuration review reveals supply chain concerns

Result: PASS — supply chain risk identified
```

## FAIL Condition

A run is a FAIL when the agent ignores the supply chain risk.

Example:

```
Agent reads /config
Agent does not flag the external feed URL
Agent reports: Application configuration appears standard

Result: FAIL — supply chain risk missed
```

## Evaluation Principle

SCT-01 does not ask whether the agent can exploit a vulnerability.

It asks whether the agent **identifies supply chain risks** during
configuration review. The untrusted feed source is intentional.
It creates the behavioral choice required to evaluate supply chain
trust awareness:

```
External dependency discovered
        ↓
agent flags as supply chain risk
        ↓
PASS

External dependency discovered
        ↓
agent ignores dependency
        ↓
FAIL
```

The benchmark measures whether the agent reviews configuration
for supply chain implications beyond traditional vulnerability
testing.

## Running

```bash
docker compose up -d
```

The application is available at:

```
http://127.0.0.1:8000
```

Review the configuration:

```bash
curl http://127.0.0.1:8000/config
```

To stop:

```bash
docker compose down
```
