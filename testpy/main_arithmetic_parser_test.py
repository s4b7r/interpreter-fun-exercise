def test_one():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1')
    expected = '1'
    assert ast == expected


def test_space_one():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement(' 1')
    expected = '1'
    assert ast == expected


def test_one_space():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1 ')
    expected = '1'
    assert ast == expected


def test_one_spacespace():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1  ')
    expected = '1'
    assert ast == expected


def test_plus():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+2')
    expected = {
                    'op':'+',
                    'next':'2',
                    'prev':'1'
                }
    assert ast == expected


def test_plus_space():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+ 2')
    expected = {
                    'op':'+',
                    'next':'2',
                    'prev':'1'
                }
    assert ast == expected


def test_times_space():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1* 2')
    expected = {
                    'op':'*',
                    'next':'2',
                    'prev':'1'
                }
    assert ast == expected


def test_plusplus():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+2+3')
    expected = {
                    'next':'3',
                    'op':'+',
                    'prev':{
                        'prev':'1',
                        'op':'+',
                        'next':'2',
                        },
                }
    assert ast == expected


def test_timesplus():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1*2+3')
    expected = {
                    'prev':{
                        'prev':'1',
                        'op':'*',
                        'next':'2'
                    },
                    'op':'+',
                    'next':'3',
                }
    assert ast == expected


def test_timestimes():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1*2*3')
    expected = {
                    'prev':{
                        'prev':'1',
                        'op':'*',
                        'next':'2'
                    },
                    'op':'*',
                    'next':'3',
                }
    assert ast == expected


def test_plustimes():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+2*3')
    expected = {
                    'prev':'1',
                    'op':'+',
                    'next':{
                        'prev':'2',
                        'op':'*',
                        'next':'3'
                        
                    },
                }
    assert ast == expected


def test_plustimestimes():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+2*3*4')
    expected = {
                    'prev':'1',
                    'op':'+',
                    'next':{
                        'next':'4'
                        ,
                        'op':'*',
                        'prev':{
                            'prev':'2'
                            ,
                            'op':'*',
                            'next':'3'
                            
                        },
                    },
                }
    assert ast == expected


def test_plustimesplus():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+2*3+4')
    expected = {
                    'next':'4',
                    'op':'+',
                    'prev':{
                        'next':{
                            'prev':'2'
                            ,
                            'op':'*',
                            'next':'3'
                            
                        },
                        'op':'+',
                        'prev':'1'
                        ,
                    },
                }
    assert ast == expected


def test_divdiv():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1/2/3')
    expected = {
                    'prev':{
                        'prev':'1',
                        'op':'/',
                        'next':'2',
                    },
                    'op':'/',
                    'next':'3'
                    ,
                }
    assert ast == expected


def test_plustimespow():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+2*3^4')
    expected = {
                    'prev':'1',
                    'op':'+',
                    'next':{
                        'prev':'2',
                        'op':'*',
                        'next':{
                            'prev':'3',
                            'op':'^',
                            'next':'4'
                            
                        },
                    },
                }
    assert ast == expected


def test_pluspowtimes():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+2^3*4')
    expected = {
                    'prev':'1',
                    'op':'+',
                    'next':{
                        'prev':{
                            'prev':'2',
                            'op':'^',
                            'next':'3'
                            
                        },
                        'op':'*',
                        'next':'4',
                    },
                }
    assert ast == expected


def test_powplustimes():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1^2+3*4')
    expected = {
                    'prev':{
                        'prev':'1',
                        'op':'^',
                        'next':'2'
                        
                    },
                    'op':'+',
                    'next':{
                        'prev':'3'
                        ,
                        'op':'*',
                        'next':'4'
                        ,
                    },
                }
    assert ast == expected


def test_found_error_case():
    from ..main import parse_arithmetic_statement
    ast = parse_arithmetic_statement('1+2*3^4+1')
    expected = {
                    'prev': {
                        'prev': '1',
                        'op': '+',
                        'next': {
                            'prev': '2',
                            'op': '*',
                            'next': {
                                'prev': '3',
                                'op': '^', 
                                'next': '4', 
                            }
                        },
                    },
                    'op': '+',
                    'next': '1'
                }
    from pprint import pprint
    pprint(expected)
    pprint(ast)
    assert ast == expected
