import pyodbc
import pytest
import config
from playwright.sync_api import Playwright, APIRequestContext,sync_playwright
from typing import Generator
from pages.login_page import loginPage
from datetime import datetime
import os
from pathlib import Path


@pytest.fixture(scope='session')
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        yield browser
        browser.close()


@pytest.fixture(scope='function')
def context(browser, request):
    context = browser.new_context(ignore_https_errors=True, viewport={"width": 1280, "height": 1080})
    yield context
    context.close()


@pytest.fixture(scope="module")
def db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=MLSQL-EXAMPLE;"
        "DATABASE=preprod;"
        "UID=test;"
        "PWD=test;"
    )
    yield conn
    conn.close()

@pytest.fixture
def item_from_db(db_connection):
    cursor = db_connection.cursor()

    # Получить  методы доставки
    query_shipment_methods = "exec [dbo].[Example$INET_Get_Shipment_Methods] @Cust='TEST'"
    cursor.execute(query_shipment_methods)
    shipment_methods = cursor.fetchall()
    

    default_shipment_method = next((row for row in shipment_methods if row[2] == 1), None)
    print("Данные из БД:", shipment_methods)
    if not default_shipment_method:
        pytest.fail("Shipment method not found")

    shipment_method_code = default_shipment_method[0]
    location_code = default_shipment_method[3]

    # Получить  договоры
    query_counter_agent = "exec [dbo].[Example$INET_Get_CounterAgent] @Cust='TEST'"
    cursor.execute(query_counter_agent)
    counter_agents = cursor.fetchall()

    default_counter_agent = next((a for a in counter_agents if a[0].strip() == '6005'), None)
    print("Данные из БД:", counter_agents)
    if not default_counter_agent:
        pytest.fail("Counter agent not found")

    counter_agent_id = default_counter_agent[2]
    agent_currency = default_counter_agent[3]

    # Получить даты доставки
    query_shipment_dates = "exec [dbo].[Example$INET_Get_Shipment_Dates] @Cust='TEST'"
    cursor.execute(query_shipment_dates)
    shipment_dates = cursor.fetchall()
 
    shipment_dates = [datetime.strptime(date[0], '%d.%m.%Y') for date in shipment_dates]
    print("Данные из БД:", shipment_dates)
    latest_shipment_date = max(shipment_dates)
    print("Последняя дата поставки:", latest_shipment_date.strftime('%d.%m.%Y'))

    # Получить список товаров в группе "Ноутбуки"
    query_group_first_level = "exec [dbo].[Example$INET_Get_GroupList] @pgroup = 'order', @B_Module = 0"
    cursor.execute(query_group_first_level)
    group_list = cursor.fetchall()
    

    laptops_and_tablets = next((g for g in group_list if g[1].strip() == 'Ноутбуки и планшеты'), None)
    print("Данные из БД:", group_list)
    if not laptops_and_tablets:
        pytest.fail('Group "Ноутбуки и планшеты" not found')

    group_code = laptops_and_tablets[0]

    query_group_second_level = f"exec [dbo].[Example$INET_Get_GroupList] @pgroup = '{group_code}', @B_Module = 0"
    cursor.execute(query_group_second_level)
    second_level_groups = cursor.fetchall()

    laptops_group = next((g for g in second_level_groups if g[1].strip() == 'Ноутбуки'), None)
    if not laptops_group:
        pytest.fail('Group "Ноутбуки" not found')

    laptops_group_code = laptops_group[0]

    query_get_group_items = f"""
        EXEC [dbo].[Example$INET_GetItems] @Group='{laptops_group_code}', @Key='group', 
        @BinCode='', @LocationCode='{location_code}', @LOCode='543', 
        @PriceColumn='5', @ShipmentDate='{latest_shipment_date}', 
        @ShipmentMethodCode='{shipment_method_code}', @PriceFactor='0', @Cust='TEST', 
        @IdDogovor='{counter_agent_id}',  @Brand='', @Name='', @Top=200, 
        @ItemList='', @DisplayQtyLimit=0, @DefCurrencyCode='{agent_currency}', 
         @OrderBy="[Name]"
    """

    cursor.execute(query_get_group_items)
    items = cursor.fetchall()
    print(items[0])
    if not items:
        pytest.fail("No items found")

    first_item_no = items[0][0]

    # Получить  данные о товаре
    query_get_items = f"""
        EXEC [dbo].[Example$INET_GetItems] @key='find', @Cust='TEST', 
        @PriceFactor='0', @DisplayQtyLimit=0, @B2B_Module=0, 
        @BinCode='', @LocationCode='{location_code}', @LOCode='543', 
        @ShipmentDate='{latest_shipment_date}', @ShipmentMethodCode='{shipment_method_code}', 
        @IdDogovor='{counter_agent_id}', @PriceColumn='5', @DefCurrencyCode='{agent_currency}', 
        @ItemList='{first_item_no}', @OrderBy="[Name]"
    """

    cursor.execute(query_get_items)
    final_items = cursor.fetchall()
    if not final_items:
        pytest.fail("No final items found")

    return final_items[0][0]


@pytest.fixture(scope='function')
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def login(page):
    login_Page = loginPage(page)
    login_Page.navigate()
    login_Page.login(config.DEFAULT_CUSTOMER_NO, config.DEFAULT_LOGIN,config.DEFAULT_PASSWORD)  
    page.wait_for_timeout(3000) 

@pytest.fixture
def download_path():
    project_root = Path(__file__).resolve().parent.parent  # корень проекта
    download_folder = project_root / "downloads"
    download_folder.mkdir(parents=True, exist_ok=True)
    
    # Создать папку, если она не существует
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    return download_folder 

@pytest.fixture
def browser_context(download_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        context = browser.new_context(accept_downloads=True, download_path=str(download_path))
        yield context
        context.close()  
        browser.close()  

        


 