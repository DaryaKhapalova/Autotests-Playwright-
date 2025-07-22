from playwright.sync_api import Page
import config


class mainPage:
    def __init__(self,page:Page):
        self.page = page
        self.elements = {
        'logo':page.locator("a[data-testid='mainPage_mainHeader_logo']"),    
        'manager':page.locator("a[data-testid='mainPage_mainHeader_customer']"), 
        'support':page.locator("svg[class='svg-icon--1rhVs svg-icon-support']"),   
        'userName':page.locator("a[data-testid='mainPage_mainHeader_customer']"),
        'logout': page.locator("button[data-testid='mainPage_mainHeader_exitButton']"),
        'searchInput':page.locator("input[data-testid='mainPage_mainHeader_searchInput']"),
        'menuOrders':page.locator("a[data-testid='mainPage_mainMenu_orders']"),
        'menuCatalog':page.locator("a[data-testid='mainPage_mainMenu_catalog']"),
        'menuFinance':page.locator("a[data-testid='mainPage_mainMenu_finance']"),
        'menuServices':page.locator("a[data-testid='mainPage_mainMenu_services']"),
        'menuInfo':page.locator("a[data-testid='mainPage_mainMenu_info']"),
        'menuSettings':page.locator("a[data-testid='mainPage_mainMenu_settings']"),
        'menuDocs':page.locator("button[data-testid='mainPage_mainMenu_docs']"),
        'menuVideoManual':page.locator("a[data-testid='mainPage_mainMenu_video']"),
        'USDHeader': page.locator("span[data-testid='mainPage_mainHeader_currency']"),
        'USDDate':page.locator("span[data-testid='mainPage_mainHeader_currencyDate']"),
        'USDAmount':page.locator("span[data-testid='mainPage_mainHeader_currencyAmount']"),
        'balanceBUHeader':page.locator("span[data-testid='mainPage_mainHeader_balanceBU']"),
        'balanceBUAmount':page.locator("span[data-testid='mainPage_mainHeader_balanceBUAmount']"),
        'balancePUHeader':page.locator("span[data-testid='mainPage_mainHeader_balancePU']"),
        'balancePUAmount':page.locator("span[data-testid='mainPage_mainHeader_balancePUAmount']"),
        'creditLimitHeader':page.locator("span[data-testid='mainPage_mainHeader_credit']"),
        'creditLimitAmount':page.locator("span[data-testid='mainPage_mainHeader_creditAmount']"),
        'turnover':page.locator("span[data-testid='mainPage_mainHeader_turnover']"),
        'turnoverAmount':page.locator("span[data-testid='mainPage_mainHeader_turnoverAmount']"),
        'inOrders':page.locator("span[data-testid='mainPage_mainHeader_inOrders']"),
        'inOrdersAmount':page.locator("span[data-testid='mainPage_mainHeader_inOrdersAmount']"),
        'ordersWidget': page.locator("div[class= 'active-orders--ss1E_']"),
        'navigation':page.locator("div[class='navigation__header--17GhX']"),
        'catalogTabs': page.locator("button[data-testid='mainPage_mainCatalog_categories']"),
        'catalogCategories': page.locator("span[data-testid ='mainPage_mainCatalog_categoryFirstLevel']"),
        'newsTitle': page.locator("h3[data-testid='mainPage_mainForm_newsTitle']"),
        'allNews':page.locator("a[data-testid='mainPage_mainForm_allNews']"),
        'newDate':page.locator("span[data-testid='mainPage_mainForm_newsDate']"),
        'newHeader':page.locator("a[data-testid='mainPage_mainForm_newsHeader']"),
        'newOverview':page.locator("p[data-testid='mainPage_mainForm_newsOverview']"),
        'eventsTitle': page.locator("h3[data-testid='mainPage_mainForm_eventsTitle']"),
        'allEvents':page.locator("a[data-testid='mainPage_mainForm_allEvents']"),
        'actionsTitle': page.locator("h3[data-testid='mainPage_mainForm_actionsTitle']"),
        'allActions':page.locator("a[data-testid='mainPage_mainForm_allActions']"),
        'actionDate':page.locator("span[data-testid='mainPage_mainForm_actionsDate']"),
        'actionName':page.locator("a[data-testid='mainPage_mainForm_actionsHeader']"),
        'actionOverview':page.locator("p[data-testid='mainPage_mainForm_actionsOverview']"),
        'actionButton':page.locator("button[data-testid='mainPage_mainForm_takePartButton']"),
        'orderStatus':page.locator("h4[data-testid='mainPage_mainVidget_orderStatus']"),
        'orderNo':page.locator("a[data-testid='mainPage_mainVidget_orderNo']"),
        'orderAmount':page.locator("span[data-testid='mainPage_mainVidget_orderAmount']"),
        'orderShipping':page.locator("p[data-testid='mainPage_mainVidget_shipping']"),
        'orderShipmentMethod':page.locator("p[data-testid='mainPage_mainVidget_shipmentMethod']"),
        'footer':page.locator("div[class='container--1hZC1 footer__container--aEWV4']")
        }

    def navigate(self):
        self.page.goto(f'{config.BASE_URL}', wait_until="load")
        self.page.wait_for_load_state("load")

    def check_elements(self,page):
        for name, locator in self.elements.items():
            try:
                if name == 'catalogCategories':
                 count = locator.count()
                 if count == 0:
                    raise Exception("catalogCategories: ни один элемент не найден!")
                 for i in range(count):
                    element = locator.nth(i)
                    element.wait_for(state="visible", timeout=5000)
                    element.scroll_into_view_if_needed()
                else:
                 locator.wait_for(state="visible", timeout=5000)
                 locator.scroll_into_view_if_needed()
            except Exception as e:
                print(f"❌ Элемент {name} НЕ найден или не отображается! Лог: {e}")
                raise

    def search_items(self, page, item_from_db):
        item_ID = item_from_db 
        input = self.elements['searchInput'].locator("input")
        input.fill(item_from_db)  
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)
        expected_url = f'{config.BASE_URL}orders/new'
        page.wait_for_load_state("networkidle")  
        assert page.url == expected_url       
          

