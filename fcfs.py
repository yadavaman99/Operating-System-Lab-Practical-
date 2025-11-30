#!/usr/bin/env python3
# fcfs.py - First Come First Serve Scheduling

def read_processes():
    n = int(input("Number of processes: ").strip())
    procs = []
    for i in range(n):
        default_name = f"P{i+1}"
        line = input(f"Process {i+1} (name arrival burst) [e.g. {default_name} 0 5]: ").strip()
        parts = line.split()
        name = parts[0] if len(parts) >= 1 else default_name
        at = int(parts[1]) if len(parts) >= 2 else 0
        bt = int(parts[2]) if len(parts) >= 3 else 0
        procs.append({"name": name, "arrival": at, "burst": bt})
    return procs

def fcfs(procs):
    # sort by arrival time
    procs = sorted(procs, key=lambda p: p["arrival"])
    time = 0
    for p in procs:
        if time < p["arrival"]:
            time = p["arrival"]
        p["start"] = time
        p["completion"] = time + p["burst"]
        p["turnaround"] = p["completion"] - p["arrival"]
        p["waiting"] = p["start"] - p["arrival"]
        time = p["completion"]
    return procs

def print_table(procs):
    print("\n{:<8} {:<8} {:<8} {:<8} {:<12} {:<8}".format(
        "Process","Arrival","Burst","Start","Completion","Waiting"))
    for p in procs:
        print("{:<8} {:<8} {:<8} {:<8} {:<12} {:<8}".format(
            p["name"], p["arrival"], p["burst"], p["start"], p["completion"], p["waiting"]))
    avg_wait = sum(p["waiting"] for p in procs)/len(procs)
    avg_turn = sum(p["turnaround"] for p in procs)/len(procs)
    print(f"\nAverage waiting time: {avg_wait:.2f}")
    print(f"Average turnaround time: {avg_turn:.2f}")

if __name__ == "__main__":
    procs = read_processes()
    res = fcfs(procs)
    print_table(res)
