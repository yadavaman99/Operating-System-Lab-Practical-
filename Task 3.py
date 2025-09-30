import os
import sys 

def create_zombie():
    pid = os.fork()
    if pid == 0:
        # Child process
        print(f" Zombie Child process (PID: {os.getpid()}) is exiting.")
        os._exit(0)
    else:
        print(f"Parent PID={os.getpid()}, not waiting for Child PID={pid}.")
        time.sleep(10)
    
def create_orphan():
    pid = os.fork()
    if pid == 0:
        time.sleep(5)
        print(f" Orphan Child: PID={os.getpid()}, new Parent PID={os.getppid()}")
        os._exit(0)
    else:
        print(f"Parent PID={os.getpid()}, exiting immediately.")
        os._exit(0)

if __name__ == "__main__":
    print("Creating a Zombie process...")
    create_zombie()
    time.sleep(2)
    print(f"\nCreating an Orphan process...")
    create_orphan