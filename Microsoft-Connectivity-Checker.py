"""
Microsoft Update Connectivity Checker

Tests DNS resolution and port connectivity (80, 443) for Microsoft Update domains.
Useful for diagnosing network connectivity issues in corporate environments.

Usage:
    python connectivity_checker.py [options]
    
Options:
    -d, --domains DOMAIN    Add custom domain to test (can be used multiple times)
    -t, --timeout SECONDS   Connection timeout in seconds (default: 3)
    -v, --verbose          Show detailed output
    -q, --quiet            Show only failed connections
    -h, --help             Show this help message

Exit codes:
    0 - All connections successful
    1 - Some connections failed
    2 - All connections failed
"""

import socket
import sys
import argparse

# Default Microsoft Update hostnames
DEFAULT_DOMAINS = [
    "windowsupdate.microsoft.com",
    "update.microsoft.com", 
    "dl.delivery.mp.microsoft.com",
    "sls.update.microsoft.com",
    "fe2.update.microsoft.com",
    "download.windowsupdate.com"
]

class ConnectivityChecker:
    def __init__(self, timeout=3, verbose=False, quiet=False):
        self.timeout = timeout
        self.verbose = verbose
        self.quiet = quiet
        self.total_domains = 0
        self.failed_domains = 0
        self.dns_failures = 0
    
    def check_domain(self, domain):
        """Check DNS resolution and port connectivity for a domain."""
        self.total_domains += 1
        
        try:
            _, _, ip_list = socket.gethostbyname_ex(domain)
        except socket.gaierror as e:
            self.dns_failures += 1
            self.failed_domains += 1
            if not self.quiet:
                print(f"[✗] {domain:<35} DNS FAIL: {e}")
            return False
        
        # Check port connectivity for each IP
        port_results = []
        has_failed_port = False
        
        for ip in ip_list:
            ip_ports = []
            for port in (80, 443):
                try:
                    sock = socket.create_connection((ip, port), timeout=self.timeout)
                    sock.close()
                    ip_ports.append(f"✓{port}")
                    if self.verbose:
                        print(f"    Connected to {ip}:{port}")
                except Exception as e:
                    ip_ports.append(f"✗{port}")
                    has_failed_port = True
                    if self.verbose:
                        print(f"    Failed to connect to {ip}:{port} - {e}")
            
            port_results.append(f"{ip}:[{','.join(ip_ports)}]")
        
        if has_failed_port:
            self.failed_domains += 1
        
        # Output logic based on verbosity settings
        status = "!" if has_failed_port else "✓"
        result_line = f"[{status}] {domain:<35} {' | '.join(port_results)}"
        
        if self.quiet:
            # Only show failed connections in quiet mode
            if has_failed_port:
                print(result_line)
        else:
            print(result_line)
        
        return not has_failed_port
    
    def run_checks(self, domains):
        """Run connectivity checks on all domains."""
        if not self.quiet:
            print("\nMicrosoft Update Connectivity Check")
            print("-" * 50)
        
        success_count = 0
        for domain in domains:
            if self.check_domain(domain):
                success_count += 1
        
        if not self.quiet:
            print(f"\nSummary: {success_count}/{self.total_domains} domains fully accessible")
            if self.failed_domains > 0:
                print(f"Issues found: {self.failed_domains} domains with connectivity problems")
            if self.dns_failures > 0:
                print(f"DNS failures: {self.dns_failures} domains")
        
        # Return exit code
        if self.dns_failures == self.total_domains:
            return 2  # All failed
        elif self.failed_domains > 0:
            return 1  # Some failed
        else:
            return 0  # All successful

def main():
    parser = argparse.ArgumentParser(
        description="Test connectivity to Microsoft Update domains",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python connectivity_checker.py
  python connectivity_checker.py -v
  python connectivity_checker.py -d google.com -d github.com
  python connectivity_checker.py -t 5 -q
        """
    )
    
    parser.add_argument(
        '-d', '--domains', 
        action='append', 
        help='Add custom domain to test (can be used multiple times)'
    )
    parser.add_argument(
        '-t', '--timeout', 
        type=int, 
        default=3,
        help='Connection timeout in seconds (default: 3)'
    )
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true',
        help='Show detailed connection attempts'
    )
    parser.add_argument(
        '-q', '--quiet', 
        action='store_true',
        help='Show only failed connections'
    )
    
    args = parser.parse_args()
    
    # Prepare domain list
    domains = DEFAULT_DOMAINS.copy()
    if args.domains:
        domains.extend(args.domains)
    
    # Validate arguments
    if args.timeout <= 0:
        print("Error: Timeout must be positive", file=sys.stderr)
        return 2
    
    if args.verbose and args.quiet:
        print("Error: Cannot use both --verbose and --quiet", file=sys.stderr)
        return 2
    
    # Run the connectivity check
    checker = ConnectivityChecker(
        timeout=args.timeout,
        verbose=args.verbose,
        quiet=args.quiet
    )
    
    try:
        exit_code = checker.run_checks(domains)
        return exit_code
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
