import json
from datetime import datetime

def format_output(results, output_file, target):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"""
╔══════════════════════════════════════════════════════════════╗
║           Minecraft Server Intelligence Report               ║
║                    Made by imscruz 🚀                        ║
╚══════════════════════════════════════════════════════════════╝

Target Server: {target}
Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n""")

        for section, data in results:
            f.write(f"📌 {section}\n")
            f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            
            try:
                if isinstance(data, dict):
                    for key, value in data.items():
                        f.write(f"{key}: {value}\n")
                else:
                    f.write(str(data))
            except:
                f.write(str(data))
            
            f.write("\n\n")

        f.write("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 GitHub: https://github.com/imscruz
🔍 IntelBroker v1.0
Generated with ❤️ by ImsCruz
""")