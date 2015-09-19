import json
import turtle
from sys import argv

def apply_rules(rules, state):
    result = list()

    for c in state:
        # If the character is in the rules, replace it with
        # whatever the rule says. Otherwise just keep the
        # character in place
        result.append(rules.get(c, c))

    # Join the list into one string
    return "".join(result)

def draw_state(step, pen):
    print step
    for c in step:
        if c == 'F':
            pen.forward(10)
        elif c == '+':
            # TODO: Need to read the angle from somewhere
            pen.left(90)
        elif c == '-':
            pen.right(90)

if __name__ == '__main__':
    system_file = argv[1]
    lsystem = {}

    # Load lsystem from file
    with open(system_file) as json_file:
        lsystem = json.load(json_file)

    # The first iteration is always 'start'
    steps = {0: lsystem['start']}

    # Apply the rules at each iteration
    for i in range(1, lsystem['iter']+1):
        steps[i] = apply_rules(lsystem['rules'], steps[i-1])

    # Create drawing environment
    wn = turtle.Screen()
    pen = turtle.Turtle()

    # This is ugly right now and I should change it - maybe refactor
    # steps to a list
    print steps[lsystem['iter']]
    draw_state(steps[lsystem['iter']], pen)

    turtle.mainloop()
