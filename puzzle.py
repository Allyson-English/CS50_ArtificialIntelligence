from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Person A is either a Knight or a Knave
    Or(AKnight, AKnave),

    # Person A cannot be both a Knight and a Knave
    Not(And(AKnight, AKnave)),

    # If Person A is a Knight (and is telling the truth) they would be both a Knight and a Knave
    Implication(AKnight, And(AKnight, AKnave)),

    # If Person A is a Knave (lying) than they are not both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Persons A and B are both either knights or knaves
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    # Both Person A and B can only be a night or a knave (not both)
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # If Person A is telling the truth, they would have to be both a knave and a knight
    Implication(AKnight, And(AKnave, BKnave)),

    # If Person A is lying, they are not both a knave and a knight
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Persons A and B are both either knights or knaves
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    # Both Person A and B can only be a night or a knave (not both)
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, Or(And(AKnight, BKnight), And(BKnave, AKnave))),

    Implication(BKnight, Or(And(AKnight, BKnave), And(BKnight, AKnave))),

    Implication(BKnave, Not(Or(And(BKnight, AKnight), And(BKnave, AKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Persons A, B and C are either knights or knaves
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),

    # Both Person A, B and C can only be a night or a knave (not both)
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # If B is lying, than neither A or C are naves
    Implication(BKnave, Not(And(AKnave, CKnave))),
    Implication(BKnave, And(AKnight, CKnight)),

    # If B is telling the truth, than both A and C are kanves
    Implication(BKnight, And(AKnave, CKnave)),

    # If A is a knight, than B was lying
    Implication(AKnight, BKnave),

    # If A is a knave (and B was telling the truth) then A was lying
    Implication(AKnave, Not(AKnave))

    # If C is a knight then A is a knight
    Implication(CKnight, AKnight),

    # If C is a knave than A is not a knight
    Implication(CKnave, Not(AKnight)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
