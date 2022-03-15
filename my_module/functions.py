"""A collection of function for doing my project."""
from string import punctuation
import numpy as np

def cap_chr(index):
    """Finds the corresponding upper case letter to an index (e.g. 0 = A).
    
    Parameters
    ----------
    index : int
        The index of the letter you want to find.
    
    Returns
    -------
    string
        The upper case letter corresponding to inputted index.
    """
    
    return chr(index + 65)

def cap_ord(letter):
    """Finds the corresponding upper case letter to an index (e.g. 0 = A).
    
    Parameters
    ----------
    letter : string
        The upper case letter you are trying to find the index of.
    
    Returns
    -------
    int
        The index of the inputted letter.
    """
    
    return ord(letter) - 65


def reverse_search(letter, dict):
    """Finds the given key of a specified value in a dictionary.
    
    Parameters
    ----------
    letter : string / char
        The value you are looking for in the dict.
    dict : dict
        The dictionary you are using to flip the values.
        
    Returns
    -------
    key : string
        The key corresponding to the key in the dictionary.
    """
    
    key = list(dict.keys())[list(dict.values()).index(letter)]
    return key

def flip_key(keylist): 
    """Flips the values and keys of a numpy array, then sorts it.
    
    Parameters
    ----------
    keylist : numpy array
        The numpy array (ideally a list of code letters like a caesar cipher.
        
    Returns
    -------
    flip_list : numpy array
        The new numpy array with all values and keys flipped and sorted.
    """
    
    flip_list = keylist.copy()
    flip_list[ :, [0,1]] = flip_list[ : , [1, 0]]
    letter_pos = 0
    num_rows, num_col = flip_list.shape

    while letter_pos < num_rows:

        letter = flip_list[letter_pos, 0]

        flip_list[[letter_pos, ord(letter) - 65]] = flip_list[[ord(letter) - 65, letter_pos]]

        if ord(letter) - 65 == letter_pos:
            letter_pos += 1

    return flip_list


def search_plugs(letter, plugs):
    """Searches for letter in plugboard connections. Replaces it, if found.
    
    Parameters
    ----------
    letter : string
        Letter that is being looked for in plugboard connections.
    dict : dict
        Plug connections to sort through in dictionary form.
    Returns
    -------
    letter : string
        Returns letter whether it got replaced or not.
    """
    
    if letter in plugs:
        letter = plugs[letter]
    elif letter in plugs.values():
        letter = reverse_search(letter, plugs)
        
    return letter

def clean_txt(text):
    """Prepares text for the encoding process.
    
    Parameters
    ----------
    text : string
        Text that is to be cleaned up.
    Returns
    -------
    clean_text : string
        Returns the cleaned and capitalized message
    """
    clean_text = ''
    
    for letter in text:
        if letter in punctuation:
            continue
        else:
            clean_text = clean_text + letter
            
    return clean_text.upper()