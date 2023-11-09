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


# class ProcessWithoutPriority:
#     def __init__(self, process_id, arrival_time, burst_time):
#         self.process_id = process_id
#         self.arrival_time = arrival_time
#         self.burst_time = burst_time
#         self.completion_time = 0
#         self.waiting_time = 0
#         self.turnaround_time = 0
#         self.remaining_time = burst_time


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
    processes.sort(key=lambda x: (x.burst_time, x.arrival_time))  # Sắp xếp tiến trình theo burst time và thời gian xuất hiện
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
        available_processes = [process for process in lst if process.arrival_time <= currTime and process.remaining_time > 0]
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
                process_id, arrival_time, burst_time, priority = map(int, process_data)
                process = Process(process_id, arrival_time, burst_time, priority)
            elif len(process_data) == 3:
                process_id, arrival_time, burst_time = map(int, process_data)
                process = Process(process_id, arrival_time, burst_time, '' )
            else:
                print(f"Invalid data in line: {line}")
                continue
            processes.append(process)
    return processes


def write_results_to_file(file_path, avg_waitingTime,avg_turnaroundTime, input_file, algorithm_type):
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

# def write_results_to_file(file_path, results, avg_waitingTime, avg_turnaroundTime, input_file, algorithm_type):
#     gantt_chart = generate_gantt_chart(results)
#     with open(file_path, 'a') as file:
#         file.write(f"\nResults for {input_file} using {algorithm_type}:\n")
#         file.write("\n.\n")
#         file.write(f"ProcessID\tArrivalTime\tBurstTime")
#         if isinstance(results[0], ProcessWithPriority):
#             file.write("\tPriority")
#         file.write("\tCompletionTime\tTurnaroundTime\tWaitingTime\n")
#         for process in results:
#             file.write(f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}")
#             if isinstance(process, ProcessWithPriority):
#                 file.write(f"\t\t\t{process.priority}")
#             file.write(f"\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}\n")
#
#         file.write(f"\nAverage Waiting Time: {avg_waitingTime}\n")
#         file.write(f"Average Turnaround Time: {avg_turnaroundTime}\n")
#         file.write(f"\nGantt Chart: \n")
#         file.write(f"\n {gantt_chart} \n")
#         file.write(f"\n--------------------------------------------------------------------------------------------------\n")
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

    with open('compare.txt', 'a') as file:
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
    else:
        print("Invalid choice. Using default file input1.txt.")
        return "input1.txt"
def choose_algorithm():
    print("Choose a scheduling algorithm:")
    print("1. FCFS (First Come First Serve)")
    print("2. SJF (Shortest Job First)")
    print("3. RR (Round Robin)")
    print("4. Priority Preemptive")
    print("5. Priority Non_Preemptive")
    print("6. Quit")

    choice = input("Enter your choice: ")


    if choice == '1':
        return fcfs, "FCFS (First Come First Serve)"
    elif choice == '2':
        return sjf_non_preemptive, "SJF (Shortest Job First)"
    elif choice == '3':
        time_quantum = int(input("Enter time quantum for Round Robin('example:4'): "))
        return lambda processes: round_robin(processes, time_quantum), f"RR (Round Robin) with Time Quantum {time_quantum}"
    elif choice == '4':
        return priority_preemptive, "Priority Preemptive"
    elif choice == '5':
        return priority_non_preemptive, "Priority Non_Preemptive"
    elif choice == '6':
        return None, None
    else:
        print("Invalid choice. Using default Priority Preemptive.")
        return priority_preemptive, "Priority Preemptive"


# Trong hàm main, cập nhật phần sau:

def main():
    while True:
        print("\nMenu:")
        print("1. Run a Single Algorithm")
        print("2. Compare Algorithms")
        print("3. Quit")
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
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()