import socket
import ssl
import requests
from datetime import datetime

class Scanner:
    @staticmethod
    def get_historical_data(target):
        try:
            response = requests.get(f"http://archive.org/wayback/available?url={target}")
            data = response.json()
            if data["archived_snapshots"]:
                return f"Site has archive history on Wayback Machine"
            return "No historical data available"
        except Exception as e:
            return f"Historical data not available: {str(e)}"

    @staticmethod
    def scan_ports(target):
        common_ports = [25565, 25575, 80, 443, 8080]
        open_ports = []
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return open_ports

    @staticmethod
    def get_ssl_info(target):
        try:
            context = ssl.create_default_context()
            with context.wrap_socket(socket.socket(), server_hostname=target) as s:
                s.connect((target, 443))
                cert = s.getpeercert()
                return {
                    "issuer": dict(x[0] for x in cert["issuer"]),
                    "expires": cert["notAfter"]
                }
        except:
            return "SSL information not available"