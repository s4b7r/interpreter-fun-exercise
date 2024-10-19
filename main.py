from copy import deepcopy


def parse_arithmetic_statement(code):
    PRECEDENCE_GROUPS = {
                        '=': -1,
                        '+-': 1,
                        '*/': 2,
                        '^': 3,
                        '1': 4
                        }
    PRECEDENCE = {}
    for group, precedence in PRECEDENCE_GROUPS.items():
        for op in group:
            PRECEDENCE[op] = precedence

    code = code.replace(' ', '')
    code = code.translate(str.maketrans({c: f' {c} ' for c in PRECEDENCE if c != '1'}))
    tokens = code.split(' ')

    root1 = {'op': '='}
    root2 = {'op': '=', 'parent': root1}
    root3 = {'op': '=', 'parent': root2}
    root2['next'] = root3
    root1['next'] = root2
    ast = root1
    roots_root = root2
    current_nexts_root = roots_root['next']

    for token in tokens:
        for ops_group in PRECEDENCE_GROUPS:
            if token in ops_group and not token.isnumeric():
                if PRECEDENCE[current_nexts_root['op']] >= PRECEDENCE[ops_group[0]]:
                    old_root = current_nexts_root
                    new_root = {'op': token, 'prev': old_root, 'parent': roots_root}
                    roots_root['next'] = new_root
                    old_root['parent'] = new_root
                    del old_root
                    del new_root
                    current_nexts_root = roots_root['next']

                    while PRECEDENCE[current_nexts_root['parent']['op']] >= PRECEDENCE[ops_group[0]]:
                        new_current = deepcopy(current_nexts_root)
                        new_currents_prev = deepcopy(current_nexts_root['parent'])
                        current_nexts_root['parent']['parent']['next'] = new_current
                        new_current['parent'] = current_nexts_root['parent']['parent']
                        new_current['prev'] = new_currents_prev
                        new_currents_prev['parent'] = new_current
                        new_currents_prev['next'] = current_nexts_root['prev']
                        current_nexts_root = new_current
                        roots_root = new_current['parent']
                        del new_current
                        del new_currents_prev

                    break
                if PRECEDENCE[current_nexts_root['op']] < PRECEDENCE[ops_group[0]]:
                    old_next = current_nexts_root.pop('next', {'op': None})
                    new_next = {'op': token, 'prev': old_next, 'parent': current_nexts_root}
                    current_nexts_root['next'] = new_next
                    old_next['parent'] = new_next
                    del old_next
                    del new_next
                    roots_root = current_nexts_root
                    current_nexts_root = current_nexts_root['next']
                    break
        else:
            current_nexts_root['next'] = {'op': '1', 'next': token, 'parent': current_nexts_root}

    to_clean = [ast]
    while len(to_clean):
        cleaning = to_clean.pop()
        if not isinstance(cleaning, dict):
            continue
        if (add := cleaning.get('prev', False)):
            if add['op'] in '1=':
                add['parent']['prev'] = add['next']
                add = add['next']
            to_clean.append(add)
        if (add := cleaning.get('next', False)):
            if add['op'] in '1=':
                add['parent']['next'] = add['next']
                add = add['next']
            to_clean.append(add)

    to_clean = [ast]
    while len(to_clean):
        cleaning = to_clean.pop()
        if not isinstance(cleaning, dict):
            continue
        if (add := cleaning.get('prev', False)):
            to_clean.append(add)
        if (add := cleaning.get('next', False)):
            to_clean.append(add)
        if cleaning.get('parent', False):
            del cleaning['parent']

    while isinstance(ast, dict) and ast['op'] in '1=':
        ast = ast['next']
    return ast


if __name__ == '__main__':
    from pprint import pprint
    pprint(parse_arithmetic_statement('1+2*3'))
