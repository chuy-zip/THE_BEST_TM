class TM():
    def __init__(self, tm_data: dict):
        self.states = tm_data["Q"]
        self.initial_state = tm_data["q0"]
        self.final_state = tm_data["F"]
        self.alphabet = tm_data["sigma"]
        self.tape_alphabet = tm_data["gamma"]
        self.transitions = tm_data["delta"]
        self.blank = tm_data["Blanc"]
        self.tape = []
        self.head = { "current_state": str, "position": int }
    # I made this to later make easier the search of a matching transitions with the state of the tm machine
    # def formatTransitions(self, transitions):

    #     new_transitions = {}

    #     for state in self.states:
    #         new_transitions[state] = []

    #     for transition in transitions:

    #         initial_state = transition["params"]["initial_state"]

    #         new_transitions[initial_state].append(transition)

    #     return new_transitions
    
    #This function must be called only after the usar has selected a tape.
    #And also when the transitions have already been formatted with the function above.
    def initializeTape(self, word: str):

        self.tape = list(word.strip())

        initial_state = self.initial_state
        self.head["current_state"] = initial_state
        self.head["position"] = 0

    def format_transition(self, input, action):
        # example: 'q0,_': ['q1', 'X', 'R']
        # input: 'q0,_'
        # action: ['q1', 'X', 'R'], change head state to q1, replace with X and move to the Right
        return f"S({input}) = {action}"

    def show_instant_description(self):

        print("Instant description")

        for index, char in enumerate(self.tape):

            if index == self.head["position"]:

                state = self.head["current_state"]

                print(f"[{state}]", end="")

            print(char, end= "")

        print("\n")

    def start_simulation(self, selected_word):
        print("\nNow testing the tape:", self.tape)
        self.show_instant_description()

        while self.head["current_state"] not in self.final_state:

            transition_found = self.update_machine()

            if transition_found == False:
                break
        
        #When we exit the simulation its either because we reached final state, or at some point
        #no transition matched the instant description of the turing machine and exit with a break

        if self.head["current_state"] == self.final_state:

            print("The turing machine accepts the string: ", selected_word)

        else:
            current_state = self.head["current_state"]
            current_position = self.head["position"]
            char_in_current_position = self.tape[current_position]

            print(f"There is no matching transition for: S({current_state},{char_in_current_position})")
            print("The turing machine does not accept the string: ", selected_word)
            
    # This method will be incharge of updating the state, cache and tape given the current condition
    # In which the turing machine currently is. It DOES NOT move.
    def update_machine(self):
        print("Now updating----------------")

        current_state = self.head["current_state"]
        current_position = self.head["position"]
        char_in_current_position = self.tape[current_position]

        transition_inputs = self.transitions.keys()

        #print(transition_inputs)

        for input in transition_inputs:
            # example
            # input: 'q0,_'
            # output: ['q1', 'X', 'R'], change head state to q1, replace with X and move to the Right

            current_transition = f"{current_state},{char_in_current_position}"
            print(f"Comparing {current_transition} with input {input}")

            if current_transition == input:

                output = self.transitions[input] 
                new_state = output[0]
                new_tape_char = output[1]
                head_direction = output[2]

                print("Matching transition for current state of TM:", self.format_transition(input, output))
                #We found the matching transition, we replace for the corresponding values
                self.head["current_state"] = new_state
                self.tape[current_position] = new_tape_char

                if head_direction == "R":
                    self.move_right()
                
                elif head_direction == "L":
                    self.move_left()

                elif head_direction == "-":
                    print("Remaining in the same position---------------")
                    self.show_instant_description()
                    continue

                #Also this method returns true if a transition is found, if not it will return false
                #This is to help the simulation stop when a string is not accepted by the language.
                return True
                
        return False       
            
            
    def move_left(self):
        print("Moving to the left----------")

        next_position = self.head["position"] - 1

        print("Then next position/index of the head would be: ", next_position)
          

        #This means that the end of the tape was reached, we have to add another symbol before moving
        if next_position < 0:
            print("adding letter at the beginning")
            self.tape.insert(0, self.blank)
            self.head["position"] = 0
        
        else:
            
            self.head["position"] = next_position

        self.show_instant_description()

    def move_right(self):
        print("Moving to the right----------")

        next_position = self.head["position"] + 1

        print("Then next position/index of the head would be: ", next_position)
          

        #This means that the end of the tape was reached, we have to add another symbol before moving
        if next_position >= len(self.tape):
            print("adding letter at the end")
            self.tape.append(self.blank)
            self.head["position"] = next_position
        
        else:
            
            self.head["position"] = next_position
        
        self.show_instant_description()
        
