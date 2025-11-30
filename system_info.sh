#!/usr/bin/env bash
# system_info.sh - print system details (some commands may need sudo)

echo "=== uname -a ==="
uname -a
echo

echo "=== lscpu ==="
lscpu
echo

echo "=== free -h ==="
free -h
echo

echo "=== lsblk ==="
lsblk
echo

echo "=== ip addr (show interfaces) ==="
ip -c addr
echo

echo "=== last reboot (uptime) ==="
uptime
echo

# dmidecode may require root privileges; print a short note if not accessible
if command -v dmidecode >/dev/null 2>&1; then
    echo "=== dmidecode -t system (requires sudo) ==="
    if [ "$(id -u)" -eq 0 ]; then
        dmidecode -t system
    else
        echo "dmidecode available but requires sudo. Run: sudo dmidecode -t system"
    fi
else
    echo "dmidecode not installed or not available."
fi

echo
echo "=== lspci (if available) ==="
if command -v lspci >/dev/null 2>&1; then
    lspci | head -n 20
else
    echo "lspci not available"
fi
