#main.py

from SJF import SJF
from SRTF import findavgTime as SRTF
from HRRN import hrrn_scheduling as HRRN, Process

def run_SJF():
    print("\n************ Running Shortest Job First (SJF) Algorithm ************\n")
    no_of_processes = int(input("Enter the number of processes: "))
    sjf = SJF()
    sjf.processData(no_of_processes)

def run_SRTF():
    print("\n************ Running Shortest Remaining Time First (SRTF) Algorithm ************\n")
    n = int(input("Enter the number of processes: "))
    proc = []
    for i in range(1, n + 1):
        arrival_time = int(input(f"Enter arrival time for Process P{i}: "))
        burst_time = int(input(f"Enter execution time for Process P{i}: "))
        proc.append([i, burst_time, arrival_time])
    SRTF(proc, n)

def run_HRRN():
    print("\n************ Running Highest Response Ratio Next (HRRN) Algorithm ************\n")
    num_processes = int(input("Enter the number of processes: "))
    processes = []
    for i in range(1, num_processes + 1):
        arrival_time = int(input(f"Enter arrival time for Process P{i}: "))
        burst_time = int(input(f"Enter execution time for Process P{i}: "))
        processes.append(Process(f"P{i}", arrival_time, burst_time))
    completed_processes, gantt_chart, total_utilization_time  = HRRN(processes)

    # Calculate average waiting time, average turnaround time, and average response time
    total_waiting_time = sum(process.waiting_time for process in completed_processes)
    total_turnaround_time = sum(process.turnaround_time for process in completed_processes)
    total_response_time = sum(process.response_time for process in completed_processes)
    num_completed_processes = len(completed_processes)
    average_waiting_time = total_waiting_time / num_completed_processes
    average_turnaround_time = total_turnaround_time / num_completed_processes
    average_response_time = total_response_time / num_completed_processes
    average_utilization_time = total_utilization_time / num_completed_processes

    # Print the table of results with completion, waiting, turnaround, response, and utilization times
    print("Process\tArrival Time\tExecution Time\tWaiting Time\tTurnaround Time\tResponse Time\tCompletion Time\tUtilization Time")
    for process in completed_processes:
        print(f"{process.name}\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}\t\t{process.response_time}\t\t{process.completion_time}\t\t{process.utilization_time:.2f}")

    # Print the Gantt chart
    print("\nGantt Chart:")
    print("-" * 30)
    print("|", end=" ")
    for item in gantt_chart:
        print(item, end=" | ")
    print("\n" + "-" * 30)

    # Print the average waiting time, average turnaround time, and average response time
    print(f"\nAverage Waiting Time: {average_waiting_time:.2f}")
    print(f"Average Turnaround Time: {average_turnaround_time:.2f}")
    print(f"Average Response Time: {average_response_time:.2f}")
    print(f"Average Utilization Time: {average_utilization_time:.2f}")

def main():
    while True:
        # Display the menu to the user
        print("\nChoose an option:")
        print("1. Run Shortest Job First (SJF) Algorithm")
        print("2. Run Shortest Remaining Time First (SRTF) Algorithm")
        print("3. Run Highest Response Ratio Next (HRRN) Algorithm")
        print("0. Quit")

        # Get user input
        choice = input("\nEnter your choice: ")

        if choice == "1":
            run_SJF()
        elif choice == "2":
            run_SRTF()
        elif choice == "3":
            run_HRRN()
        elif choice == "0":
            print("Process end.")
            break
        else:
            print("Invalid choice. Please select a valid option (1, 2, 3, or 0).")

if __name__ == "__main__":
    main()