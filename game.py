def printGame(Ainput: str, Binput: str, Apoint: int, Bpoint: int):
    print("=== Game Theory Simulation ===")
    print(f"AI A: {Ainput}")
    print(f"AI B: {Binput}")
    print("Points:")
    print(f"AI A: {Apoint}")
    print(f"AI B: {Bpoint}")
    print("-" * 30)


def playGame(Ainput: str, Binput: str):
    Apoint = 0
    Bpoint = 0

    if Ainput == "Cooperate" and Binput == "Cooperate":
        Apoint += 3
        Bpoint += 3
    elif Ainput == "Cooperate" and Binput == "Defect":
        Bpoint += 5
        Apoint -= 1
    elif Ainput == "Defect" and Binput == "Cooperate":
        Apoint += 5
        Bpoint -= 1
    elif Ainput == "Defect" and Binput == "Defect":
        Apoint -= 1
        Bpoint -= 1
    else:
        # Phạt nếu đầu vào không hợp lệ
        if Ainput not in ("Cooperate", "Defect"):
            Apoint -= 5
        if Binput not in ("Cooperate", "Defect"):
            Bpoint -= 5

    return Apoint, Bpoint
