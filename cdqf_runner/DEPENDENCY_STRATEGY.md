# Dependency Strategy - CLASS and Upstream Modules

## Strategy: Prefer Original Modules, Fallback to Standalone

**Rationale:** The original upstream modules are more complete and validated. The standalone versions are fallbacks for when CLASS/universe modules are unavailable.

---

## Dependency Priority

### 1. **Upstream Modules (Preferred)**
- **ProperCorrectedGrowth** - Full implementation with CLASS support
- **TSESEResponseDerivation** - Full implementation with CLASS support  
- **compute_S_ESE_proper** - Full implementation from parent repo

**Requirements:**
- Parent project accessible (for imports)
- CLASS available (for ProperCorrectedGrowth and TSESEResponseDerivation)

**Benefits:**
- More complete and validated
- Uses CLASS for σ₈ normalization and sound horizon
- Matches production codebase

---

### 2. **Integrated Standalone Modules (Fallback)**
- **ProperGrowthStandalone** - Extracted without CLASS
- **RXResponseStandalone** - Extracted without CLASS
- **compute_S_ESE_proper** (integrated) - With dependency handling

**Requirements:**
- Only NumPy/SciPy (already in requirements)

**Benefits:**
- Works without CLASS dependency
- Self-contained
- Still provides core functionality

---

## CLASS Installation

**Option 1: Use CLASS from parent project**
- If parent project is accessible, CLASS is already there
- Just need to ensure imports work

**Option 2: Install classy-community**
```bash
pip install classy-community
```

**Option 3: Build from source**
- Clone class_public repository
- Build classy module
- Add to PYTHONPATH

---

## Current Implementation

The runner now uses **priority-based fallback**:

1. **Try upstream module first** (requires CLASS)
2. **Fallback to integrated standalone** (no CLASS needed)
3. **Final fallback** to simple computations

This ensures:
- Best functionality when dependencies available
- Graceful degradation when unavailable
- No hard failures

---

## Recommendations

1. **Include CLASS in requirements** (as optional/comment)
   - Standard cosmology tool
   - Useful for σ₈ and sound horizon
   - Better accuracy

2. **Keep standalone versions**
   - Provide fallback when CLASS unavailable
   - Enable testing without full dependencies
   - Maintain isolation capability

3. **Document dependency status**
   - Clear what requires CLASS
   - What works without it
   - How to install CLASS if desired

