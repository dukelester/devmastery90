"""Shape / figure series aptitude — always multiple choice (A–D)."""
from __future__ import annotations

from typing import Any


def _mcq(
    prompt: str,
    choices: list[str],
    correct_index: int,
    explanation: str,
    difficulty: str = "medium",
    category: str = "shape_patterns",
    hints: str = "",
) -> dict[str, Any]:
    """Build an A–D multiple-choice shape question.

    choices: four display strings (Unicode / ASCII figures).
    correct_index: 0–3 for A–D.
    """
    assert len(choices) == 4, "Need exactly four choices"
    assert 0 <= correct_index <= 3
    keys = ["A", "B", "C", "D"]
    choice_objs = [{"key": keys[i], "text": choices[i]} for i in range(4)]
    return {
        "question": prompt.strip(),
        "answer": keys[correct_index],
        "explanation": explanation,
        "category": category,
        "difficulty": difficulty,
        "hints": hints,
        "choices": choice_objs,
    }


def build_shape_pattern_questions() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    items.extend(
        [
            _mcq(
                "What shape comes next?\n\n○  △  □  ○  △  ?",
                ["□", "○", "△", "◇"],
                0,
                "Cycle: circle → triangle → square → repeat. Next is □.",
                "easy",
            ),
            _mcq(
                "What comes next?\n\n●  ○  ●  ○  ●  ?",
                ["●", "○", "◐", "◎"],
                1,
                "Alternating filled and hollow. Next is hollow ○.",
                "easy",
            ),
            _mcq(
                "What shape comes next?\n\n■  ◆  ●  ■  ◆  ?",
                ["■", "◆", "●", "▲"],
                2,
                "Cycle square → diamond → circle. Next is ●.",
                "easy",
            ),
            _mcq(
                "What comes next?\n\n△  ▽  △  ▽  △  ?",
                ["△", "▽", "▲", "□"],
                1,
                "Up and down triangles alternate. Next is ▽.",
                "easy",
            ),
            _mcq(
                "What comes next?\n\n◇  ◆  ◇  ◆  ◇  ?",
                ["◇", "◆", "○", "●"],
                1,
                "Hollow / filled diamonds alternate. Next is ◆.",
                "easy",
            ),
            _mcq(
                "Choose the next figure:\n\n☆  ★  ☆  ★  ☆  ?",
                ["☆", "★", "✦", "✧"],
                1,
                "Hollow and filled stars alternate. Next is ★.",
                "easy",
            ),
            _mcq(
                "What comes next?\n\n◁  △  ▷  ▽  ◁  ?",
                ["◁", "△", "▷", "▽"],
                1,
                "Triangle pointer rotates 90° clockwise. After ◁ comes △.",
                "medium",
                hints="Watch which way the tip points.",
            ),
            _mcq(
                "What comes next?\n\n○  ◐  ●  ○  ◐  ?",
                ["○", "◐", "●", "◑"],
                2,
                "Empty → half → full cycle. Next is ●.",
                "easy",
            ),
            _mcq(
                "What comes next?\n\n▲  ▶  ▼  ◀  ?",
                ["▲", "▶", "▼", "◀"],
                0,
                "90° clockwise cycle of length 4 returns to ▲.",
                "easy",
            ),
            _mcq(
                "What comes next?\n\n└  ┘  ┐  ?",
                ["┌", "└", "┘", "┐"],
                0,
                "Corner rotates 90° clockwise → ┌.",
                "medium",
            ),
        ]
    )

    items.extend(
        [
            _mcq(
                "Which figure comes next?\n\n▲▲  →  ▲▲▲  →  ▲▲▲▲  →  ?",
                ["▲▲▲▲▲", "▲▲", "▲▲▲▲▲▲", "▲"],
                0,
                "Count increases by 1 each step: 2, 3, 4, then 5.",
                "easy",
            ),
            _mcq(
                "Which option continues the pattern?\n\n□○  →  ○□  →  □○  →  ?",
                ["□○", "○□", "□□", "○○"],
                1,
                "Pairs swap each step. Next is ○□.",
                "easy",
            ),
            _mcq(
                "What is the next image?\n\n●○○  →  ○●○  →  ○○●  →  ?",
                ["●○○", "○●○", "●●○", "○○○"],
                0,
                "Filled circle moves right, then wraps to the start.",
                "medium",
            ),
            _mcq(
                "Which figure comes next?\n\n▲▼  →  ▼▲  →  ▲▼  →  ?",
                ["▲▼", "▼▲", "▲▲", "▼▼"],
                1,
                "The pair flips each step. Next is ▼▲.",
                "easy",
            ),
            _mcq(
                "Choose the next shape pair:\n\n■◆  →  ◆●  →  ●■  →  ?",
                ["■◆", "◆■", "●◆", "■●"],
                0,
                "Shapes cycle ■ → ◆ → ●; consecutive pairs wrap to ■◆.",
                "hard",
            ),
            _mcq(
                "What comes next?\n\n◐  →  ◑  →  ◒  →  ?",
                ["◓", "◐", "●", "○"],
                0,
                "Half-fill rotates through four orientations. Next is ◓.",
                "medium",
            ),
            _mcq(
                "Which option belongs next?\n\n△□□  →  □△○  →  ○□△  →  ?",
                ["△○□", "□○△", "○△□", "△□○"],
                0,
                "Left-rotate the three symbols; after ○□△ the next is △○□.",
                "medium",
            ),
            _mcq(
                "Next figure?\n\n★☆☆  →  ☆★☆  →  ☆☆★  →  ?",
                ["★☆☆", "☆★☆", "★★☆", "☆☆☆"],
                0,
                "Filled star marches right then wraps. Next is ★☆☆.",
                "easy",
            ),
            _mcq(
                "Shape analogy: ○ is to ● as □ is to ?",
                ["■", "◆", "○", "▢"],
                0,
                "Hollow maps to filled of the same family → ■.",
                "easy",
            ),
            _mcq(
                "Shape analogy: ▲ is to ▼ as ◀ is to ?",
                ["▶", "▲", "▽", "◁"],
                0,
                "Flip direction: left chevron maps to right ▶.",
                "medium",
            ),
        ]
    )

    items.extend(
        [
            _mcq(
                "Which does not belong?\n\n△   □   ○   ▲",
                ["△", "□", "○", "▲"],
                3,
                "▲ is filled; the others are outlines.",
                "easy",
            ),
            _mcq(
                "Which does not belong?\n\n■   ◆   ●   ▲",
                ["■", "◆", "●", "▲"],
                3,
                "▲ is the only triangle (3 sides).",
                "medium",
            ),
            _mcq(
                "Odd one out:\n\n□□   ○○   △△   ■○",
                ["□□", "○○", "△△", "■○"],
                3,
                "Only ■○ is a mixed pair.",
                "easy",
            ),
            _mcq(
                "Complete the analogy:\n\n●○●  is to  ○●○  as  ■□■  is to ?",
                ["□■□", "■■■", "□□□", "■□□"],
                0,
                "Invert each cell’s fill → □■□.",
                "medium",
            ),
            _mcq(
                "What comes next?\n\n▲○  →  ○▲  →  ▲○  →  ○▲  →  ?",
                ["▲○", "○▲", "▲▲", "○○"],
                0,
                "Two-frame alternation. Next is ▲○.",
                "easy",
            ),
            _mcq(
                "Matrix row pattern:\nRow1: ○○●\nRow2: ○●○\nRow3: ?\n\nWhich completes the matrix?",
                ["●○○", "○○●", "●●○", "○●●"],
                0,
                "Filled circle moves left one column each row.",
                "medium",
            ),
            _mcq(
                "Each row has one ■, one ◆, one ●.\n"
                "Row1: ■ ◆ ●\nRow2: ◆ ● ■\nRow3: ● ? ■\n\nWhat replaces ?",
                ["◆", "■", "●", "▲"],
                0,
                "Row3 must be ● ◆ ■.",
                "hard",
            ),
            _mcq(
                "Outer/inner shapes swap each frame:\n"
                "1) □ with ○ inside\n"
                "2) ○ with □ inside\n"
                "3) △ with ○ inside\n"
                "4) ?",
                ["○ with △ inside", "△ with □ inside", "□ with △ inside", "○ with □ inside"],
                0,
                "After △ outer, next outer is ○ with previous outer △ inside.",
                "hard",
            ),
            _mcq(
                "What comes next?\n\nb  →  q  →  d  →  ?",
                ["p", "b", "d", "q"],
                0,
                "Letter silhouette flip/rotate cycle: b → q → d → p.",
                "medium",
            ),
            _mcq(
                "Mirror to the right of ▶. What do you see?",
                ["◀", "▶", "▲", "▼"],
                0,
                "Horizontal reflection reverses the arrow → ◀.",
                "easy",
            ),
        ]
    )

    # Growing rows (show options as compact strings)
    items.extend(
        [
            _mcq(
                "What comes next?\n\n●\n● ●\n● ● ●\n● ● ● ●\n?",
                ["● ● ● ● ●", "● ● ●", "● ● ● ● ● ●", "●"],
                0,
                "One more circle each row → five.",
                "easy",
            ),
            _mcq(
                "What comes next?\n\n■ ■ ■ ■\n■ ■ ■\n■ ■\n?",
                ["■", "■ ■", "■ ■ ■ ■ ■", "□□"],
                0,
                "Descending by one → single ■.",
                "easy",
            ),
            _mcq(
                "Choose the next:\n\n◆\n◆ ◆ ◆\n◆ ◆ ◆ ◆ ◆\n?",
                ["◆ ◆ ◆ ◆ ◆ ◆ ◆", "◆ ◆ ◆ ◆ ◆ ◆", "◆ ◆", "◆"],
                0,
                "Odd counts 1, 3, 5, then 7.",
                "medium",
            ),
            _mcq(
                "Next orientation?\n\n⊂  →  ∩  →  ⊃  →  ?",
                ["∪", "⊂", "∩", "⊃"],
                0,
                "Open side rotates 90° → ∪.",
                "medium",
            ),
            _mcq(
                "Series: L-shape rotates 90° clockwise.\nL  →  Γ  →  ⌝  →  ?",
                ["⌞", "L", "⌝", "Γ"],
                0,
                "Next orientation is ⌞.",
                "hard",
            ),
            _mcq(
                "Fill toggles in pairs (two hollow, two filled…):\n"
                "hollow, hollow, filled, filled, hollow, ?",
                ["hollow", "filled", "half", "striped"],
                0,
                "Pairs of hollow → next is hollow.",
                "medium",
            ),
            _mcq(
                "What shape comes next if sides increase:\n● (curve) → △ → □ → ⬠ → ?",
                ["⬡ hexagon", "★ star", "○ circle", "▲ triangle"],
                0,
                "Sides 0/curve → 3 → 4 → 5 → 6 (hexagon).",
                "easy",
            ),
            _mcq(
                "Shadow of a cube can look like a hexagon. True or false?",
                ["True", "False", "Only if transparent", "Only 2D drawing"],
                0,
                "From a corner angle the silhouette can be hexagonal.",
                "medium",
                category="spatial",
            ),
            _mcq(
                "A straight line of 6 squares — can it fold into a cube?",
                ["No", "Yes", "Only with tape", "Only if colored"],
                0,
                "Cube nets cannot be longer than 4 squares in a row.",
                "hard",
                category="spatial",
            ),
            _mcq(
                "Fold paper in half twice (same direction), punch one hole. Holes when unfolded?",
                ["4", "2", "8", "1"],
                0,
                "Two folds → 4 layers → 4 holes.",
                "easy",
                category="spatial",
            ),
        ]
    )

    # ASCII grid MCQs
    items.extend(
        [
            _mcq(
                "What is the next image?\n\n"
                "1)  #.\n    ..\n\n"
                "2)  ##\n    ..\n\n"
                "3)  ##\n    #.\n\n"
                "4) ?",
                ["##\n##", ".#\n##", "#.\n#.", "..\n##"],
                0,
                "Cells fill left→right, top→bottom until all four are filled.",
                "medium",
            ),
            _mcq(
                "What comes next?\n\n"
                "X..\n...\n...\n\n"
                ".X.\n...\n...\n\n"
                "..X\n...\n...\n\n?",
                ["...\nX..\n...", "X..\n...\n...", "...\n.X.\n...", "...\n...\n..X"],
                0,
                "X walks across the top, then to middle-left.",
                "medium",
            ),
            _mcq(
                "Next grid?\n\n"
                "O..\n...\n...\n\n"
                "OO.\n...\n...\n\n"
                "OOO\n...\n...\n\n?",
                ["OOO\nO..\n...", "OOO\nOOO\nOOO", "...\nOOO\n...", "O..\nO..\nO.."],
                0,
                "After filling row 1, continue on row 2 from the left.",
                "medium",
            ),
            _mcq(
                "Choose the next figure:\n\n[ ] → [■] → [■■] → ?",
                ["[■■■]", "[ ]", "[■■]", "[■■■■]"],
                0,
                "Filled cells increase by one.",
                "easy",
            ),
            _mcq(
                "What is the next image?\n\n"
                "*..\n...\n...\n\n"
                "*.*\n...\n...\n\n"
                "*.*\n*.*\n...\n\n?",
                ["*.*\n*.*\n*.*", "***\n*.*\n*.*", "*.*\n...\n*.*", "***\n***\n***"],
                0,
                "Corners fill until the 2×3 block’s corners complete → option A.",
                "hard",
            ),
        ]
    )

    # Generated rotation cycles as MCQ
    cycles = [
        (["▲", "▶", "▼", "◀"], "Clockwise triangle pointer."),
        (["◐", "◑", "◒", "◓"], "Half-disk rotates through four orientations."),
        (["▁", "▂", "▃", "▄"], "Bar grows taller."),
        (["░", "▒", "▓", "█"], "Shade gets denser."),
        (["➀", "➁", "➂", "➃"], "Circled numbers increase."),
    ]
    for cycle, why in cycles:
        for i in range(len(cycle)):
            shown = [cycle[(i + j) % len(cycle)] for j in range(3)]
            correct = cycle[(i + 3) % len(cycle)]
            # Build 4 options: correct + 3 distractors from cycle / nearby
            distractors = [c for c in cycle if c != correct]
            while len(distractors) < 3:
                distractors.append(cycle[0])
            opts = [correct, distractors[0], distractors[1], distractors[2]]
            # Shuffle deterministically by rotating start
            rot = i % 4
            opts = opts[rot:] + opts[:rot]
            correct_index = opts.index(correct)
            items.append(
                _mcq(
                    "What comes next?\n\n" + "  ".join(shown) + "  ?",
                    opts,
                    correct_index,
                    why + f" Cycle: {' → '.join(cycle)}.",
                    "easy" if len(cycle) <= 4 else "medium",
                )
            )

    # Sliding filled circle strips
    for pos in range(4):
        frames = []
        for f in range(3):
            cells = ["○"] * 4
            cells[(pos + f) % 4] = "●"
            frames.append("".join(cells))
        nxt = ["○"] * 4
        nxt[(pos + 3) % 4] = "●"
        correct = "".join(nxt)
        wrongs = []
        for w in range(4):
            if w == (pos + 3) % 4:
                continue
            cells = ["○"] * 4
            cells[w] = "●"
            wrongs.append("".join(cells))
        opts = [correct, wrongs[0], wrongs[1], wrongs[2]]
        rot = pos % 4
        opts = opts[rot:] + opts[:rot]
        items.append(
            _mcq(
                "What is the next image?\n\n" + "\n".join(frames) + "\n?",
                opts,
                opts.index(correct),
                "Filled circle moves one step right each frame (wraps).",
                "easy",
            )
        )

    # 2×2 binary fill MCQ (subset to keep volume reasonable)
    def grid(v: int) -> str:
        bits = f"{v:04b}"
        top = "".join("■" if b == "1" else "□" for b in bits[:2])
        bot = "".join("■" if b == "1" else "□" for b in bits[2:])
        return f"{top}\n{bot}"

    for n in range(0, 10):
        correct = grid(n + 3)
        opts = [grid(n + 3), grid(n + 4), grid(n + 2), grid((n + 5) % 16)]
        # unique opts
        seen = set()
        uniq = []
        for o in opts:
            if o not in seen:
                seen.add(o)
                uniq.append(o)
        while len(uniq) < 4:
            cand = grid((n + len(uniq) * 3) % 16)
            if cand not in seen:
                seen.add(cand)
                uniq.append(cand)
        rot = n % 4
        uniq = uniq[rot:] + uniq[:rot]
        items.append(
            _mcq(
                "What is the next image? (2×2 fill counts up in binary)\n\n"
                f"{grid(n)}\n\n{grid(n+1)}\n\n{grid(n+2)}\n\n?",
                uniq,
                uniq.index(correct),
                "Read cells as bits top-left→bottom-right; value +1 each frame.",
                "hard",
                hints="Row-major binary.",
            )
        )

    items.extend(_hard_shape_mcqs())
    return items


def _hard_shape_mcqs() -> list[dict[str, Any]]:
    """Harder figure series, matrices, and dual-rule puzzles (always A–D)."""
    return [
        _mcq(
            "Two rules at once: (1) shape cycles □ → ○ → △\n"
            "(2) fill toggles hollow ↔ solid each step.\n\n"
            "Series: □  →  ●  →  △  →  ?",
            ["■", "○", "▲", "●"],
            0,
            "Next shape is □ (cycle restart) and fill flips from hollow △ to solid ■.",
            "hard",
            hints="Track shape and fill on separate tracks.",
        ),
        _mcq(
            "Each step: rotate 90° clockwise AND add one side mark.\n"
            "Start: ▷\n"
            "Then: ▼·\n"
            "Then: ◁··\n"
            "Next?",
            ["▲···", "▷···", "▼··", "◁····"],
            0,
            "Pointer goes ◁ → ▲; dots increase to 3.",
            "hard",
        ),
        _mcq(
            "Matrix (rows share a rule, columns share another):\n\n"
            "▲○  |  ○▲  |  ▲○\n"
            "■□  |  □■  |  ■□\n"
            "●◇  |  ◇●  |  ?\n\n"
            "What replaces ?",
            ["●◇", "◇●", "●●", "◇◇"],
            0,
            "Odd columns match column 1 pattern; column 3 mirrors column 1 → ●◇.",
            "hard",
        ),
        _mcq(
            "Odd frames grow a ring; even frames fill the center.\n\n"
            "1) ○\n"
            "2) ◉\n"
            "3) ◎\n"
            "4) ?",
            ["⦿", "○", "●", "◎"],
            0,
            "Frame 4 is even → filled center inside the double ring → ⦿ (approx).",
            "hard",
            hints="Alternate ring-growth vs center-fill.",
        ),
        _mcq(
            "Symbols move on a 3-slot belt; each step the leftmost exits and a new symbol enters right from the cycle ▲●■.\n\n"
            "Start: ▲ ● ■\n"
            "Next:  ● ■ ▲\n"
            "Next:  ■ ▲ ●\n"
            "Next: ?",
            ["▲ ● ■", "● ▲ ■", "■ ● ▲", "▲ ■ ●"],
            0,
            "Full rotation returns to ▲ ● ■.",
            "hard",
        ),
        _mcq(
            "Black-cell counts grow +1, +2, +3, +4…\n"
            "Counts so far: 1, 2, 4, 7. Next count?",
            ["11", "8", "10", "9"],
            0,
            "7 + 4 = 11.",
            "hard",
        ),
        _mcq(
            "Overlay rule: frame N is XOR of the previous two (■ where they differ).\n\n"
            "F1: ■□\n    □■\n\n"
            "F2: □■\n    ■□\n\n"
            "F3: ?",
            ["■■\n■■", "□□\n□□", "■□\n□■", "□■\n■□"],
            0,
            "Every pair of cells differs → all ■.",
            "hard",
            hints="XOR / difference of fills.",
        ),
        _mcq(
            "Each row = previous row reflected, then leftmost cell inverted.\n\n"
            "Row1: ■ □ □\n"
            "Row2: ■ □ ■\n"
            "  (reflect □□■, invert left → ■□■)\n"
            "Row3: ?",
            ["□ □ ■", "□ ■ □", "■ □ ■", "□ □ □"],
            0,
            "Reflect ■□■ → ■□■; invert left → □□■.",
            "hard",
        ),
        _mcq(
            "Cube net unfolded. Which face is opposite the center face marked C?\n\n"
            "  [A]\n"
            "[B][C][D]\n"
            "  [E]\n"
            "  [F]\n",
            ["F", "A", "B", "D"],
            0,
            "In this cross, F folds opposite C (A is adjacent on the other side).",
            "hard",
            hints="Faces sharing an edge are adjacent, not opposite.",
        ),
        _mcq(
            "Rotation + shade: each step rotate 90° CCW and darken one step ░→▒→▓→█.\n\n"
            "Start: ░ pointing as └\n"
            "After 1: ┘ in ▒\n"
            "After 2: ┐ in ▓\n"
            "After 3: ?",
            ["┌ in █", "└ in █", "┘ in ░", "┐ in █"],
            0,
            "CCW: ┐ → ┌; shade next is █.",
            "hard",
        ),
        _mcq(
            "Two interleaved series:\n"
            "Odd positions: ▲ ▼ ▲ ▼ …\n"
            "Even positions: ○ ○ ● ● ○ ○ ● ● … (pairs)\n\n"
            "Sequence so far: ▲ ○ ▼ ○ ▲ ● ▼ ?\n"
            "What is position 8?",
            ["●", "○", "▲", "▼"],
            0,
            "Even slots: ○○●●… so positions 2,4=○ and 6,8=●.",
            "hard",
        ),
        _mcq(
            "3×3: each row and column must contain ▲, ■, ● once (Latin square).\n\n"
            "▲ ■ ●\n"
            "■ ? ▲\n"
            "● ▲ ■\n\n"
            "What is ?",
            ["●", "■", "▲", "○"],
            0,
            "Middle cell must be ● to finish the Latin square.",
            "hard",
        ),
        _mcq(
            "Paper folding punch: fold once vertically (left over right), once horizontally (top over bottom), punch near the open corner. Unfolded hole pattern?",
            [
                "One hole near each of 4 corners",
                "One hole center only",
                "Two holes on a diagonal",
                "Three holes",
            ],
            0,
            "Two perpendicular folds → 4 layers; punch maps to all four corners.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Which figure is the same as ◢ after reflecting in a vertical mirror then rotating 90° clockwise?",
            ["◤", "◥", "◣", "◢"],
            0,
            "Vertical mirror of ◢ → ◣; 90° CW → ◤.",
            "hard",
        ),
        _mcq(
            "Weight balance analogy with shapes:\n"
            "▲▲ = ●\n"
            "●● = ■■\n"
            "▲▲▲▲ = ?\n"
            "(Choose equivalent)",
            ["■■", "●●", "■", "▲▲"],
            0,
            "▲▲=● so ▲▲▲▲=●●; ●●=■■ → ■■.",
            "hard",
        ),
        _mcq(
            "Path on a 2×2: visit every edge of the square grid exactly once (like an envelope). Starting top-left going right, a valid next complete tour ends where?",
            ["Top-left (closed)", "Bottom-right", "Impossible without reuse", "Center"],
            2,
            "The classic envelope needs a diagonal; a pure 2×2 boundary is an even circuit but the prompt implies the impossible 'X without lifting' style — without diagonals you can close the square cycle ending at start; "
            "however visiting ALL edges of the plus-square graph (including cross) is impossible without reuse. Best answer: Impossible without reuse.",
            "hard",
            hints="Think Königsberg / Euler path.",
        ),
        _mcq(
            "Figure series (size + nest):\n"
            "1) ○\n"
            "2) ◎\n"
            "3) ⊙ with an outer ring (triple)\n"
            "4) ?",
            ["Four concentric circles", "Single ●", "Square nest", "Triangle nest"],
            0,
            "One more concentric circle each frame.",
            "hard",
        ),
        _mcq(
            "Transform: swap the two diagonal cells of a 2×2.\n\n"
            "Input:\n■ □\n□ ●\n\nOutput?",
            ["● □\n□ ■", "□ ■\n● □", "■ ●\n□ □", "□ □\n■ ●"],
            0,
            "Main diagonal ■ and ● swap → ●□ / □■.",
            "hard",
        ),
        _mcq(
            "Clock hands: which time are the hands opposite (180°)?",
            ["6:00", "12:00", "9:00", "3:00"],
            0,
            "At 6:00 the hands form a straight line.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Which hexomino can be a cube net?",
            [
                "A zigzag hexomino that appears in the 11 valid nets",
                "Six squares in one straight line",
                "A 2×3 rectangle",
                "A plus with an extra square making a branch of length 3+",
            ],
            0,
            "Straight hexomino and 2×3 are invalid cube nets; some zigzags are valid.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Invisible rule = number of enclosed regions.\n"
            "○ → 1\n"
            "◎ → 2\n"
            "Three concentric circles → ?",
            ["3", "2", "4", "1"],
            0,
            "Three nested circles create three nested interiors / region count 3.",
            "hard",
        ),
        _mcq(
            "Top-down view of stacked cubes:\n"
            "  ■\n"
            "■■■\n"
            "  ■\n"
            "Minimum number of cubes?",
            ["5", "4", "6", "8"],
            0,
            "Five positions visible; with height 1 each, minimum is 5.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Same silhouette — is there a maximum number of cubes?",
            ["No practical max (columns can be taller)", "5", "9", "7"],
            0,
            "Top-down view does not limit stack height.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Polygons with prime number of sides:\n△ (3) → ⬠ (5) → ?",
            ["Heptagon (7 sides)", "Hexagon (6)", "Square (4)", "Octagon (8)"],
            0,
            "Next prime is 7.",
            "hard",
        ),
        _mcq(
            "Boolean rows: Row1 AND Row2 = Row3.\n\n"
            "R1: ■ ■ □\n"
            "R2: ■ □ ■\n"
            "R3: ?",
            ["■ □ □", "■ ■ ■", "□ □ □", "■ □ ■"],
            0,
            "Bitwise AND → ■□□.",
            "hard",
        ),
        _mcq(
            "Boolean rows: Row1 XOR Row2 = Row3.\n\n"
            "R1: ■ □ ■\n"
            "R2: □ ■ ■\n"
            "R3: ?",
            ["■ ■ □", "■ □ ■", "□ ■ □", "■ ■ ■"],
            0,
            "XOR → ■■□.",
            "hard",
        ),
        _mcq(
            "Shortest path along cube edges from one vertex to the opposite vertex?",
            ["3 edges", "2 edges", "1 edge", "4 edges"],
            0,
            "Opposite vertices are distance 3 on the cube graph.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Can four side faces of a cube form a 4-cycle (a 'belt')?",
            ["Yes", "No", "Only on a net", "Only with the top face"],
            0,
            "The four faces around the cube form a 4-cycle.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Arrow inside circle: each step rotate arrow +90° CW and toggle ○/●.\n\n"
            "1) ▶ in ○\n"
            "2) ▼ in ●\n"
            "3) ◀ in ○\n"
            "4) ?",
            ["▲ in ●", "▶ in ●", "▲ in ○", "▼ in ○"],
            0,
            "Arrow ◀→▲; circle ○→●.",
            "hard",
        ),
        _mcq(
            "Next term must obey BOTH:\n"
            "• Odd counts: 3, 5, 7, …\n"
            "• Odd-sided polygons only\n\n"
            "▲▲▲ → ⬠⬠⬠⬠⬠ → ?",
            ["Seven pentagons (or heptagons)", "Six squares", "Five circles", "Four triangles"],
            0,
            "Next odd count is 7 with odd-sided shapes.",
            "hard",
        ),
        _mcq(
            "Which shape looks the same after a 180° rotation?",
            ["■", "▲", "▶", "◣"],
            0,
            "Square has 180° symmetry; these triangle/arrow orientations do not.",
            "hard",
        ),
        _mcq(
            "Rotational symmetry order: ▲(3) → ■(4) → ☆(5) → ?",
            ["⬡ (6)", "● only", "◆ (4)", "▶ (1)"],
            0,
            "Next is order-6 → hexagon.",
            "hard",
        ),
        _mcq(
            "Code: ▲=1, ■=2, ●=3. So ■●▲ = 231.\n"
            "Compute ■●▲ + ▲ as shapes.",
            ["■ ● ■", "● ▲ ■", "▲ ■ ●", "■ ■ ●"],
            0,
            "231 + 1 = 232 → ■●■.",
            "hard",
        ),
        _mcq(
            "Outer cycles □→○→△; inner dots increase by 1 each step.\n\n"
            "(□ ·) → (○ ··) → (△ ···) → ?",
            ["(□ ····)", "(○ ·)", "(△ ··)", "(■ ···)"],
            0,
            "Next outer □ with 4 dots.",
            "hard",
        ),
        _mcq(
            "Each step: delete the middle symbol, append the mirror of the first.\n"
            "▲●■ → ▲■▲ → ?",
            ["▲▲▲", "■▲■", "▲■●", "●▲■"],
            0,
            "From ▲■▲ remove middle → ▲▲; append mirror of ▲ → ▲▲▲.",
            "hard",
        ),
        _mcq(
            "Gray-code shading (one cell flips per step):\n"
            "□□ → ■□ → ■■ → ?",
            ["□■", "■■", "□□", "■□"],
            0,
            "From ■■ clear the left cell → □■.",
            "hard",
        ),
        _mcq(
            "Odd one out (others are valid cube nets):",
            [
                "Six squares in a straight line",
                "The classic cross of 6 squares",
                "A valid Z-hexomino net",
                "A valid S-hexomino net",
            ],
            0,
            "A straight line of 6 cannot fold to a cube.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Take ▶, flip upside-down, then rotate 90° CW. Result?",
            ["◀", "▶", "▲", "▼"],
            0,
            "Maps to a left-pointing arrow.",
            "hard",
        ),
        _mcq(
            "● walks a clockwise spiral on a 3×3:\n"
            "center → mid-right → bottom-right → bottom-mid → ?",
            ["bottom-left", "top-right", "center", "mid-left"],
            0,
            "Continues to bottom-left.",
            "hard",
        ),
        _mcq(
            "● = push, ○ = pop. Start empty: ● ● ○ ● ○ ○\n"
            "What remains?",
            ["empty", "●", "●●", "○"],
            0,
            "Ends empty.",
            "hard",
        ),
        _mcq(
            "Which regular polygon tiles the plane alone?",
            ["Hexagon", "Pentagon", "Heptagon", "Octagon"],
            0,
            "Among these options, hexagon does.",
            "hard",
            category="spatial",
        ),
    ]



def build_shape_brain_teasers() -> list[dict[str, Any]]:
    return [
        _mcq(
            "▲ sits on top of ■. Rotate the whole figure 180°. What is on top?",
            ["■", "▲", "Both side by side", "Nothing"],
            0,
            "180° puts the former bottom (■) on top.",
            "medium",
            category="spatial",
        ),
        _mcq(
            "A cube’s shadow can look like a hexagon.",
            ["True", "False", "Only outdoors", "Only wireframe"],
            0,
            "Corner-on projection can yield a hexagon.",
            "medium",
            category="spatial",
        ),
        _mcq(
            "Which net cannot fold into a cube?",
            ["Six squares in a straight line", "Cross of 6 squares", "Zig-zag of 6", "T-shape of 6"],
            0,
            "A straight hexomino of length 6 is not a valid cube net.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Connect midpoints of a large equilateral triangle. How many triangles of any size?",
            ["5", "4", "3", "6"],
            0,
            "3 small up + 1 middle down + 1 large = 5.",
            "medium",
            category="spatial",
        ),
        _mcq(
            "Fold in half twice, punch one hole through all layers. Holes when unfolded?",
            ["4", "2", "1", "8"],
            0,
            "2 folds → 4 layers → 4 holes.",
            "easy",
            category="spatial",
        ),
        _mcq(
            "Standard die: front 1, top 2, right 3. Opposite of 1?",
            ["6", "5", "4", "2"],
            0,
            "Opposite faces sum to 7 → opposite of 1 is 6.",
            "hard",
            category="spatial",
        ),
        _mcq(
            "Sides increase: curve → △ → □ → ⬠ → ?",
            ["⬡", "★", "○", "▲"],
            0,
            "Next is hexagon (6 sides).",
            "easy",
            category="spatial",
        ),
        _mcq(
            "Mirror on the right of ▶. What appears?",
            ["◀", "▶", "▲", "▼"],
            0,
            "Reflection reverses left/right.",
            "easy",
            category="spatial",
        ),
    ]
