def parse_arithmetic_statement(code):
    PRECEDENCE_GROUPS = {
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
    code = code.translate(str.maketrans({c: f' {c} ' for c in PRECEDENCE.keys() if c != '1'}))
    tokens = code.split(' ')
    ast = {'op': '1', 'next': {'op': '1'}}
    roots_root = ast
    current_nexts_root = roots_root['next']
    for token in tokens:
        for ops_group in PRECEDENCE_GROUPS:
            if token in ops_group and token != '1':
                if PRECEDENCE[current_nexts_root['op']] >= PRECEDENCE[ops_group[0]]:
                    old_root = current_nexts_root
                    roots_root['next'] = {'op': token, 'prev': old_root}
                    del old_root
                    current_nexts_root = roots_root['next']
                    continue
                if PRECEDENCE[current_nexts_root['op']] < PRECEDENCE[ops_group[0]]:
                    old_next = current_nexts_root.pop('next', {'op': None})
                    current_nexts_root['next'] = {'op': token, 'prev': old_next}
                    del old_next
                    roots_root = current_nexts_root
                    current_nexts_root = current_nexts_root['next']
                    continue
        current_nexts_root['next'] = token
    ast = ast['next']
    return ast


if __name__ == '__main__':
    from pprint import pprint
    pprint(parse_arithmetic_statement('1+2*3'))
