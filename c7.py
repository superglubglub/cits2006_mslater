import socket
from datetime import datetime

# Common ports for quick scans
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 8080, 8443]

def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                # Attempt to grab banner
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors='ignore').strip()
            except:
                banner = "No banner"
            print(f"[+] Port {port} open - Banner: {banner}")
        sock.close()
    except Exception as e:
        print(f"[-] Error scanning port {port}: {e}")

def run_scan(target, ports=None):
    print(f"[*] Starting scan on {target}")
    print(f"[*] Time: {datetime.now()}")
    print("="*50)

    if ports is None:
        ports = COMMON_PORTS

    for port in ports:
        scan_port(target, port)

    print("="*50)
    print("[*] Scan complete.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python port_scanner.py <target_ip> [port1,port2,...]")
        sys.exit(1)

    target_ip = sys.argv[1]

    if len(sys.argv) == 3:
        port_list = [int(p.strip()) for p in sys.argv[2].split(",")]
    else:
        port_list = None

    run_scan(target_ip, port_list)
