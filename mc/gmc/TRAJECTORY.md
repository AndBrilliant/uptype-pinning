# Out-of-sample: the trajectory between PDG editions

Sources: PDG 2019 quark-mass review (fetched, rpp2019-rev-quark-masses),
PDG 2024/2026 as used throughout. Values as PDG quotes them: light quarks
MSbar at 2 GeV, c and b at their own scales.

| input | PDG 2019 | PDG 2024 | error tightened |
|---|---|---|---|
| m_u | 2.32(10) | 2.16(7) | 1.3x |
| m_d | 4.71(9) | 4.70(7) | 1.3x |
| m_s | 92.9(7) | 93.5(8) | 0.9x |
| m_c(m_c) | 1280(13) | 1272.9(4.6) | 2.8x |
| m_b(m_b) | 4198(12) | 4183(7) | 1.7x |

## Did the residuals move toward the predictions?

| relation | 2019 | 2024 | verdict |
|---|---|---|---|
| sqrt(m_c m_b) = (1+a)mu* | +0.513% | +0.055% | TOWARD, 9.4x |
| m_c m_b = (3/2)mu*^2 | +1.029% | +0.110% | TOWARD, 9.4x |
| m_b/m_c = pi^2/3 | -0.309% | -0.112% | TOWARD, 2.8x |
| m_u^2 = m_d 2m_e | +11.816% | -2.869% | TOWARD 4.1x, crossed zero |
| m_s/m_d = a^-2 | -0.374% | +0.483% | crossed zero, |dev| grew |

4 of 5 moved toward.

## What is and is not established

NOT established by the count alone: 4-of-5 under a coin flip is p = 0.19.
The tally is not the evidence.

Suggestive, and the reason to record this:

  1. The involution improved 9.4x while its dominant input (m_c) tightened
     only 2.8x. A false relation's residual stays put as errors shrink; this
     one converged faster than the error shrinkage alone accounts for.

  2. Two relations CROSSED ZERO rather than drifting: m_u^2 = m_d 2m_e from
     +11.8% to -2.9%, and m_s/m_d from -0.37% to +0.48%. Passing through the
     predicted value is what a true relation with fluctuating measurements
     does. Monotone drift away is what a false one does. Neither drifted.

  3. m_s/m_d is the one that got worse in absolute terms, and it also
     crossed. Its 2024 value sits 0.48% high where 2019 sat 0.37% low.

## Why this matters more than the forecast

The forecast in FORECAST.md is a projection under assumptions. This is data
that already existed, chosen by no one, and it points the same way. It is the
only out-of-sample evidence in the corpus that did not require waiting.

## The next data point

FLAG/PDG next cycle. Under scenario A the heavy-pair residual should stay at
or below 0.05% and m_s/m_d should return toward 19.80. Under scenario B the
involution should stop improving and settle at a nonzero value as m_c
precision continues to improve. Both are checkable without any new work.
