"""Classes used throughout project"""
import numpy as np
import my_module.functions as func
from string import ascii_uppercase

class Encryptor:
    
    def __init__(self, name, code): 
        self.code = np.stack((list(ascii_uppercase), list(code)), axis = 1)
        self.name = name

    
class Rotor(Encryptor):
    """Class that holds the keys and name of inputted rotor
    
    Attributes
    ----------
    name : string
        Name of the rotor
    code : numby array
        Array of letters corresponding to their code letter (like a caesar cipher)
    turnover : string
        The letter that the next rotor will turnover (physically this would be where its turnover notch would activate).
    """
    
    def __init__(self, name, code, turnover):
        super().__init__(name, code)
        self.turnover = turnover

        
class Reflector(Encryptor):
    """Class that holds the keys and name of inputted reflector
    
    Attributes
    ----------
    name : string
        Name of the reflector
    code : numby array
        Array of letters corresponding to their code letter (like a caesar cipher)
    """
    
    pass


class Machine:

    def __init__(self, rotors, reflector, plugboard): 
        """Array that simulates an instance of the enigma machine.
        
        Attributes
        ----------
        rotors : tuple
            A tuple of the desired rotors to put in the machine.
        reflector : reflector object
            The reflector you would like to use your this machine.
        plugboard : tuple
            The tuple holding all the values of the plugboard.
            
        Methods
        -------
        code
            Encodes or decodes inputted messages
        """
        
        self.rotors = rotors
        self.reflector = reflector
        dict1 = {}

        for x in plugboard:    
            a = x[0]
            b = x[1]
            dict1.update({a : b})

        self.plugboard = dict1
        self.info = 'First rotor is ' + rotors[0].name + \
                    '\nSecond rotor is ' + rotors[1].name + \
                    '\nThird rotor is ' + rotors[2].name + \
                    '\nReflector is ' + reflector.name + \
                    '\nPlugboard connections are:\n' + str(dict1)
       
              
    def code(self, input_msg, start_pos): 
        """Encodes (or decodes) a given message and starting position for rotors.
        
        Parameters
        ----------
        message : string
            The message to be encoded or decoded.
        start_pos : int tuple
            The 3 number start position of the rotors.
            
        Returns
        -------
        new_msg : string
            The encoded (or decoded) message corresponding to the inputted message and rotor positions.
        """
        
        msg_index = 0   # Where in the message we are (index)
        rot_shift = list(start_pos)   # Rotation shift on the rotors
        new_msg = ""   # Encoded / decoded message

        # First the message is cleaned and prepared like a vegetable
        message = func.clean_txt(input_msg)
        
        while msg_index < len(message):
            letter = message[msg_index]   # Letter we are at 
            
            # If the current letter is a space just skip over it 
            if letter == " ":
                new_msg = new_msg + letter
                msg_index += 1
                continue

            msg_index += 1   # Adding one to the index to simulate a keypress
            rot_shift[0] = (rot_shift[0] % 26) + 1    # Adding one to the rotation shift of the first rotor

            # Search through the plugboard connection dictionary to see if our letter shows up, and replace it if so
            letter = func.search_plugs(letter, self.plugboard)

            # If it has gone over the turnover key then turn the next rotor    
            if chr(rot_shift[0] + 64) == self.rotors[0].turnover: 
                rot_shift[1] += 1 
                
                # If the second rotor has gone over turnover then turn the last rotor
                if chr(rot_shift[1] + 64) == self.rotors[1].turnover: 
                    rot_shift[2] += 1

            # Ltr_shift is letter shift, calculating how much each rotor has shifted from each other       
            ltr_shift = [] 
            ltr_shift.append(rot_shift[0] - 1) 
            
            for x in range(1,3):
                # If the value is negative then we make it positive to simplify future calculations
                if (rot_shift[x] - rot_shift[x - 1]) < 0: 
                    ltr_shift.append((rot_shift[x] - rot_shift[x - 1] + 26))
                else:
                    ltr_shift.append((rot_shift[x] - rot_shift[x - 1]))
            ltr_shift.append((1 - rot_shift[2] + 26) % 26)

            letter_num = (func.cap_ord(letter))   # Number value of letter currently stored

            # Shifting each letter by the rotor shifts then doing substitutions based on the key of the rotor
            for x in range(0,3): 
                letter_num = (letter_num + ltr_shift[x]) % 26

                letter_num = (ord(self.rotors[x].code[letter_num, 1]) - 65)

            # Shift of last rotor to unmoving reflector
            letter_num = (letter_num + ltr_shift[3]) % 26   

            letter_num = (func.cap_ord(self.reflector.code[letter_num, 1])) # Reflection of input

            # Quick list made to store inverted rotor codes for the encoded letter's trip back from reflector
            frotors = [] 
            for x in range(0, 3):
                frotors.append(func.flip_key(self.rotors[x].code))

             # Shifting each letter by the rotor shifts then doing substitutions based on the key of the rotor
            for x in range(2, -1, -1):
                letter_num = (letter_num - ltr_shift[x + 1] + 26) % 26

                letter_num = (ord((frotors[x][letter_num, 1])) - 65)
                
            # Final shift then turning the number back into a real letter
            letter_num = (letter_num - ltr_shift[0]) % 26   
            letter = func.cap_chr(letter_num)

            # Search through the plugboard connection dictionary to see if our letter shows up, and replace it if so
            letter = func.search_plugs(letter, self.plugboard)

            new_msg = new_msg + letter

        return new_msg