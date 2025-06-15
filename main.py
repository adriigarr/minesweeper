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

# 5. Dentro del tablero, seleccionamos todas las celdas que tengan clase "square"
cells = board.find_elements(By.CLASS_NAME, "square")

# 6. Mostramos cuántas celdas hay
print(f"Cantidad total de celdas encontradas: {len(cells)}")

# Construir y mostrar la matriz del tablero
board_matrix = basic_functions.parse_board_to_matrix(cells)

print("\nEstado del tablero inicial como matriz:")
for row in board_matrix:
    print(" ".join(row))

# 8. hacer click en la primera celda
basic_functions.click_first_blank(cells)

# esperar a que se actualice el tablero
time.sleep(5)

# volver a capturar las celdas
cells = board.find_elements(By.CLASS_NAME, "square")

# Construir y mostrar la matriz del tablero
board_matrix = basic_functions.parse_board_to_matrix(cells)

print("\nEstado del tablero tras primer click como matriz:")
for row in board_matrix:
    print(" ".join(row))
