from pages.catalog_page import catalogPage

def test_catalog_settings_view(page,login,download_path):
    ##Проверка вида категории каталога, заголовков и содержимого столбцов
    catalog_Page = catalogPage(page)
    catalog_Page.navigate()
    catalog_Page.select_category(page)
    catalog_Page.check_view(page)
    catalog_Page.check_checkboxes_active(page)
    catalog_Page.check_checkboxes_disabled(page)    
    catalog_Page.select_checkboxes(page)
    catalog_Page.check_columns(page)
    

    