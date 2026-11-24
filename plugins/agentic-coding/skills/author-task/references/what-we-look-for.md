# What we look for

The rubrics in `agentic_coding_docs` (topics `idea` and `review`) are the bar the automated gates apply. This file covers why tasks miss that bar, and what Askable staff check once a task reaches review. Ask about each item as a question, one at a time, and let the engineer answer in their own words. When an answer is weak, say so plainly and why.

Every item serves one question: **when a strong model fails this task, is it because the task is hard in the way it claims, or because the task is wrong?** A good task fails strong models for fair, varied reasons that match the difficulty it claims.

## The idea

- **The wrong fix.** Can the engineer name the fix a capable model writes first, and say exactly why it is wrong? This is the strongest predictor of a hard task. If they cannot name it, the task is probably easy, however hard it feels.
- **Reasoning, not volume.** The difficulty comes from understanding the codebase: two components that interact, an invariant the obvious change breaks, a lifecycle path the caller never sees. Long, tedious or trivia-heavy work is not hard in the way we need.
- **No oracle in reach.** If the agent can check its output against a reference inside the environment (a sibling implementation, a parser in the dependencies, the repository's own importer), it iterates until green. Choose changes where being right needs understanding, not comparison.
- **A change a maintainer would merge.** It lives in a real, permissively licensed upstream, starts at a commit on its default branch, and touches at least two non-test files. Name where it lands and what it must do.
- **Their own ground.** The best tasks come from a codebase the engineer has built or debugged in, where they already know the failure that bit them.

## The brief

- **A brief, not a plan.** `instruction.md` states the end state a maintainer asked for. It gives no diff, no algorithm and no file-by-file plan.
- **Inferred, not enumerated.** The strongest tasks have a requirement the agent finds by reading the code: a sibling path that must change too, a cache to keep consistent, an existing behaviour the change must match. A brief that lists every property tests whether the agent can follow a checklist, not whether it can engineer.
- **One voice.** Read the brief end to end for sentences that contradict each other. An attempt that follows one section and fails a check written for another is an unfair failure.
- **Every asserted value is reachable.** Every exact name, flag, string or number a check asserts is in the brief, in a repository doc it points to, or derivable from the code. A value the brief names but never defines is a defect, even when the engineer finds it obvious.
- **The runtime is stated.** If the tests run as a particular user, with a particular `PATH`, toolchain, ownership or permissions, or under a time budget, and a correct solution depends on it, the brief says so or the repository makes it plain.
- **Exclusions hold.** Nothing the brief puts out of scope is tested.
- **Stated rules are checked.** If the brief requires formatting, a lint, or "no new unsafe code", a check enforces it.

## The checks

- **Every check follows from the brief.** A check on something the brief and repository do not imply is a hidden requirement. It gets the version rejected, and it is not the difficulty we want.
- **Behaviour, not design.** Tests assert observable behaviour, not helper names, call order, call counts, internal tables, record layout or the golden's ordering. Ask: could a structurally different correct design pass every check? Write one and try it.
- **Every check tells right from wrong.** Compare the reference and untouched repository with the control outcomes specified in the current project docs. Inspect which checks decided each outcome. Repeating a check on the same input should give the same verdict across timing, order and locale changes unless the brief makes one of them relevant.
- **Scope that fits the brief.** The path allowlist admits every file a reasonable solution touches, including the small accessor or helper in a neighbouring file that a different design needs. A line cap bounds scope; it does not set difficulty. Tests count toward it, so leave room for the tests the brief asks for.
- **Concrete judged criteria.** A `prompt` check names exactly what passes. It never penalises a change the repository's own rules require (a changelog entry, a version or copyright bump, a regenerated file), or a correct change for living in a different file than the golden's.
- **Independent scenarios.** A suite that stops at its first failing case hides every later failure, from the engineer as much as from the review. Let each case report on its own.
- **Requirements are enforced.** For each requirement the brief names directly, point to the test that fails the plausible wrong fix for it: symptom-only, half a fix, the hard-coded example, the wrong edge case. A requirement with no such test is a weak test, and review sends it back.
- **Regression guards are welcome.** A check that the fix keeps behaviour the brief says must stay unchanged rewards an agent that verifies its own change. It is one of the best sources of fair difficulty.

## Reviewing a version

Ask the engineer to choose one requirement, show where the solver can discover it, and explain how their check distinguishes their reference solution from their plausible wrong fix. Use the engineer’s own cases and expected results.

Look at the local run output together. Did the check reach the behaviour the engineer meant to test? If it stopped during setup, that requirement is still unverified. For a discrepancy, record what the engineer expected and what actually happened.

## Calibration and attacks

- **Near-misses a model would write.** The calibration attempts cover different ways to be almost right. At least one is the golden patch with one small bug inside the code it adds, and a blocker catches it. A valid alternative differs from the golden in structure, not just names.
- **Attack it yourself first.** Before submitting, try to earn reward without solving the task: a lazy solution, tampering with the tests or their runner, reading the answer from the image or git history, matching the example output. Close every gap in the checks, never by adding hints to the brief. Record each attempt in `docs/hack-report.md`.

## The environment

- **Nothing to find.** The image, its files, its git history and its dependencies hold neither the solution nor the hidden tests. Look at what the image already has at the paths the tests use.
- **The brief's commands work.** Every test, lint or build command the brief gives passes on the untouched base inside the image, and leaves no stray files behind.
- **Budgets fit.** Per-check time budgets add up to less than the verifier's deadline, and the golden runs within the task's memory and CPU.

## The docs

- **Docs match the task.** `README.md` and `docs/` agree with the golden, the hidden tests and the brief: no stale path or command, no behaviour the golden lacks, no test described that does not exist. Review sends back documentation that contradicts the task.
- **Claimed difficulty is real.** What `docs/source.md` and `docs/rationale.md` say makes the task hard is what attempts actually fail. If every attempt solves the advertised hard part and a late edge case decides the result, the docs overstate the task.
- **An honest history.** `docs/hack-report.md` records what each version added and why. Original work, honestly sourced: the golden patch is the engineer's own change, and the contamination searches are recorded as they ran.

## What weakens a passing task

These can still pass review, but they make the task worth less. Raise them before the engineer builds, while they are cheap to avoid.

- **One narrow trap.** Most failures come from one check or one case, while the difficulty the task claims is solved by every attempt. The reward is then nearly a single bit. Aim for failures that vary across the claimed difficulty.
- **Rare deciding cases.** The behaviour that decides the result appears in a handful of hidden cases and none of the examples the agent can see.
- **Difficulty tuned, not designed.** Hidden cases added only because the last model run passed, with no change to the brief, or a hint trimmed until the score dropped into range. Review judges each case on whether the brief grounds it, not on how it was found. A rule that survives only as one sentence makes the reward measure that sentence.

## What staff review checks

A task that passes every automated gate is reviewed by Askable staff before delivery. They send it back when they can reproduce one of these:

1. A correct solution that follows the brief gets the wrong result.
2. A result can be earned without doing the work.
3. The golden patch breaks something the brief names directly.
4. A weak test: a requirement the brief names directly is not enforced, or a plausible wrong fix passes while the golden behaves differently.
5. Wrong documentation, as above.

To get there, reviewers run the golden on cases the brief names beyond the engineer's own tests, try a structurally different valid design, check what the solver can read and write, and read the failed attempts to see whether each failure was fair. Engineers who do the same before submitting rarely get sent back.

## After a result

- **Fix the whole list.** Each version fixes every item the feedback lists, not one at a time. Versions are limited, and only failures on Askable's side are free.
- **Keep what works.** When a version is sent back, change what was asked and leave the rest alone. Review checks that the requested fixes closed and that nothing else moved.
- **Read the attempts.** When a version is too easy, `agentic_coding_get_submission` links each model attempt's trajectory. Read how the model solved it before changing anything. The fix is usually visible there.
- **Verify a revision.** Repeat the engineer’s original example after the change and compare the result with the feedback.
- **Make it harder by going deeper.** Add an invariant the brief implies and the obvious fix breaks, a guard on existing behaviour that the obvious fix breaks, or more of the cases the brief already covers. Keep every requirement stated: blurring the brief, or checking behaviour it does not imply, gets rejected.
