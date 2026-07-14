import httpx
import re

urls = [
    "https://cisco.wd1.myworkdayjobs.com/GlobalCareers",
    "https://flipkart.wd3.myworkdayjobs.com/Flipkart",
    "https://jpmc.wd1.myworkdayjobs.com/Careers"
]

for url in urls:
    print(f"Checking {url}")
    try:
        r = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        match = re.search(r'/wday/cxs/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', r.text)
        if match:
            print(f"  Found endpoint: {match.group(0)}")
        else:
            print("  No endpoint found in HTML")
    except Exception as e:
        print(f"  Error: {e}")
