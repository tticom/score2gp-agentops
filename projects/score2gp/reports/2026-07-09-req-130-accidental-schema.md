# Req-130 Accidental and Key Signature Pitch Mapping Schema

This document defines the schema, modifier lookup tables, precedence rules, scope limits, and fail-closed behaviors for modifying base natural MIDI pitches based on accidental candidates and key signatures.

## 1. Mathematical Modifier Model

The final pitch of a note candidate, $P_{\text{final}}$, is resolved by applying a semitone modifier offset $M$ to the baseline natural MIDI pitch $P_{\text{natural}}$:

$$P_{\text{final}} = P_{\text{natural}} + M$$

Where:
- $P_{\text{natural}}$ is the MIDI pitch resolved by `map_staff_step_to_midi_pitch` (representing the natural scale degree of the staff position under the active clef).
- $M \in \mathbb{Z}$ is the combined modifier offset in semitones.

## 2. Key Signature Lookups

A key signature defines default alterations (sharps or flats) for specific pitch classes (note letter names, independent of octave). Minor keys are mapped directly to their relative major counterparts.

### 2.1. Sharp Key Signatures (Major and Relative Minor)

| Major Key | Relative Minor | Sharps | Affected Pitch Classes |
| :--- | :--- | :---: | :--- |
| **C Major** | A Minor | 0 | None |
| **G Major** | E Minor | 1 | F |
| **D Major** | B Minor | 2 | F, C |
| **A Major** | F# Minor | 3 | F, C, G |
| **E Major** | C# Minor | 4 | F, C, G, D |
| **B Major** | G# Minor | 5 | F, C, G, D, A |
| **F# Major**| D# Minor | 6 | F, C, G, D, A, E |
| **C# Major**| A# Minor | 7 | F, C, G, D, A, E, B |

### 2.2. Flat Key Signatures (Major and Relative Minor)

| Major Key | Relative Minor | Flats | Affected Pitch Classes |
| :--- | :--- | :---: | :--- |
| **F Major** | D Minor | 1 | B |
| **Bb Major**| G Minor | 2 | B, E |
| **Eb Major**| C Minor | 3 | B, E, A |
| **Ab Major**| F Minor | 4 | B, E, A, D |
| **Db Major**| Bb Minor | 5 | B, E, A, D, G |
| **Gb Major**| Eb Minor | 6 | B, E, A, D, G, C |
| **Cb Major**| Ab Minor | 7 | B, E, A, D, G, C, F |

---

## 3. Accidental Modifier Values

Accidental candidates modify the pitch class as follows:

| Accidental Type | Symbol/Label | Modifier Value (semitones) |
| :--- | :---: | :---: |
| **Flat** | `b` | $-1$ |
| **Natural** | `n` (or `♮`) | $0$ (overrides key signature) |
| **Sharp** | `#` | $+1$ |
| **Double Flat** | `bb` | $-2$ |
| **Double Sharp**| `##` (or `x`) | $+2$ |

---

## 4. Precedence and Modifier Resolution Rules

When resolving the modifier $M$ for a note candidate at pitch class $PC$ (e.g., `'F'`) and octave $OCT$ (e.g., $5$):

### 4.1. Precedence Levels

1. **Level 1 (Highest): Direct Local Accidental**
   If an accidental candidate is directly attached to the notehead (based on spatial proximity boundaries, typically within $1.5 \cdot \text{staff\_spacing}$ to the left of the notehead), its modifier value is applied.

2. **Level 2: Measure-Local Accidental Memory**
   If no direct accidental is attached, but a previous note candidate with the same pitch class $PC$ *and the same octave* $OCT$ in the current measure had an accidental applied, that accidental's modifier carries over.

3. **Level 3: Key Signature Accidental**
   If no measure-local accidental is active, the modifier defined by the key signature for the pitch class $PC$ is applied ($+1$ for sharps, $-1$ for flats, $0$ otherwise).

4. **Level 4 (Lowest): Natural Base**
   Modifier $M = 0$.

### 4.2. Scope and Lifetime of Accidentals

- **Accidental Scope**: A measure-local accidental is octave-specific (e.g., an accidental on F5 does not alter F4).
- **Accidental Lifetime**: The modifier persists until:
  - Overridden by another local accidental on the same pitch class and octave.
  - A barline candidate is crossed (the end of the measure), at which point all measure-local accidental memory is cleared and the key signature resets.

---

## 5. Fail-Closed Behaviors

To maintain strict safety and prevent invalid conversion artifacts:

1. **Conflicting Accidentals**: If multiple conflicting local accidental candidates are associated with the same notehead, ignore both and apply Level 2 or Level 3 rules (fail-closed).
2. **Ambiguous Association**: If an accidental candidate is positioned too far from any notehead (exceeding proximity tolerance limits), it is treated as noise and ignored.
3. **Unrecognized or Ambiguous Key Signature**: If the key signature candidate is missing, ambiguous, or fails validation, the system falls back to C Major (0 accidentals), ensuring no spurious pitch alterations are performed.
