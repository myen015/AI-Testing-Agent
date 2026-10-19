import pytest
from app.browser.browser_client import BrowserClient


@pytest.mark.e2e
def test_open_web_page():
    browser = BrowserClient().open()

    try:
        response = browser.navigate("https://example.com")

        # Проверяем HTTP-ответ
        assert response is not None
        assert response.status == 200

        # Проверяем заголовок и содержимое страницы
        assert browser.get_title() == "Example Domain"

        body_text = browser.get_body_text()
        assert "This domain is for use in documentation examples" in body_text

        # Сохраняем скриншот
        browser.take_screenshot("artifacts/screenshots/example_page.png")

        # Проверяем JavaScript-ошибки
        assert not browser.page_errors, (
            f"JavaScript errors found: {browser.page_errors}"
        )

        print("HTTP status:", response.status)
        print("Console errors:", browser.console_errors)
        print("JavaScript errors:", browser.page_errors)

    finally:
        browser.close()
