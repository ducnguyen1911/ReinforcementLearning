__author__ = 'duc07'

import math
from collections import Counter


def majority_value(examples, target_attr):
    vals = [record[target_attr] for record in examples]
    count = Counter(vals)
    return count.most_common()[0][0]  # the most common value is the first element


def choose_attribute(examples, attributes, target_attr):
    best_attr = ''
    min_entropy = 99999
    for attr in attributes:
        if attr != target_attr:
            cur_entropy = 0
            for val in get_values(examples, attr):
                temp_entropy = 0
                exam_in_val = get_examples(examples, attr, val)
                numb_exam_in_val = len(exam_in_val)
                target_vals = [record[target_attr] for record in exam_in_val]
                count = Counter(target_vals)
                for (target_v, c) in count.most_common():
                    if (c > 0) and (numb_exam_in_val > 0):
                        temp_entropy += - (float(c) / numb_exam_in_val) * math.log(float(c) / numb_exam_in_val, 2)
                temp_entropy = temp_entropy * float(numb_exam_in_val) / len(examples)
                cur_entropy += temp_entropy
            if cur_entropy < min_entropy:
                best_attr = attr
                min_entropy = cur_entropy
    return best_attr


def get_values(examples, attr):
    vals = [record[attr] for record in examples]
    return list(set(vals))


def get_examples(examples, attr, val):
    return [record for record in examples if record[attr] == val]


def create_decision_tree(examples, attributes, target_attr):
    """
    Returns a new decision tree based on the examples given.
    """
    examples    = examples[:]
    vals    = [record[target_attr] for record in examples]
    default = majority_value(examples, target_attr)

    # If the dataset is empty or the attributes list is empty, return the
    # default value. When checking the attributes list for emptiness, we
    # need to subtract 1 to account for the target attribute.
    if not examples or (len(attributes) - 1) <= 0:
        return default
    # If all the records in the dataset have the same classification,
    # return that classification.
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        # Choose the next best attribute to best classify our data
        best = choose_attribute(examples, attributes, target_attr)

        # Create a new decision tree/node with the best attribute and an empty
        # dictionary object--we'll fill that up next.
        tree = {best:{}}

        # Create a new decision tree/sub-node for each of the values in the
        # best attribute field
        for val in get_values(examples, best):
            # Create a subtree for the current value under the "best" field
            subtree = create_decision_tree(
                get_examples(examples, best, val),
                [attr for attr in attributes if attr != best],
                target_attr)

            # Add the new subtree to the empty dictionary object in our new
            # tree/node we just created.
            tree[best][val] = subtree

    return tree


def create_graph(tree, index, attrs, leaves, connections):
    node = tree.keys()[0]

    if isinstance(tree[node], dict):  # node is attribute
        for k, v in tree[node].iteritems():  # k is connection
            if not isinstance(v, dict):  # v is a leaf
                leaves.append('leaf' + str(len(leaves) + 1) +' [shape="plaintext", label="' + v + '"]')
                connections.append('attr' + str(index) + ' -> leaf' + str(len(leaves)) + ' [label="' + str(node) + '=' + str(k) + '"]')
            else:  # v is an attribute, v is a dict
                for k1, v1 in v.iteritems():  # k1 is attr
                    new_index = len(attrs) + 1
                    attrs.append('attr' + str(new_index) + ' [shape="rectangle", label="' + k1 + '"]')
                    connections.append('attr' + str(index) + ' -> attr' + str(len(attrs)) + ' [label="' + str(node) + '=' + str(k) + '"]')
                    if isinstance(v, dict):
                        attrs, leaves, connections = create_graph(v, new_index, attrs, leaves, connections)
    return attrs, leaves, connections


def print_list(ls):
    for l in ls:
        print l


def print_graph(attrs, leaves, connections):
    print 'digraph G {'
    print '// attributes'
    print_list(attrs)
    print '// leaves'
    print_list(leaves)
    print '// connections'
    print_list(connections)
    print '}'


def main():
    examples = []

    examples.append({'Age': 2, 'Sex': 'Male', 'Breed': 'Pomeranian', 'Decision': 'N'})
    examples.append({'Age': 1, 'Sex': 'Male', 'Breed': 'Chihuahua', 'Decision': 'Y'})
    examples.append({'Age': 4, 'Sex': 'Female', 'Breed': 'Australian Shepherd', 'Decision': 'Y'})
    examples.append({'Age': 2, 'Sex': 'Male', 'Breed': 'Pit Bull', 'Decision': 'N'})
    examples.append({'Age': 1, 'Sex': 'Male', 'Breed': 'Australian Shepherd', 'Decision': 'Y'})
    examples.append({'Age': 1, 'Sex': 'Male', 'Breed': 'Pit Bull', 'Decision': 'N'})
    examples.append({'Age': 1, 'Sex': 'Female', 'Breed': 'Australian Shepherd', 'Decision': 'N'})
    examples.append({'Age': 1, 'Sex': 'Female', 'Breed': 'Chihuahua', 'Decision': 'Y'})
    examples.append({'Age': 4, 'Sex': 'Female', 'Breed': 'Pomeranian', 'Decision': 'N'})
    examples.append({'Age': 2, 'Sex': 'Male', 'Breed': 'Chihuahua', 'Decision': 'Y'})
    examples.append({'Age': 2, 'Sex': 'Female', 'Breed': 'Pomeranian', 'Decision': 'Y'})
    examples.append({'Age': 2, 'Sex': 'Female', 'Breed': 'Australian Shepherd', 'Decision': 'N'})


    attributes = ['Age', 'Sex', 'Breed', 'Decision']
    target_attr = 'Decision'
    tree = create_decision_tree(examples, attributes, target_attr)
    print tree

    attrs = []
    attrs.append('attr1' + ' [shape="rectangle", label="' + tree.keys()[0] + '"]')
    attrs, leaves, connections = create_graph(tree, 1, attrs, [], [])
    print_graph(attrs, leaves, connections)


if __name__ == "__main__":
    main()