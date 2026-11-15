from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    # Локаторы всплывающих уведомлений банка об успехе или ошибке
    SUCCESS_NOTIFICATION = (By.CSS_SELECTOR, ".notification_status_ok .notification__content")
    ERROR_NOTIFICATION = (By.CSS_SELECTOR, ".notification_status_error .notification__content")

# Инициализируем браузер и настраиваем ожидание 15 секунд
def __init__(self,driver):
    self.driver = driver
    self.wait = WebDriverWait(driver, 15)

# Открываем форму обычной оплаты по карте
def open_payment_form(self):
    self.driver.find_element(*self.BUY_BUTTON).click()

# Открываем форму покупки тура в кредит
def open_credit_form(self):
    self.driver.find_element(*self.CREDIT_BUTTON).click()

# Заполняем все 5 полей формы и нажимаем кнопку Продолжить
def fill_form(self, card_number, month, year, owner, cvc)
    self.driver.find_element(*self.CARD_NUMBER_INPUT).send_keys(card_number)
    self.driver.find_element(*self.MONTH_INPUT).send_keys(month)
    self.driver.find_element(*self.YEAR_INPUT).send_keys(year)
    self.driver.find_element(*self.OWNER_INPUT).send_keys(owner)
    self.driver.find_element(*self.CVC_INPUT).send_keys(cvc)
    self.driver.find_element(*self.CONTINUE_BUTTON).click()

# Ждём появления зелёного уведомления об успехе и возвращаем его текст
def get_success_notification_text(self):
    return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_NOTIFICATION)).text

# Ждём появления красного уведомления об ошибке и возвращаем его текст
def get_error_notification_text(self):
    return self.wait.until(EC.visibility_of_element_located(self.ERROR_NOTIFICATION)).text




