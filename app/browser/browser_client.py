from playwright.sync_api import sync_playwright


class BrowserClient:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.console_errors = []
        self.page_errors = []

    def open(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

        self.page.on(
            "console",
            lambda message: self.console_errors.append(message.text)
            if message.type == "error"
            else None,
        )
        self.page.on(
            "pageerror",
            lambda error: self.page_errors.append(str(error)),
        )

        return self

    def navigate(self, url):
        return self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=20000,
        )

    def get_title(self):
        return self.page.title()

    def get_body_text(self):
        return self.page.locator("body").inner_text()

    def take_screenshot(self, path):
        self.page.screenshot(path=path, full_page=True)

    def close(self):
        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()
