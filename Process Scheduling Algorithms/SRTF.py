# Criteria: Shortest Remaining Time First
# Mode: Pre-Emptive
#TAT = FT-AT
#WT = TAT-BT
#RT = {CPU first time-AT}

# Function to find the waiting time and response time for all processes
def findWaitingResponseTime(processes, n, wt, rt):
    remaining_time = [0] * n

    # Copy the burst time into remaining_time[]
    for i in range(n):
        remaining_time[i] = processes[i][1]
    complete = 0
    t = 0
    minm = 999999999
    short = 0
    check = False

    timeline = []  # To store the Gantt chart timeline

    # Process until all processes get completed
    while complete != n:

        # Find process with minimum remaining time among the processes that arrive till the current time
        for j in range(n):
            if processes[j][2] <= t and remaining_time[j] < minm and remaining_time[j] > 0:
                minm = remaining_time[j]
                short = j
                check = True
        if check == False:
            t += 1
            continue

        # Reduce remaining time by one
        remaining_time[short] -= 1

        # Update minimum
        minm = remaining_time[short]
        if minm == 0:
            minm = 999999999

        # If a process gets completely executed
        if remaining_time[short] == 0:

            # Increment complete
            complete += 1
            check = False

            # Find finish time of the current process
            fint = t + 1

            # Calculate waiting time
            wt[short] = fint - processes[short][1] - processes[short][2]

            if wt[short] < 0:
                wt[short] = 0

            # Calculate response time
            rt[short] = wt[short] + processes[short][2]

        # Append process to the timeline along with finish time
        timeline.append((short, t + 1))

        # Increment time
        t += 1

    return timeline

# Function to calculate turn-around time
def findTurnAroundTime(processes, n, wt, tat):
    # Calculating turnaround time
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]

# Function to calculate average waiting, response, and turn-around times.
def findavgTime(processes, n):
    wt = [0] * n
    rt = [0] * n
    tat = [0] * n
    utilization_time = [0] * n  # List to store utilization time for each process

    # Function to find waiting and response times of all processes
    timeline = findWaitingResponseTime(processes, n, wt, rt)

    # Function to find turn-around time for all processes
    findTurnAroundTime(processes, n, wt, tat)

    # Display processes along with all details
    print("Processes Burst Time     Arrival Time    Waiting Time    Response Time   Turn-Around Time    Finish Time   Utilization Time")
    total_wt = 0
    total_rt = 0
    total_tat = 0
    total_utilization = 0  # Total utilization time for calculating average
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_rt = total_rt + rt[i]
        total_tat = total_tat + tat[i]
        utilization_time[i] = processes[i][1] / tat[i]  # Calculate utilization time
        total_utilization += utilization_time[i]
        finish_time = processes[i][2] + tat[i]
        
        print(" ", processes[i][0], "\t\t", processes[i][1], "\t\t", processes[i][2], "\t\t", wt[i], "\t\t",
              rt[i], "\t\t", tat[i], "\t\t", finish_time, "\t\t", utilization_time[i])

    print("\nAverage waiting time = %.5f" % (total_wt / n))
    print("Average response time = %.5f" % (total_rt / n))
    print("Average turn-around time = %.5f" % (total_tat / n))
    print("Average utilization time = %.5f" % (total_utilization / n))

    # Display Gantt Chart
    print("\nGantt Chart:")
    print("-" * (sum(tat) + n + 1))  # Horizontal line
    print("|", end="")
    for event in timeline:
        print(f" P{processes[event[0]][0]} |", end="")
    print("\n" + "-" * (sum(tat) + n + 1))  # Horizontal line

#***For Running this code individualy***

# Driver code
# if __name__ == "__main__":
#     print("\n************ SRTF (Shortest Remaining Time First) Algorithm ************\n")
#     n = int(input("Enter the number of processes: "))
#     proc = []

#     for i in range(n):
#         pid = i + 1
#         arrival_time = int(input(f"Enter arrival time for process {pid}: "))
#         burst_time = int(input(f"Enter burst time for process {pid}: "))
#         proc.append([pid, burst_time, arrival_time])

#     findavgTime(proc, n)