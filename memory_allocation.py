#!/usr/bin/env python3
# memory_allocation.py
# Simulate First Fit, Best Fit, and Worst Fit memory allocation strategies

def first_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i in range(len(processes)):
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                allocation[i] = j
                blocks[j] -= processes[i]
                break
    return allocation

def best_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i in range(len(processes)):
        best_index = -1
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                if best_index == -1 or blocks[j] < blocks[best_index]:
                    best_index = j
        if best_index != -1:
            allocation[i] = best_index
            blocks[best_index] -= processes[i]
    return allocation

def worst_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i in range(len(processes)):
        worst_index = -1
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                if worst_index == -1 or blocks[j] > blocks[worst_index]:
                    worst_index = j
        if worst_index != -1:
            allocation[i] = worst_index
            blocks[worst_index] -= processes[i]
    return allocation

def display_result(strategy_name, allocation, processes):
    print(f"\n{strategy_name} Allocation Result:")
    print("{:<12}{:<12}{:<12}".format("Process", "Size", "Block No."))
    for i in range(len(processes)):
        if allocation[i] != -1:
            print("{:<12}{:<12}{:<12}".format(f"P{i+1}", processes[i], allocation[i]+1))
        else:
            print("{:<12}{:<12}{:<12}".format(f"P{i+1}", processes[i], "Not Allocated"))

if __name__ == "__main__":
    # Input memory blocks and process sizes
    n_blocks = int(input("Enter number of memory blocks: "))
    blocks = [int(input(f"Block {i+1} size: ")) for i in range(n_blocks)]

    n_processes = int(input("\nEnter number of processes: "))
    processes = [int(input(f"Process {i+1} size: ")) for i in range(n_processes)]

    # Copy of blocks for each strategy
    ff_allocation = first_fit(blocks.copy(), processes)
    bf_allocation = best_fit(blocks.copy(), processes)
    wf_allocation = worst_fit(blocks.copy(), processes)

    # Display results
    display_result("First Fit", ff_allocation, processes)
    display_result("Best Fit", bf_allocation, processes)
