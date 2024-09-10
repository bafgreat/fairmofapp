from mofstructure import filetyper


class AdjacencyMatrixLoader:
    _instance = None
    _adj_matrix = None

    @classmethod
    def load_adjacency_matrix(cls, file_path=None):
        """
        Loads the adjacency matrix from a file only once.
        Returns the loaded adjacency matrix on subsequent calls.

        **parameters:**
            file_path (str): Path to the file containing the adjacency matrix.
                             If provided, it will load the matrix only the first time.

        **returns:**
            dict: The loaded adjacency matrix.
        """
        if cls._adj_matrix is None and file_path:
            cls._adj_matrix = filetyper.load_data(file_path)
        return cls._adj_matrix


def get_adjacency_matrix(file_path=None):
    return AdjacencyMatrixLoader.load_adjacency_matrix(file_path)