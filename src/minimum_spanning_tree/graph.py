import math
import functools
from src.minimum_spanning_tree.edge import Edge


class Graph:
    def __init__(self, init_adj_matrix=None):
        """A graph (size is N x N) with non-existing edges equal to infinity

        :param init_adj_matrix: a list of lists of nodes
        """
        self.adj_matrix = init_adj_matrix if init_adj_matrix else [[]]
        self.is_bidirectional = True

    def add_vertex(self, *edges):
        """Add a new node to the graph

        :param edges: a list of
            :class:`~src.minimum_spanning_tree.graph.Edge` whose start index is
            the new node (don't need to define start in Edge objects)
        :return:
        """
        n = len(self.adj_matrix)
        # adj_matrix is empty
        if self.adj_matrix[0] == []:
            edges = (Edge(),) if edges == () else edges
            self.adj_matrix[0] = [edges[0].value]
            return

        # add new row with all init values being infinity
        self.adj_matrix.append([math.inf] * (n + 1))

        # allow disconnected vertex
        if len(edges) == 0:
            for i in range(len(self.adj_matrix) - 1):
                self.adj_matrix[i].append(math.inf)
            return

        # iterate over edge given for new node
        for edge in edges:
            # invalid value in argument
            if not isinstance(edge, Edge):
                raise Exception("Value was {} of type {} but {} was expected"
                                .format(type(edge), type(Edge)))

            self.adj_matrix[n][edge.end] = edge.value
            # if a -> b then b -> a; avoid appending to last row (alrdy updated)
            if self.is_bidirectional and edge.end != n:
                self.adj_matrix[edge.end].append(edge.value)

        # iterate over remaining rows that need last value to be infinity
        remaining = set(range(n)) - set(edge.end for edge in edges)
        for row_index in remaining:
            self.adj_matrix[row_index].append(math.inf)

    def __repr__(self):
        """The direction conversion of the adj_matrix to str"""
        final = ""
        for row in self.adj_matrix:
            final += str(row) + "\n"
        return final

    def __str__(self):
        """The neatly formatted string representation of this Graph"""
        final = ""
        for row in self.adj_matrix:
            for weight in row:
                final += "{: <8}".format(weight)
            final += '\n'
        return final


if __name__ == '__main__':
    E = Edge

    g = Graph()
    g.add_vertex()
    g.add_vertex(E(end=0, value=3))
    g.add_vertex(E(end=1, value=4))
    g.add_vertex(E(end=0, value=2))
    g.add_vertex(E(end=3, value=4), E(end=1, value=5))
    print(repr(g))
