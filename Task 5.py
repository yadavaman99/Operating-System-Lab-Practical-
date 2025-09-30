import os
import time

def cpu_intensive_task():
    count = 0
    for i in range(10**7):
        count += i
    print(f"process PID={os.getpid()} finished counting.")

def main():
    nice_values = [o, 5, 10]
    children_pids = []

    for nice_val in nice_values:
        pid = os.fork()
        if pid == 0:
            os.nice(nice_val)
            print(f"Child PID={os.getpid()} with nice value {nice_val} started.")
            cpu_intensive_task()
            os._exit(0)
        else:
            children_pids.append(pid)
    
    for _ in children_pids:
        os.wait()

if __name__ == "__main__":
    main()