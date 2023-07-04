from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = "chromedriverbeta"
CHROMEDRIVER_PATH = ROOT_PATH / "chrome_driver" / CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    # Exclude this line after resolution chrome driver version 103
    # chrome_options.binary_location = r'C:\Users\jackson.milhomens\AppData\Local\Google\Chrome Beta\Application\chrome.exe'

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    chrome = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return chrome


def make_chrome_browser_manager():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--headless")

    chrome = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    return chrome


if __name__ == "__main__":
    pass
