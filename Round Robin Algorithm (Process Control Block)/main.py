import random

def generate_2d_list(quanta, b):
    instructions = []

    for i in range(len(b)):
        division_result = b[i] / quanta
        if division_result.is_integer():
            row_size = int(division_result)
        else:
            row_size = int(division_result) + 1
        row = [random.randint(1, 20) for _ in range(row_size)]
        instructions.append(row)
    
    return instructions

print("\nImplementation of Round Robin Scheduling Project Task!\n")



def print_process_state(processes, current_time, process_states, resource_states):
    print("At time {}:".format(current_time))
    for i, state in enumerate(process_states):
        resource_demand = "  Resource demand = 1" if resource_states[i] == 1 else "  Resource demand = 0"
        print("P{} is {}-{}".format(i + 1, state, resource_demand))
    if running_process_index != -1 and instructions_execution_progress[running_process_index] < len(instructions[running_process_index]):
        executed_instructions = instructions[running_process_index][:instructions_execution_progress[running_process_index]]
        instruction_to_execute = instructions[running_process_index][instructions_execution_progress[running_process_index]]
        print("Instructions for Each Process:")
        print("Process P{}: {}, {}".format(running_process_index + 1, ", ".join(map(str, executed_instructions)), instruction_to_execute))
        print("Instruction Register", instruction_to_execute)
        instructions_execution_progress[running_process_index] += 1




def print_gantt_chart(gantt_chart):
    print("\nGantt Chart:")
    print("-" * (sum([segment + 3 for _, segment in gantt_chart]) + 3))
    for process_id, segment in gantt_chart:
        print("| P{}{} ".format(process_id + 1, "" * (segment - len(str(process_id + 1)))), end="")
    print("|")
    print("-" * (sum([segment + 3 for _, segment in gantt_chart]) + 3))
    start = 0
    for _, segment in gantt_chart:
        print("{:d}    ".format(start), end="")
        start += segment
    print("{:d}".format(start))

n = int(input("Enter the no. of processes: "))
quant = int(input("Enter the quantum: "))

# Input arrays for arrival times and execution times
input_arrival_times = []
input_execution_times = []

for i in range(n):
    input_arrival_times.append(int(input(f"Enter arrival time for process P{i+1}: ")))
    input_execution_times.append(int(input(f"Enter execution time for process P{i+1}: ")))

p = []

for i in range(n):
    p.append({
        'pos': i + 1,
        'AT': input_arrival_times[i],  # Use input_arrival_times array
        'BT': input_execution_times[i],  # Use input_execution_times array
        'ST': [0] * 20,
        'WT': 0,
        'FT': 0,
        'TAT': 0
    })

c = n
s = [[-1] * 20 for _ in range(n)]
time = 0
mini = float('inf')
b = [0] * n
a = [0] * n

for i in range(n):
    b[i] = p[i]['BT']
    a[i] = p[i]['AT']

tot_wt = 0
tot_tat = 0

process_states = ["not started"] * n

response_times = [-1] * n  # Initialize response_times array

gantt_chart = []  # Initialize the Gantt chart

# Initialize resource states for each process
resource_states = [0] * n




# Print input arrays for arrival times and execution times
print("\nInput Arrival Times Array:", input_arrival_times)
print("Input Execution Times Array:", input_execution_times)

print("\nGenerating Instructions for Each Process...\n")
instructions = generate_2d_list(quant, b)  # Generate instructions using the function

# Initialize the instructions execution progress for each process
instructions_execution_progress = [0] * n

print("\nSimulating Round-Robin Scheduling...\n")
blocked_process_indices = []  # Initialize to an empty list (no blocked processes)
running_process_index = -1  # Initialize the running process index
# Create arrays to track the execution of each process
execution_process = [[] for _ in range(n)]



while c != 0:
    mini = float('inf')
    flag = False

    if running_process_index != -1 and random.random() < 0.3:
        if running_process_index not in blocked_process_indices and process_states[running_process_index] != "finished":
            blocked_process_indices.append(running_process_index)
            process_states[running_process_index] = "blocked"
            resource_states[running_process_index] = 1  # Mark resource demand as 1
            print("Process P{} blocked at time {}".format(running_process_index + 1, time))
            running_process_index = -1  # Pause the running process

    for i in range(n):
        p_val = time + 0.1
        if a[i] <= p_val and mini > a[i] and b[i] > 0:
            index = i
            mini = a[i]
            flag = True

    if not flag:
        time += 1
        continue
    
    # Unblock the process
    if index in blocked_process_indices:
        blocked_process_indices.remove(index)
        process_states[index] = "unblocked"
        resource_states[index] = 0  # Mark resource demand as 0
        print("Process P{} unblocked at time {}".format(index + 1, time))
    


    if running_process_index != index:
        if running_process_index != -1:
            if b[running_process_index] > 0:
                process_states[running_process_index] = "waiting"
                resource_states[running_process_index] = 0  # Mark resource demand as 0
            else:
                process_states[running_process_index] = "finished"
                resource_states[running_process_index] = 0  # Mark resource demand as 0
        if response_times[index] == -1:
            response_times[index] = time - p[index]['AT']
        running_process_index = index

    j = 0
    while s[index][j] != -1:
        j += 1

    if s[index][j] == -1:
        s[index][j] = time
        p[index]['ST'][j] = time

    if b[index] <= quant:
        gantt_chart.append((index, b[index]))
        print("Process P{} resumed at time {}".format(index + 1, time))
        
        execution_process[index].extend([time + i for i in range(b[index])])  # Add execution times to the process
        
        time += b[index]
        p[index]['FT'] = time
        b[index] = 0
        process_states[index] = "finished"
        resource_states[index] = 0  # Mark resource demand as 0
        c -= 1
    else:
        gantt_chart.append((index, quant))
        print("Process P{} resumed at time {}".format(index + 1, time))
        
        execution_process[index].extend([time + i for i in range(quant)])  # Add execution times to the process
        
        time += quant
        b[index] -= quant
        process_states[index] = "running"
        resource_states[index] = 0  # Mark resource demand as 0

    if b[index] > 0:
        a[index] = time + 0.1

    if b[index] == 0:
        p[index]['WT'] = p[index]['FT'] - p[index]['AT'] - p[index]['BT']
        tot_wt += p[index]['WT']
        p[index]['TAT'] = p[index]['BT'] + p[index]['WT']
        tot_tat += p[index]['TAT']
        process_states[index] = "finished"
        resource_states[index] = 0  # Mark resource demand as 0

    print_process_state(p, time, process_states, resource_states)  # Print instructions here
    print("\n")


# Print the instructions arrays for each process
print("Instructions for Each Process:")
for i in range(n):
    print("Process P{}: {}".format(i + 1, instructions[i]))

# Finish executing blocked process if any
while blocked_process_indices:
    index = blocked_process_indices.pop(0)
    if process_states[index] == "blocked":
        gantt_chart.append((index, b[index]))
        print("Process P{} resumed at time {}".format(index + 1, time))
        execution_process[index].extend([time + i for i in range(b[index])])  # Add execution times to the process
        time += b[index]
        p[index]['FT'] = time
        b[index] = 0
        process_states[index] = "finished"
        resource_states[index] = 0  # Mark resource demand as 0
        c -= 1

# Print the execution process of each individual process
print("\nExecution Process Times:")
for i, execution_times in enumerate(execution_process):
    print("Process P{} executed at times: {}".format(i + 1, execution_times))

avg_wt = tot_wt / float(n)
avg_tat = tot_tat / float(n)
avg_response_time = sum(response_times) / float(n)

total_burst_time = sum(p[i]['BT'] for i in range(n))
utilization_time = total_burst_time / sum(p[i]['TAT'] for i in range(n))

print("\nIndividual Process Metrics:")
print("--------------------------------------------------------------------------------------------------------------------------")
print("| Processes | Arrival time | Burst time | Wait time | Response time | Turnaround time | Completion time |    Start time  |")
print("--------------------------------------------------------------------------------------------------------------------------")
for i in range(n):
    first_start_time = p[i]['ST'][0] if p[i]['ST'][0] != 0 else p[i]['AT']
    response_time = first_start_time - p[i]['AT']
    
    # Calculate the start time
    start_time = first_start_time if process_states[i] != "waiting" else "-"
    
    print("|   P{:d}      |     {:3d}      |    {:3d}     |   {:3d}     |       {:3d}     |      {:3d}        |      {:3d}        |      {:3}        |".format(
        i + 1, p[i]['AT'], p[i]['BT'], p[i]['WT'], response_times[i], p[i]['TAT'], p[i]['FT'], start_time))
print("--------------------------------------------------------------------------------------------------------------------------")

# Print Gantt Chart
print_gantt_chart(gantt_chart)

print("\nAverage timings of Round Robin Scheduling process:-")
print("The average Wait time is:", avg_wt)
print("The average TurnAround time is:", avg_tat)
print("The average Response time is:", avg_response_time)
print("The Utilization time of processes in Round Robin Scheduling Algo:", utilization_time)

print("\nThis is all about Round Robin Project Task!\n")