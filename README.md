# 🎮 IntelBroker - Minecraft Server Intelligence Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red.svg">
</p>

## 📖 About

IntelBroker is a powerful Minecraft server intelligence gathering tool that provides comprehensive information about any Minecraft server. Created by ImsCruz, this tool helps server administrators, security researchers, and players gather detailed information about Minecraft servers.

## ✨ Features

- 🔍 Server Status Monitoring
- 🌐 DNS Information Gathering
- 🔒 Security Analysis
- 📊 Performance Metrics
- 📱 Social Media Presence Detection
- 🕒 Uptime Tracking
- 📜 Historical Data (Wayback Machine)
- 🔐 SSL Certificate Analysis
- 📋 WHOIS Information
- 🔍 Forum Mentions Tracking

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/imscruz/intelbroker.git
cd intelbroker
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the tool:
```bash
python intelbroker.py
```

## 📋 Output
The tool generates a detailed report in ip_intel.txt containing:

- Server status and version
- Player count and capacity
- DNS records
- Security analysis
- Social media presence
- Historical data
- SSL certificate details
- WHOIS information
- Forum mentions
- And more!

## 🤝 Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Trae AI
Used 1 Reference

I'll help you enhance the code with those features and add a nice interface. Here's the improved version:

```python
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

init()

BANNER = f"""{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║ ╦┌┐┌┌┬┐┌─┐┬  ╔╗ ┬─┐┌─┐┬┌─┌─┐┬─┐                            ║
║ ║│││ │ ├┤ │  ╠╩╗├┬┘│ │├┴┐├┤ ├┬┘                            ║
║ ╩┘└┘ ┴ └─┘┴─┘╚═╝┴└─└─┘┴ ┴└─┘┴└─                            ║
║                                                              ║
║           Minecraft Server Intelligence Gatherer             ║
║                    Made by ImsCruz 🚀                        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""

class MCServerIntel:
    def __init__(self, target):
        self.target = target
        self.results = []
        self.output_file = "ip_intel.txt"

    def log_status(self, method, status):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status == "starting":
            print(f"{Fore.YELLOW}[{timestamp}] 🔄 {method} is starting...{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[{timestamp}] ✅ {method} completed!{Style.RESET_ALL}")

    def monitor_uptime(self):
        self.log_status("Uptime Monitor", "starting")
        try:
            uptime_data = []
            for _ in range(3):  # Check 3 times with 5 second intervals
                response = requests.get(f"https://api.mcsrvstat.us/2/{self.target}")
                uptime_data.append({
                    "timestamp": datetime.now().isoformat(),
                    "online": response.json().get("online", False)
                })
                time.sleep(5)
            self.results.append(("Server Uptime", uptime_data))
        except Exception as e:
            self.results.append(("Uptime Error", str(e)))
        self.log_status("Uptime Monitor", "finished")

    def check_security(self):
        self.log_status("Security Analysis", "starting")
        try:
            nm = nmap.PortScanner()
            ip = socket.gethostbyname(self.target)
            nm.scan(ip, '20-30000')
            
            security_info = {
                "open_ports": [],
                "services": []
            }
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        security_info["open_ports"].append(port)
                        security_info["services"].append(nm[host][proto][port])
                        
            self.results.append(("Security Analysis", security_info))
        except Exception as e:
            self.results.append(("Security Analysis Error", str(e)))
        self.log_status("Security Analysis", "finished")

    def check_wayback(self):
        self.log_status("Wayback Machine Check", "starting")
        try:
            url = Url(f"https://{self.target}")
            wayback = url.wayback_machine()
            self.results.append(("Wayback History", wayback.near()))
        except Exception as e:
            self.results.append(("Wayback Error", str(e)))
        self.log_status("Wayback Machine Check", "finished")

    def get_social_media(self):
        self.log_status("Social Media Search", "starting")
        platforms = [
            "twitter.com", "facebook.com", "instagram.com", "discord.gg",
            "youtube.com", "reddit.com"
        ]
        social_links = []
        
        for platform in platforms:
            try:
                response = requests.get(
                    f"https://www.google.com/search?q=site:{platform}+{self.target}",
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and platform in href:
                        social_links.append(href)
            except:
                continue
                
        self.results.append(("Social Media", social_links))
        self.log_status("Social Media Search", "finished")

    def get_whois(self):
        self.log_status("WHOIS Lookup", "starting")
        try:
            domain_info = whois.whois(self.target)
            self.results.append(("WHOIS Information", domain_info))
        except Exception as e:
            self.results.append(("WHOIS Error", str(e)))
        self.log_status("WHOIS Lookup", "finished")

    def get_ssl_info(self):
        self.log_status("SSL Certificate Check", "starting")
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=self.target) as s:
                s.connect((self.target, 443))
                cert = s.getpeercert()
                self.results.append(("SSL Certificate", cert))
        except Exception as e:
            self.results.append(("SSL Error", str(e)))
        self.log_status("SSL Certificate Check", "finished")

    def run_analysis(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks = [
                executor.submit(self.get_server_status),
                executor.submit(self.get_dns_info),
                executor.submit(self.search_forums),
                executor.submit(self.check_host_info),
                executor.submit(self.monitor_uptime),
                executor.submit(self.check_security),
                executor.submit(self.check_wayback),
                executor.submit(self.get_social_media),
                executor.submit(self.get_whois),
                executor.submit(self.get_ssl_info)
            ]
        
        self.save_results()

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def main():
    clear_screen()
    print(BANNER)
    
    target = input(f"{Fore.CYAN}[?] Enter target Minecraft server IP/domain: {Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}[+] Starting intelligence gathering for {target}...{Style.RESET_ALL}\n")
    
    intel = MCServerIntel(target)
    intel.run_analysis()
    
    print(f"\n{Fore.GREEN}[+] Intelligence gathering completed! 🎉")
    print(f"[+] Results saved to {intel.output_file} 📁{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
 ```
```

Bu güncellenmiş versiyonda eklenen özellikler:

1. Renkli ve emoji'li terminal arayüzü
2. İlerleme logları
3. Uptime takibi
4. Güvenlik analizi (port taraması)
5. Wayback Machine kontrolü
6. Sosyal medya hesapları taraması
7. WHOIS bilgileri
8. SSL sertifika kontrolü
9. Performans optimizasyonları
Kullanmak için ek kütüphaneler kurmanız gerekiyor:

```bash
pip install colorama python-whois python-nmap waybackpy
 ```
```

Program artık daha profesyonel görünüyor ve daha fazla bilgi topluyor. Tüm işlemler paralel olarak çalışıyor ve ilerlemeler ekranda gösteriliyor.

## Dot Nokta ScruzDot
Copy

Delete

requiremetns dosyası ve readme verirmisin mukemmel bir github readmesi olusturmanı istiyorum

## Trae AI
Used 1 Reference

mc_intel.py 27-27

İşte projeniz için requirements.txt ve README.md dosyaları:

```plaintext
requests>=2.28.0
beautifulsoup4>=4.11.0
dnspython>=2.2.0
colorama>=0.4.5
python-whois>=0.8.0
python-nmap>=0.7.1
waybackpy>=3.0.6
psutil>=5.9.0
 ```

```markdown
# 🎮 IntelBroker - Minecraft Server Intelligence Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red.svg">
</p>

## 📖 About

IntelBroker is a powerful Minecraft server intelligence gathering tool that provides comprehensive information about any Minecraft server. Created by ImsCruz, this tool helps server administrators, security researchers, and players gather detailed information about Minecraft servers.

## ✨ Features

- 🔍 Server Status Monitoring
- 🌐 DNS Information Gathering
- 🔒 Security Analysis
- 📊 Performance Metrics
- 📱 Social Media Presence Detection
- 🕒 Uptime Tracking
- 📜 Historical Data (Wayback Machine)
- 🔐 SSL Certificate Analysis
- 📋 WHOIS Information
- 🔍 Forum Mentions Tracking

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/imscruz/intelbroker.git
cd intelbroker
 ```
```

2. Install required packages:
```bash
pip install -r requirements.txt
 ```

## 💻 Usage
Run the tool using:

```bash
python mc_intel.py
 ```

When prompted, enter the Minecraft server IP or domain name you want to analyze.

## 📋 Output
The tool generates a detailed report in ip_intel.txt containing:

- Server status and version
- Player count and capacity
- DNS records
- Security analysis
- Social media presence
- Historical data
- SSL certificate details
- WHOIS information
- Forum mentions
- And more!
## 🛠️ Requirements
- Python 3.8 or higher
- Internet connection
- Required Python packages (listed in requirements.txt)
## 🔧 Configuration
No additional configuration is needed. The tool works out of the box!

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch ( git checkout -b feature/AmazingFeature )
3. Commit your changes ( git commit -m 'Add some AmazingFeature' )
4. Push to the branch ( git push origin feature/AmazingFeature )
5. Open a Pull Request
## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer
This tool is for educational purposes only. Users are responsible for complying with applicable laws and regulations.

## 👨‍💻 Author
Imscruz
- GitHub: @imscruz

## 📞 Contact
If you have any questions or suggestions, feel free to reach out!

Made with ❤️ by imscruz
