from ea.individual import Individual


class MusicWindowViewModel:
    def __init__(
            self,
            parent,
            pieces: [Individual],
            curr_piece: Individual = None,
            options = None
    ):
        self.parent = parent
        self.individuals = pieces
        if curr_piece is None:
            self.curr_individual = pieces[0]
            self.curr_piece_idx = 0
        else:
            self.curr_individual = curr_piece
            self.curr_piece_idx = pieces.index(curr_piece)
        self.options = options
