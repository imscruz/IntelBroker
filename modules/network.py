import socket
import dns.resolver
import requests

def get_dns_info(target):
    try:
        ip = socket.gethostbyname(target)
        records = []
        
        for record_type in ['A', 'MX', 'NS', 'TXT']:
            try:
                answers = dns.resolver.resolve(target, record_type)
                for answer in answers:
                    records.append(f"{record_type}: {answer}")
            except:
                continue
                
        return {"IP": ip, "Records": records}
    except Exception as e:
        return {"error": str(e)}

def check_host(target):
    try:
        ip = socket.gethostbyname(target)
        response = requests.get(
            f"http://check-host.net/check-tcp?host={ip}:25565",
            headers={'Accept': 'application/json'},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}