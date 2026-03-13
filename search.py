# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    seen = set()
    frontier = util.Stack()

    start = [problem.getStartState()]
    frontier.push([start])

    # Cada neighbor node te da `[position tuple, direction, step cost]`

    while not frontier.isEmpty():
        path = frontier.pop()
        node = path[-1]
        pos = node[0]

        if pos in seen:
            continue

        seen.add(pos)

        if problem.isGoalState(pos):
            # We want the path without the start state
            return list(map(lambda n: n[1], path[1:]))

        neighbors = problem.getSuccessors(pos)

        for neighbor in neighbors:
            n_pos = neighbor[0]
            if n_pos not in seen:
                this_path = path.copy()
                this_path.append(neighbor)
                frontier.push(this_path)

    return []


def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    seen = set()
    frontier = util.Queue()

    start = [problem.getStartState()]
    frontier.push([start])

    # Cada neighbor node te da `[position tuple, direction, step cost]`

    while not frontier.isEmpty():
        path = frontier.pop()
        node = path[-1]
        pos = node[0]

        if pos in seen:
            continue

        seen.add(pos)

        if problem.isGoalState(pos):
            # We want the path without the start state
            return list(map(lambda n: n[1], path[1:]))

        neighbors = problem.getSuccessors(pos)

        for neighbor in neighbors:
            n_pos = neighbor[0]
            if n_pos not in seen:
                this_path = path.copy()
                this_path.append(neighbor)
                frontier.push(this_path)

    return []


def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    seen = set()
    frontier = util.PriorityQueue()

    start = [problem.getStartState()]
    frontier.push([[start], 0], 0)

    # Cada neighbor node te da `[position tuple, direction, step cost]`

    while not frontier.isEmpty():
        path_n_cost = frontier.pop()
        path = path_n_cost[0]
        node = path[-1]
        pos = node[0]
        path_cost = path_n_cost[1]

        if pos in seen:
            continue

        seen.add(pos)

        if problem.isGoalState(pos):
            # We want the path without the start state
            return list(map(lambda n: n[1], path[1:]))

        neighbors = problem.getSuccessors(pos)

        for neighbor in neighbors:
            n_pos = neighbor[0]
            cost = path_cost + neighbor[2]
            if n_pos not in seen:
                this_path = path.copy()
                this_path.append(neighbor)
                frontier.push([this_path, cost], cost)

    return []


def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    visited = {}

    start_pos = problem.getStartState()
    frontier.push((start_pos, [], 0), heuristic(start_pos, problem))

    # Cada neighbor node te da `[position tuple, direction, step cost]`

    while not frontier.isEmpty():
        pos, actions, current_g = frontier.pop()

        # We only update the path to a previously explored node
        # if the new path is cheaper
        if pos in visited and visited[pos] <= current_g:
            continue

        visited[pos] = current_g

        if problem.isGoalState(pos):
            # We want the path without the start state
            return actions

        neighbors = problem.getSuccessors(pos)

        for next_pos, action, step_cost in neighbors:
            new_g = current_g + step_cost
            new_actions = actions + [action]
            f = new_g + heuristic(next_pos, problem)
            frontier.push((next_pos, new_actions, new_g), f)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
