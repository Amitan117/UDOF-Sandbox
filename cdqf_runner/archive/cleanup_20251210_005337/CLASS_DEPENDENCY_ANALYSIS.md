# CLASS Dependency Analysis

## Current Usage of CLASS in CDQF

CLASS (via `classy` Python wrapper) is used in `CDQFBoltzmannFull` for:

1. **σ₈ Normalization** (line 317-329):
   - Gets reference `sigma8_0` from standard CLASS
   - Used to normalize σ₈(z) = σ₈(0) × D(z)
   - **Not essential** - can use reference value or Planck constraint

2. **Sound Horizon** (line 412):
   - Computes `r_s_drag` for BAO calculations
   - **Not essential** - BAO tests can use observed values directly

## Conclusion: CLASS is Optional for Growth Factor

**Growth factor computation itself doesn't require CLASS** - it's only used for:
- Reference σ₈ normalization (can use fixed value ~0.81)
- Sound horizon (can use fixed value ~147 Mpc)

## Recommendation

Since CLASS is a standard cosmology tool and the runner validates cosmology, **we should add it to requirements** if:
1. Installation is straightforward (`pip install classy-community` or similar)
2. It's useful for other tests (BAO, CMB, etc.)
3. It doesn't break sandbox isolation

**If CLASS is problematic to install**, we can:
- Use reference values for σ₈(0) and r_s
- Keep standalone versions as fallback
- Document CLASS as optional for full functionality

