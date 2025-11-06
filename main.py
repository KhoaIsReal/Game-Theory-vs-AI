from google import genai
import game
import time

def safe_generate(client, model, prompt, retries=20):
    for i in range(retries):
        try:
            return client.models.generate_content(model=model, contents=prompt)
        except Exception as e:
            if "503" in str(e):
                print(f"[WARN] Model overloaded, retrying {i+1}/{retries}...")
                time.sleep(2 * (i + 1))
            else:
                raise e
    raise RuntimeError("Model overloaded too long — aborting.")


GAME_PROMPT = (
    "You're playing Prisoner's Dilemma.\n"
    "Rule:Say only 'Cooperate' or 'Defect'\n"
    "Failure to comply with the rule will result in a -5 penalty point.\n"
    "Scoring: CC=+3/+3, CD=-1/+5, DC=+5/-1, DD=-1/-1.\n" \
    "After 15 rounds,who has the highest score is the winner,if both have the same scores,draw\n"
)


# === Initialize AIs ===
AI_A = genai.Client(api_key="Put API key here")
AI_B = genai.Client(api_key="Put API key here")

AI_A_SCORE = 0
AI_B_SCORE = 0

AI_A_LAST_MOVE = ""
AI_B_LAST_MOVE = ""

for i in range(15):
    AI_A_PROMPT = f"\nYour total score: {AI_A_SCORE}, Opponent's total: {AI_B_SCORE}"
    AI_B_PROMPT = f"\nYour total score: {AI_B_SCORE}, Opponent's total: {AI_A_SCORE}"

    # responseA = AI_A.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents=GAME_PROMPT
    #     + f"\nRound {i}: Opponent's last move: {AI_B_LAST_MOVE or 'None'}"
    #     + AI_A_PROMPT,
    # )

    # responseB = AI_B.models.generate_content(
    #     model="gemini-2.5-pro",
    #     contents=GAME_PROMPT
    #     + f"\nRound {i}: Opponent's last move: {AI_A_LAST_MOVE or 'None'}"
    #     + AI_B_PROMPT,
    # )

    responseA = safe_generate(AI_A,"gemini-2.5-flash",GAME_PROMPT+ f"\nRound {i}: Opponent's last move: {AI_A_LAST_MOVE or 'None'}" + AI_A_PROMPT)
    responseB = safe_generate(AI_B,"gemini-2.5-pro",GAME_PROMPT+ f"\nRound {i}: Opponent's last move: {AI_B_LAST_MOVE or 'None'}" + AI_B_PROMPT)

    # Extract text
    moveA = responseA.candidates[0].content.parts[0].text.strip()
    moveB = responseB.candidates[0].content.parts[0].text.strip()

    # Calculate points for this round
    roundA, roundB = game.playGame(moveA, moveB)

    # Update total scores
    AI_A_SCORE += roundA
    AI_B_SCORE += roundB

    # Show round result
    game.printGame(moveA, moveB, AI_A_SCORE, AI_B_SCORE)
    time.sleep(0.3)  # Slow down output

    # Update last moves
    AI_A_LAST_MOVE = moveA
    AI_B_LAST_MOVE = moveB
    time.sleep(20)

# Final winner
print("\n=== FINAL RESULT ===")
if AI_A_SCORE > AI_B_SCORE:
    print("🏆 AI A WINS!")
elif AI_B_SCORE > AI_A_SCORE:
    print("🏆 AI B WINS!")
else:
    print("🤝 It's a tie!")
