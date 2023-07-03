# A knight's tour is a sequence of moves of a knight on a chessboard such that the knight
# visits every square exactly once. (https://en.wikipedia.org/wiki/Knight%27s_tour)
# 
# This file contains 3 solvers: DFS_recursive_solver, DFS_iterative_solver, Warnsdorff_solver


import numpy as np
import itertools as it
import random
from dataclasses import dataclass


def main(desk_size: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Solve Knight's path problem for arbitrary chess board of size m*n
    where m and n are from [4, 100].
    """

    m, n = desk_size
    if m == 4 and n == 4:
        # 4*4 chess board has no Knight's tour 
        return DFS_iterative_solver(desk_size).solve()

    start_positions = list(it.product(range(m), range(n)))

    # We use Wansdorf heuristic. It doesn't guarantee finding a tour
    # but we can repeat search until sucess is achieved
    while True:
        for i, j in start_positions:
            res = Warnsdorff_solver(desk_size, repeats=1).solve((i, j))
            if res is not None:
                return res


class DFS_recursive_solver:
    """
    Recursive implementation of random walk with backtracking and without heuristics or SOTA algorithms.  
    """

    def __init__(self, desk_size: tuple[int, int], repeats=3):
        """
        Params
        ------
            repeats: number of times that is allowed to visit each position
        """

        self.repeats = repeats

        # resulting list of Knight's path points
        self._points = []

        # set of positions that were not visited yet,
        # to keep track of when DFS can be stopped
        m, n = desk_size
        self._unvisited_positions = set((i, j) for i, j in it.product(range(m), range(n)))

        # 2dim matrix storing counts of how many times each position was visited,
        # to ensure that limit of 5*m*n steps won't be reached
        self._visits_counter = np.zeros(desk_size)

    def solve(self, position=(0, 0)) -> list[tuple[int, int]]:
        """
        Params
        ------
            position: coords in chess board as index in 2dim matrix where to make step into

        Return
        ------
            list of Knight's path points
        """

        # make step
        self._points.append(position)
        self._visits_counter[position] += 1
        pioneer = position in self._unvisited_positions
        if pioneer:
            self._unvisited_positions.remove(position)

        if len(self._unvisited_positions) == 0:
            # Knight's path is done!
            return self._points

        # search for next move
        for pos in self._get_possible_moves(position):
            res = self.solve(pos)
            if res is not None:
                return res

        # unmake step
        self._points.pop()
        self._visits_counter[position] -= 1
        if pioneer:
            self._unvisited_positions.add(position)

        return None

    def _get_possible_moves(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Params
        ------
            position: index of position at chess board as index for 2dim matrix

        Return
        ------
            Randomly shuffled list of all available and unvisited next positions for Knight at given position.
        """

        # to store result
        res = []

        # iterate over all 8 Knight's moves
        for x_dir, y_dir, shift in it.product([-1, 1], [-1, 1], [1, 2]):
            x_shift = x_dir * shift
            y_shift = y_dir * (3 - shift)
            next_position = (position[0] + x_shift, position[1] + y_shift)
            if self._is_possible_move(next_position):
                res.append(next_position)

        random.shuffle(res)

        return res

    def _is_possible_move(self, position: tuple[int, int]) -> bool:
        """
        For given position return True if it resides inside desk and wasn't visited more than REPEATS times.
        Note: latter restriction is used to ensure that total number of points in path is less than 5*m*n.
        """

        desk_size = self._visits_counter.shape

        # check if it's out of desk
        if (position[0] < 0 or position[1] < 0) or (position[0] >= desk_size[0] or position[1] >= desk_size[1]):
            return False

        # check if it was visited more than 4 times
        if self._visits_counter[position] >= self.repeats:
            return False

        return True


# helper to DFS_iterable_solver
@dataclass
class Node:
    make_step: bool
    pioneer: bool
    position: tuple[int, int]


class DFS_iterative_solver(DFS_recursive_solver):
    """
    Iterative implementation of random walk with backtracking and without heuristics or SOTA algorithms. 
    """

    def solve(self, position=(0, 0)) -> list[tuple[int, int]]:

        # set of positions that were not visited yet, to kee[ track of when DFS can be stopped
        m, n = self._visits_counter.shape

        stack = [Node(True, True, position)]
        while stack:
            node = stack.pop()

            if node.make_step:
                # we will revisit this node if it has no solutions
                node.make_step = False
                stack.append(node)

                # make step of DFS
                self._points.append(node.position)
                self._visits_counter[node.position] += 1

                # to keep track of positions left
                if node.pioneer:
                    self._unvisited_positions.remove(node.position)

                if len(self._unvisited_positions) == 0:
                    # Knight's path is done!
                    return self._points

                # search for next move
                for pos in self._get_possible_moves(node.position):
                    stack.append(
                        Node(True, pos in self._unvisited_positions, pos))
            else:
                # if we met this node second time it means there's no solutions in it's subtrees
                self._points.pop()
                self._visits_counter[node.position] -= 1
                if node.pioneer:
                    self._unvisited_positions.add(node.position)

        return None


class Warnsdorff_solver(DFS_recursive_solver):
    """
    On each step select node with minimum degree w.r.t. unvisited nodes.
    """

    def solve(self, position=(0, 0)) -> list[tuple[int, int]]:
        
        # until dead end or tour end
        while len(self._unvisited_positions) != 0 and position is not None:
            # add point to path
            self._points.append(position)
            
            # do not return to previous points
            self._visits_counter[position] = 1
            
            # to check if constructed path is Knight's tour
            self._unvisited_positions.discard(position)
            
            # Warnsdorff heuristic
            position = self.get_move(position)
        
        if len(self._unvisited_positions) == 0:
            # yay!
            return self._points

    def get_move(self, position: tuple[int, int]) -> tuple[int, int]:
        """
        Implement Warnsdorff heuristic.

        Params
        ------
            position: where to make step from
        
        Return
        ------
            Next Knight's position
        """

        # all valid Knight's unvisited next moves
        degree_list = []
        adj_nodes = super()._get_possible_moves(position)

        # get degree for each adjacent node
        for pos in adj_nodes:
            degree_list.append(len(super()._get_possible_moves(pos)))

        if len(degree_list) == 0:
            # dead end
            return None

        return adj_nodes[np.argmin(degree_list)]
