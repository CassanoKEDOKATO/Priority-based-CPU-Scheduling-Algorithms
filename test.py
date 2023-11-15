import os
from collections import deque


class Process:
    def __init__(self, process_id, arrival_time, burst_time, priority):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = burst_time


def fcfs(processes):
    processes.sort(key=lambda x: x.arrival_time)  # Sắp xếp tiến trình theo thời gian xuất hiện
    curr_time = 0
    for process in processes:
        if process.arrival_time > curr_time:
            curr_time = process.arrival_time
        process.completion_time = curr_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        curr_time = process.completion_time
    return processes


def sjf_non_preemptive(processes):
    processes.sort(
        key=lambda x: (x.burst_time, x.arrival_time))  # Sắp xếp tiến trình theo burst time và thời gian xuất hiện
    curr_time = 0
    for process in processes:
        if process.arrival_time > curr_time:
            curr_time = process.arrival_time
        process.completion_time = curr_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        curr_time = process.completion_time
    return processes


def round_robin(processes, time_quantum):
    curr_time = 0
    queue = deque(processes)
    completed_processes = []
    while queue:
        process = queue.popleft()
        if process.remaining_time <= time_quantum:
            curr_time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = curr_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            completed_processes.append(process)
        else:
            curr_time += time_quantum
            process.remaining_time -= time_quantum
            queue.append(process)
    return completed_processes


def priority_preemptive(processes):
    def find_max_prior_arrived(currTime, lst):
        available_processes = [process for process in lst if
                               process.arrival_time <= currTime and process.remaining_time > 0]
        if available_processes:
            available_processes.sort(key=lambda x: x.priority)
            return available_processes[0], True
        return None, False

    def all_done(lst):
        return all(process.remaining_time == 0 for process in lst)

    curr_time = 0
    while not all_done(processes):
        process, has_arrived = find_max_prior_arrived(curr_time, processes)
        if not has_arrived:
            curr_time += 1
            continue

        process.remaining_time -= 1
        curr_time += 1
        if process.remaining_time == 0:
            process.completion_time = curr_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time

    return processes


def priority_non_preemptive(processes):
    processes.sort(key=lambda x: (x.priority, x.arrival_time))  # Sắp xếp tiến trình theo ưu tiên và thời gian xuất hiện
    curr_time = 0
    for process in processes:
        if process.arrival_time > curr_time:
            curr_time = process.arrival_time
        process.completion_time = curr_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        curr_time = process.completion_time
    return processes

def srtf_preemptive(processes):
    processes.sort(key=lambda x: x.arrival_time)  # Sort processes by arrival time
    current_time = 0
    remaining_processes = list(processes)
    completed_processes = []

    while remaining_processes:
        eligible_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
        if not eligible_processes:
            current_time += 1
            continue

        # Find the process with the shortest remaining burst time
        shortest_process = min(eligible_processes, key=lambda x: x.remaining_time)

        # Execute the process for one time unit
        shortest_process.remaining_time -= 1
        current_time += 1

        # Check if the process has completed
        if shortest_process.remaining_time == 0:
            shortest_process.completion_time = current_time
            shortest_process.turnaround_time = shortest_process.completion_time - shortest_process.arrival_time
            shortest_process.waiting_time = shortest_process.turnaround_time - shortest_process.burst_time
            completed_processes.append(shortest_process)
            remaining_processes.remove(shortest_process)

    return completed_processes

def average_turnaround_time(processes):
    if not processes:
        return 0
    return sum(process.turnaround_time for process in processes) / len(processes)


def average_waiting_time(processes):
    if not processes:
        return 0
    return sum(process.waiting_time for process in processes) / len(processes)


def generate_gantt_chart(processes):
    gantt_chart = " "
    curr_time = 0
    for process in processes:
        gantt_chart += "|"
        for i in range(process.completion_time - curr_time):
            gantt_chart += "-"
        gantt_chart += f"P{process.process_id}"
        curr_time = process.completion_time

    gantt_chart += "|"
    return gantt_chart


def get_processes_from_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            process_data = line.split()
            if len(process_data) == 4:
                if process_data[0] != None:
                    process_id, arrival_time, burst_time = process_data
                    process = Process(process_id, int(arrival_time), int(burst_time), int(priority))
                else:
                    process_id, arrival_time, burst_time, priority = map(int, process_data)
                    process = Process(process_id, arrival_time, burst_time, priority)
            elif len(process_data) == 3:
                if process_data[0] != None:
                    process_id, arrival_time, burst_time = process_data
                    process = Process(process_id, int(arrival_time), int(burst_time), '')
                else:
                    process_id, arrival_time, burst_time = map(int, process_data)
                    process = Process(process_id, arrival_time, burst_time, '')
            else:
                print(f"Invalid data in line: {line}")
                continue
            processes.append(process)
    return processes


def write_results_to_file(file_path, avg_waitingTime, avg_turnaroundTime, input_file, algorithm_type):
    with open(file_path, 'a') as file:
        file.write(f"Results using {algorithm_type}:\n")
        file.write(f"Average Waiting Time: {avg_waitingTime}\n")
        file.write(f"Average Turnaround  Time: {avg_turnaroundTime}\n")
        file.write(f"Input File: {input_file.upper()}\n")
        file.write("\n")


def sort_output_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    algorithms = []
    algorithm_data = {}
    current_algorithm = None

    for line in lines:
        if line.startswith("Results using"):
            if current_algorithm:
                algorithms.append((current_algorithm, algorithm_data))
            current_algorithm = line.strip().split(" using ")[1][:-1]
            algorithm_data = {"avg_waiting_time": None, "avg_turnaround_time": None, "input_file": None}
        elif line.startswith("Average Waiting Time:"):
            algorithm_data["avg_waiting_time"] = float(line.strip().split(": ")[1])
        elif line.startswith("Input File:"):
            algorithm_data["input_file"] = line.strip().split(": ")[1]

    algorithms.append((current_algorithm, algorithm_data))
    sorted_algorithms = sorted(algorithms, key=lambda x: x[1]["avg_waiting_time"])

    with open(file_path, 'w') as file:
        for algorithm, data in sorted_algorithms:
            file.write(f"--------------------------------------\n")
            file.write(f"Results using {algorithm}:\n")
            file.write(f"Average Waiting Time: {data['avg_waiting_time']}\n")
            file.write(f"Input File: {data['input_file']}\n")
            file.write("\n")


def compare_algorithms():
    print("Compare Algorithms")
    num_algorithms = int(input("Enter the number of algorithms to compare: "))

    chosen_algorithms = []
    for i in range(num_algorithms):
        print(f"\nChoose algorithm {i + 1}:")
        scheduling_algorithm, algorithm_type = choose_algorithm()
        if scheduling_algorithm is None:
            return None
        chosen_algorithms.append((scheduling_algorithm, algorithm_type))

    file_name = choose_input_file()
    list_processes = get_processes_from_file(file_name)
    output_file_name = input("Enter the output file name (Example: compare_results.txt): ")
    results = []
    for algorithm, algorithm_type in chosen_algorithms:
        result = algorithm(list_processes)
        avg_turnaroundTime = average_turnaround_time(result)
        avg_waitingTime = average_waiting_time(result)
        results.append((algorithm_type, result, avg_waitingTime, avg_turnaroundTime))

        print(f"\nResult Table {algorithm_type}:")
        print(f"ProcessID\tArrivalTime\tBurstTime\tPriority\tCompletionTime\tTurnaroundTime\tWaitingTime")
        for process in result:
            if hasattr(process, 'priority'):
                print(
                    f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}\t\t\t{process.priority}\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}")
            else:
                print(
                    f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}\t\t\tNo Priority\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}")
    with open(output_file_name, 'a') as file:
        file.write(f"-------------------- {file_name.upper()}--------------------\n")
        file.write(f"Comparing {num_algorithms} algorithms for {file_name}:\n")
        for algorithm_type, _, avg_waitingTime, avg_turnaroundTime in results:
            print(f"------------------------------------\n")
            file.write(f"Algorithm: {algorithm_type}\n")
            print(f"Algorithm: {algorithm_type}\n")
            file.write(f"Average Waiting Time: {avg_waitingTime}\n")
            print(f"Average Waiting Time: {avg_waitingTime}\n")
            file.write(f"Average Turnaround Time: {avg_turnaroundTime}\n")
            print(f"Average Turnaround Time: {avg_turnaroundTime}\n")
            file.write("\n")


# def compare_algorithms():
#     print("Compare Algorithms")
#     num_algorithms = int(input("Enter the number of algorithms to compare: "))
#
#     chosen_algorithms = []
#     for i in range(num_algorithms):
#         print(f"\nChoose algorithm {i + 1}:")
#         scheduling_algorithm, algorithm_type = choose_algorithm()
#         if scheduling_algorithm is None:
#             return None
#         chosen_algorithms.append((scheduling_algorithm, algorithm_type))
#
#     file_name = choose_input_file()
#
#     list_processes = get_processes_from_file(file_name)
#
#     output_file_name = input("Enter the output file name (Example: compare_results.txt): ")
#
#     avg_waiting_times = []
#     avg_turnaround_times = []
#
#     with open(output_file_name, 'a') as output_file:
#         output_file.write(f"Comparison Results for {file_name}:\n")
#
#         for algorithm, algorithm_type in chosen_algorithms:
#             result = algorithm(list_processes)
#             avg_turnaround_time = average_turnaround_time(result)
#             avg_waiting_time = average_waiting_time(result)
#             avg_waiting_times.append(avg_waiting_time)
#             avg_turnaround_times.append(avg_turnaround_time)
#
#             output_file.write(f"\nAlgorithm: {algorithm_type}\n")
#             output_file.write(f"Average Waiting Time: {avg_waiting_time}\n")
#             output_file.write(f"Average Turnaround Time: {avg_turnaround_time}\n")
#
#             print(f"\n{algorithm_type}:")
#             print(f"Average Waiting Time: {avg_waiting_time}")
#             print(f"Average Turnaround Time: {avg_turnaround_time}")
#
#     print(f"Results saved to {output_file_name}")

# ... Rest of the code ...

# def compare_algorithms():
#     print("Compare Algorithms")
#     num_algorithms = int(input("Enter the number of algorithms to compare: "))
#
#     chosen_algorithms = []
#     for i in range(num_algorithms):
#         print(f"\nChoose algorithm {i + 1}:")
#         scheduling_algorithm, algorithm_type = choose_algorithm()
#         if scheduling_algorithm is None:
#             return None
#         chosen_algorithms.append((scheduling_algorithm, algorithm_type))
#
#     file_name = choose_input_file()
#
#     list_processes = get_processes_from_file(file_name)
#
#     for algorithm, algorithm_type in chosen_algorithms:
#         result = algorithm(list_processes)
#         avg_turnaroundTime = average_turnaround_time(result)
#         avg_waitingTime = average_waiting_time(result)
#
#         print(f"\nResult Table {algorithm_type}:")
#         print(f"ProcessID\tArrivalTime\tBurstTime\tPriority\tCompletionTime\tTurnaroundTime\tWaitingTime")
#         for process in result:
#             if hasattr(process, 'priority'):
#                 print(
#                     f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}\t\t\t{process.priority}\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}")
#             else:
#                 print(
#                     f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}\t\t\tNo Priority\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}")
#
#         with open('compare.txt', 'a') as file:
#             file.write(f"Algorithm: {algorithm_type}\n")
#             file.write(f"Average Waiting Time: {avg_waitingTime}\n")
#             file.write(f"Average Turnaround Time: {avg_turnaroundTime}\n\n")
#
#         print(f"\n{algorithm_type}:")
#         print(f"Average Waiting Time: {avg_waitingTime}")
#         print(f"Average Turnaround Time: {avg_turnaroundTime}")

# ... Rest of the code ...

def choose_input_file():
    print("Choose an input file:")
    print("1. input1.txt")
    print("2. input2.txt")
    print("3. input3.txt")
    print("4. input4.txt")
    print("5. input5.txt")
    print("6. input6.txt")
    print("7. input7.txt")
    choice = input("Enter your choice: ")

    if choice == '1':
        return "input1.txt"
    elif choice == '2':
        return "input2.txt"
    elif choice == '3':
        return "input3.txt"
    elif choice == '4':
        return "input4.txt"
    elif choice == '5':
        return "input5.txt"
    elif choice == '6':
        return "input6.txt"
    elif choice == '7':
        return "input7.txt"
    else:
        print("Invalid choice. Using default file input1.txt.")
        return "input1.txt"


def choose_algorithm():
    print("Choose a scheduling algorithm:")
    print("1. FCFS (First Come First Serve)")
    print("2. SJF (Shortest Job First)")
    print("3. RR (Round Robin)")
    print("4. SRTF Preemptive (Shortest Remaining Time First)")
    print("6. Priority Preemptive")
    print("6. Priority Non_Preemptive")
    print("7. Quit")
    choice = input("Enter your choice: ")

    if choice == '1':
        return fcfs, "FCFS (First Come First Serve)"
    elif choice == '2':
        return sjf_non_preemptive, "SJF (Shortest Job First)"
    elif choice == '3':
        time_quantum = int(input("Enter time quantum for Round Robin('example:4'): "))
        return lambda processes: round_robin(processes,
                                             time_quantum), f"RR (Round Robin) with Time Quantum {time_quantum}"
    elif choice == '4':
        return srtf_preemptive, "SRTF Preemptive (Shortest Remaining Time First)"
    elif choice == '5':
        return priority_preemptive, "Priority Preemptive"
    elif choice == '6':
        return priority_non_preemptive, "Priority Non_Preemptive"
    elif choice == '7':
        return None, None
    else:
        print("Invalid choice. Using default Priority Preemptive.")
        return fcfs, "Priority Preemptive"


def get_input_files_from_directory(directory_path):
    input_files = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # Chỉ xem xét các file có đuôi là .txt
            input_files.append(os.path.join("", file_name))
    return input_files


# Sử dụng hàm get_input_files_from_directory để lấy danh sách các file input từ một thư mục cụ thể
directory_path = "C:/Users/ADMIN/PycharmProjects/pythonCPU"
input_files = get_input_files_from_directory(directory_path)

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")

def main():
    while True:
        print("\nCPU SCHEDULING ALGORITHM:")
        print("1. Run a Single Algorithm")
        print("2. Compare Algorithms")
        print("3. Display file")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            scheduling_algorithm, algorithm_type = choose_algorithm()
            if scheduling_algorithm is not None:
                file_name = choose_input_file()
                list_processes = get_processes_from_file(file_name)
                result = scheduling_algorithm(list_processes)
                avg_turnaroundTime = average_turnaround_time(list_processes)
                avg_waitingTime = average_waiting_time(list_processes)
                print(f"\nResult Table {algorithm_type}:")
                print(f"ProcessID\tArrivalTime\tBurstTime\tPriority\tCompletionTime\tTurnaroundTime\tWaitingTime")
                for process in result:
                    if hasattr(process, 'priority'):
                        print(
                            f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}\t\t\t{process.priority}\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}")
                    else:
                        print(
                            f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}\t\t\tNo Priority\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}")
                print(f"\nAverage Waiting Time: {avg_waitingTime}")
                print(f"Average Turnaround Time: {avg_turnaroundTime}")
                print("\nGantt Chart: \n")
                gantt_chart = generate_gantt_chart(result)
                print(gantt_chart)
                print(
                    "\n--------------------------------------------------------------------------------------------------\n")
                output_file = "output.txt"
                write_results_to_file(output_file, avg_waitingTime, avg_turnaroundTime, file_name, algorithm_type)
                sort_output_file(output_file)

        elif choice == '2':
            compare_algorithms()
        elif choice == '3':
            # break
            print("All Files in the Directory:")
            for file_path in input_files:
                print(file_path)
            print("-------------------")
            file_name = input("Open Files name : ")
            read_file(file_name)
        elif choice == '4':
            print("Goodbye 😊😊")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
