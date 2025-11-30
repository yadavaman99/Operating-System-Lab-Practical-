#!/usr/bin/env python3
"""
detect_vm.py - heuristics to detect if running inside a virtual machine.
Checks multiple indicators and prints a best-effort conclusion.
"""
import subprocess
import os

def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True, text=True)
        return out.strip()
    except Exception:
        return ""

def check_systemd_detect_virt():
    if shutil_which("systemd-detect-virt"):
        out = run_cmd("systemd-detect-virt")
        if out and out != "none":
            return True, f"systemd-detect-virt: {out}"
    return False, ""

def shutil_which(cmd):
    from shutil import which
    return which(cmd) is not None

def check_proc_cpuinfo():
    # hypervisor flag present in /proc/cpuinfo often indicates VM
    try:
        with open("/proc/cpuinfo", "r") as f:
            data = f.read()
        if "hypervisor" in data:
            return True, "hypervisor flag in /proc/cpuinfo"
    except Exception:
        pass
    return False, ""

def check_dmi():
    # check DMI strings if available
    dmi_paths = [
        "/sys/class/dmi/id/product_name",
        "/sys/class/dmi/id/sys_vendor",
        "/sys/class/dmi/id/chassis_vendor",
    ]
    found = []
    for p in dmi_paths:
        try:
            with open(p, "r") as f:
                v = f.read().strip().lower()
            if v:
                found.append((p, v))
        except Exception:
            continue
    # common VM signatures
    vm_signatures = ["vmware", "virtualbox", "kvm", "qemu", "microsoft corporation", "virtual", "amazon", "xen", "bochs", "parallels"]
    for path, val in found:
        for sig in vm_signatures:
            if sig in val:
                return True, f"{path} contains '{val}' (matched '{sig}')"
    return False, ""

def check_mac_oui():
    # optional: check MAC addresses for known virtual vendors
    try:
        import re, netifaces
    except Exception:
        return False, ""
    try:
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface).get(netifaces.AF_LINK, [])
            for a in addrs:
                mac = a.get('addr')
                if mac:
                    prefix = mac.replace(":", "").upper()[:6]
                    # simple list of virtual vendor OUIs (not exhaustive)
                    virtual_ouis = {"000C29","000569","001C14","080027","525400"}  # vmware, virtualbox, etc.
                    if prefix in virtual_ouis:
                        return True, f"MAC OUI {prefix} suggests virtual NIC on {iface}"
    except Exception:
        pass
    return False, ""

def main():
    checks = []

    # 1) systemd-detect-virt (best, if available)
    if shutil_which("systemd-detect-virt"):
        out = run_cmd("systemd-detect-virt")
        if out and out != "none":
            print("Detected virtualization via systemd-detect-virt:", out)
            return

    # 2) /proc/cpuinfo hypervisor flag
    ok, reason = check_proc_cpuinfo()
    if ok:
        print("Likely running inside a VM:", reason)
        return

    # 3) DMI strings
    ok, reason = check_dmi()
    if ok:
        print("Likely running inside a VM (DMI):", reason)
        return

    # 4) optional MAC OUI check (requires netifaces)
    ok, reason = check_mac_oui()
    if ok:
        print("Likely running inside a VM (NIC OUI):", reason)
        return

    print("No strong indicators of virtualization found (host might be physical).")
    print("Note: detection is heuristic and may be inconclusive.")

if __name__ == "__main__":
    main()
