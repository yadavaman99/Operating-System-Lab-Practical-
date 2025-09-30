
import os 
import time

def main():
    N = int(input("enter the number of child processes to create: "))
    children_pids = []
 
    for i in range(N):
        pid = os.fork()
        if pid == 0:
            
            print(f"child {i+1}: PID={os.getpid()}, Parent PID={os.getppid()}")
            print(f"child {i+1}: hello from child process!")
            time.sleep(1)
            os._exit(0)
       else:
           children_pids.append(pid)
    

    for _ in children_pids:
        finished_pid, status = os.wait()
        print(f"parent: chaild with PID {finished_pid} finished with status {status}")
 

if __name__ == "__main__":
    main()