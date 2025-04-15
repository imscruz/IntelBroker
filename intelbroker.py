import requests
import json
import socket
import ssl
import whois
import nmap
import os
import sys
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime
import dns.resolver
import re
from colorama import init, Fore, Style
import platform
from waybackpy import Url
import psutil

# Local modules
from modules.server_status import get_server_status
from modules.network import get_dns_info, check_host
from modules.formatters import format_output  # file işleri haıyrlı işler forfor

init()

BANNER = f"""{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║             ╦┌┐┌┌┬┐┌─┐┬    ╔╗ ┬─┐┌─┐┬┌─┌─┐┬─┐                ║
║             ║│││ │ ├┤ │    ╠╩╗├┬┘│ │├┴┐├┤ ├┬┘                ║
║             ╩┘└┘ ┴ └─┘┴─┘  ╚═╝┴└─└─┘┴ ┴└─┘┴└─                ║
║                                                              ║
║           Minecraft Server Intelligence Gatherer             ║
║                    Made by imscruz 🚀                        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""

class MCServerIntel:
    def __init__(self, target):
        self.target = target
        self.results = []
        self.output_file = "target_IntelBroker.txt"

    def log_status(self, method, status):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status == "starting":
            print(f"{Fore.YELLOW}[{timestamp}] 🔄 {method} is starting...{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[{timestamp}] ✅ {method} completed!{Style.RESET_ALL}")

    def run_analysis(self):
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(get_server_status, self.target): "Server Status",
                    executor.submit(get_dns_info, self.target): "DNS Information",
                    executor.submit(check_host, self.target): "Host Check"
                }

                for future in futures:
                    try:
                        result = future.result(timeout=15)
                        self.results.append((futures[future], result))
                    except Exception as e:
                        print(f"{Fore.YELLOW}[!] {futures[future]} failed: {str(e)}{Style.RESET_ALL}")
                        
        except Exception as e:
            print(f"{Fore.RED}[!] Analysis error: {str(e)}{Style.RESET_ALL}")
        finally:
            self.save_results()

    def save_results(self):
        format_output(self.results, self.output_file, self.target)

def main():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(BANNER)
    
    target = input(f"{Fore.CYAN}[?] Enter target Minecraft server IP/domain: {Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}[+] Starting intelligence gathering for {target}...{Style.RESET_ALL}\n")
    
    intel = MCServerIntel(target)
    intel.run_analysis()
    
    print(f"\n{Fore.GREEN}[+] Intelligence gathering completed! 🎉")
    print(f"[+] Results saved to {intel.output_file} 📁{Style.RESET_ALL}")

if __name__ == "__main__":
    main()