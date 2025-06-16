from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import basic_functions

# 1. preparar el driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 2. Abrir la web
driver.get("https://minesweeperonline.com/#beginner")

# Aceptar cookies si aparecen
basic_functions.accept_cookies(driver)

# 3. esperar a que cargue el juego
time.sleep(5)

# 4. Buscamos el elemento <table id="game"> que contiene el tablero
board = driver.find_element(By.ID, "game")

# Capturar estado inicial
board_matrix, cells = basic_functions.capture_board(driver)
print(f"Cantidad total de celdas encontradas: {len(cells)}")

print("\nEstado del tablero inicial como matriz:")
for row in board_matrix:
    print(" ".join(row))

print("\nEstado visual del tablero:")
basic_functions.render_board(board_matrix)

# Hacer clic en una celda en blanco
basic_functions.click_random_blank(cells)

# Esperar y volver a capturar el estado
time.sleep(5)
board_matrix, cells = basic_functions.capture_board(driver)

print("\nEstado del tablero tras primer click como matriz:")
for row in board_matrix:
    print(" ".join(row))

print("\nEstado visual del tablero:")
basic_functions.render_board(board_matrix)

