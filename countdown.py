#!/usr/bin/env python3
import operator

OPS = (operator.add, operator.sub, operator.mul, operator.truediv)
ASSOCIATIVE_OPERATIONS = (operator.add, operator.mul)

OPS_TO_STR = {
    operator.add: "+",
    operator.sub: "-",
    operator.mul: "*",
    operator.truediv: "/",
}


def operations_to_string(operations):
    if not operations:
        return "impossible"

    op_strs = []
    for op in operations:
        op_strs.append("{} {} {} = {}".format(op[0], OPS_TO_STR[op[1]], op[2], op[3]))

    return "\n".join(op_strs)


# this won't remove all unused results in the case of duplicate numbers
def remove_unused_results(operations, target):
    used_results = (
        tuple(op[0] for op in operations)
        + tuple(op[2] for op in operations)
        + (target,)
    )
    return tuple(op for op in operations if op[3] in used_results)


def used_pair_already(num1, num2, already_used_pairs):
    return any(
        num1 in prev_pair and num2 in prev_pair for prev_pair in already_used_pairs
    )


# operations is a list of tuples where the tuples are:
# (num1, operator, num2, result)
def solve(target, selection, operations):
    if not operations:
        operations = []

    # nothing to do with one number
    if len(selection) <= 1:
        return False

    for op in OPS:
        already_used_pairs = []
        for index1, num1 in enumerate(selection):
            for index2, num2 in enumerate(selection):
                if index1 == index2:
                    continue

                if op in ASSOCIATIVE_OPERATIONS:
                    if used_pair_already(num1, num2, already_used_pairs):
                        continue
                    already_used_pairs.append((num1, num2))

                try:
                    result = op(num1, num2)
                except ZeroDivisionError:
                    continue

                if result == target:
                    operations.append((num1, op, num2, result))
                    return remove_unused_results(operations, target)

                if result < 0 or int(result) != result or result in (num1, num2):
                    continue

                new_operations = list(operations)
                new_operations.append((num1, op, num2, result))
                new_selection = list(selection)
                new_selection.remove(num1)
                new_selection.remove(num2)
                new_selection.append(result)

                solution_operations = solve(target, new_selection, new_operations)
                if solution_operations:
                    return solution_operations

    return False


target = 346
selection = [6, 5, 4, 5, 9, 75]
selection.reverse()

print("{:^24}".format(target))
for number in selection:
    print("{:^4}".format(number), end="")
print("\n")
print(operations_to_string(solve(target, selection, False)))
