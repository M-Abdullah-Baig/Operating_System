# Criteria: Shortest Job First
# Mode: Non Pre-Emptive (WT = RT)
#TAT = FT-AT
#WT = TAT-BT
#RT = {CPU first time-AT}


class SJF:

    def processData(self, no_of_processes):
        process_data = []
        for i in range(no_of_processes):
            temporary = {}
            temporary['Process_ID'] = int(input("Enter Process ID: "))
            temporary['Arrival_Time'] = int(input(f"Enter Arrival Time for Process {temporary['Process_ID']}: "))
            temporary['Burst_Time'] = int(input(f"Enter Burst Time for Process {temporary['Process_ID']}: "))
            temporary['Completed'] = False
            process_data.append(temporary)
        self.schedulingProcess(process_data)  # Use 'self' to call class methods

    def schedulingProcess(self, process_data):
        start_times = []  # Renamed from start_time to start_times
        s_time = 0
        process_data.sort(key=lambda x: x['Arrival_Time'])
        gantt_chart = []  # Initialize an empty Gantt Chart
        for i in range(len(process_data)):
            ready_queue = []
            temp = {}
            normal_queue = []

            for j in range(len(process_data)):
                if (process_data[j]['Arrival_Time'] <= s_time) and (not process_data[j]['Completed']):
                    temp['Process_ID'] = process_data[j]['Process_ID']
                    temp['Arrival_Time'] = process_data[j]['Arrival_Time']
                    temp['Burst_Time'] = process_data[j]['Burst_Time']
                    ready_queue.append(temp.copy())
                elif not process_data[j]['Completed']:
                    temp['Process_ID'] = process_data[j]['Process_ID']
                    temp['Arrival_Time'] = process_data[j]['Arrival_Time']
                    temp['Burst_Time'] = process_data[j]['Burst_Time']
                    normal_queue.append(temp.copy())

            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x['Burst_Time'])
                # Calculate Start Time as the maximum of Arrival Time and completion time of the previous process
                start_times.append(max(s_time, ready_queue[0]['Arrival_Time']))
                s_time = start_times[-1] + ready_queue[0]['Burst_Time']
                completion_time = s_time
                for k in range(len(process_data)):
                    if process_data[k]['Process_ID'] == ready_queue[0]['Process_ID']:
                        process_data[k]['Completed'] = True
                        process_data[k]['Completion_Time'] = completion_time
                        # Calculate Response Time when a process is added to the ready queue
                        process_data[k]['Response_Time'] = start_times[-1] - process_data[k]['Arrival_Time']
                        gantt_chart.append((process_data[k]['Process_ID'], ready_queue[0]['Burst_Time']))
                        break

            elif len(normal_queue) != 0:
                if s_time < normal_queue[0]['Arrival_Time']:
                    s_time = normal_queue[0]['Arrival_Time']
                # Calculate Start Time as the maximum of Arrival Time and completion time of the previous process
                start_times.append(max(s_time, normal_queue[0]['Arrival_Time']))
                normal_queue.sort(key=lambda x: x['Burst_Time'])  # Sort the normal queue by burst time
                s_time = start_times[-1] + normal_queue[0]['Burst_Time']
                completion_time = s_time
                for k in range(len(process_data)):
                    if process_data[k]['Process_ID'] == normal_queue[0]['Process_ID']:
                        process_data[k]['Completed'] = True
                        process_data[k]['Completion_Time'] = completion_time
                        # Calculate Response Time when a process is added to the ready queue
                        process_data[k]['Response_Time'] = start_times[-1] - process_data[k]['Arrival_Time']
                        gantt_chart.append((process_data[k]['Process_ID'], normal_queue[0]['Burst_Time']))
                        break

        t_time = self.calculateTurnaroundTime(process_data, start_times)  # Pass start_times to calculateTurnaroundTime
        w_time = self.calculateWaitingTime(process_data)  # Use 'self' to call class methods
        self.calculateUtilizationTime(process_data)  # Calculate utilization time
        average_utilization_time = sum(process['Utilization_Time'] for process in process_data) / len(process_data)
        self.printData(process_data, average_turnaround_time=t_time, average_waiting_time=w_time, average_utilization_time=average_utilization_time, start_times=start_times)  # Pass start_times to printData
        self.print_gantt_chart(gantt_chart)  # Print the Gantt Chart

    def calculateTurnaroundTime(self, process_data, start_times):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i]['Completion_Time'] - process_data[i]['Arrival_Time']
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i]['Turnaround_Time'] = turnaround_time
        average_turnaround_time = total_turnaround_time / len(process_data)
        return average_turnaround_time

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i]['Turnaround_Time'] - process_data[i]['Burst_Time']
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i]['Waiting_Time'] = waiting_time
        average_waiting_time = total_waiting_time / len(process_data)
        return average_waiting_time

    def calculateUtilizationTime(self, process_data):
        for process in process_data:
            turnaround_time = process['Turnaround_Time']
            burst_time = process['Burst_Time']
            utilization_time = burst_time / turnaround_time
            process['Utilization_Time'] = utilization_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time, average_utilization_time, start_times):
        n = len(process_data)
        process_states = [""] * n

        process_data.sort(key=lambda x: x['Process_ID'])

        # Define the column headers
        headers = ["Processes", "Arrival time", "Burst time", "Wait time", "Response time", "Turnaround time", "Completion time", "Start time", "Utilization time"]

        # Print the table headers
        print("-------------------------------------------------------------------------------------------------------------------------")
        print("|Processes|ArrivalTime|BurstTime|WaitTime|ResponseTime|TurnaroundTime|CompletionTime|StartTime|UtilizationTime|")
        print("-------------------------------------------------------------------------------------------------------------------------")

        for i in range(n):
            # Calculate the start time, response time, and utilization time
            start_time = start_times[i] if process_states[i] != "waiting" else "-"
            response_time = process_data[i]['Response_Time']
            utilization_time = process_data[i]['Utilization_Time']

            print("|   P{:d}    |     {:d}     |   {:2d}    |   {:2d}   |     {:2d}     |      {:2d}      |      {:2d}      |   {:2}    |     {:.2f}     |".format(
                i + 1, process_data[i]['Arrival_Time'], process_data[i]['Burst_Time'], process_data[i]['Waiting_Time'], response_time, process_data[i]['Turnaround_Time'], process_data[i]['Completion_Time'], start_time, utilization_time))
        print("-------------------------------------------------------------------------------------------------------------------------")

        # Print the average turnaround time, average waiting time, and average utilization time
        print(f'Average Response Time: {average_waiting_time}')
        print(f'Average Turnaround Time: {average_turnaround_time}')
        print(f'Average Waiting Time: {average_waiting_time}')
        print(f'Average Utilization Time: {average_utilization_time:.2f}')

    def print_gantt_chart(self, gantt_chart):
        print("\nGantt Chart:")
        print("-" * (sum([segment + 3 for _, segment in gantt_chart]) + 3))
        for process_id, segment in gantt_chart:
            print("| P{}{} ".format(process_id, "" * (segment - len(str(process_id)))), end="")
        print("|")
        print("-" * (sum([segment + 3 for _, segment in gantt_chart]) + 3))
        start = 0
        for _, segment in gantt_chart:
            print("{:d}    ".format(start), end="")
            start += segment
        print("{:d}".format(start))


#***For Running this code individualy***

# if __name__ == "__main__":
#     print("\n************ SJF (Shortest Job First) Algorithm ************\n")
#     no_of_processes = int(input("Enter the number of processes: "))
#     sjf = SJF()  # Create an instance of the SJF class
#     sjf.processData(no_of_processes)

