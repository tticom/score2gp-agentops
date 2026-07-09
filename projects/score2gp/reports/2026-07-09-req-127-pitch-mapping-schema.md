# Req-127 Clef-Aware Pitch Mapping Schema

This document defines the mathematical models, algorithms, and lookup tables for translating notehead vertical staff positions to MIDI pitches in the Score2GP system based on the active logical clef (Treble, Bass, or Alto).

## 1. Staff Coordinate System

As implemented in [pdf_staff_position_diagnostics.py](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/pdf_staff_position_diagnostics.py), the vertical position of noteheads is represented by `staff_step_index`, which grows downward from the top staff line (Line 0):

$$\text{staff\_step\_index} = \frac{y_{\text{candidate}} - y_{\text{line\_0}}}{\frac{1}{2} \cdot \text{staff\_spacing}}$$

Where:
- Even values of `staff_step_index` correspond to staff lines.
- Odd values of `staff_step_index` correspond to staff spaces.
- Values $< 0$ represent positions above the staff (ledger lines/spaces).
- Values $> 8$ represent positions below the staff (ledger lines/spaces).

## 2. Diatonic Step Representation

We define a reference diatonic step scale $d$ where Middle C (C4) is diatonic step $0$. Each integer step corresponds to one diatonic scale degree (natural notes only, assuming C major baseline):

$$d \in \mathbb{Z}$$

The mapping from a diatonic step $d$ to a baseline MIDI pitch is defined as:

$$\text{midi}(d) = 60 + 12 \cdot \text{octave}(d) + \text{OFFSET}[d \pmod 7]$$

Where:
- $\text{octave}(d) = d \text{ div } 7$ (using floor integer division, e.g., $-1 \text{ div } 7 = -1$)
- $\text{OFFSET} = [0, 2, 4, 5, 7, 9, 11]$ (representing C, D, E, F, G, A, B offsets)

## 3. Clef Diatonic Offsets

Each clef maps `staff_step_index` (step) to the diatonic step $d$ via a clef-specific starting offset constant $C_{\text{clef}}$:

$$d = C_{\text{clef}} - \text{step}$$

The offsets for the three logical clefs are:

| Clef | Top Line (step=0) Note | Diatonic Offset $C_{\text{clef}}$ |
| :--- | :--- | :--- |
| **Treble Clef** | F5 | $10$ |
| **Bass Clef** | A3 | $-2$ |
| **Alto Clef** | G4 | $4$ |

---

## 4. Treble Clef Reference Table ($C_{\text{treble}} = 10$)

Covers 3 ledger lines above/below:

| Step | Type | Location Description | Note Name | Diatonic $d$ | MIDI Pitch |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **-6** | Line | 3rd Ledger Line Above | E6 | $16$ | 88 |
| **-5** | Space | Space above 2nd Ledger Line | D6 | $15$ | 86 |
| **-4** | Line | 2nd Ledger Line Above | C6 | $14$ | 84 |
| **-3** | Space | Space above 1st Ledger Line | B5 | $13$ | 83 |
| **-2** | Line | 1st Ledger Line Above | A5 | $12$ | 81 |
| **-1** | Space | Space above Staff | G5 | $11$ | 79 |
| **0** | Line | **Line 0 (Top Line)** | F5 | $10$ | 77 |
| **1** | Space | Space 0 | E5 | $9$ | 76 |
| **2** | Line | Line 1 | D5 | $8$ | 74 |
| **3** | Space | Space 1 | C5 | $7$ | 72 |
| **4** | Line | Line 2 (Middle Line) | B4 | $6$ | 71 |
| **5** | Space | Space 2 | A4 | $5$ | 69 |
| **6** | Line | Line 3 | G4 | $4$ | 67 |
| **7** | Space | Space 3 | F4 | $3$ | 65 |
| **8** | Line | **Line 4 (Bottom Line)** | E4 | $2$ | 64 |
| **9** | Space | Space below Staff | D4 | $1$ | 62 |
| **10** | Line | 1st Ledger Line Below | C4 (Middle C) | $0$ | 60 |
| **11** | Space | Space below 1st Ledger Line | B3 | $-1$ | 59 |
| **12** | Line | 2nd Ledger Line Below | A3 | $-2$ | 57 |
| **13** | Space | Space below 2nd Ledger Line | G3 | $-3$ | 55 |
| **14** | Line | 3rd Ledger Line Below | F3 | $-4$ | 53 |

---

## 5. Bass Clef Reference Table ($C_{\text{bass}} = -2$)

Covers 3 ledger lines above/below:

| Step | Type | Location Description | Note Name | Diatonic $d$ | MIDI Pitch |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **-6** | Line | 3rd Ledger Line Above | G4 | $4$ | 67 |
| **-5** | Space | Space above 2nd Ledger Line | F4 | $3$ | 65 |
| **-4** | Line | 2nd Ledger Line Above | E4 | $2$ | 64 |
| **-3** | Space | Space above 1st Ledger Line | D4 | $1$ | 62 |
| **-2** | Line | 1st Ledger Line Above | C4 (Middle C) | $0$ | 60 |
| **-1** | Space | Space above Staff | B3 | $-1$ | 59 |
| **0** | Line | **Line 0 (Top Line)** | A3 | $-2$ | 57 |
| **1** | Space | Space 0 | G3 | $-3$ | 55 |
| **2** | Line | Line 1 | F3 | $-4$ | 53 |
| **3** | Space | Space 1 | E3 | $-5$ | 52 |
| **4** | Line | Line 2 (Middle Line) | D3 | $-6$ | 50 |
| **5** | Space | Space 2 | C3 | $-7$ | 48 |
| **6** | Line | Line 3 | B2 | $-8$ | 47 |
| **7** | Space | Space 3 | A2 | $-9$ | 45 |
| **8** | Line | **Line 4 (Bottom Line)** | G2 | $-10$ | 43 |
| **9** | Space | Space below Staff | F2 | $-11$ | 41 |
| **10** | Line | 1st Ledger Line Below | E2 | $-12$ | 40 |
| **11** | Space | Space below 1st Ledger Line | D2 | $-13$ | 38 |
| **12** | Line | 2nd Ledger Line Below | C2 | $-14$ | 36 |
| **13** | Space | Space below 2nd Ledger Line | B1 | $-15$ | 35 |
| **14** | Line | 3rd Ledger Line Below | A1 | $-16$ | 33 |

---

## 6. Alto Clef Reference Table ($C_{\text{alto}} = 4$)

Covers 3 ledger lines above/below:

| Step | Type | Location Description | Note Name | Diatonic $d$ | MIDI Pitch |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **-6** | Line | 3rd Ledger Line Above | F5 | $10$ | 77 |
| **-5** | Space | Space above 2nd Ledger Line | E5 | $9$ | 76 |
| **-4** | Line | 2nd Ledger Line Above | D5 | $8$ | 74 |
| **-3** | Space | Space above 1st Ledger Line | C5 | $7$ | 72 |
| **-2** | Line | 1st Ledger Line Above | B4 | $6$ | 71 |
| **-1** | Space | Space above Staff | A4 | $5$ | 69 |
| **0** | Line | **Line 0 (Top Line)** | G4 | $4$ | 67 |
| **1** | Space | Space 0 | F4 | $3$ | 65 |
| **2** | Line | Line 1 | E4 | $2$ | 64 |
| **3** | Space | Space 1 | D4 | $1$ | 62 |
| **4** | Line | Line 2 (Middle Line) | C4 (Middle C) | $0$ | 60 |
| **5** | Space | Space 2 | B3 | $-1$ | 59 |
| **6** | Line | Line 3 | A3 | $-2$ | 57 |
| **7** | Space | Space 3 | G3 | $-3$ | 55 |
| **8** | Line | **Line 4 (Bottom Line)** | F3 | $-4$ | 53 |
| **9** | Space | Space below Staff | E3 | $-5$ | 52 |
| **10** | Line | 1st Ledger Line Below | D3 | $-6$ | 50 |
| **11** | Space | Space below 1st Ledger Line | C3 | $-7$ | 48 |
| **12** | Line | 2nd Ledger Line Below | B2 | $-8$ | 47 |
| **13** | Space | Space below 2nd Ledger Line | A2 | $-9$ | 45 |
| **14** | Line | 3rd Ledger Line Below | G2 | $-10$ | 43 |
