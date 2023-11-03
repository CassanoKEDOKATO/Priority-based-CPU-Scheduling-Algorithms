from collections import deque


class ProcessWithPriority:
    def __init__(self, process_id, arrival_time, burst_time, priority):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = burst_time


class ProcessWithoutPriority:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
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
                process = ProcessWithPriority(process_id, arrival_time, burst_time, priority)
            elif len(process_data) == 3:
                process_id, arrival_time, burst_time = map(int, process_data)
                process = ProcessWithoutPriority(process_id, arrival_time, burst_time)
            else:
                print(f"Invalid data in line: {line}")
                continue
            processes.append(process)
    return processes



def write_results_to_file(file_path, results, avg_waitingTime, avg_turnaroundTime, input_file, algorithm_type):
    gantt_chart = generate_gantt_chart(results)
    with open(file_path, 'a') as file:
        file.write(f"\nResults for {input_file} using {algorithm_type}:\n")
        file.write("\n.\n")
        file.write(f"ProcessID\tArrivalTime\tBurstTime")
        if isinstance(results[0], ProcessWithPriority):
            file.write("\tPriority")
        file.write("\tCompletionTime\tTurnaroundTime\tWaitingTime\n")
        for process in results:
            file.write(f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}")
            if isinstance(process, ProcessWithPriority):
                file.write(f"\t\t\t{process.priority}")
            file.write(f"\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}\n")

        file.write(f"\nAverage Waiting Time: {avg_waitingTime}\n")
        file.write(f"Average Turnaround Time: {avg_turnaroundTime}\n")
        file.write(f"\nGantt Chart: \n")
        file.write(f"\n {gantt_chart} \n")
        file.write(f"\n--------------------------------------------------------------------------------------------------\n")
def choose_input_file():
    print("Choose an input file:")
    print("1. fcfs_process.txt")
    print("2. sjf_process.txt")
    print("3. rr_process.txt")
    print("4. priority_process1.txt")
    print("5. priority_process2.txt")
    choice = input("Enter your choice: ")

    if choice == '1':
        return "fcfs_process.txt"
    elif choice == '2':
        return "sjf_process.txt"
    elif choice == '3':
        return "rr_process.txt"
    elif choice == '4':
        return "priority_process1.txt"
    elif choice == '5':
        return "priority_process2.txt"
    else:
        print("Invalid choice. Using default file input1.txt.")
        return "heheh"
def choose_algorithm():
    print("Choose a scheduling algorithm:")
    print("1. Priority Preemptive")
    print("2. Priority Non Preemptive")
    print("3. FCFS (First Come First Serve)")
    print("4. SJF (Shortest Job First)")
    print("5. RR (Round Robin)")
    print("6. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        return priority_preemptive, "Priority Preemptive"
    elif choice == '2':
        return priority_non_preemptive, "Priority Non Preemptive"
    elif choice == '3':
        return fcfs, "FCFS (First Come First Serve)"
    elif choice == '4':
        return sjf_non_preemptive, "SJF (Shortest Job First)"
    elif choice == '5':
        time_quantum = int(input("Enter time quantum for Round Robin: "))
        return lambda processes: round_robin(processes, time_quantum), f"RR (Round Robin) with Time Quantum {time_quantum}"
    elif choice == '6':
        return None, None
    else:
        print("Invalid choice. Using default Priority Preemptive.")
        return priority_preemptive, "Priority Preemptive"


# Trong hàm main, cập nhật phần sau:

def main():
    while True:
        scheduling_algorithm, algorithm_type = choose_algorithm()
        if scheduling_algorithm is None:
            break

        file_name = choose_input_file()

        list_processes = get_processes_from_file(file_name)

        result = scheduling_algorithm(list_processes)
        avg_turnaroundTime = average_turnaround_time(list_processes)
        avg_waitingTime = average_waiting_time(list_processes)
        print("\nResult Table " f"{algorithm_type}" ":")
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
        print("\n--------------------------------------------------------------------------------------------------\n")
        output_file = "output.txt"
        write_results_to_file(output_file, result, avg_waitingTime, avg_turnaroundTime, file_name, algorithm_type)

# Cuối cùng, gọi hàm main:

if __name__ == "__main__":
    main()