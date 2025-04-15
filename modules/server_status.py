import requests

def get_server_status(target):
    try:
        api_url = f"https://api.mcsrvstat.us/2/{target}"
        response = requests.get(api_url)
        data = response.json()
        
        if data.get("online", False):
            return {
                "status": "Online",
                "version": data.get("version", "Unknown"),
                "players": f"{data.get('players', {}).get('online', 0)}/{data.get('players', {}).get('max', 0)}",
                "motd": data.get("motd", {}).get("clean", ["No MOTD"])[0]
            }
        return {"status": "Offline"}
    except Exception as e:
        return {"status": "Error", "error": str(e)}