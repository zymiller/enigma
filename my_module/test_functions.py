"""Test for my functions.

Note: because these are 'empty' functions (return None), here we just test
  that the functions execute, and return None, as expected.
"""
import numpy as np


from my_module.functions import reverse_search, flip_key, search_plugs, clean_txt

# Tests the reverse search function
def test_reverse_search():
    test_dict = {'A': 'B', 'C': 'D'}
    assert callable(reverse_search)
    assert type(reverse_search('B', test_dict)) == str
    assert reverse_search('B', test_dict) == 'A'

# Tests the key flipping function
def test_flip_key():
    test_2Darray = np.array([['A', 'C'], ['B', 'A'], ['C', 'B']])
    assert callable(flip_key)
    assert flip_key(test_2Darray).ndim == 2
    solution_array = np.array([['A', 'B'], ['B', 'C'], ['C', 'A']])
    flipped_array = flip_key(test_2Darray)
    assert  np.array_equal(solution_array, flipped_array)
    
# Tests the reverse dictionary search function    
def test_search_plugs():
    test_dict = {'A': 'B', 'C': 'D'}
    assert callable(search_plugs)
    assert type(search_plugs('B', test_dict)) == str
    assert search_plugs('B', test_dict) == 'A'
    assert search_plugs('E', test_dict) == 'E'

# Tests the text preparer for the actual machine
def clean_txt():
    test_string = 'hello!'
    assert callable(clean_txt)
    assert type(clean_txt(test_string)) == str
    assert clean_txt(test_string) == 'HELLO'

    
from my_module.classes import Rotor, Reflector, Machine    
from string import ascii_uppercase # Used this because I can't trust myself typing A-Z by hand

# Tests the initilization of a Rotor class
def test_rotor():
    test_rotor = Rotor('Test', code = ascii_uppercase, turnover = 'A')
    assert test_rotor.name == 'Test'
    assert type(test_rotor.code) == np.ndarray
    assert test_rotor.turnover == 'A'

# Tests the initilization of a Reflector class
def test_reflector():
    test_reflector = Reflector('Test', code = ascii_uppercase)
    assert test_reflector.name == 'Test'
    assert type(test_reflector.code) == np.ndarray
    
# Tests a machine that will be generated and tests the coding method within the Machine class
def test_machine():
    test2_board = ('CM', 'KO', 'GZ', 'FS', 'BD', 'AE', 'VX', 'LI', 'RJ', 'UN')
    test2_rotor = Rotor('Test', code = ascii_uppercase, turnover = 'A')
    test2_reflector = Reflector('Test', code = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ')
    
    test_machine = Machine((test2_rotor, test2_rotor, test2_rotor), test2_reflector, test2_board)

    assert test_machine.plugboard == {'C':'M', 'K':'O', 'G':'Z', 'F': 'S', 'B':'D', 'A':'E', 'V':'X', 'L':'I', 'R':'J', 'U':'N'}
    assert test_machine.reflector.name == 'Test'
    assert test_machine.code('A', start_pos = (1, 1, 1)) == 'I'