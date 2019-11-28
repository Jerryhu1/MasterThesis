import constants
import modelTrainer


def update_matrix(individuals, matrix):
    if constants.N_GRAM == 'trigram':
        get_matrix = modelTrainer.get_trigram_matrix
    else:
        get_matrix = modelTrainer.get_bigram_matrix

    update_matrices = []

    for p in individuals:
        for m in p.measures:
            learning_rate = get_learning_rate(p.user_score, m.user_score)
            n_matrix = get_matrix(m.notes)
            n_matrix = modelTrainer.get_probabilistic_matrix(n_matrix)
            update_matrices.append((n_matrix, learning_rate))

    new_matrix = matrix.copy()

    for m in update_matrices:
        u_matrix = m[0]
        learning_rate = m[1]
        for i in new_matrix.keys():
            for j in new_matrix.keys():
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
    if score == "Very good":
        return 0.6
    if score == "Good":
        return 0.4
    if score == "Neutral":
        return 0.2
    return 0.0