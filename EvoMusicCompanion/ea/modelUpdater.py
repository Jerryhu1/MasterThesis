from ea import modelTrainer, constants, util
import copy

def update_matrix(individuals, matrix, backoff=False):
    if constants.N_GRAM == 'trigram' and not backoff:
        get_matrix = modelTrainer.get_trigram_matrix
    else:
        get_matrix = modelTrainer.get_bigram_matrix

    update_matrices = []
    all_pitches = []
    for p in individuals:
        notes = p.get_flattened_notes()
        pitches = list(map(lambda x: x.pitch, notes))
        all_pitches.append(pitches)
        # for m in p.measures:
        #     learning_rate = constants.LEARNING_RATE
        #     n_matrix = get_matrix(m.notes)
        #     n_matrix = modelTrainer.get_probabilistic_matrix(n_matrix)
        #     update_matrices.append((n_matrix, learning_rate))

    all_pitches = util.flatten(all_pitches)
    n_matrix = get_matrix(all_pitches)
    n_matrix = modelTrainer.get_probabilistic_matrix(n_matrix)
    update_matrices.append((n_matrix, constants.LEARNING_RATE))

    if constants.LEARNING_RATE == 1.0:
        return n_matrix

    for m in update_matrices:
        u_matrix = m[0]
        learning_rate = m[1]
        for i in matrix.keys():
            for j in matrix[i].keys():
                if i in u_matrix and j in u_matrix[i]:
                    # u_matrix contains the values, subtract from each other
                    difference = u_matrix[i][j] - matrix[i][j]
                elif i not in u_matrix:
                    # u_matrix does not contain the column, we can not update transitions strating from this note
                    difference = 1/len(matrix.values) - matrix[i][j]# laplace smoothing
                else:  # u_matrix contains the column, but not the row. So no transitions to that note at all
                    difference = -matrix[i][j]

                matrix[i][j] = matrix[i][j] + (difference * learning_rate)

    return matrix


def update_duration(individuals, matrix):
    update_matrices = []
    all_durations = []
    for p in individuals:
        notes = p.get_flattened_notes()
        durations = list(map(lambda x: x.duration.duration_name, notes))
        all_durations.append(durations)
        # for m in p.measures:
        #     learning_rate = constants.LEARNING_RATE
        #     n_matrix = get_matrix(m.notes)
        #     n_matrix = modelTrainer.get_probabilistic_matrix(n_matrix)
        #     update_matrices.append((n_matrix, learning_rate))

    all_durations = util.flatten(all_durations)
    n_matrix = modelTrainer.get_bigram_matrix(all_durations)
    n_matrix = modelTrainer.get_probabilistic_matrix(n_matrix)
    update_matrices.append((n_matrix, constants.LEARNING_RATE))
    new_matrix = copy.deepcopy(matrix)

    for m in update_matrices:
        u_matrix = m[0]
        learning_rate = m[1]
        for i in new_matrix.keys():
            for j in new_matrix[i].keys():
                if i in u_matrix and j in u_matrix[i]:
                    # u_matrix contains the values, subtract from each other
                    difference = u_matrix[i][j] - matrix[i][j]
                elif i not in u_matrix:
                    # u_matrix does not contain the column, we can not update transitions strating from this note
                    difference = 0.0
                else:  # u_matrix contains the column, but not the row. So no transitions to that note at all
                    difference = -matrix[i][j]

                new_matrix[i][j] = matrix[i][j] + (difference * learning_rate)

    return new_matrix


def get_learning_rate(piece_score, measure_score):
    piece_score_num = get_num_score(piece_score)
    measure_score_num = get_num_score(measure_score)
    return constants.Wp * piece_score_num + constants.Wm * measure_score_num * constants.Wn


def get_num_score(score):
    if score == 5:
        return 0.8
    if score == 3:
        return 0.3
    return 0.0
