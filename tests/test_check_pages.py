from pages.main_page import mainPage
from pages.orders_page import ordersPage
from pages.catalog_page import catalogPage
import pytest

@pytest.mark.parametrize("PageClass", [
    mainPage, ordersPage, catalogPage
])

def test_check_pages(page, login, PageClass):
    ##Проверка наличия элементов на страницах
    page_object = PageClass(page)
    page_object.navigate()
    page_object.check_elements(page)
