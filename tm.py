class TM():
    def __init__(self, tm_data: dict):
        self.states = tm_data["q_states"]["q_list"]
        self.initial_state = tm_data["q_states"]["initial"]
        self.final_state = tm_data["q_states"]["final"]
        self.alphabet = tm_data["alphabet"]
        self.tape_alphabet = tm_data["tape_alphabet"]
        self.transitions = self.formatTransitions(tm_data["delta"])
        self.words = tm_data["simulation_strings"]
        self.tape = []
        self.head = { "current_state": str, "current_cache": str, "position": int }
    
    # I made this to later make easier the search of a matching transitions with the state of the tm machine
    def formatTransitions(self, transitions):

        new_transitions = {}

        for state in self.states:
            new_transitions[state] = []

        for transition in transitions:

            initial_state = transition["params"]["initial_state"]

            new_transitions[initial_state].append(transition)

        return new_transitions
    
    #This function must be called only after the usar has selected a tape.
    #And also when the transitions have already been formatted with the function above.
    def initializeTape(self, word: str):

        self.tape = list(word.strip())

        initial_state = self.initial_state
        self.head["current_state"] = initial_state
        self.head["current_cache"] = "B"
        self.head["position"] = 0

    def format_transition(self, transition):
        parameters = transition["params"]
        output = transition["output"]

        return f"S([{parameters["initial_state"]},{parameters["mem_cache_value"]}],{parameters["tape_input"]}) = ([{output["final_state"]},{output["mem_cache_value"]}],{output["tape_output"]},{output["tape_displacement"]})"

    def show_instant_description(self):

        print("Instant description")

        for index, char in enumerate(self.tape):

            if index == self.head["position"]:

                state = self.head["current_state"]
                cache = self.head["current_cache"]

                print(f"[{state},{cache}]", end="")

            print(char, end= "")

        print("\n")

    def start_simulation(self, selected_word):
        print("\nNow testing the tape:", self.tape)
        self.show_instant_description()

        while self.head["current_state"] != self.final_state:

            transition_found = self.update_machine()

            if transition_found == False:
                break
        
        #When we exit the simulation its either because we reached final state, or at some point
        #no transition matched the instant description of the turing machine and exit with a break

        if self.head["current_state"] == self.final_state:

            print("The turing machine accepts the string: ", selected_word)

        else:
            current_state = self.head["current_state"]
            current_cache = self.head["current_cache"]
            current_position = self.head["position"]
            char_in_current_position = self.tape[current_position]

            print(f"There is no matching transition for: S([{current_state},{current_cache}],{char_in_current_position})")
            print("The turing machine does not accept the string: ", selected_word)
            
    # This method will be incharge of updating the state, cache and tape given the current condition
    # In which the turing machine currently is. It DOES NOT move.
    def update_machine(self):
        print("Now updating----------------")

        current_state = self.head["current_state"]
        current_cache = self.head["current_cache"]
        current_position = self.head["position"]
        char_in_current_position = self.tape[current_position]

        state_transitions = self.transitions[current_state]

        for transition in state_transitions:

            if current_cache == transition["params"]["mem_cache_value"] and char_in_current_position == transition["params"]["tape_input"]:

                print("Matching transition for current state of TM:", self.format_transition(transition))
                #We found the matching transition, we replace for the corresponding values
                self.head["current_state"] = transition["output"]["final_state"]
                self.head["current_cache"] = transition["output"]["mem_cache_value"]
                self.tape[current_position] = transition["output"]["tape_output"]

                if transition["output"]["tape_displacement"] == "R":
                    self.move_right()
                
                
                elif transition["output"]["tape_displacement"] == "L":
                    self.move_left()

                elif transition["output"]["tape_displacement"] == "S":
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
            self.tape.insert(0, "B")
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
            self.tape.append("B")
            self.head["position"] = next_position
        
        else:
            
            self.head["position"] = next_position
        
        self.show_instant_description()
        
