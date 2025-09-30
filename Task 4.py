import os 

def main():
    pid = input("enter PID to inspect: ")
    status_file = f"/proc/{pid}/status"
    exe_file = f"/proc/{pid}/exe"
    fd_file = f"/proc/{pid}/fd"

    try:
        with open(status_file) as f:
            for line in f:
                if line.startswith(("name", "state", "VmRSS"));
                    print(line.strip())

        exe_path = os.readlink(exe_file)
        print(f"Executable Path: {exe_path}")

        fds = os.listdir(fd_folder)
        print(f"open file description: {fds}")

    except FileNotFoundError:   
        print(f"no process with PID {pid}")

if __name__ == "__main__":
    main()