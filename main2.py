import json
from fibo_tm import TM

# reference: https://www.geeksforgeeks.org/python-program-to-covert-decimal-to-binary-number/
def num_to_binary(num):
    binary_string = ""

    while num > 0:
        binary_string = str(num % 2) + binary_string
        num //= 2
    print(binary_string)

    return binary_string

tm_data = {}
# Open and read the JSON file
with open('TM.json', 'r') as file:
    tm_data = json.load(file)

# Print the data
menu_open = True

while menu_open:
    
    print("\nWelcome to the Fibonacci Turing Machine Simulation")
    binary_num = num_to_binary(5)

    Turing_Machine = TM(tm_data)

    Turing_Machine.initializeTape(binary_num)

    #print(Turing_Machine.initial_state)
    #print(Turing_Machine.final_state)
    #print(Turing_Machine.tape)

    tr = Turing_Machine.transitions

    #for key, value in tr.items():
    #    print(Turing_Machine.format_transition("a", key, value))
    Turing_Machine.update_machine()

    tm_opt = input()