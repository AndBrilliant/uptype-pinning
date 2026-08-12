# WORKLOG — running state, update as you go

Purpose: this session keeps timing out mid-task. Anything not written here is
lost. Update after EVERY completed step, not at the end.

Last updated: 2026-08-12, after P3 recovery + statistics citations (02bdb72).

## STATUS: MC COMPLETE, LEAN COMPLETE, BOTH INTEGRATED
All five operation nulls run. All Lean modules build and sweep clean.
The manuscript cites the actual repo state (133 decls, seven modules).

---

## ENVIRONMENT

- gateway token at `/home/claude/token.txt`, expires 2026-08-13 03:20 UTC
- helper `/home/claude/mcp.py` — `session(slug)`, `bash(sid,url,cmd)`
- ganymede: 32 cores, Lean at `~/.elan/bin`, repos in `~`
- manuscript: `/home/claude/manuscript` -> Overleaf origin/main
- MC + findings: `~/gmc` on ganymede (git, local only)
- Lean: `~/uptype-pinning` (git, pushes to github.com/AndBrilliant/uptype-pinning)

Upload pattern that works (avoid heredoc quoting hell):
  base64 the file, chunk at 3000 chars, `printf '%s' >>` each chunk, then
  `base64 -d file.b64 > file && rm file.b64`

Long jobs: `setsid env PYTHONUNBUFFERED=1 nohup <cmd> > log 2>&1 </dev/null &
disown`, then poll the log in a later call. Do NOT wait inline.

---

## DONE

### Manuscript (`d208ca8`, Overleaf, 6pp, clean)
- [x] heavy-pair letter restructured around the involution
- [x] frames section corrected (self-scale, not scale-free; common-scale ratio 4.5328 disclosed)
- [x] ladder-extension test (nothing at n=+-2) + pair self-scale negative (11 sigma)
- [x] top excluded on five grounds incl. the sectoral one (m_H^2 = m_Z m_t, cite 2605.21721)
- [x] split constant priced honestly (sqrt(10.8), 23/7, pi+1/7 all fit better)
- [x] census section reports its NEGATIVE result
- [x] trajectory section (PDG 2014/2019/2024, rms 6.27 -> 1.31)
- [x] amplification lemma with closed form
- [x] formal-verification section

### MC (`~/gmc`, 14 commits)
- [x] SPEC_GMC frozen, 8 gates, hash seeds the RNG
- [x] census: NEGATIVE (frame-invariant means all fail; common-scale collapse 6->2->0)
- [x] mu* MC: 5 constraints, p < 1.5e-6 at 2e6 draws
- [x] cumulative/monotonicity: every subset, every order, no plateau
- [x] look-elsewhere menus: O1 .081-.104, O2 .091-.171, O3 .057-.075, O4 .072-.136
- [x] private number: ~3 sigma fully corrected
- [x] out-of-sample trajectory + pdg_migration.png

### Lean (`7d93477`, pushed)
- [x] HeavyPair.lean wired into build (was orphaned, never compiled) — 21 decls
- [x] Sensitivity.lean NEW — 18 decls, the amplification lemma
- [x] axiom sweep clean on all; 110 declarations total, zero stubs
- [x] VERIFICATION_SENSITIVITY.md

---

## IN PROGRESS

- [x] falsification criterion DONE, manuscript pushed. Two-part:
      (A) joint frequency above 1e-3 at measurement-driven tolerance
      (B) either relation beyond 1.5 sigma in TWO CONSECUTIVE PDG editions
      calibrated: 1.5 sigma vs present worst pull 0.28 sigma (this letter),
      0.33 sigma (wider set). two-edition clause needed because PDG central
      values move ~0.5 sigma on reanalysis alone.
- [x] Lean: FrameInvariance.lean DONE (7 decls) + LightMap.lean DONE (16 decls)
      pushed as a9271f8. 133 declarations across seven modules, 8565 jobs,
      axiom sweep clean throughout.
      NOTE: LightMap.lean was written in a turn that TIMED OUT before it
      could report. The detached build finished anyway. This is exactly the
      failure mode the worklog exists for — always check the repo state
      before assuming a task is undone.

## NEXT, in priority order

- [x] O5 ladder menu null DONE: 525 declared entries, 6 land, assignment
      unique for 4 of 5 quarks, null 1.1-1.6, worst-prior p = 0.013.
      In the manuscript census section (2a7056d).
- [ ] decide whether Gpair (+2.67% at mu*) belongs in the joint claim or
      stays in the heavy-pair letter alone — USER DECISION, do not guess

## CITATIONS THAT MUST NOT DRIFT AGAIN

- PDG quark-mass review: the QCD renormalisation factor is identical for
  EVERY flavour, so pairwise ratios are scheme- and scale-independent up to
  negligible QED between different-charge quarks. This is the authoritative
  statement of the invariance and it is FLAVOUR-UNIVERSAL, not same-sector.
  I got this wrong once; the paper now cites PDG2019 directly.
- P3 leaves open whether an ASCENDING orbit exists. P4 answers it. Use that
  framing, not "the map does not stop at the light quarks".
- P3's three-routes-to-mu* over-determination, gains differing by 3500,
  agreeing to 0.0031 percent. This is the constructive use of the
  amplification lemma and is the precedent for it.
- Statistics: Gross-Vitells (trials factor), Cousins 1807.05996
  (foundations, local vs global), Lyons 1310.1284 (why 5 sigma, and why a
  low-prior claim needs more). All three now cited.
- Kocik arXiv:1201.2067 appears in P3's bibliography and is NOT yet used
  here — check whether it is relevant before the next draft.

## KNOWN OPEN QUESTIONS FOR THE USER

- Gpair in or out of the joint five
- whether the wave-grammar paper (the frame-free one) gets restructured
  given that three of the four frame-free claims are its content
- m_s/m_d is the only relation that moved AWAY in 2019->2024 and is also the
  only frame-invariant one. Flagged, not explained.

---

## ERRORS I MADE THIS SESSION (do not repeat)

1. Called the mu* relations "convention-dependent". They are SCALE-FIXED.
   mu* is the lepton pole sum, fixed before any quark enters. User caught it.
2. Built a joint MC that let the data use two values of m_b (2 GeV for Q_D,
   self-scale for Gpair) while the null got one. Invalid; discarded.
3. Ran the top below its own threshold to get "m_t at mu*". Not a defined
   quantity; produced a -4% error in Q_U that was pure bug.
4. Let the tolerance float with the residuals in the first epoch MC, so the
   null scaled too and the result was flat and meaningless.
5. Quoted m_b agreement as 0.001% when the input error is 0.167% — that is
   0.01 sigma, luck inside the bar, not a sharper relation.
