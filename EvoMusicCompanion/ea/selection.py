from ea.individual import Individual

from random import shuffle


def tournament_selection(individuals: [Individual], k: int):
    shuffle(individuals)
    selection = []
    for i in range(0, len(individuals), k):
        end = i + k
        if end > len(individuals):
            break
        tournament = individuals[i:end]
        tournament.sort(key=lambda x: x.fitness, reverse=True)
        selection.extend(tournament[0:2])
    return selection

