# ============================================================
#  WEEK 12 LAB — Q1: SCANNER INHERITANCE
#  COMP2152 — Pusala Raghuram Badavath
# ============================================================

import socket
import urllib.request


class Scanner:
    """Parent class — shared by all scanner types."""

    def _init_(self, target):
        self.target = target
        self.results = []

    # TODO: Write display_results(self)
    #   Print "Results for {self.target}:"
    #   If self.results is empty: print "  (no results)"
    #   Otherwise: print each result with "  " indent
    def display_results(self):
        print(f"Results for {self.target}:")
        if not self.results:
            print("  (no results)")
        else:
            for result in self.results:
                print(f"  {result}")


class PortScanner(Scanner):
    """Child class — scans for open ports."""

    # TODO: Write _init_(self, target, ports)
    #   Call the parent constructor: super()._init_(target)
    #   Store self.ports (a list of port numbers)
    def _init_(self, target, ports):
        super()._init_(target)
        self.ports = ports

    # TODO: Write scan(self)
    #   Loop through self.ports
    #   For each port:
    #     Create a socket, set timeout to 1, use connect_ex
    #     If result == 0: append f"Port {port}: OPEN" to self.results
    #     Else: append f"Port {port}: closed" to self.results
    #     Close the socket
    def scan(self):
        for port in self.ports:
            # Note: We create a NEW socket for each port to avoid state issues
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                self.results.append(f"Port {port}: OPEN")
            else:
                self.results.append(f"Port {port}: closed")
            sock.close()


class HTTPScanner(Scanner):
    """Child class — scans HTTP paths for accessible pages."""

    # TODO: Write _init_(self, target, paths)
    #   Call the parent constructor: super()._init_(target)
    #   Store self.paths (a list of URL paths like "/", "/admin")
    def _init_(self, target, paths):
        super()._init_(target)
        self.paths = paths

    # TODO: Write scan(self)
    #   Loop through self.paths
    #   For each path:
    #     Try: urllib.request.urlopen(f"http://{self.target}{path}")
    #       Append f"{path} → {response.status} (accessible)" to self.results
    #     Except: Append f"{path} → NOT FOUND" to self.results
    def scan(self):
        for path in self.paths:
            try:
                # Constructing the full URL
                url = f"http://{self.target}{path}"
                with urllib.request.urlopen(url) as response:
                    # Using status for standard response codes
                    self.results.append(f"{path} → {response.status} (accessible)")
            except Exception:
                self.results.append(f"{path} → NOT FOUND")


# --- Main (provided) ---
if _name_ == "_main_":
    print("=" * 60)
    print("  Q1: SCANNER INHERITANCE")
    print("=" * 60)

    print("\n--- Port Scanner ---")
    ps = PortScanner("127.0.0.1", [22, 80, 443])
    print(f"  Scanning {ps.target} ports...")
    ps.scan()
    ps.display_results()

    print("\n--- HTTP Scanner ---")
    hs = HTTPScanner("127.0.0.1", ["/", "/admin", "/.git/config"])
    print(f"  Scanning {hs.target} paths...")
    hs.scan()
    hs.display_results()

    print("\n" + "=" * 60)