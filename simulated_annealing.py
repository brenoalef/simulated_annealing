import math
import random
import sys


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
    
    def expand(self, problem):
        return [child_node(problem, self, action) for action in problem.actions(self.state)]


def child_node(problem, parent, action):
    new_state = problem.result(parent.state, action)
    return Node(new_state, parent, action)


def exp_schedule(k=20, lam=0.0003, limit=10000):
    return lambda t: (k * math.exp(-lam * t) if t < limit else 0)


def simulated_annealing(problem, schedule=exp_schedule()):
    current_node = Node(problem.initial_state)
    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            return current_node.state
        neighbors = current_node.expand(problem)
        if not neighbors:
            return current_node.state
        next_node = random.choice(neighbors)
        delta_e = problem.value(next_node.state) - problem.value(current_node.state)
        if delta_e > 0 or math.exp(delta_e/T) > random.uniform(0.0, 1.0):
            current_node = next_node
