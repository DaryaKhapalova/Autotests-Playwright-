from pages.main_page import mainPage
from pages.catalog_page import catalogPage

def test_check_itemID_in_db(item_from_db):
     ##Поиск товара в БД
     assert item_from_db, "Товар не найден в БД"
     print("Код товара:", item_from_db)
   

def test_check_itemID_in_web(page,login, item_from_db):
     ##Поиск товара на сайте
     main_Page = mainPage(page)
     main_Page.navigate()
     main_Page.search_items(page, item_from_db)
     catalog_Page = catalogPage(page)
     catalog_Page.element_contains(page, item_from_db)
