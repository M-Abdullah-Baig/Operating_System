# Criteria: Highest Response Ratio Next
# Mode: Non Pre-Emptive (WT = RT)
#TAT = FT-AT
#WT = TAT-BT
#RT = {CPU first time-AT}
#Response Ratio of process = {(WT of process)-(BT of process)}/BT of process

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0
        self.completion_time = 0
        self.utilization_time = 0

def hrrn_scheduling(processes):
    current_time = 0
    completed_processes = []
    gantt_chart = []
    total_utilization_time = 0  # Add a variable for total utilization time

    while processes:
        # Filter out processes that have arrived
        eligible_processes = [process for process in processes if process.arrival_time <= current_time]

        if not eligible_processes:
            current_time += 1
            gantt_chart.append("IDLE")
            continue

        # Calculate the response ratio for each eligible process
        for process in eligible_processes:
            process.waiting_time = current_time - process.arrival_time
            process.response_ratio = (process.waiting_time + process.burst_time) / process.burst_time

        # Select the process with the highest response ratio
        selected_process = max(eligible_processes, key=lambda x: x.response_ratio)

        # Update current time and calculate turnaround time
        current_time += selected_process.burst_time
        selected_process.turnaround_time = current_time - selected_process.arrival_time
        selected_process.response_time = selected_process.waiting_time
        selected_process.completion_time = current_time

        # Calculate utilization time and update the total utilization time
        selected_process.utilization_time = selected_process.burst_time / selected_process.turnaround_time
        total_utilization_time += selected_process.utilization_time

        # Remove the completed process from the list
        processes.remove(selected_process)

        # Add the completed process to the list of completed processes
        completed_processes.append(selected_process)

        # Add the process to the Gantt chart
        gantt_chart.append(selected_process.name)

    return completed_processes, gantt_chart, total_utilization_time

#***For Running this code individualy***

# if __name__ == "__main__":
#     print("\n************ HRRN (Highest Response Ratio Next) Algorithm ************\n")
#     num_processes = int(input("Enter the number of processes: "))

#     # Initialize an empty list to store processes
#     processes = []

#     # Input arrival times and execution times for each process
#     for i in range(1, num_processes + 1):
#         arrival_time = int(input(f"Enter arrival time for Process P{i}: "))
#         burst_time = int(input(f"Enter execution time for Process P{i}: "))
#         processes.append(Process(f"P{i}", arrival_time, burst_time))

#     # Run HRRN scheduling
#     completed_processes, gantt_chart, total_utilization_time = hrrn_scheduling(processes)

#     # Calculate average waiting time, average turnaround time, average response time, and average utilization time
#     total_waiting_time = sum(process.waiting_time for process in completed_processes)
#     total_turnaround_time = sum(process.turnaround_time for process in completed_processes)
#     total_response_time = sum(process.response_time for process in completed_processes)
#     num_completed_processes = len(completed_processes)
#     average_waiting_time = total_waiting_time / num_completed_processes
#     average_turnaround_time = total_turnaround_time / num_completed_processes
#     average_response_time = total_response_time / num_completed_processes
#     average_utilization_time = total_utilization_time / num_completed_processes

#     # Print the table of results with completion, waiting, turnaround, response, and utilization times
#     print("Process\tArrival Time\tExecution Time\tWaiting Time\tTurnaround Time\tResponse Time\tCompletion Time\tUtilization Time")
#     for process in completed_processes:
#         print(f"{process.name}\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}\t\t{process.response_time}\t\t{process.completion_time}\t\t{process.utilization_time:.2f}")

#     # Print the Gantt chart
#     print("\nGantt Chart:")
#     print("-" * 30)
#     print("|", end=" ")
#     for item in gantt_chart:
#         print(item, end=" | ")
#     print("\n" + "-" * 30)

#     # Print the average waiting time, average turnaround time, average response time, and average utilization time
#     print(f"\nAverage Waiting Time: {average_waiting_time:.2f}")
#     print(f"Average Turnaround Time: {average_turnaround_time:.2f}")
#     print(f"Average Response Time: {average_response_time:.2f}")
#     print(f"Average Utilization Time: {average_utilization_time:.2f}")
#     print("\n")