import math
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

"""
name: accept_cookies
parameters: 
    driver -> the Selenium webdriver instance

returns:
    None

This function accepts the cookie banner that appears when the page loads.
It switches to the iframe that contains the message and clicks the 'Aceptar' button.
If the banner is not present (already accepted), it safely continues without error.
"""

def accept_cookies(driver):
    try:
        time.sleep(2)  # Espera breve por si el iframe tarda en cargar

        # Detectar iframe del banner de cookies
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[id^='sp_message_iframe']")
        driver.switch_to.frame(iframe)

        # Hacer clic en el botón "Aceptar"
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Aceptar')]")
        accept_button.click()

        driver.switch_to.default_content()  # Volver al contenido principal
        print("✅ Banner de cookies aceptado automáticamente.")
        time.sleep(1)  # Esperar a que desaparezca

    except (NoSuchElementException, TimeoutException):
        print("ℹ️ No se encontró el banner de cookies o ya estaba cerrado.")

"""
name: click_cell
parameters: 
    cell -> the cell to be clicked
returns:
    None

this function clicks on a cell, it is used to click on the first cell
"""

def click_first_blank(cells):
    """
    Busca y hace clic en la primera celda en blanco ('blank').
    """
    for cell in cells:
        if "blank" in cell.get_attribute("class"):
            cell.click()
            break


"""
name of function: parse_board_to_matrix
parameters: 
    cells -> list of cells

returns: 
    board_matrix -> a matrix representing a board

it is very important to understand that the board is not always squared. 
Because of this, the cells are going to be read and grouped by their vertical
position. 
"""
def parse_board_to_matrix(cells):
    
    # get the coordinates top left of each cell
    positions = [cell.location for cell in cells]

    # group the cells by row according to their vertical position
    rows = {}
    for i, pos in enumerate(positions):
        y = pos['y']
        y_key = round(y/10) *10
        rows.setdefault(y_key, []).append((i, pos))

    # sort the rows by their y coordinate
    sorted_rows = sorted(rows.items())

    # create the matrix
    board_matrix = []

    for _, row in sorted_rows:
        # Ordenamos columnas por X (horizontal)
        row_sorted = sorted(row, key=lambda item: item[1]["x"])
        row_states = []
        for index, _ in row_sorted:
            class_name = cells[index].get_attribute("class")
            state = class_name.split()[1]  # 'blank', 'open2', etc.
            row_states.append(state)
        board_matrix.append(row_states)
    
    return board_matrix