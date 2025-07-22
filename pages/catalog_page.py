from playwright.sync_api import Page
from playwright.async_api import async_playwright
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import pandas as pd
import os
import requests
import pytest
import asyncio
import config
import re
import websockets
import json
import time

order_number = None

class  catalogPage:
    def __init__(self,page:Page):
        self.page = page
        self.elements = {
        'searchInput':page.locator("input#search-hints-input"),    
        'catalogButton':page.locator("button[id='catalog']"),
        'catalogHeader':page.locator("h3[class='catalog__header--1xTo2']"),
        'catalogCategories':page.locator("div[class='catalog__categories-list--T9sgj']"),
        'emptyOrderContainer':page.locator("div[class='card--kpSsy footnote--s+GqX empty-order__footnote--YWDvf table-container__header__order--3Y7rq']"),
        'selectOrder':page.locator("div[class='card--kpSsy footnote--s+GqX order-header--v5Zo0 table-container__header__order--3Y7rq']"),
        'createOrder':page.locator("button[class='button--AE6Di order-header__submit--z2zcI button--secondary--Oi+OC']")
        }

    def navigate(self):
        self.page.goto(f'{config.BASE_URL}orders/new', wait_until="load")
        self.page.wait_for_load_state("load")

    def select_category(self,page):
        firstLevel = page.locator("span.catalog__category-name--Kev56>> text='Ноутбуки и планшеты'")
        secondLevel = page.locator("h4.catalog__sub-category-name--tCzV2 >> text='Ноутбуки'") 
        element = page.locator('button[class*="good-list-item__expand-btn--K+Wm1"][class*="button--AE6D"][class*="button--ternary--gG23p"]').first
        firstLevel.click() 
        secondLevel.wait_for(state="visible", timeout=6000)
        secondLevel.click()
        element.wait_for(state="visible", timeout=9000)    


    def check_view(self,page):  
        shortView = page.locator("button[data-testid='icon-button']:has(svg.svg-icon-view-detail)")
        fullView = page.locator("button[data-testid='icon-button']:has(svg.svg-icon-view)")
        short_fill = shortView.locator("rect").first.get_attribute("fill")
        full_fill = fullView.locator("rect").first.get_attribute("fill") 
        if full_fill == "#236192":
            print("Вид подробный уже включён.")
        elif short_fill == "#236192":
            print("Сейчас включен краткий вид . Переключаемся на вид 1...")
            fullView.click()
        else:
            raise Exception("Не удалось определить текущий вид. Элементы иконок не найдены.") 

    def check_checkboxes_active(self,page):
        setupButton = page.get_by_role("row", name="Фильтр") \
             .locator("button[data-testid='button']:has(svg.svg-icon-settings)")
        self.checkbox_ids = {
            "Доступно ": "available1_NEW",
            "На складе ": "inventory1_NEW",
            "На СКЛАДЕ 1": "warehouse1",
            "Доступно  СКЛАД 1": "available1",
            }
        setupButton.wait_for(state="visible")
        setupButton.click() 
        for name, checkbox_id in self.checkbox_ids.items():
            print(f"🔍 Проверяем чекбокс '{name}' (id={checkbox_id})")
            input_locator = self.page.locator(f"input#{checkbox_id}")
            label_locator = self.page.locator(f"label:has(input#{checkbox_id})")
            assert input_locator.count() == 1, f"❌ Чекбокс '{name}' не найден"
            is_checked = input_locator.is_checked()
            print(f"   • Изначальное состояние: {'отмечен' if is_checked else 'не отмечен'}")
            label_locator.click()
            is_after_click = input_locator.is_checked()
            assert is_after_click != is_checked, f"❌ Чекбокс '{name}' не изменяет состояние при клике"
            print(f"   ✅ Состояние изменилось после клика")
            label_locator.click()
            is_restored = input_locator.is_checked()
            assert is_restored == is_checked, f"❌ Чекбокс '{name}' не вернулся в исходное состояние"
            print(f"   🔁 Состояние успешно восстановлено\n")

    def check_checkboxes_disabled(self,page):
        self.disabled_checkbox = {
            "Доступно склад 2": "available2"
        }
        for name, checkbox_id in self.disabled_checkbox.items():
            print(f"🚫 Проверяем задизейбленный чекбокс: {name} (id={checkbox_id})")
            span_locator = self.page.locator(f"label:has(input#{checkbox_id}) span[class*='checkbox--Llduo']")
            input_locator = self.page.locator(f"input#{checkbox_id}")
            assert span_locator.count() == 1, f"❌ Чекбокс '{name}' не найден"
            class_name = span_locator.get_attribute("class") or ""
            assert "checkbox--disabled" in class_name, f"❌ Чекбокс '{name}' должен быть disabled, но не имеет класса `checkbox--disabled`"
            print(f"   ✅ Чекбокс задизейблен (class='{class_name}')")
            label_locator = self.page.locator(f"label:has(input#{checkbox_id})")
            before_state = input_locator.is_checked()
            label_locator.click(force=True)  # принудительный клик
            after_state = input_locator.is_checked()
            assert before_state == after_state, f"❌ Состояние чекбокса '{name}' изменилось, хотя он должен быть неактивен"
            print(f"   🔒 Состояние не изменилось после клика — как и должно быть\n")

        
    def select_checkboxes(self,page):
        saveButton = page.locator("button.button--AE6Di.button--primary--l8973")
        self.checkbox_ids = {
            "Доступно": "available1_NEW",
            "На складе": "inventory1_NEW",
            "На СКЛАДЕ 1": "warehouse1",
            "Доступно СКЛАД 1": "available1",
            }
        for name, checkbox_id in self.checkbox_ids.items():
            print(f"🔍 Проверка чекбокса: {name} (id={checkbox_id})")
            input_locator = self.page.locator(f"input#{checkbox_id}")
            label_locator = self.page.locator(f"label:has(input#{checkbox_id})")
            assert input_locator.count() == 1, f"❌ Не найден чекбокс с id={checkbox_id}"
            if input_locator.is_checked():
                print(f"   ✅ Уже установлен — ничего не делаем")
            else:
                print(f"   ⚠️ Не установлен — ставим")
                label_locator.click()
                assert input_locator.is_checked(), f"❌ Не удалось установить чекбокс '{name}'"
                print(f"   ☑️ Установлен успешно")    
        saveButton.click() 

   
    def check_columns(self,page):
        self.column_headers = {
            "Доступно ": "available1_NEW",
            "На складе ": "inventory1_NEW",
            "На СКЛАДЕ 1": "warehouse1",
            "Доступно СКЛАД 1": "available1",
        }
        self.column_cells = {
        "Доступно ": "available1_NEW",
        "На складе ": "inventory1_NEW",
        "На  СКЛАДЕ 1": "warehouse1",
        "Доступно СКЛАД 1": "available1",
        }
        for column_name, header_text in self.column_headers.items():
            print(f"🔍 Проверяем столбец: {column_name}")
            header = self.page.locator(f"[data-for='{self.column_headers[column_name]}']")
            assert header.count() > 0, f"❌ Заголовок столбца '{column_name}' не найден"

            column_id = self.column_cells[column_name]
            cells = self.page.locator(f"[data-id='{column_id}']")
            assert cells.count() > 0, f"❌ Ячейки для столбца '{column_name}' не найдены"
            for i in range(cells.count()):
                value = cells.nth(i).inner_text().strip()
                assert value != "", f"❌ Пустая ячейка в '{column_name}' на позиции {i}"
                print(f"   ✅ Ячейка {i}: '{value}'")
            print(f"✅ Столбец '{column_name}' прошёл проверку\n")    
     

    def check_elements(self,page):
        for name, locator in self.elements.items():
            try:
                locator.wait_for(state="visible", timeout=5000)
                locator.scroll_into_view_if_needed()
            except Exception as e:
                print(f"❌ Элемент {name} НЕ найден или не отображается! Лог: {e}")
                raise 

    def element_contains(self, page, item_from_db):
        item_ID = item_from_db
        element = page.locator(f"div.item-column--2ggGc.item-column--compact--1X9bc[data-key='{item_from_db}']").nth(2)
        element.wait_for(state="visible", timeout=5000)
        element_text = element.text_content().strip()
        print(f"Полный текст элемента: '{element_text}'")
         
        match = re.match(r'^\d+', element_text)
        if match:
            first_line = match.group(0)  
        else:
            first_line = ""
        assert item_from_db == first_line

    def create_order_header(self, page):
        notifier = page.locator("span[class='notifier-toast__text--WLxds notifier-toast__text--done--QcyyF']")
        self.elements['createOrder'].click()
        
        
        notifier.wait_for(state="visible")
        print(f"DEBUG: Текст уведомления: '{notifier.inner_text().strip()}'")
 

    def add_item_in_order(self,page):   
        catalogButton = page.locator("button#catalog.icon-button--m1T3S") 
        firstLevel = page.locator("span.catalog__category-name--Kev56>> text='Ноутбуки и планшеты'")
        secondLevel = page.locator("h4.catalog__sub-category-name--tCzV2 >> text='Ноутбуки'") 
        element = page.locator('button[class*="good-list-item__expand-btn--K+Wm1"][class*="button--AE6D"][class*="button--ternary--gG23p"]').first
        quantity = page.locator("input.text-input--Zl6hU.smart-input__input--tjskp.smart-input__input--count--6TAV1").first
        addInOrder = page.locator("button[class='button--AE6Di order-header__submit--z2zcI button--secondary--Oi+OC']").first
        catalogButton.click()
        firstLevel.wait_for(state="visible", timeout=6000)
        firstLevel.click() 
        secondLevel.wait_for(state="visible", timeout=6000)
        secondLevel.click()
        element.wait_for(state="visible", timeout=8000)
        time.sleep(15)
        quantity.fill('1')
        box = addInOrder.bounding_box()
        page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        page.mouse.down()
        page.mouse.up()
        addInOrder.evaluate("element => element.click()")
        time.sleep(15)

      

    def redirect_to_order_view(self,page):
        elseButton = page.locator("button.icon-button--m1T3S >> text='Еще'") 
        orderActions = page.locator("div[class='popover__content--cd-EP actions__popover-content--ExF2I order-list-popover__list--k3EiF undefined']")   
        editButton = page.get_by_role("link", name="Редактировать")
        elseButton.wait_for(state="visible", timeout=6000)
        elseButton.click()
        orderActions.wait_for(state="visible", timeout=6000)
        editButton.click()
        time.sleep(10)
        

    def download_order(self, page,download_path): 
       order_number = main
       elseButton = page.locator("button.icon-button--m1T3S >> text='Еще'")
       orderActions = page.locator("div[class='popover__content--cd-EP actions__popover-content--ExF2I order-list-popover__list--k3EiF undefined']") 
       downloadExcel = page.get_by_role("link", name="Выгрузка заказа в Excel")
       elseButton.wait_for(state="visible", timeout=6000)
       elseButton.click()
       orderActions.wait_for(state="visible", timeout=6000)
       downloadExcel.click()
       time.sleep(10)
       downloaded_file = download_path / f"Заказ_{order_number}.xlsx"

    def search_group(self, page):
        input = self.elements['searchInput']
        input.fill('ekey')  
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)
        expected_url = f'{config.BASE_URL}orders/new'
        page.wait_for_load_state("networkidle")  
        assert page.url == expected_url 

       
async def main():
    global order_number
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Ожидаем WebSocket-соединение с увеличенным таймаутом
        try:
            ws = await page.expect_websocket(
                "wss://example.services.example.local:8443/centrifugo/connection/websocket",
                timeout=60000  # Увеличиваем таймаут до 60 сек
            )

            print(f"WebSocket подключен: {ws.url}")

            # Отправляем тестовое сообщение, если сервер этого требует
            await ws.send_json({"type": "subscribe", "channel": "orders"})

            # Ждем первое сообщение от сервера
            async for message in ws:
                print(f"Получено сообщение: {message}")

                # Преобразуем JSON, если данные есть
                try:
                    response_json = message.json()
                    order = response_json["result"]["data"]["data"]["payload"]["order"]["orderNo"]
                    print(f"Номер заказа: {order}")

                    # Проверка на корректность сообщения в элементе `notifier`
                    # Получаем текст из элемента `notifier` и сравниваем
                    notifier_text = await page.locator('notifier').inner_text()
                    print(f"Текст из notifier: {notifier_text.strip()}")

                    # Сравниваем с ожидаемой строкой
                    expected_text = f'Заказ {order} сохранён'
                    if notifier_text.strip() == expected_text:
                        print("Текст в notifier совпадает с ожидаемым.")
                    else:
                        print("Текст в notifier не совпадает с ожидаемым.")

                except Exception as e:
                    print(f"Ошибка обработки JSON: {e}")

        except Exception as e:
            print(f"Ошибка WebSocket: {e}")

        await browser.close()

 
    return order_number
  
@pytest.fixture
async def get_order_number():
    # Запуск WebSocket и получение номера заказа
       order_number = await main()
       return order_number

    