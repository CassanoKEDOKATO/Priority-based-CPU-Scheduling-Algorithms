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
    queue = []
    processed_processes = []
    curr_time = 0

    while processes or queue:
        while processes and processes[0].arrival_time <= curr_time:
            queue.append(processes.pop(0))

        if queue:
            process = queue.pop(0)
            if process.remaining_time <= time_quantum:
                curr_time += process.remaining_time
                process.remaining_time = 0
                process.completion_time = curr_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                processed_processes.append(process)
            else:
                curr_time += time_quantum
                process.remaining_time -= time_quantum
                queue.append(process)

        else:
            curr_time += 1

    return processed_processes

def average_turnaround_time(processes):
    return sum(process.turnaround_time for process in processes) / len(processes)


def average_waiting_time(processes):
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
            process_id, arrival_time, burst_time, priority = map(int, process_data)
            process = Process(process_id, arrival_time, burst_time, priority)
            processes.append(process)
    return processes

def write_results_to_file(file_path, results, avg_waitingTime, avg_turnaroundTime,input_file,algorithm_type):
    gantt_chart = generate_gantt_chart(results)
    with open(file_path, 'a') as file:
        file.write(f"\nResults for {input_file} using {algorithm_type}:\n")
        file.write("\n.\n")
        file.write(f"ProcessID\tArrivalTime\tBurstTime\tPriority\tCompletionTime\tTurnaroundTime\tWaitingTime\n")
        for process in results:
            file.write(f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}\t\t\t{process.priority}\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}\n")

        file.write(f"\nAverage Waiting Time: {avg_waitingTime}\n")
        file.write(f"Average Turnaround Time: {avg_turnaroundTime}\n")
        # print("\nGantt Chart:\n")
        # print(gantt_chart)
        file.write(f"\nGantt Chart: \n")
        file.write(f"\n {gantt_chart} \n")
        file.write(f"\n--------------------------------------------------------------------------------------------------\n")
def choose_input_file():
    print("Choose an input file:")
    print("1. input1.txt")
    print("2. input2.txt")
    print("3. process3.txt")
    print("4. non_preemptive_process.txt")
    print("5. preemptive_process.txt")
    choice = input("Enter your choice: ")

    if choice == '1':
        return "input1.txt"
    elif choice == '2':
        return "input2.txt"
    elif choice == '3':
        return "process3.txt"
    elif choice == '4':
        return "non_preemptive_process.txt"
    elif choice == '5':
        return "preemptive_process.txt"
    else:
        print("Invalid choice. Using default file input1.txt.")
        return "input1.txt"
def main():
    while True:
        print("Choose a scheduling algorithm:")
        print("1. Priority Preemptive")
        print("2. Priority Non Preemptive")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            file_name = choose_input_file()
            scheduling_algorithm = priority_preemptive
            algorithm_type = "Priority Preemptive"
        elif choice == '2':
            file_name = choose_input_file()
            scheduling_algorithm = priority_non_preemptive
            algorithm_type = "Priority Non Preemptive"
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        list_processes = get_processes_from_file(file_name)

        result = scheduling_algorithm(list_processes)
        avg_turnaroundTime = average_turnaround_time(list_processes)
        avg_waitingTime = average_waiting_time(list_processes)
        print("\nResult Table " f"{algorithm_type}" ":")
        print(f"ProcessID\tArrivalTime\tBurstTime\tPriority\tCompletionTime\tTurnaroundTime\tWaitingTime")
        for process in result:
            print(
                f"{process.process_id}\t\t\t{process.arrival_time}\t\t\t{process.burst_time}\t\t\t{process.priority}\t\t\t{process.completion_time}\t\t\t\t{process.turnaround_time}\t\t\t\t{process.waiting_time}")

        print(f"\nAverage Waiting Time: {avg_waitingTime}")
        print(f"Average Turnaround Time: {avg_turnaroundTime}")
        print("\nGantt Chart: \n")
        gantt_chart = generate_gantt_chart(result)
        print(gantt_chart)
        print("\n--------------------------------------------------------------------------------------------------\n")
        output_file = "output.txt"
        write_results_to_file(output_file, result, avg_waitingTime, avg_turnaroundTime, file_name, algorithm_type)

# Call the main function
main()