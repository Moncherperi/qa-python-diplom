import pytest
from pages.payment_page import PaymentPage
from helpers.db_helper import get_status
import allure

@allure.title("Позитивный тест: успешная оплата тура по одобренной карте")
def test_successful_card_payment(driver):
    # Создаём объект страницы и открываем форму обычной оплаты
    page = PaymentPage(driver)
    page.open_payment_form()
    # Заполняем поля валидными данными одобренной карты и нажимаем "Продолжить"
    page.fill_form('4444 4444 4444 4441', '11', '27', 'IVAN IVANOV', '333')
    assert 'Операция одобрена Банком.' in page.get_success_notification_text()
    assert get_status('payment_entity') == 'APPROVED'

@allure.title("Позитивный тест: успешная покупка тура в кредит по одобренной карте")
def test_successful_credit_payment(driver):
    # Создаём объект страницы и открываем форму оплаты по кредитной карте
    page = PaymentPage(driver)
    page.open_credit_form()
    # Заполняем поля валидными данными одобренной карты и нажимаем "Продолжить"
    page.fill_form('4444 4444 4444 4441', '11', '27', 'IVAN IVANOV', '333')
    assert 'Операция одобрена Банком.' in page.get_success_notification_text()
    assert get_status('credit_request_entity') == 'APPROVED'

@allure.title("Негативный тест: отказ в оплате по отклоненной карте")
def test_declined_card_payment(driver):
    # Создаём объект страницы и открываем форму обычной оплаты
    page = PaymentPage(driver)
    page.open_payment_form()
    # Заполняем поля данными отклоненной карты и нажимаем "Продолжить"
    page.fill_form('4444 4444 4444 4442', '11', '27', 'IVAN IVANOV', '333')
    assert 'Ошибка! Банк отказал в проведении операции.' in page.get_error_notification_text()
    assert get_status('payment_entity') == 'DECLINED'

@allure.title("Негативный тест: отказ в кредите по отклоненной карте")
def test_declined_credit_payment(driver):
    # Создаём объект страницы и открываем форму оплаты по кредитной карте
    page = PaymentPage(driver)
    page.open_credit_form()
    # Заполняем поля данными отклоненной карты и нажимаем "Продолжить"
    page.fill_form('4444 4444 4444 4442', '11', '27', 'IVAN IVANOV', '333')
    assert 'Ошибка! Банк отказал в проведении операции.' in page.get_error_notification_text()
    assert get_status('credit_request_entity') == 'DECLINED'

@allure.title("Негативный тест: отправка пустой формы - отображение ошибок валидации под полями")
def test_empty_form(driver):
    # Создаём объект страницы и открываем форму обычной оплаты
    page = PaymentPage(driver)
    page.open_payment_form()
    # Оставляем поля формы пустыми и нажимаем "Продолжить"
    page.fill_form('', '', '', '', '')
    errors = page.get_field_errors()
    assert len(errors) == 5
    assert get_status('payment_entity') is None

@allure.title("Негативный тест: невалидный номер карты (менее 16 цифр, несуществующая карта, ввод букв и спецсимволов)")
@pytest.mark.parametrize("card_number", ["4444 4444 4444 444","0000 0000 0000 0000","abcd !@#$ %^&* ()_+"])
def test_invalid_card_number(driver, card_number):
    # Создаём объект страницы и открываем форму обычной оплаты
    page = PaymentPage(driver)
    page.open_payment_form()
    # Заполняем номер карты невалидными данными, остальные поля корректны, и нажимаем "Продолжить"
    page.fill_form(card_number, '11', '27', 'IVAN IVANOV', '333')
    errors = page.get_field_errors()
    assert len(errors) == 1
    assert get_status('payment_entity') is None

@allure.title("Негативный тест: некорректный месяц (00, 13, ввод одной цифры)")
@pytest.mark.parametrize("month", ["00", "13", "abcd !@#$ %^&* ()_+"])
def test_invalid_month(driver, month):
    # Создаём объект страницы и открываем форму обычной оплаты
    page = PaymentPage(driver)
    page.open_payment_form()
    # Заполняем месяц невалидными данными, остальные поля корректны, и нажимаем "Продолжить"
    page.fill_form('4444 4444 4444 4441', month, '27', 'IVAN IVANOV', '333')
    errors = page.get_field_errors()
    assert len(errors) == 1
    assert get_status('payment_entity') is None

@allure.title("Негативный тест: некорректный год (прошедший год, например 25; далёкий будущий год, например 50; ввод одной цифры)")
@pytest.mark.parametrize("year", ["25", "50", "1"])
def test_invalid_year(driver, year):
    # Создаём объект страницы и открываем форму обычной оплаты
    page = PaymentPage(driver)
    page.open_payment_form()
    # Заполняем год невалидными данными, остальные поля корректны, и нажимаем "Продолжить"
    page.fill_form('4444 4444 4444 4441', '11', year, 'IVAN IVANOV', '333')
    errors = page.get_field_errors()
    assert len(errors) == 1
    assert get_status('payment_entity') is None

@allure.title("Негативный тест: некорректное имя владельца (кириллица, цифры, спецсимволы, граничные значения: 1 символ и 250 символов)")
@pytest.mark.parametrize("owner", ["ИВАН ИВАНОВ", "12345", "abcd !@#$ %^&* ()_+", "!", "A" * 250])
def test_invalid_owner(driver, owner):
    # Создаём объект страницы и открываем форму обычной оплаты
    page = PaymentPage(driver)
    page.open_payment_form()
    # Заполняем владельца невалидными данными, остальные поля корректны, и нажимаем "Продолжить"
    page.fill_form('4444 4444 4444 4441', '11', '27', owner, '333')
    errors = page.get_field_errors()
    assert len(errors) == 1
    assert get_status('payment_entity') is None

@allure.title("Негативный тест: некорректный CVC/CVV (менее 3 цифр, ввод букв и спецсимволов)")
@pytest.mark.parametrize("cvc", ["33", "abcd !@#$ %^&* ()_+"])
def test_invalid_cvc(driver, cvc):
    # Создаём объект страницы и открываем форму обычной оплаты
    page = PaymentPage(driver)
    page.open_payment_form()
    # Заполняем поле cvc невалидными данными, остальные поля корректны, и нажимаем "Продолжить"
    page.fill_form('4444 4444 4444 4441', '11', '27', 'IVAN IVANOV', cvc)
    errors = page.get_field_errors()
    assert len(errors) == 1
    assert get_status('payment_entity') is None