import math
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random

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
name: capture_board
parameters:
    driver -> the Selenium webdriver instance

returns:
    board_matrix -> a 2D list representing the current state of the Minesweeper board

This function captures the current visible state of the Minesweeper board.
It locates all valid cell elements inside the board (with id format "x_y")
and filters them to include only the inner 9x9 playable area.

It returns the parsed matrix using parse_board_to_matrix so that it can be used
for decision making or display after each move.
"""
def capture_board(driver):
    board = driver.find_element(By.ID, "game")
    cells = board.find_elements(By.CLASS_NAME, "square")

    filtered_cells = []
    for cell in cells:
        cell_id = cell.get_attribute("id")
        if cell_id and "_" in cell_id:
            parts = cell_id.split("_")
            try:
                row = int(parts[0])
                col = int(parts[1])
                if 1 <= row <= 9 and 1 <= col <= 9:
                    filtered_cells.append(cell)
            except ValueError:
                continue

    board_matrix = parse_board_to_matrix(filtered_cells)
    return board_matrix, filtered_cells 




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
name: click_random_blank
parameters:
    cells -> list of Selenium WebElement objects

returns:
    None

This function filters all blank cells (those with class containing 'blank') and selects one at random to click on.

It is useful for testing or simulating a beginner player making a non-strategic move.
"""

def click_random_blank(cells):
    blank_cells = [cell for cell in cells if "blank" in cell.get_attribute("class")]

    if not blank_cells:
        print("⚠️ No blank cells available to click.")
        return

    cell = random.choice(blank_cells)
    cell.click()

"""
name: parse_board_to_matrix
parameters: 
    cells -> list of Selenium WebElement objects representing the cells

returns: 
    board_matrix -> a 2D list representing the visual structure of the board

This function takes a flat list of cell elements from the Minesweeper board
and organizes them into a matrix based on their vertical and horizontal position
on screen.

It uses a pixel tolerance to group cells into rows by Y coordinate, to avoid
issues caused by small vertical shifts between elements. Within each row,
cells are sorted by X coordinate.

This ensures that the resulting matrix accurately represents the visual layout
of the Minesweeper board, regardless of whether the board is square or rectangular.
"""

def parse_board_to_matrix(cells):
    positions = [cell.location for cell in cells]

    row_groups = []
    tolerance = 5  # pixel threshold to group by vertical position

    for i, pos in enumerate(positions):
        y = pos["y"]
        placed = False
        for group in row_groups:
            if abs(group["y"] - y) <= tolerance:
                group["cells"].append((i, pos))
                placed = True
                break
        if not placed:
            row_groups.append({"y": y, "cells": [(i, pos)]})

    row_groups.sort(key=lambda g: g["y"])

    board_matrix = []
    for group in row_groups:
        row_sorted = sorted(group["cells"], key=lambda item: item[1]["x"])
        row_states = []
        for index, _ in row_sorted:
            class_name = cells[index].get_attribute("class")
            state = class_name.split()[1]  # e.g., 'blank', 'open2'
            row_states.append(state)
        board_matrix.append(row_states)

    return board_matrix


"""
name: render_board
parameters:
    board_matrix -> a matrix representing the current state of the board

returns:
    None

This function receives a matrix representing the game board and prints
a visual representation to the console. It maps each internal cell state
(e.g., 'blank', 'open2', 'flag') to a simplified symbol for easier reading:

- 'blank'  → '#' (unrevealed cell)
- 'flag'   → '⚑' (flagged cell)
- 'open0'  → '.' (revealed with 0 adjacent mines)
- 'open1' to 'open8' → corresponding numbers ('1' to '8')

This helps visualize the Minesweeper board clearly in the terminal.
"""

def render_board(board_matrix):
    symbol_map = {
        "blank": "#",
        "flag": "⚑",
        "open0": ".",
        "open1": "1",
        "open2": "2",
        "open3": "3",
        "open4": "4",
        "open5": "5",
        "open6": "6",
        "open7": "7",
        "open8": "8"
    }

    for row in board_matrix:
        symbols = [symbol_map.get(cell, "?") for cell in row]
        print(" ".join(symbols))
