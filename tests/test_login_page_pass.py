from pages.login_page import loginPage
from pages.main_page import mainPage
import config

def test_passed(page):
    #### Успешный ввод данных на странице авторизации, переход на главную
    login_Page = loginPage(page)
    login_Page.navigate()
    login_Page.login(config.DEFAULT_CUSTOMER_NO, config.DEFAULT_LOGIN,config.DEFAULT_PASSWORD)
    page.wait_for_load_state("load")
    assert page.url == config.BASE_URL
    main_Page = mainPage(page)
    main_Page.check_elements(page)
    page.wait_for_timeout(4000)

    ###Успешное выполнение запроса авторизации
    data = {
            "clientNo": config.DEFAULT_CUSTOMER_NO,
            "clientLogin": config.DEFAULT_LOGIN,
            "password": config.DEFAULT_PASSWORD
        }
    response = page.request.post(f'{config.BASE_URL}api/login',data=data)
    response_json = response.json()
    assert response.status == 200
    assert response_json.get("auth") is True
    
