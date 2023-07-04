try:
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
except ImportError:
    raise

import os
from time import sleep

from dotenv import load_dotenv
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    presence_of_element_located,
    visibility_of_element_located,
)
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.make_chrome_browser import make_chrome_browser_manager

load_dotenv()


class Blip:
    def __init__(
        self,
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD_BLIP"),
    ) -> None:
        self.user = user
        self.password = password
        self.chrome = make_chrome_browser_manager()
        self.wait = self.__crete_web_driver_wait()
        self.login()

    def __crete_web_driver_wait(self):
        return WebDriverWait(driver=self.chrome, timeout=30, poll_frequency=0.5)

    def login(self) -> None:
        self.chrome.get("https://intelbras.blip.ai/application")

        self.wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'input[id="email"]')))

        self.chrome.find_element(By.CSS_SELECTOR, 'input[id="email"]').send_keys(
            self.user
        )
        self.chrome.find_element(By.CSS_SELECTOR, 'input[id="password"]').send_keys(
            self.password
        )
        self.wait.until(
            element_to_be_clickable((By.CSS_SELECTOR, 'button[id="blip-login"]'))
        )
        self.chrome.find_element(By.CSS_SELECTOR, 'button[id="blip-login"]').click()

        self.wait.until(
            visibility_of_element_located(
                (By.CSS_SELECTOR, 'contact-list[class="contact-list"]')
            )
        )

    def share_chatbots(self, users_email: list[str], permission: str) -> None:
        """
        Share chatbots to one or many users

        Set the permission level for sharing chatbots, being necessary to send as parameter "SAC" or "ADMIN"
        """

        id = self.chatbot_id
        list_users: list = []

        for user in users_email:
            if (
                self.chrome.current_url
                != f"https://intelbras.blip.ai/application/detail/{id}/team"
            ):
                self.chrome.get(
                    f"https://intelbras.blip.ai/application/detail/{id}/team"
                )

            self.wait.until_not(
                visibility_of_element_located(
                    (By.CSS_SELECTOR, 'local-loading[class=""]')
                )
            )

            self.wait.until(
                element_to_be_clickable(
                    (By.CSS_SELECTOR, 'bds-button[ng-click="$ctrl.addUser()"]')
                )
            )

            if len(list_users) == 0:
                self.wait.until(
                    element_to_be_clickable(
                        (By.CSS_SELECTOR, 'div[class="row team-cards"]')
                    )
                )

                sleep(1)
                team_cards = self.chrome.find_elements(
                    By.CSS_SELECTOR, 'div[class="row team-cards"] > div'
                )

                for card in team_cards:
                    try:
                        email_member = card.find_element(
                            By.CSS_SELECTOR,
                            'div[class="card-section card-section--no-overflow w-20"]',
                        )
                    except Exception:
                        email_member = card.find_element(
                            By.CSS_SELECTOR,
                            'div[class="card-section card-section--no-overflow w-40"]',
                        )

                    list_users.append(
                        email_member.find_element(By.TAG_NAME, "span").text
                    )

            if user in list_users:
                continue

            self.chrome.find_element(
                By.CSS_SELECTOR, 'bds-button[ng-click="$ctrl.addUser()"]'
            ).click()

            self.chrome.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(
                user
            )
            li = self.chrome.find_elements(By.CSS_SELECTOR, 'ul[class="rz-ticks"] > li')

            match permission:
                case "SAC":
                    permission_number = 1
                    selector = (
                        'button[class="bp-btn bp-btn--bot bp-btn--small bp-btn--arrow"]'
                    )
                case "ADMIN":
                    permission_number = 3
                    selector = 'button[class="bp-btn bp-btn--bot bp-btn--small"]'

            li[permission_number].find_element(
                By.CSS_SELECTOR, 'span[class="rz-tick-legend"]'
            ).click()

            while True:
                button = self.chrome.find_element(
                    By.CSS_SELECTOR,
                    selector,
                )

                if button.get_attribute("disabled"):
                    continue
                else:
                    break

            button.click()

            if permission == "SAC":
                for j in range(1, 12):
                    if j == 2 or j == 6:
                        continue
                    if j == 4 or j == 7 or j == 8:
                        self.chrome.find_element(
                            By.XPATH,
                            f'//*[@id="main-content-area"]/div[2]/div/card/div/div/div[1]/ng-include/form/expandable-list/div/expandable-item[{j}]/div/div[1]/span[2]/item-header/div/span[3]/blip-radio',
                        ).click()
                    else:
                        self.chrome.find_element(
                            By.XPATH,
                            f'//*[@id="main-content-area"]/div[2]/div/card/div/div/div[1]/ng-include/form/expandable-list/div/expandable-item[{j}]/div/div[1]/span[2]/item-header/div/span[2]/blip-radio',
                        ).click()

                self.chrome.find_element(By.TAG_NAME, "html").send_keys(Keys.PAGE_UP)
                self.chrome.find_element(By.TAG_NAME, "html").send_keys(Keys.PAGE_UP)
                self.wait.until(
                    visibility_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            'button[class="bp-btn bp-btn--bot bp-btn--small fr"]',
                        )
                    )
                )
                sleep(2)
                try:
                    self.chrome.find_element(
                        By.CSS_SELECTOR,
                        'button[class="bp-btn bp-btn--bot bp-btn--small fr"]',
                    ).click()
                except ElementClickInterceptedException:
                    input()

            try:
                self.wait.until(
                    visibility_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            'div[class="alert alert-success alert-dismissible"]',
                        )
                    )
                )
            except Exception:
                continue
            else:
                self.wait.until_not(
                    visibility_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            'div[class="alert alert-success alert-dismissible"]',
                        )
                    )
                )

    def change_flow_chatbots(self) -> None:
        """
        Change flow of multiple chatbots

        Send the name of the excel file that has the chatbot id in Blip and Idash

        And the name of the json file that has the updated flow
        """

        id_blip = self.chatbot_id

        self.chrome.get(
            f"https://intelbras.blip.ai/application/detail/{id_blip}/templates/builder/"
        )

        self.wait.until(
            visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'div[class="no-style flex flex-column z-10 builder-icon-button-list"]',
                )
            )
        )

        self.chrome.find_elements(
            By.CSS_SELECTOR, 'bds-button-icon[ng-click="$ctrl.editConfig()"]'
        )[1].click()

        self.wait.until(
            presence_of_element_located(
                (By.CSS_SELECTOR, 'bds-tab-item[label="Versões"]')
            )
        )

        self.chrome.execute_script(
            "arguments[0].open = true;",
            self.chrome.find_element(By.CSS_SELECTOR, 'bds-tab-item[label="Versões"]'),
        )
        self.chrome.execute_script(
            "arguments[0].open = false;",
            self.chrome.find_element(
                By.CSS_SELECTOR, 'bds-tab-item[label="Variáveis"]'
            ),
        )

        self.wait.until(
            visibility_of_element_located((By.CSS_SELECTOR, 'bds-icon[name="upload"]'))
        )

        self.chrome.find_element(
            By.CSS_SELECTOR, 'input[id="flowFileInput"]'
        ).send_keys(r"C:\Users\ja058700\Downloads\emergenciadefechaduras2 (2).json")

        # change_flow(f"{json_file_name}.json", id_bot)

        # upload_flow.send_keys(
        #     rf"C:\Users\ja058700\Downloads\emergenciadefechaduras2 (2).json"
        # )

        self.wait.until(
            element_to_be_clickable((By.CSS_SELECTOR, 'bds-button[type="submit"]'))
        )
        self.chrome.find_element(By.CSS_SELECTOR, 'bds-button[type="submit"]').click()

        self.wait.until_not(
            visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'bds-illustration[name="blip-ballon-white"]',
                )
            )
        )

        self.wait.until(
            visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'div[class="no-style flex flex-column z-10 builder-icon-button-list"]',
                )
            )
        )
        self.wait.until(
            visibility_of_element_located(
                (By.CSS_SELECTOR, 'bds-button-icon[icon="builder-publish-bot"]')
            )
        )
        self.wait.until(
            element_to_be_clickable(
                self.chrome.find_elements(
                    By.CSS_SELECTOR, 'bds-button-icon[ng-click="$ctrl.publish()"]'
                )[1]
            )
        )
        self.chrome.find_elements(
            By.CSS_SELECTOR, 'bds-button-icon[ng-click="$ctrl.publish()"]'
        )[1].click()

        self.wait.until(
            visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'div[class="alert alert-success alert-dismissible"]',
                )
            )
        )

    def create_chatbot(self, name: str):
        self.chrome.get("https://intelbras.blip.ai/application/create/marketplace")
        self.wait.until(
            visibility_of_element_located(
                (
                    (
                        By.CSS_SELECTOR,
                        'bds-paper[class="option-card flex flex-column items-center pointer relative paper__elevation--static hydrated"]',
                    )
                )
            )
        )
        self.chrome.find_element(
            By.CSS_SELECTOR,
            'bds-icon[name="file-empty-file"]',
        ).click()
        self.wait.until(
            visibility_of_element_located(
                ((By.CSS_SELECTOR, 'input[name="shortName"]'))
            )
        )
        self.chrome.find_element(By.CSS_SELECTOR, 'input[name="shortName"]').send_keys(
            name
        )
        self.wait.until(
            visibility_of_element_located(
                ((By.CSS_SELECTOR, 'bds-button[type="submit"]'))
            )
        )
        self.chrome.find_element(By.CSS_SELECTOR, 'bds-button[type="submit"]').click()

        self.wait.until(
            visibility_of_element_located(
                ((By.CSS_SELECTOR, 'div[class="chatbot-home-content"]'))
            )
        )
        url = self.chrome.current_url
        self.chatbot_id = url.replace(
            "https://intelbras.blip.ai/application/detail/", ""
        ).replace("/home", "")

        return self


if __name__ == "__main__":
    pass
