import yaml
import requests
import time
import sys
import urllib.parse
from collections import defaultdict

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Extract hostname without port
def get_domain(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.hostname

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    try:
        start = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=0.5)
        elapsed_ms = (time.time() - start) * 1000

        if 200 <= response.status_code < 300 and elapsed_ms <= 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            domain = get_domain(endpoint["url"])
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        print("\nAvailability Report:")
        for domain, stats in domain_stats.items():
            availability = int((stats["up"] / stats["total"]) * 100)
            print(f"{domain} has {availability}% availability")

        print("-" * 40)
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")