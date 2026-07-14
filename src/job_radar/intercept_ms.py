from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    def handle_request(request):
        if "api" in request.url or "graphql" in request.url:
            print("API REQUEST:", request.url)
            if request.post_data:
                print("POST DATA:", request.post_data)

    def handle_response(response):
        if "api" in response.url or "graphql" in response.url:
            try:
                if response.status == 200:
                    print("API RESPONSE:", response.url)
                    print("RESPONSE DATA:", response.text()[:300])
            except Exception as e:
                print("Error reading response:", e)

    page.on("request", handle_request)
    page.on("response", handle_response)
    
    print("Navigating...")
    page.goto("https://jobs.careers.microsoft.com/global/en/search?l=en_us&pg=1&pgSz=20&loc=India", wait_until="networkidle")
    print("Done navigating.")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
