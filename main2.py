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
with open('test_tm.json', 'r') as file:
    tm_data = json.load(file)

# Print the data


print("\nWelcome to the Fibonacci Turing Machine Simulation")
print("Enter the max number you want to execute (5 would execute fibo(1), fibo(2).... until fibo(5))")
print("The time will be measured for each TM simulation and then will be plotted")

tm_opt = int(input())
number_counter = tm_opt

while number_counter != 30:

    binary_num = num_to_binary(number_counter)
    print(f"We will be testing the string: {binary_num}")

    Turing_Machine = TM(tm_data)

    #simulation
    Turing_Machine.initializeTape(binary_num)
    Turing_Machine.start_simulation(binary_num)

    number_counter = 30
