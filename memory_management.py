# memory_management.py
# Lakshita - 2301420008
# Assignment 3: MFT and MVT Memory Management Simulation

def mft(total_memory, partition_size, process_sizes):
    partitions = total_memory // partition_size
    internal_frag = 0
    external_frag = 0
    allocated = 0

    print("\n--- MFT (Multiprogramming with Fixed Tasks) ---")
    print(f"Total Memory: {total_memory} | Partition Size: {partition_size} | Partitions: {partitions}")
    print("\nProcess\tSize\tStatus\t\tFragmentation")

    for i, size in enumerate(process_sizes):
        if allocated < partitions:
            if size > partition_size:
                print(f"P{i+1}\t{size}\tNot Allocated\t(Process too large)")
            else:
                frag = partition_size - size
                internal_frag += frag
                print(f"P{i+1}\t{size}\tAllocated\tInternal Frag = {frag}")
                allocated += 1
        else:
            print(f"P{i+1}\t{size}\tNot Allocated\t(No free partition left)")

    if allocated < len(process_sizes):
        external_frag = total_memory - (partitions * partition_size)

    print(f"\nTotal Internal Fragmentation: {internal_frag}")
    print(f"Total External Fragmentation: {external_frag}\n")


def mvt(total_memory, process_sizes):
    print("\n--- MVT (Multiprogramming with Variable Tasks) ---")
    remaining = total_memory
    allocated = []
    external_frag = 0

    print(f"Total Memory: {total_memory}")
    print("\nProcess\tSize\tStatus\t\tRemaining Memory")

    for i, size in enumerate(process_sizes):
        if size <= remaining:
            allocated.append(size)
            remaining -= size
            print(f"P{i+1}\t{size}\tAllocated\t{remaining}")
        else:
            print(f"P{i+1}\t{size}\tNot Allocated\t(Insufficient memory)")

    external_frag = remaining
    print(f"\nTotal External Fragmentation: {external_frag}\n")


if __name__ == "__main__":
    print("Memory Management Simulation (MFT and MVT)")
    total_memory = int(input("Enter total memory size: "))

    choice = input("Choose (1) MFT or (2) MVT: ")

    if choice == '1':
        partition_size = int(input("Enter partition size: "))
        n = int(input("Enter number of processes: "))
        process_sizes = [int(input(f"Enter size of P{i+1}: ")) for i in range(n)]
        mft(total_memory, partition_size, process_sizes)

    elif choice == '2':
        n = int(input("Enter number of processes: "))
        process_sizes = [int(input(f"Enter size of P{i+1}: ")) for i in range(n)]
        mvt(total_memory, process_sizes)

    else:
        print("Invalid choice. Please choose 1 for MFT or 2 for MVT.")
