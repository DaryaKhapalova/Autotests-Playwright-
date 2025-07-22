from pages.login_page import loginPage
import config
invalid_customer = 'TEST99999'

def test_invalid_customer(page):
    #### Некорректный ввод данных на странице авторизации (код клиента)
    login_Page = loginPage(page)
    login_Page.navigate()
    login_Page.login(invalid_customer, config.DEFAULT_LOGIN,config.DEFAULT_PASSWORD)
    page.wait_for_load_state("load")
    error_text = login_Page.get_error_message()
    assert error_text == "Вход запрещён. Проверьте правильность введенных данных", \
        f" Ошибка: '{error_text}'"
    page.wait_for_timeout(4000)

    ###Выполнение запроса авторизации с результатом False
    data = {
            "clientNo": invalid_customer,
            "clientLogin": config.DEFAULT_LOGIN,
            "password": config.DEFAULT_PASSWORD
        }
    response = page.request.post(f'{config.BASE_URL}api/login',data=data)
    response_json = response.json()
    assert response.status == 200
    assert response_json.get("auth") is False
    assert "error" in response_json
    assert response_json["error"]["code"] == "badCredentials"
    assert response_json["error"]["message"] == "Вход запрещён. Проверьте правильность введенных данных"
    
