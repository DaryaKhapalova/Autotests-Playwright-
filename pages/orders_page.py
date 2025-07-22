from playwright.sync_api import Page
import config

class ordersPage:
    def __init__(self,page:Page):
        self.page = page
        self.elements = {
        'ordersList':page.locator("ul[class='order-list--mqRBC']"),
        'purchases':page.locator("a[class='orders-header__action--A1L6q']"),
        'notification':page.locator("button[class='icon-button--m1T3S orders-header__action--A1L6q orders-status-change-notification__open-button--8wlwd']"),
        'createOrder':page.locator("a[class='link-button--X1eK8 orders-header__action--A1L6q']"),
        'searchOrder':page.locator("div[class='search-input--YA8Rz order-search--6d8FA search-input--without-search-icon---zZJI search-input--primary--m9mZ6']"),
        'showOrders':page.locator("div.orders-control__filter--LxYCN >> text='Отображать заказы'"),
        'selectContact':page.locator("div.orders-control__filter--LxYCN >> text='Контакт'"),
        'sorted':page.locator("div.orders-control__filter--LxYCN >> text='Сортировать по'"),
        'viewSwitcher':page.locator("div[class='switcher-view--sauxp']")
        }

    def navigate(self):
        self.page.goto(f'{config.BASE_URL}orders', wait_until="load")
        self.page.wait_for_load_state("load")

    def check_elements(self,page):
        for name, locator in self.elements.items():
            try:
                locator.wait_for(state="visible", timeout=5000)
                locator.scroll_into_view_if_needed()
            except Exception as e:
                print(f"❌ Элемент {name} НЕ найден или не отображается! Лог: {e}")
                raise   

    def create_order(self, page):
        self.elements['createOrder'].click()
        page.wait_for_timeout(3000)
        expected_url = f'{config.BASE_URL}orders/edit/NEW'
        page.wait_for_load_state("networkidle")  
        assert page.url == expected_url

                   