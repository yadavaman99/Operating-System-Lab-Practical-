import os
def main():
    commands = ["ls", "pwd", "whoami"]

    N = len(commands)
    for i in range(N):
        pid = os.fork()
        if pid == 0:
            print(f"child {i+1}: PID={os.getpid()}, executing {commands[i]}")
            # Child process
            os.execlp(commands[i], [commands[i]])
            
    for _ in range(N):
        os.wait()

if __name__ == "__main__":
    main()