import requests

class APIServices:
    @staticmethod
    def get_shodan_info(target):
        try:
            url = f"https://internetdb.shodan.io/{target}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return f"Shodan data not available: {str(e)}"

    @staticmethod
    def get_dns_info(target):
        try:
            url = f"https://dns.google/resolve?name={target}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return f"DNS data not available: {str(e)}"

    @staticmethod
    def get_threat_info(target):
        try:
            url = f"https://urlscan.io/api/v1/search/?q=domain:{target}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return f"Threat data not available: {str(e)}"