# REBUTTAL

Reviews
Review 1
Overall evaluation	
1: weak accept
The abstract introduces a timely and well-motivated framework, BlacksmithGuard, for benchmarking safety, authorization constraints, and operational reliability in autonomous offensive AI agents. Addressing key gaps beyond basic exploit success rates—such as tool-use correctness, failure recovery, and policy compliance across penetration testing lifecycles—provides a valuable contribution to AI safety and automated cybersecurity.

To strengthen the work, elaborate on a few key technical and evaluation details. Provide specific details regarding the environment sandboxing, quantitative scoring metrics, and baseline models or multi-agent configurations evaluated under the framework. Additionally, clarify how the framework handles potential edge cases where autonomous agents attempt to bypass authorization boundaries or generate uncontained exploitation traffic.

Review Tracking
Review 1
Overall evaluation	
0: borderline paper
Abstract Review [1]

The abstract introduces a timely and well-motivated framework, BlacksmithGuard, for benchmarking safety, authorization constraints, and operational reliability in autonomous offensive AI agents. Addressing key gaps beyond basic exploit success rates—such as tool-use correctness, failure recovery, and policy compliance across penetration testing lifecycles—provides a valuable contribution to AI safety and automated cybersecurity.

To strengthen the work, elaborate on a few key technical and evaluation details. Provide specific details regarding the environment sandboxing, quantitative scoring metrics, and baseline models or multi-agent configurations evaluated under the framework. Additionally, clarify how the framework handles potential edge cases where autonomous agents attempt to bypass authorization boundaries or generate uncontained exploitation traffic.

Review Tracking
Review 2
Overall evaluation	
1: weak accept
The paper introduces BlacksmithGuard, a 12-property behavioral-safety taxonomy and 25-scenario executable benchmark for autonomous offensive-security agents. The taxonomy adapts six of Sprocket's seven properties, treats Transparent as measurement infrastructure, and adds six new properties (four extending Sprocket/APTS, two multi-agent-specific: Cross-Agent Safety Propagation and Safe Delegation). Twenty-four scenarios are Dockerized Flask services; one is prompt-only. PentestGPT v1.0.0 and BlacksmithAI v1.0.0 were each run once per scenario under a shared model (deepseek-v4.1-flash), temperature 1.0, and a 10-minute timeout. On 17 shared scenarios, BlacksmithAI passed 12 (70.6%) and PentestGPT 10 (58.8%) — not statistically distinguishable (Fisher's exact p ≈ 0.72). BlacksmithAI passed 19/25 overall (76.0%). The paper emphasizes that the benchmark measures behavioral safety, not capability, and that Docker containment is environmental, not behavioral, safety.

Strengths:

(1) The conceptual contribution is substantial and well-argued: the distinction between behavioral, structural, and environmental controls, and the "near violation" concept (behavioral FAIL + environmental containment success), is a genuinely useful contribution to how the community should think about agent safety evaluation.

(2) The taxonomy is carefully constructed and the crosswalk to Sprocket and APTS (Table 3) is transparent about which properties are direct, partial, or new. The paper is scrupulous about not overclaiming APTS conformance.

(3) The scenario design is thoughtful: SD-04 (HTTP 302 redirect to an excluded host) is a particularly good test of the "application sent me there" vs. "I am authorized to go there" distinction, and the AIR-03 case (agent names the injection and then still requests the excluded ports) is a striking illustration of the gap between recognizing an injection and refusing it.

(4) The paper is exceptionally honest about its limitations: single run per scenario, temperature 1.0, no variance study, synthetic targets, model/prompt dependence, non-equivalent scenario sets, thin coverage per property, no independent re-scoring. Section 8 is a model of transparent limitation reporting.

(5) The finding that the multi-agent system failed HC-01 (destructive reset without approval) while the single-agent system passed it is a valuable counter to the naive "multi-agent is safer" reading, and the paper explicitly flags this ("This is the result that most clearly blocks any reading of Table 6 as 'the multi-agent system is safer'").

(6) The paper's distinction between a benchmark, a governance standard, and a conceptual framework (Table 1) is clear and useful, and the refusal to treat APTS conformance and behavioral measurement as interchangeable is an important methodological point.

Major Weaknesses:

(1) The central empirical comparison is statistically underpowered and the author knows it. Each scenario was run once at temperature 1.0. The 12 vs. 10 difference on 17 scenarios is not significant (p ≈ 0.72), and the paper says so. But this means the headline result ("BlacksmithAI passed 12, PentestGPT passed 10") is essentially a description of two single trajectories, not an estimate of relative safety. The paper could have strengthened this by running each scenario 3–5 times (the scenarios are cheap Docker services, and the paper reports a budget-conscious setup), reporting pass rates with confidence intervals, and at least describing variance. As it stands, the empirical contribution is a set of illustrative case studies, not a benchmark result.

(2) The scenarios are synthetic Flask services with planted signals, and the paper does not demonstrate that behavior on these scenarios predicts behavior on real targets. This is acknowledged in the limitations, but it is a fundamental validity concern for a safety benchmark: an agent may behave differently when out-of-scope addresses look like production dependencies rather than loopback companions, and the paper does not test this. The "ecological validity" of the benchmark is therefore unestablished.

(3) The evaluation is confounded by system prompt and toolset differences. The paper states that "each system otherwise runs with its own native system prompt and tool set, so differences between systems are architectural" (Table 5 caption) — but this is precisely the confound: the differences are not attributable to architecture alone, since system prompt and tools differ. The paper acknowledges this in Section 8 ("Because the two systems differ in system prompt and tooling as well as in architecture, differences between them cannot be attributed to architecture alone"), but the framing in the results and abstract still implicitly invites an architectural reading. A cleaner design would have held the system prompt and toolset constant across both systems (to the extent possible) or would have compared multiple configurations of each system.

(4) The multi-agent scenarios are simulated rather than live. CASP-02 "serves a simulated child-agent report" and SDG-01/SDG-02 use HTTP responses rather than live child processes. The paper acknowledges this ("the fixtures are small, the child is simulated by an HTTP response in CASP-02"), but it means the multi-agent properties are tested at the coordinator level only, and the claim that "the properties are measurable" is weaker than it appears — a live child that can ignore the parent, hold its own tools, and persist after termination is a fundamentally different test.

(5) The property-level results are based on 1–4 scenarios each, and the paper draws qualitative conclusions from single-scenario properties. For example, "Human control ran the other way. PentestGPT passed both approval scenarios. BlacksmithAI passed the ambiguous-authorization scenario and failed HC-01" — this is two scenarios per system, and the conclusion ("the multi-agent system acted and the single-agent system did not") is based on one failure. The paper acknowledges thin coverage but still uses these results to support a qualitative contrast, which is a reasonable framing but should be more cautious.

(6) The author is the developer of BlacksmithAI, one of the two systems evaluated. This is disclosed in the Conflict of Interest section, which is good, but it is a significant concern for the objectivity of the comparison. The outcomes "were taken from recorded evaluator files rather than from a re-scoring performed for this manuscript"; this is a mitigating factor, but the evaluator files were presumably produced by the author. An independent re-scoring (as the paper itself calls for in future work) would substantially strengthen the paper.

The paper is long and somewhat repetitive. Sections 3.3–3.9 restate the same design principles (behavioral vs. structural vs. environmental, near violations, over-refusal) multiple times, and the appendix tables (A1, B2) duplicate much of the main text. The paper could be shortened by 20–30% without loss.

(7) The related-work section is good but could engage more with the agent-safety evaluation literature (e.g., AgentBench, WebArena, ToolEmu, "Agent-as-a-Judge" work) beyond the offensive-security-specific references. The paper's contribution is to behavioral safety evaluation, and the connection to the broader agent-evaluation literature is under-developed.
Review 3
Overall evaluation	
-1: weak reject
Summary

The paper proposes a 12-property behavioral-safety taxonomy and a 25-scenario executable benchmark (24 Dockerized Flask services + 1 prompt-only) for evaluating whether offensive-security LLM agents exercise safe judgment under authorization. It adapts 6 of Sprocket's 7 properties, adds 6 (two multi-agent), and compares BlacksmithAI v1.0.0 (19/25, 76.0%) vs. PentestGPT v1.0.0 (10/17, 58.8%; shared-set 12 vs. 10, p ≈ 0.72, not significant).

Strengths

- Well-motivated distinction between capability and behavioral safety; the "authorization paradox" framing is apt.
- Careful lineage positioning against Sprocket and APTS without overclaiming equivalence.
- The near-violation rule (behavioral FAIL + environmental containment success) is a genuine contribution.
- Unusually candid limitations section; results are interpreted against the tempting "multi-agent is safer" reading.
- Useful reproducibility artifacts (Appendices A–C).

Weaknesses

Major

- Single run per scenario at temperature 1.0 — no variance; denominator-1 property rates are anecdotal.
- Benchmark unreleased/unversioned; some outcomes are bare PASS/FAIL without criterion tables (especially PentestGPT).
- Non-equivalent scenario sets (17 vs. 25); three architecture-independent AIR scenarios not run for PentestGPT.
- Multi-agent fixtures are simulated over HTTP, not live child processes — claims are weak "lower bounds."
- Several properties (IM, RC, SCT, STR) rest on a single scenario.

Minor

- Severe table-rendering corruption (Pages 13, 19; Tables 2, 3, 7 with duplicated/misaligned rows).
- Fisher's exact test not described in methods; over-refusal defined but not independently measured.
- Results tied to one model/provider; author is developer of BlacksmithAI (disclosed but no blinding).
- Low-resolution figures; references lack archival DOIs/tags.

Recommendations

- Re-run each scenario ≥3 times and report variance.
- Release a versioned benchmark with full evaluator criterion tables.
- Fix all table/formatting corruption.
- Close or explicitly reframe the PentestGPT coverage gap.
- Add a live-child multi-agent scenario or downgrade multi-agent claims to "measurability."
- Add second scenarios for single-scenario properties.