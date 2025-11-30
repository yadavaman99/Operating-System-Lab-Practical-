#!/usr/bin/env python3
# round_robin.py - Round Robin Scheduling

def read_processes():
    n = int(input("Number of processes: ").strip())
    quantum = int(input("Enter time quantum: ").strip())
    procs = []
    for i in range(n):
        default_name = f"P{i+1}"
        line = input(f"Process {i+1} (name arrival burst) [e.g. {default_name} 0 5]: ").strip()
        parts = line.split()
        name = parts[0] if len(parts) >= 1 else default_name
        at = int(parts[1]) if len(parts) >= 2 else 0
        bt = int(parts[2]) if len(parts) >= 3 else 0
        procs.append({"name": name, "arrival": at, "burst": bt, "remaining": bt})
    return procs, quantum

def round_robin(procs, quantum):
    time = 0
    queue = []
    completed = []
    procs = sorted(procs, key=lambda p: p["arrival"])
    while procs or queue:
        # add processes that have arrived
        while procs and procs[0]["arrival"] <= time:
            queue.append(procs.pop(0))
        if not queue:
            time = procs[0]["arrival"]
            continue
        p = queue.pop(0)
        if "start" not in p:
            p["start"] = time
        run_time = min(p["remaining"], quantum)
        p["remaining"] -= run_time
        time += run_time
        # add new arrivals during this slice
        while procs and procs[0]["arrival"] <= time:
            queue.append(procs.pop(0))
        if p["remaining"] > 0:
            queue.append(p)
        else:
            p["completion"] = time
            p["turnaround"] = p["completion"] - p["arrival"]
            p["waiting"] = p["turnaround"] - p["burst"]
            completed.append(p)
    return completed

def print_table(procs):
    print("\n{:<8} {:<8} {:<8} {:<12} {:<8}".format(
        "Process","Arrival","Burst","Completion","Waiting"))
    for p in procs:
        print("{:<8} {:<8} {:<8} {:<12} {:<8}".format(
            p["name"], p["arrival"], p["burst"], p["completion"], p["waiting"]))
    avg_wait = sum(p["waiting"] for p in procs)/len(procs)
    avg_turn = sum(p["turnaround"] for p in procs)/len(procs)
    print(f"\nAverage waiting time: {avg_wait:.2f}")
    print(f"Average turnaround time: {avg_turn:.2f}")

if __name__ == "__main__":
    procs, q = read_processes()
    res = round_robin(procs, q)
    print_table(res)
