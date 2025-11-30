#!/usr/bin/env python3
# priority_scheduling.py
# Priority Scheduling (non-preemptive and preemptive)
# Usage: interactive input. Lower priority value => higher priority.

from copy import deepcopy

def read_processes():
    n = int(input("Number of processes: ").strip())
    procs = []
    for i in range(n):
        default_name = f"P{i+1}"
        line = input(f"Process {i+1} (name arrival burst priority) [e.g. {default_name} 0 5 2]: ").strip()
        parts = line.split()
        name = parts[0] if len(parts) >= 1 and parts[0] != "-" else default_name
        at = int(parts[1]) if len(parts) >= 2 else 0
        bt = int(parts[2]) if len(parts) >= 3 else 0
        pr = int(parts[3]) if len(parts) >= 4 else 0
        procs.append({
            "name": name,
            "arrival": at,
            "burst": bt,
            "priority": pr,
            # runtime fields
            "remaining": bt,
            "start": None,
            "completion": None,
            "waiting": None,
            "turnaround": None,
            "done": False
        })
    return procs

def print_table(procs):
    print("\n{:<8} {:<8} {:<8} {:<9} {:<9} {:<11} {:<8}".format(
        "Process","Arrival","Burst","Priority","Start","Completion","Waiting"))
    for p in procs:
        print("{:<8} {:<8} {:<8} {:<9} {:<9} {:<11} {:<8}".format(
            p["name"], p["arrival"], p["burst"], p["priority"],
            p.get("start","-"), p.get("completion","-"), p.get("waiting","-")))
    avg_wait = sum(p["waiting"] for p in procs)/len(procs)
    avg_turn = sum(p["turnaround"] for p in procs)/len(procs)
    print(f"\nAverage waiting time: {avg_wait:.2f}")
    print(f"Average turnaround time: {avg_turn:.2f}")

def non_preemptive_priority(procs):
    procs = sorted(procs, key=lambda x: (x["arrival"], x["priority"], x["burst"], x["name"]))
    time = 0
    completed = []
    remaining = deepcopy(procs)
    while remaining:
        available = [p for p in remaining if p["arrival"] <= time]
        if not available:
            # advance time to next arrival
            time = remaining[0]["arrival"]
            continue
        # select process with highest priority (lowest priority value)
        current = min(available, key=lambda x: (x["priority"], x["arrival"], x["burst"], x["name"]))
        current["start"] = max(time, current["arrival"])
        current["completion"] = current["start"] + current["burst"]
        current["turnaround"] = current["completion"] - current["arrival"]
        current["waiting"] = current["start"] - current["arrival"]
        time = current["completion"]
        completed.append(current)
        remaining.remove(current)
    # return in order of start times for neat output
    return sorted(completed, key=lambda x: x["start"])

def preemptive_priority(procs):
    # preemptive: treat it like time-driven simulation, always pick available with highest priority
    procs = sorted(procs, key=lambda x: (x["arrival"], x["priority"], x["burst"], x["name"]))
    n = len(procs)
    time = 0
    completed_count = 0
    result = []
    # copy remaining times
    for p in procs:
        p["remaining"] = p["burst"]
        p["done"] = False
        p["start"] = None
    while completed_count < n:
        # pick available processes
        available = [p for p in procs if p["arrival"] <= time and not p["done"] and p["remaining"] > 0]
        if not available:
            # no process ready; jump to next arrival
            future = [p["arrival"] for p in procs if not p["done"] and p["arrival"] > time]
            if future:
                time = min(future)
                continue
            else:
                break
        # choose highest priority among available (lowest priority number)
        current = min(available, key=lambda x: (x["priority"], x["arrival"], x["remaining"], x["name"]))
        if current["start"] is None:
            current["start"] = time
        # execute for 1 time unit (granular simulation)
        time += 1
        current["remaining"] -= 1
        # if completed
        if current["remaining"] == 0:
            current["completion"] = time
            current["turnaround"] = current["completion"] - current["arrival"]
            current["waiting"] = current["turnaround"] - current["burst"]
            current["done"] = True
            completed_count += 1
            result.append(current)
        # loop continues and a higher priority process may preempt next iteration
    # sort result by completion or start for neat printing
    return sorted(result, key=lambda x: (x.get("start", 0), x["name"]))
