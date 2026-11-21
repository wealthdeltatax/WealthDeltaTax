# Agent system: review and improvement plan

**Status:** recommendations for staged adoption  
**Scope:** the five-role agent system, its instructions, skills, repository workflow and quality controls  
**Purpose:** improve reliability, consistency and throughput without adding agents or making the instruction set unnecessarily large

## Executive recommendation

The current five-role structure is sound. Keep the roles and the progressive-disclosure design: a short router, shared rules, a role guide, then only the task-specific reference material. The system's advantage comes less from making a model generally more capable and more from reducing the number of decisions it must make, defining boundaries, and giving it reliable project memory.

The next improvement should therefore be **more executable guardrails, not more agents or longer prompts**. Fix ambiguity at the boundaries, automate checks that can be deterministic, and preserve author control over substantive decisions.

This is a proposal, not an instruction to implement every item at once. Some safeguards described below already exist in the current guides. Retain and build on them rather than duplicating them.

## 1. What is already working

The five roles have useful and distinct purposes:

| Role | Main contribution |
|---|---|
| Guru | Maintains project direction, settled decisions, briefs, status and coordination |
| Code | Implements models and data pipelines within explicit technical constraints |
| Writing | Produces and edits the canonical written papers while preserving the author's voice |
| Research | Verifies literature, sources, citations and reference records |
| Web | Builds and deploys the public-facing Quarto site without changing the underlying research |

The separation works because each role receives a narrower definition of success:

- **Code** is told where parameters belong, which architectural boundaries matter, how tests are run, and not to alter tests merely to obtain a pass. This reduces silent numerical drift and makes implementation more reproducible.
- **Writing** has explicit style and formatting rules, plus boundaries around changes to claims and structure. This is important because generic editing can make technically correct prose less faithful to the author's argument and voice.
- **Research** has a verification workflow and explicit rules against inventing or silently correcting references. This makes uncertainty and provenance visible.
- **Guru** uses the Project Map, decisions register, briefs and status documents as institutional memory. This reduces repeated debate and prevents settled decisions being reopened casually.
- **Web** is constrained to present the research rather than independently reinterpret it. That separation protects the distinction between the argument and its public presentation.

The current instructions also contain several valuable operational lessons: input audits before releasing a stage, early magnitude checks, separate test-suite invocations where test configuration clashes, asserted replacements for scripted edits, and clear stop conditions. These are examples of instructions derived from actual failure modes. Keep that approach.

## 2. Design principles to preserve

1. **Five roles are enough for now.** Do not create another role unless a recurring body of work has a genuinely distinct owner, workflow and acceptance criteria.
2. **Keep progressive disclosure.** Shared rules belong in `AGENTS.md`; role behaviour belongs in role guides; detailed procedures belong in referenced material. Avoid copying the same rule into several places.
3. **One authoritative source for each rule.** Other files should link to it, not paraphrase it.
4. **Use briefs for consequential work, not bureaucracy.** A brief should make scope, ownership, inputs, acceptance criteria and checks clearer. It should not be a mandatory ceremony for a trivial, obvious edit.
5. **Prefer deterministic checks to repeated prose.** If a rule can be checked by a script, make the script authoritative and keep the instruction concise.
6. **Keep authorial authority explicit.** Agents can make implementation decisions within scope; they must not silently make policy, economic, philosophical or irreversible project decisions.
7. **Optimise for total task time.** The relevant measure is completed, verified work, including coordination and integration cost, not the number of agents working simultaneously.

## 3. Priority improvements

### Priority 1: make ownership unambiguous

The role guides already distinguish much of the work, but there are boundary areas where two roles can reasonably touch related files. The clearest example is `pipeline/`: Code owns model/data pipeline work while Web owns site-build scripts. The Guru also has broad ownership of `docs/`, while Research and Writing have narrower responsibilities in parts of that tree.

Keep the current division, but add a compact ownership and escalation table in the agent documentation. Define ownership by file pattern or subdirectory, not just by broad subject.

Suggested baseline:

| Area | Primary owner | Boundary |
|---|---|---|
| `model_v1/`, `model_v3/` | Code | Model implementation and model tests |
| Data/model pipeline scripts | Code | Excludes site-only build and rendering scripts |
| `tests/` | Code | Specialist may propose a test; Code owns test implementation and suite integrity |
| `site/`, site-only pipeline scripts, `.github/workflows/` | Web | No changes to canonical paper claims |
| `source/` | Writing | Canonical paper text; substantive argument changes need author approval |
| `registry/references.bib`, reference records and `docs/research/` | Research | Changes to author-controlled fields or records require confirmation |
| Project overview, status, decisions, briefs and agent documentation | Guru | Does not override specialist ownership of research/reference records or paper text |
| Cross-role or unclear ownership | Guru coordinates | Ask the author if the decision changes substance or cannot be resolved from an existing rule |

This table is a starting point, not a reason to split files artificially. Where a task crosses boundaries, nominate one **change owner** and name the other role as reviewer. Avoid two agents editing the same file in parallel.

### Priority 2: clarify the authority model

Make the decision boundary explicit in the shared rules and role guides:

- **Author:** decides policy positions, economic assumptions, philosophical commitments, substantive paper conclusions and irreversible choices.
- **Guru:** decides task scope, sequencing, delegation, documentation and whether a question is already settled. Recommends a course of action but does not impersonate the author.
- **Specialists:** choose technical methods and implementation details within the brief and established project constraints.
- **Reviewers:** test whether the work meets its stated criteria; they do not silently expand the scope.

When an unresolved decision must be presented, require a concise decision note containing:
1. the recommendation;
2. the strongest practical alternative;
3. the reason for preferring the recommendation;
4. the consequence if the recommendation is wrong; and
5. whether the decision is reversible.

This gives the author useful decision material without escalating every small implementation choice.

### Priority 3: make role routing more discriminating

Keep the five skill entry points short. Their descriptions should route by **task type**, not merely by mentioning WDT or the repository.

Recommended routing:

- **Guru:** mechanism, policy/design questions, project planning, cross-paper consistency, brief creation and coordination.
- **Code:** Python, numerical models, data/model pipelines, tests and implementation bugs.
- **Writing:** drafting, editing, compression, paper formatting, citations as they appear in prose, and cross-references.
- **Research:** literature searches, source verification, bibliography and evidence coverage.
- **Web:** Quarto, HTML/CSS/JS, site routing, rendering, accessibility, build and deployment.

Add short exclusions to prevent role drift:

- Research reports evidence; it does not decide policy.
- Writing improves expression and structure; it does not change substantive conclusions without approval.
- Code implements the specified mechanism; it does not reinterpret surprising economic results.
- Web presents the approved work; it does not rewrite findings or canonical source text.
- Guru coordinates specialist work; it should not redo specialist implementation merely because it can.

Avoid broad overlapping trigger phrases in the skill descriptions. The role guide should be loaded only after the task has been classified.

### Priority 4: route model work by version and stage

The Code guide distinguishes legacy v1/v2 material from staged model v3 work. Make the reference routing equally explicit so a general conventions document cannot accidentally be treated as authoritative for every model generation.

Specify:
- v1 work: use the v1 conventions and relevant legacy tests;
- v2: treat it as a specification/reference unless a brief explicitly says otherwise;
- v3: use `docs/model-v3/architecture.md`, the named stage contract and v3-specific tests;
- shared pipeline work: use pipeline-specific conventions and the relevant data contracts.

The brief's `Read:` section should name the applicable version, stage and contract. If a convention conflicts with a newer architecture or a stage contract, stop and surface the conflict rather than choosing silently.

### Priority 5: automate scaffold integrity

The agent system should be able to detect its own documentation drift. Add a small validation script, then run it in CI and locally before merging changes to agent documentation.

It should check:

- internal Markdown links and referenced paths;
- paths named in role guides and the agent README;
- existence of referenced briefs, templates and workflow documents where required;
- skill source/package parity;
- duplicate or contradictory shared rules where practical;
- changed-file ownership against the ownership table, with an explicit override for cross-role work.

**Important:** the current references such as `reference/framework.md` in files under `docs/agents/` are relative to that directory. Do not mechanically rewrite them as root-relative paths. A validator should resolve Markdown links relative to the file containing them, which avoids false positives.

Keep the validator narrow and maintainable. A simple path/link checker that catches real breakage is more valuable than an elaborate agent-policy linter that produces noise.

### Priority 6: remove manual skill-package drift

The current documentation describes role skill stubs under `.claude/skills/` and corresponding `.skill` archives for the claude.ai account, with a manual rebuild and comparison process.

Retain the canonical source, but generate the packaged archives from it with a script. Add a check that unpacks each generated archive and compares its contents with the source. CI should fail if a committed package is stale.

This removes a predictable manual failure point. Do not maintain two independently edited versions of the same skill.

### Priority 7: provide a reliable test orchestrator

The current guides correctly warn that some test suites must run as separate commands because their pytest configuration can clash. Preserve that isolation.

Add a thin orchestrator that:
- invokes each required suite in its own process;
- records the exact command and exit status;
- continues through the required suites even if one fails;
- produces a concise pass/fail summary and preserves useful output;
- supports selecting only the suites relevant to a brief.

It should not combine test collection into one pytest process or change test expectations. The brief still determines which checks are required; the orchestrator only makes those checks easier to run consistently.

### Priority 8: strengthen the build and deployment gate

Because pushing to `main` deploys the live site, deployment needs an explicit quality gate. Before enabling or changing automation, inspect the current workflow and preserve its intended deployment behaviour.

At minimum, changes that can affect the live site should have the relevant build, link and route checks run before deployment. Verify that the deployed commit is the intended commit and that the workflow completed successfully.

A failed deployment should trigger a clear stop-and-report procedure. Reverting should be deliberate and based on the actual failure, not an automatic reaction to every transient workflow issue.

## 4. Risk-based review and merge policy

The current auto-merge model reduces unnecessary author interruptions. Keep that benefit, but distinguish routine work from changes whose author or independent review is important.

| Change class | Minimum verification | Author involvement |
|---|---|---|
| Routine documentation, typo or link fix | Diff review and link check | Not normally required |
| Formatting or site presentation | Relevant format/build/link checks | Only if meaning or presentation choice is substantive |
| Reference database or evidence records | Source verification, discrepancy report, required confirmation | Required where current rules specify confirmation |
| Model or numerical implementation | Relevant isolated tests, input audit, magnitude/invariant checks | Required for changed assumptions or unexplained findings |
| Economic assumptions, policy positions or paper conclusions | Explicit alternatives and consequences documented | Required |
| Deployment workflow, generated-data contract or other high-impact infrastructure | Build/CI checks and independent review of the change | Required where deployment or project risk is material |

The author should not have to review every low-risk change. Conversely, an agent should not be the sole judge of a high-impact change simply because it authored the implementation.

A practical rule: **the more consequential, irreversible or difficult-to-detect a failure is, the more independent verification it needs.**

## 5. Improve specialist behaviour without expanding the prompts

### Guru

- Continue using the Project Map and decisions register as the source of settled project context.
- Before creating parallel briefs, estimate whether the work is genuinely independent. Parallelise when expected time saved exceeds coordination, review and integration costs.
- Avoid splitting small related tasks into multiple briefs merely to make the lane plan look busy.
- Delegate independent research, implementation and review; keep cross-cutting decisions with the Guru and author.
- Keep briefs small, with disjoint `Touches`, measurable acceptance criteria, named inputs and explicit checks.

### Code

- When a run produces an unexpected economic result, report the mathematical result, inputs, parameter values and reproducibility evidence. Do not decide what the result means for policy or the paper.
- Add or preserve input-availability checks, numerical invariants and reproducibility checks where they protect important contracts.
- Keep the existing early magnitude check: test whether a stage can plausibly reach its target before building more stages on top of it.
- Never weaken a test or alter a benchmark merely to obtain a pass.

### Writing

Use three levels of editing and state which one is being performed:

1. **Mechanical:** formatting, references, cross-links, captions and consistency.
2. **Editorial:** clarity, structure, compression and flow without changing the argument.
3. **Substantive:** changes to claims, assumptions, interpretation or conclusions.

Mechanical and editorial work can normally be delegated within scope. Substantive changes require explicit author approval. A useful claim check is: is the claim supported, is its scope precise, is uncertainty represented honestly, and does the wording imply more than the evidence establishes?

### Research

- Label evidence by type: primary/official data, peer-reviewed work, working paper/preprint, secondary reporting, or author judgement.
- Record date, provenance and what the source actually supports.
- Surface disagreement between sources rather than choosing the most convenient value.
- Distinguish absence of evidence from evidence of absence.
- Keep the existing confirmation rules for changes to author-controlled reference records.

### Web

- Add accessibility, mobile layout and link integrity to the repeatable site checks.
- Keep builds reproducible and verify that the deployed revision matches the intended commit.
- Treat site architecture documentation as a maintained technical contract, not an aspirational description.
- Preserve the boundary between rendering the research and changing the research.

## 6. Brief quality and completion checks

The existing brief template should remain the main unit of delegated work. Consider adding a compact completion checklist or validator that checks whether a brief has:

- a clear objective and reason for the task;
- a single accountable owner;
- bounded `Touches` and named inputs;
- measurable acceptance criteria;
- named tests/build checks;
- an explicit author-decision point, or a statement that none is expected;
- a change report when files were changed;
- a clear branch/merge state.

Do not require every field to be elaborate. Partial briefs should remain possible when the task is exploratory, but they must state what is unknown and what decision the exploratory work is meant to inform.

## 7. Suggested implementation sequence

### Phase A: clarify the existing system

1. Add the ownership and authority table.
2. Tighten skill descriptions and exclusions.
3. Make model-version/stage reference routing explicit.
4. Check that shared rules have one authoritative home and that skill stubs only route to the guides.
5. Review the brief template for proportionality and decision clarity.

**Exit condition:** an agent can identify the right role, file owner, applicable rules and decision authority without guessing.

### Phase B: automate the repetitive checks

1. Add the documentation/link/path validator.
2. Generate skill archives and check package parity.
3. Add the isolated test-suite orchestrator.
4. Add a brief completion check if it can be done without excessive ceremony.
5. Wire the appropriate checks into CI.

**Exit condition:** common scaffold, packaging and test-running errors are caught automatically before merge.

### Phase C: strengthen verification where risk justifies it

1. Add risk-based review requirements to the merge workflow.
2. Confirm the pre-deployment quality gate and deployed-commit verification.
3. Add accessibility/mobile checks to the site workflow.
4. Review actual task outcomes and remove rules that create friction without preventing meaningful errors.

**Exit condition:** high-impact changes receive independent verification while routine work remains low-friction.

## 8. What not to do

- Do not add more agents yet.
- Do not put every reference document into every role's context.
- Do not duplicate shared rules across five skill files.
- Do not make every minor edit require a brief, an author approval or a second agent.
- Do not parallelise work with overlapping file ownership.
- Do not automate policy decisions or substantive interpretation.
- Do not build a large framework for checking the agent framework. Start with simple checks tied to observed failure modes.

## 9. How to judge whether the changes worked

Evaluate the system by operational outcomes, not by prompt length or agent count. Track a small set of measures over a sample of real tasks:

- proportion of tasks completed without ownership or instruction clarification;
- avoidable rework caused by missed inputs, broken paths or stale skill packages;
- proportion of required checks run successfully before merge;
- number of integration conflicts and overlapping-file edits;
- author interruptions per completed task, separated into necessary decisions and avoidable questions;
- regressions discovered after merge or deployment.

The goal is not zero questions. It is fewer avoidable questions, with important decisions reaching the author in a form that is quick to evaluate.

## Final recommendation

The current system has the right basic architecture. Its strongest feature is the combination of narrow roles, explicit boundaries, accumulated project decisions and practical failure-prevention rules. Preserve that.

The biggest opportunity is to move from **asking agents to remember and follow every operational rule** toward **making the repository check those rules automatically**. Start by clarifying ownership and routing, then automate paths, skill packaging and isolated tests. Keep the author in control of substance, and use independent review in proportion to risk.

That should improve consistency and efficiency more than adding another agent or making the existing instructions substantially longer.
