from pages.login_page import loginPage
import config
invalid_password = 'Q123456'

def test_invalid_password(page):
    #### Некорректный ввод данных на странице авторизации (пароль)
    login_Page = loginPage(page)
    login_Page.navigate()
    login_Page.login(config.DEFAULT_CUSTOMER_NO, config.DEFAULT_LOGIN,invalid_password)
    page.wait_for_load_state("load")
    error_text = login_Page.get_error_message()
    assert error_text == "Вход запрещён. Проверьте правильность введенных данных", \
        f" Ошибка: '{error_text}'"
    page.wait_for_timeout(7000)

    ###Выполнение запроса авторизации с результатом False
    data = {
            "clientNo": config.DEFAULT_CUSTOMER_NO,
            "clientLogin": config.DEFAULT_LOGIN,
            "password": invalid_password
        }
    response = page.request.post(f'{config.BASE_URL}api/login',data=data)
    response_json = response.json()
    assert response.status == 200
    assert response_json.get("auth") is False
    assert "error" in response_json
    assert response_json["error"]["code"] == "badCredentials"
    assert response_json["error"]["message"] == "Вход запрещён. Проверьте правильность введенных данных"
    
