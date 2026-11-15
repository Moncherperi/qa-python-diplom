import pytest
from selenium import webdriver
from helpers.db_helper import clear_tables

# Фикстура запуска браузера Chrome и открытия тестируемого сайта перед каждым тестом
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8080")
    # Передаём открытый браузер в тест, а после завершения теста закрываем его
    yield driver
    driver.quit()

# Фикстура автоматической очистки таблиц БД перед каждым тестом (autouse=True)
@pytest.fixture(autouse=True)
def clean_db():
    clear_tables()




