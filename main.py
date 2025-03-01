import yaml
from tm import TM

from yaml.loader import SafeLoader
# open yaml file in read

tm_data_1 = {}
tm_data_2 = {}

with open('input.yaml', 'r') as f:
	yaml_data = list(yaml.load_all(f, Loader=SafeLoader))
	tm_data_1 = yaml_data[0]
      
with open('input2.yaml', 'r') as f:
	yaml_data2 = list(yaml.load_all(f, Loader=SafeLoader))
	tm_data_2 = yaml_data2[0]

Turing_Machine1 = TM(tm_data_1)
Turing_Machine2 = TM(tm_data_2)

menu_open = True

while menu_open:
    
    print("\nWelcome to the Turing Machine Simulation")
    print("Please select wich turing machine do you want to test")
    print("1. {a^n b^n | n >= 1}")
    print("2. 2's complement of a bit string (Altering turing Machine)")

    selected_turing_machine: TM = None

    tm_opt = input()
    
    selected_turing_machine = Turing_Machine1 if tm_opt == "1" else Turing_Machine2 if tm_opt == "2" else None

    if selected_turing_machine != None:
        print("Please enter the number corresponding to the word you want to test in the turing machine")
        for index, word in enumerate(selected_turing_machine.words):
            
            print(f"{index + 1}.{word}")

        selection = int(input("Or select any other number to quit: "))

        if selection >= 1 and selection <= len(selected_turing_machine.words):
            selected_word = selected_turing_machine.words[selection - 1]
            print(f"You selected the string: {selected_word}")
            selected_turing_machine.initializeTape(selected_word)

            selected_turing_machine.start_simulation(selected_word)

        else:
            menu_open = False