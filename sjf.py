#!/usr/bin/env python3
# sjf.py - Shortest Job First (Non-Preemptive Scheduling)

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

def sjf(procs):
    n = len(procs)
    procs = sorted(procs, key=lambda p: p["arrival"])
    completed = []
    time = 0
    while procs:
        # get all available processes
        available = [p for p in procs if p["arrival"] <= time]
        if not available:
            time = procs[0]["arrival"]
            continue
        # choose process with shortest burst
        p = min(available, key=lambda x: x["burst"])
        procs.remove(p)
        p["start"] = max(time, p["arrival"])
        p["completion"] = p["start"] + p["burst"]
        p["turnaround"] = p["completion"] - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]
        time = p["completion"]
        completed.append(p)
    return completed

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
    res = sjf(procs)
    print_table(res)
