from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

# Класс Page Object для описания элементов и действий на странице покупки тура
class PaymentPage:
    # Локаторы кнопок выбора способа покупки и отправки формы
    BUY_BUTTON = (By.XPATH, "//button[.//span[text()='Купить']]")
    CREDIT_BUTTON = (By.XPATH, "//button[.//span[text()='Купить в кредит']]")
    CONTINUE_BUTTON = (By.XPATH, "//button[.//span[text()='Продолжить']]")

    # Локаторы полей ввода формы
    CARD_NUMBER_INPUT = (By.XPATH, "//span[text()='Номер карты']/following-sibling::span/input")
    MONTH_INPUT = (By.XPATH, "//span[text()='Месяц']/following-sibling::span/input")
    YEAR_INPUT = (By.XPATH, "//span[text()='Год']/following-sibling::span/input")
    OWNER_INPUT = (By.XPATH, "//span[text()='Владелец']/following-sibling::span/input")
    CVC_INPUT = (By.XPATH, "//span[text()='CVC/CVV']/following-sibling::span/input")

    # Локатор подсказок при заполнении полей формы
    FIELD_ERROR = (By.CSS_SELECTOR, ".input__sub")

    # Локаторы всплывающих уведомлений банка об успехе или ошибке
    SUCCESS_NOTIFICATION = (By.CSS_SELECTOR, ".notification_status_ok .notification__content")
    ERROR_NOTIFICATION = (By.CSS_SELECTOR, ".notification_status_error .notification__content")

    # Инициализируем браузер и настраиваем ожидание 15 секунд
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть форму оплаты по карте")
    def open_payment_form(self):
        self.driver.find_element(*self.BUY_BUTTON).click()

    @allure.step("Открыть форму покупки тура в кредит")
    def open_credit_form(self):
        self.driver.find_element(*self.CREDIT_BUTTON).click()

    @allure.step("Заполнить все 5 полей формы и нажать кнопку 'Продолжить'")
    def fill_form(self, card_number, month, year, owner, cvc):
        self.driver.find_element(*self.CARD_NUMBER_INPUT).send_keys(card_number)
        self.driver.find_element(*self.MONTH_INPUT).send_keys(month)
        self.driver.find_element(*self.YEAR_INPUT).send_keys(year)
        self.driver.find_element(*self.OWNER_INPUT).send_keys(owner)
        self.driver.find_element(*self.CVC_INPUT).send_keys(cvc)
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    @allure.step("Появление зелёного уведомления об успехе и возвращение его текста")
    def get_success_notification_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_NOTIFICATION)).text

    @allure.step("Появление красного уведомления об ошибке и возвращение его текста")
    def get_error_notification_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_NOTIFICATION)).text

    @allure.step("Найти все подсказки об ошибках под полями и вернуть список их текстов")
    def get_field_errors(self):
        elements = self.driver.find_elements(self.FIELD_ERROR[0], self.FIELD_ERROR[1])
        errors = []
        for element in elements:
            errors.append(element.text)

        return errors
    
