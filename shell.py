"""
OGAME LULZ
Shell Module

elliot 2010
"""

import sys
import threading

class ShellManager:
    """
    The shell manager spins new threads for new commands to be executed by the
    shell.
    """
    def __init__(self):
        
        while True:
            sys.stdout.write("ogame $ ")
            cmd = sys.stdin.readline()
            cmd = cmd.rstrip('\n')

            # Test for quit, exit commands
            if cmd == "quit" or cmd == "exit":
                print "later gator"
                break

            
class Shell:
    """
    A new instance of this class executes a Command
    """
    def __init(self, command):
        """
        command must be of type Command
        """
        pass

if __name__ == '__main__':
    print "Welcome to OGame shell."
    ShellManager()
    
