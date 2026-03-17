from logic_utils import check_guess, parse_guess, update_score


# ── Existing baseline tests ────────────────────────────────────────────────

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── Bug 1: Hints were backwards ────────────────────────────────────────────
# The original code returned "Go LOWER" for a too-low guess and "Go HIGHER"
# for a too-high guess.  After the fix the messages must match the direction.

def test_hint_message_too_high():
    """Guess above secret → message must say LOWER, not HIGHER."""
    outcome, message = check_guess(70, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint but got: {message!r}"

def test_hint_message_too_low():
    """Guess below secret → message must say HIGHER, not LOWER."""
    outcome, message = check_guess(30, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: {message!r}"


# ── Bug 2: Invalid guesses must not count as attempts ──────────────────────
# Before the fix the attempt counter was incremented before input was
# validated, so typing a letter still used up an attempt.

def test_parse_guess_letter_is_invalid():
    """A letter string must be rejected so no attempt is consumed."""
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error is not None

def test_parse_guess_empty_is_invalid():
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_none_is_invalid():
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_guess_valid_number():
    """A valid integer string must be accepted."""
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None


# ── Bug 3: Wrong-guess scoring must deduct, not add ───────────────────────
# The original code added +5 for a "Too High" guess instead of subtracting.

def test_too_high_deducts_score():
    """Score must go DOWN after a Too High guess."""
    new_score = update_score(100, "Too High", 1)
    assert new_score < 100, f"Expected score < 100 but got {new_score}"
    assert new_score == 95

def test_too_low_deducts_score():
    """Score must go DOWN after a Too Low guess."""
    new_score = update_score(100, "Too Low", 1)
    assert new_score < 100, f"Expected score < 100 but got {new_score}"
    assert new_score == 95


# ── Bug 4: Win score off-by-one in attempt_number ─────────────────────────
# The original formula used `attempt_number + 1`, awarding 10 fewer points
# than it should.  Winning on attempt 1 must give 100 - 10*1 = 90.

def test_win_score_first_attempt():
    """Win on attempt 1 from score 0 → 90 points (not 80)."""
    new_score = update_score(0, "Win", 1)
    assert new_score == 90, f"Expected 90 but got {new_score}"

def test_win_score_second_attempt():
    """Win on attempt 2 from score 0 → 80 points (not 70)."""
    new_score = update_score(0, "Win", 2)
    assert new_score == 80, f"Expected 80 but got {new_score}"

def test_win_score_floor():
    """Win score must never drop below 10, even on a very late attempt."""
    new_score = update_score(0, "Win", 20)
    assert new_score >= 10, f"Expected at least 10 but got {new_score}"
