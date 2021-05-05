# Kevin Dawson
# Operating Systems Final Spring 2021
# Python CPU Scheduling Simulator

def getFCFSData(proc, n):

    print("Calculating FCFS")

    wt = [0] * n
    tat = [0] * n
    wt[0] = 0
    order = []

    # gets waiting time for each process.

    for i in range(1, n):
        wt[i] = proc[i - 1][1] + wt[i - 1]

    # gets turn around time for each process.

    for i in range(n):
        tat[i] = proc[i][1] + wt[i]
        order.append((proc[i][0], proc[i][1]))

    # gets response time for each process.
        res_t = wt

        # displays process details.
    displayProcessDetails(proc, n, wt, tat, res_t, order)


def getRRData(proc, n, quantum):

    print("Calculating Round Robin")

    wt = [0] * n
    tat = [0] * n
    rem_bt = [0] * n
    res_t = [0] * n
    order = []

    # gets waiting time of all processes.

    # adds remaining burst times into list.
    for i in range(n):
        rem_bt[i] = proc[i][1]

    t = 0

    while(1):
        done = True

        for i in range(n):

            # check if process has remaining burst time.
            if (rem_bt[i] > 0):
                done = False

                if (rem_bt[i] > quantum):
                    t += quantum
                    order.append((proc[i][0], quantum))

                    # decrease remaining burst time by value of quantum.
                    rem_bt[i] -= quantum

                # if remaining burst time is smaller than quantum, final burst for process.
                else:

                    # increment time by burst time.
                    t += rem_bt[i]
                    order.append((proc[i][0], rem_bt[i]))

                    # waiting time = time - time used by this process.
                    wt[i] = t - proc[i][1]

                    # set remaining burst time for process to 0.
                    rem_bt[i] = 0

        # checks if all processes have no remaining burst time.
        if (done == True):
            break

    # gets turn around time of all processes.

    for i in range(n):
        tat[i] = proc[i][1] + wt[i]

    # gets response time for each process.
    r = 0
    res_t[0] = 0
    for i in range(1, n):
        if proc[i - 1][1] >= quantum:
            r += quantum
            res_t[i] = r
        else:
            r += proc[i - 1][1]
            res_t[i] = r

    # displays chart of all processes and details.
    displayProcessDetails(proc, n, wt, tat, res_t, order)


def getSJFData(proc, n):

    print("Calculating SJF")

    proc = sorted(proc, key=lambda proc: proc[1])

    wt = [0] * n
    tat = [0] * n
    rem_bt = [0] * n
    res_t = [0] * n
    order = []

    # gets waiting time of each process.

    # adds remaining burst times into a list.
    for i in range(n):
        rem_bt[i] = proc[i][1]

    # amount of completed processes.
    complete = 0
    # total time.
    t = 0
    # variables to keep track of process state.
    minimum = 999999999
    short = 0
    check = False

    # checks that all processes have not been completed.
    while (complete != n):

        # finds process with minimum remaining time.
        for j in range(n):
            if ((rem_bt[j] < minimum) and (rem_bt[j] > 0)):
                minimum = rem_bt[j]
                short = j
                check = True

        if (check == False):
            t += 1
            continue

        # reduces time remaining of process.
        rem_bt[short] -= 1

        minimum = rem_bt[short]
        if (minimum == 0):
            minimum = 999999999

        # checks if a process is done executing and increments complete.
        if (rem_bt[short] == 0):
            complete += 1
            check = False
            fint = t + 1

            # gets waiting time.
            wt[short] = (fint - proc[short][1])

            if (wt[short] < 0):
                wt[short] = 0

        # increments total time.
        t += 1

    # gets turn around time of each process.

    for i in range(n):
        tat[i] = proc[i][1] + wt[i]
        order.append((proc[i][0], proc[i][1]))

    # gets response time of each process.

    res_t[0] = 0

    for i in range(1, n):
        res_t[i] = wt[i]

        # displays chart of all processes and details.
    displayProcessDetails(proc, n, wt, tat, res_t, order)


def getPriorityData(proc, n):

    print("Calculating Priority")

    # Sort processes by priority.
    proc = sorted(proc, key=lambda proc: proc[2], reverse=True)

    # create lists for process wait time, turn around time, and response time.
    wt = [0] * n
    tat = [0] * n
    res_t = [0] * n
    order = []

    # gets waiting time of all processes.

    # wait time of first process is 0.
    wt[0] = 0

    # waiting time = burst time + wait time of previous process.
    for i in range(1, n):
        wt[i] = proc[i - 1][1] + wt[i - 1]

    # gets turn around time of all processes.

    for i in range(n):
        tat[i] = proc[i][1] + wt[i]
        order.append((proc[i][0], proc[i][1]))

    # gets response time of all processes.

    res_t[0] = 0

    for i in range(1, n):
        res_t[i] = wt[i]

    # display processes along with all details.
    displayProcessDetails(proc, n, wt, tat, res_t, order)


def displayProcessDetails(proc, n, wt, tat, rt, order):

    total_wait = 0
    total_turnaround = 0
    total_response = 0

    for i in order:
        print("Process", i[0], "ran for", i[1], "seconds.")

    for i in range(n):

        total_wait += wt[i]
        total_turnaround += tat[i]
        total_response += rt[i]

    print("\nAverage Waiting Time: ", (total_wait / n))
    print("Average Turn Around Time: ", total_turnaround / n)
    print("Average Response Time:", total_response / n)
    print("Total CPU Usage = ", max(tat))


def getProcesses():

    processes = []
    max_processes = 10

    amount = int(input("Enter the amount of processes between 3 and 10: \n"))
    if amount < 3:
        print("You need atleast three processes, please try again!")
        getProcesses()
    if amount > max_processes:
        print("You cannot have more than", max_processes, "processes!")
        getProcesses()

    for i in range(1, amount + 1):
        newprocess = []
        print("New process...")
        newprocess.append(i)
        newprocess.append(int(input("Enter the burst time: ")))
        newprocess.append(int(input("Enter the priority: ")))

        processes.append(newprocess)

    quantum = int(input("Enter a time quantum for round robin scheduling: "))

    return processes, quantum


if __name__ == "__main__":

    # processes is a matrix, each node contains [0]: pid, [1]: burst time, [2]: priority.
    # example processes taken from OS HW3.
    proc = getProcesses()
    n = len(proc[0])
    print('\n')

    getFCFSData(proc[0], n)
    print("\n")
    getRRData(proc[0], n, proc[1])
    print("\n")
    getSJFData(proc[0], n)
    print("\n")
    getPriorityData(proc[0], n)
