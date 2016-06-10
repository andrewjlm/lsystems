from bokeh.plotting import figure, output_file, show
import json
from math import sin, cos, radians
from sys import argv

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        newx = self.x + other.x
        newy = self.y + other.y
        return Point(newx, newy)

    def __repr__(self):
        return "({0}, {1})".format(self.x, self.y)

class State(object):
    def __init__(self, angle):
        self.current = Point(0, 0)
        self.steps = [self.current]
        self.movement = Point(10, 0)
        self.angle = angle
        self.stack = []


    def rotate_movement(self, angle):
        State.rotate_point(self.movement, angle)

    def rotate_point(point, angle):
        # Rotate point around origin
        s = sin(radians(angle))
        c = cos(radians(angle))

        xnew = point.x * c - point.y * s
        ynew = point.y * c + point.x * s

        point.x = xnew
        point.y = ynew


def apply_rules(rules, state):
    result = list()

    for c in state:
        # If the character is in the rules, replace it with
        # whatever the rule says. Otherwise just keep the
        # character in place
        result.append(rules.get(c, c))

    # Join the list into one string
    return "".join(result)

def parse_step(step, state):
    if step in 'F':
        def draw_step(state):
            state.current += state.movement
            state.steps.append(state.current)
    elif step == '+':
        def draw_step(state):
            state.rotate_movement(state.angle)
    elif step == '-':
        def draw_step(state):
            state.rotate_movement(-state.angle)
    elif step == '[':
        def draw_step(state):
            state.stack.append(state.current)
            state.stack.append(state.movement)
    elif step == ']':
        def draw_step(state):
            state.movement = state.stack.pop()
            state.current = state.stack.pop()
    else:
        def draw_step(state):
            pass

    return draw_step

if __name__ == '__main__':
    system_file = argv[1]
    lsystem = {}

    # Load lsystem from file
    with open(system_file) as json_file:
        lsystem = json.load(json_file)

    # The first iteration is always 'start'
    steps = [lsystem['start']]

    # Apply the rules at each iteration
    for i in range(1, lsystem['iter']):
        steps.append(apply_rules(lsystem['rules'], steps[i-1]))

    # Create drawing environment
    output_file("fig.html", title=system_file)
    p = figure(title=system_file)
    state = State(lsystem['angle'])

    # Parse steps and convert to drawing instructions
    for step in steps[-1]:
        step_func = parse_step(step, state)
        step_func(state)

    xs = [step.x for step in state.steps]
    ys = [step.y for step in state.steps]

    # Draw lines
    p.line(xs, ys, line_width=2)

    show(p)
