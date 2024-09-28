from game import Game
from autoplay import solve
from random import random


def mutate(prob: float) -> float:
    prob += (random() - 0.5) * 0.1
    return prob if prob <= 1 and prob >= 0 else (1 if prob > 1 else 0)


def procGen(width: int, height: int, desiredMovesToWin: int, allowance: int):
    trials = []

    for treeProbability in [0.0,1.0]:
        for monsterProbabilty in [0.0,1.0]:
            for wallProbability in [0.0,1.0]:
                trials.append(Game(width,height,monsterProbabilty,treeProbability,wallProbability))

    solves = [(solve(trial), trial) for trial in trials]

    differences = [(abs(sol[1] - desiredMovesToWin), trial) for sol, trial in solves if sol[0]]
    sortedByDiffs = sorted(differences, key=lambda x: x[0])

    while (sortedByDiffs[0][0] > allowance):
        trials = [trial for _, trial in sortedByDiffs[:2]]

        for monsterIdx in [0,1]:
            for treeIdx in [0,1]:
                for wallIdx in [0,1]:
                    trials.append(
                        Game(
                            width,
                            height,
                            mutate(trials[monsterIdx].monsterProbability),
                            mutate(trials[treeIdx].treeProbability),
                            mutate(trials[wallIdx].wallProbability)
                        )
                    )

        trials.append(
            Game(
                width,
                height,
                (trials[0].monsterProbability + trials[1].monsterProbability) / 2,
                (trials[0].treeProbability + trials[1].treeProbability) / 2,
                (trials[0].wallProbability + trials[1].wallProbability) / 2,
            )
        )

        solves = [(solve(trial), trial) for trial in trials]

        differences = [(abs(sol[1] - desiredMovesToWin), trial) for sol, trial in solves if sol[0]]
        sortedByDiffs = sorted(differences, key=lambda x: x[0])

    return sortedByDiffs[0]

difference, bestGame = procGen(15, 15, 200, 5)
print(difference + 200)
bestGame.renderBoard()