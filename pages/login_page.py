from playwright.sync_api import Page
import config

class loginPage:
    def __init__(self,page:Page):
        self.page = page
        self.customerNo = page.locator("input[name='clientNo']")
        self.loginID = page.locator("input[name='clientLogin']")
        self.password = page.locator("input[name='password']")
        self.entryButton = page.locator("input[value='Войти']")
        self.errorMessage = page.locator("div[class='text-center error__message']")
        self.errorText = page.locator("strong[class='text-danger']")

    def navigate(self):
        self.page.goto(config.BASE_URL, wait_until="load")
        self.page.wait_for_load_state("load")

    def login(self, customerNo=config.DEFAULT_CUSTOMER_NO, 
                    loginID=config.DEFAULT_LOGIN,password=config.DEFAULT_PASSWORD):
        self.page.wait_for_selector("input[name='clientNo']", state="visible", timeout=30000)
        self.page.wait_for_selector("input[name='clientLogin']", state="visible", timeout=30000)
        self.page.wait_for_selector("input[name='password']", state="visible", timeout=30000)

        self.customerNo.fill(customerNo)
        self.loginID.fill(loginID)
        self.password.fill(password)
        self.entryButton.click() 

    def get_error_message(self):
        return self.errorMessage.inner_text().strip()