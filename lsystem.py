import json

def apply_rules(rules, state):
    result = list()

    for c in state:
        # If the character is in the rules, replace it with
        # whatever the rule says. Otherwise just keep the
        # character in place
        result.append(rules.get(c, c))

    # Join the list into one string
    return "".join(result)

if __name__ == '__main__':
    lsystem = {}

    # Load lsystem from file
    with open("sample.json") as json_file:
        lsystem = json.load(json_file)

    # The first iteration is always 'start'
    steps = {0: lsystem['start']}

    # Apply the rules at each iteration
    for i in range(1, lsystem['iter']):
        steps[i] = apply_rules(lsystem['rules'], steps[i-1])

    print steps
