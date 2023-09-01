from  selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import pytest
import time
import datetime

def datosJSON(filePath,attributes=False):
    "Obtiene datos de un Json en un diccionario y verifico que cumpla con los atributos"

    try:
        with open(filePath) as file:
            data = json.load(file)
    except FileNotFoundError:
        pytest.fail(f"No se encuentra el archivo en la ruta: {filePath}")
    except Exception:
        pytest.fail("El archivo no posee la estructura correcta de JSON")
    
    if attributes and set(attributes) != set(data.keys()):
        pytest.fail(f"El archivo no posee los atributos correctos: {attributes}")

    return data


def posIsClosed(cursor,pos,fecha):
    "Verifica si la pos se encuentra cerrada"
    
    cursor.execute(f"""
        SELECT business_date, pos_number, pos_state 
        FROM tld_pos
        WHERE pos_number = {pos} AND pos_state NOT IN ('OPENED', 'LOGGED') AND business_date = '{fecha}'
    """)

    if cursor.fetchone():
        return
    pytest.fail(f"La pos {pos} no se encuentra cerrada para la fecha {fecha}")

def validateHTML(driver,html,by):
    "Espera a que el elemento sea clickeable y validamos la existencia de XPATH, ID, etc."

    try:
        wait = WebDriverWait(driver, 60)  # Tiempo de espera máximo de 60 segundos
        wait.until(EC.element_to_be_clickable((by,html)))
        return driver.find_element(by,html)
    except NoSuchElementException:
        pytest.fail(f"El objeto HTML no existe: {html}")

def validateInvisiblyHTML(driver,htmlOut,by):
    "Esperamos a que el elemento se vaya y validamos existencia de XPATH, ID, etc."

    try:
        wait = WebDriverWait(driver, 60)  # Tiempo de espera máximo de 60 segundos
        wait.until(EC.invisibility_of_element_located((by,htmlOut)))
    except NoSuchElementException:
        pytest.fail(f"El objeto HTML no existe: {htmlOut}")
    except Exception:
        pytest.fail("Error")

def changeFormatDate(date):
    """Devuelve la fecha en formato YYYYMMDD"""

    date = date.split("/")
    date.reverse()
    return ''.join(date)

def getDataExcel(sheet,row):
    """Devuelve en un diccionario una fila del excel"""

    dataTest = {
    "UserFlex": str(sheet[f"A{row}"].value),
    "PasswordFlex": str(sheet[f"B{row}"].value),
    "Date": sheet[f"C{row}"].value,
    "Pos": sheet[f"D{row}"].value,
    "Shift": sheet[f"E{row}"].value,
    "Diff": 0 if sheet[f"F{row}"].value is None else sheet[f"F{row}"].value
    #"PageFlex": sheet[f"G{row}"].value
    }
    
    if any(x is None or x == "" for x in dataTest.values()):
        pytest.fail("El test tiene algun dato de prueba vacío")
    return dataTest

def acceptAlert(driver):
    "Aceptar cualquier alerta que arroje el navegador"
    
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        return

def take_screenshot(driver,name):
    time.sleep(1)
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    report_direct = "./Reportes/"
    driver.save_screenshot(report_direct + '/Imagenes/'+name + timestamp + '.png')
    print (report_direct + '/Imagenes/'+name + timestamp + '.png')


def selectComboBox(comboBox,option):
    "Del comboBox, selecciona por el texto visible"
    select = Select(comboBox)
    select.select_by_visible_text(option)

def getVoucherNumber(table,dataTest):
    """table debe ser el webdriver con la tabla de html y dataTest son los datos del test actual.
    Devuelve el número de comprobante (int), de no poder encontrarlo arroja test fail.
    """
    rows = table.find_elements(By.TAG_NAME,'tr')[1:]

    for row in rows:
        columns = row.find_elements(By.TAG_NAME,'td')
        if int(changeFormatDate(columns[4].text)) == dataTest["Date"] and int(columns[5].text) == dataTest["Pos"] and int(columns[6].text) == dataTest["Shift"]:
            return int(columns[1].text)
    
    pytest.fail(f"No se encontró el comprobante")