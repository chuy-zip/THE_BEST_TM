import json
import time
import matplotlib.pyplot as plt
import numpy as np
import csv
from fibo_tm import TM

# reference: https://www.geeksforgeeks.org/python-program-to-covert-decimal-to-binary-number/
def num_to_unary(num):
    counter_string = "|"

    if num == 1:
        return "|1|"
    
    if num > 1:
        for i in range(num):
            counter_string = counter_string + "1"

        counter_string = counter_string + "|"
    print(counter_string)

    return counter_string

tm_data = {}
# Open and read the JSON file
with open('TM.json', 'r') as file:
    tm_data = json.load(file)

# Print the data


print("\nWelcome to the Fibonacci Turing Machine Simulation")
print("Enter the max number you want to execute (5 would execute fibo(1), fibo(2).... until fibo(5))")
print("The time will be measured for each TM simulation and then will be plotted")
tm_opt = int(input("Max number: "))

print("Enter the step size (e.g., 1 for a step of 1 by 1, 5 for 5 by 5, etc.)")
step = int(input("Step: "))


number_counter = 1

# 2 arrays, one for saving execution time
execution_times = []
#and the other for the corresponding input number
input_numbers = []

while number_counter <= tm_opt:

    binary_num = num_to_unary(number_counter)
    print(f"\nWe will be converting the number {number_counter} to binary and test the string -> {binary_num}")

    Turing_Machine = TM(tm_data)

    #simulation reset
    Turing_Machine.initializeTape(binary_num)

    #simulation running
    start_time = time.perf_counter()  # initial time
    Turing_Machine.start_simulation(binary_num)
    end_time = time.perf_counter()  # final time

    # exec time
    execution_time = end_time - start_time
    print(f"Execution time for {number_counter}: {execution_time:.6f} seconds")

    # time and number
    execution_times.append(execution_time)
    input_numbers.append(number_counter)

    number_counter += step

plt.plot(input_numbers, execution_times, marker='o')

degree = 2  
coefficients = np.polyfit(input_numbers, execution_times, degree)
polynomial = np.poly1d(coefficients)

x_values = np.linspace(min(input_numbers), max(input_numbers), 100)
y_values = polynomial(x_values)

plt.plot(x_values, y_values, label=f"Polynomial Regression (degree {degree})", linestyle="--")

plt.title("Turing Machine Execution Time")
plt.xlabel("Input Number")
plt.ylabel("Execution Time (seconds)")
plt.legend()
plt.grid(True)
plt.show()

with open('execution_times.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Input Number", "Execution Time (seconds)"]) 
    for number, time in zip(input_numbers, execution_times):
        writer.writerow([number, time])

print("Data saved to 'execution_times.csv'")
