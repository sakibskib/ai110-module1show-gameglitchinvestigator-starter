# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

ans: the number of attempts were not decreasing with the tries.

The hints were backwards.

the game modes numbers were reveresed, the guess saying the guess numbers were wrong.

Additional bugs found later: The "New Game" button was not fully resetting the game — score, status, and history were left over from the previous game, so if you won and clicked New Game the game would immediately end again. Invalid guesses (like typing a letter) were counting as an attempt even though no number was submitted. The scoring for a "Too High" guess was giving +5 points on even attempts instead of deducting points, which rewarded wrong answers. The win score formula had an off-by-one error (`attempt_number + 1`) that made every win score 10 points less than it should have.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Ans: Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Ans: Claude correctly identified that the hints in `check_guess` (logic_utils.py) were swapped — it was returning `"Go LOWER"` when `guess < secret` and `"Go HIGHER"` when `guess > secret`, which is the opposite of correct. Claude suggested flipping the messages so `guess > secret` maps to `"Go LOWER"`. I verified this by opening the debug panel to see the secret number, then entering a value I knew was higher and confirming the hint now read "Go LOWER" as expected.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
Ans: When fixing the attempt counter bug (invalid guesses consuming an attempt), Claude initially suggested changing the display formula `attempt_limit - st.session_state.attempts` on the info line, saying the subtraction was wrong. That was misleading — the display was fine. The actual bug was that `st.session_state.attempts += 1` ran before `parse_guess` was called, so even a letter triggered an increment. I typed "abc" into the guess box and watched the counter drop to confirm the first suggestion had no effect, then moved the increment inside the `else` block and retested to verify it stayed stable on bad input.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Ans: A bug was only considered fixed when I could reproduce the original broken behavior, apply the fix, and then confirm the behavior was gone through manual play. I also checked the Developer Debug Info panel (secret, attempts, score, history) to verify internal state matched what the UI showed.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
Ans: For the invalid-guess bug I ran a focused manual test: I opened the debug panel, noted the current attempt count, typed the letter "z" into the input box, and clicked Submit. Before the fix, attempts dropped by 1 even though no valid number was submitted. After moving the increment inside the `else` block, the count stayed the same — confirming the fix worked. I repeated the same test with a decimal, a negative number, and an empty string to make sure all non-integer paths were safe. Additional manual tests I ran:
  - **New Game reset**: Won a game, noted the score, clicked New Game, and confirmed score returned to 0, history was empty, and the game did not immediately end again.
  - **Hint direction**: Used the debug panel to find the secret, guessed one number above it, and confirmed the hint said "Go LOWER".
  - **Scoring deduction**: Made a "Too High" guess and watched the score in the debug panel drop by 5 (not increase).

- Did AI help you design or understand any tests? How?
Ans: Claude pointed out each bug location by reading the code and explained the root cause in plain terms (e.g., "the increment is before validation, so it runs even when the input is rejected"). That explanation directly shaped my test strategy — once I understood *why* a bug existed I knew exactly what input to use to reproduce it and what state to watch in the debug panel to confirm it was gone.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Ans: Every time you interacted with the app — clicking a button, typing in a box — Streamlit re-ran the entire Python script from top to bottom. Without any guard, `random.randint()` was called every single rerun, generating a brand new secret number each time. So the number you were guessing kept silently changing underneath you.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Ans: Imagine every time you click a button on a website, the whole page script restarts from scratch and forgets everything. That's Streamlit by default. Session state is like a small notebook that survives each restart — anything you write into `st.session_state` stays there across reruns, so the game can remember the secret number, your score, and how many attempts you've used.

- What change did you make that finally gave the game a stable secret number?
Ans: I wrapped the `random.randint()` call in an `if "secret" not in st.session_state` check. That way the secret is only generated once on the very first load, and every subsequent rerun just reuses the value already stored in session state instead of rolling a new one.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Ans: I want to keep the habit of manually testing edge cases right after a fix — things like typing invalid input or clicking a button in an unexpected order. This project showed me that a fix can look correct in the code but still break in a scenario you didn't think to check, so playing through edge cases by hand catches things that just reading the code misses.

- What is one thing you would do differently next time you work with AI on a coding task?
Ans: I would ask Claude to explain *why* a bug exists before accepting the fix, not just what to change. A couple of times I applied a suggestion without fully understanding the cause, and then a related bug showed up later that I could have caught earlier if I had understood the root issue first.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
Ans: I used to assume that if the code ran without crashing, it was probably correct. This project made it clear that AI-generated code can be logically broken in subtle ways — wrong scoring, state that never resets, off-by-one errors — that only show up when you actually play through the feature carefully.
