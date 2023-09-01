from selenium.webdriver.common.by import By
from Scripts.funciones import validateHTML, validateInvisiblyHTML, datosJSON
from time import sleep

#attributes = ['input_UserLogin','wait_Load','btn_FlexCash','btn_CierreCajero','table_CierreCajero','input_PES','btn_Guardar','btn_AceptarCierreCajero']
dataHTML = datosJSON(r"Objetos\nameObjectFlex.json")

def input_UserLogin(driver):
    return validateHTML(driver,dataHTML["LoginFlex"]["input_UserLogin"],By.XPATH)

def btn_FlexCash(driver):
    validateInvisiblyHTML(driver,dataHTML["HomeFlex"]["wait_Load"],By.XPATH)
    sleep(8)
    return driver.find_element(By.XPATH,dataHTML["HomeFlex"]["btn_FlexCash"])

def btn_CierreCajero(driver):
    return validateHTML(driver,dataHTML["HomeFlex"]["btn_CierreCajero"],By.XPATH)

def table_CierreCajero(driver):
    return validateHTML(driver,dataHTML["ShiftsCloseFlex"]["table_CierreCajero"],By.XPATH)

def table_Comprobantes(driver):
    validateInvisiblyHTML(driver,dataHTML["ticketreprinting"]["wait_load"],By.XPATH)
    #sleep(3)
    return validateHTML(driver,dataHTML["ticketreprinting"]["table_Comprobantes"],By.XPATH)

def input_PES(driver):
    return validateHTML(driver,dataHTML["SaveValueShift"]["input_PES"],By.XPATH)

def btn_Guardar(driver):
    return validateHTML(driver,dataHTML["SaveValueShift"]["btn_Guardar"],By.XPATH)

def btn_AceptarCierreCajero(driver):
    return validateHTML(driver,dataHTML["SaveValueShift"]["btn_AceptarCierreCajero"],By.XPATH)

def btn_AceptarPrePDF(driver):
    return validateHTML(driver,dataHTML["SaveValueShift"]["btn_AceptarPrePDF"],By.XPATH)

def comboBox_Operacion(driver):
    return validateHTML(driver,dataHTML["ticketreprinting"]["comboBox_Operacion"],By.XPATH)

def choice_Amonestacion(driver):
    return validateHTML(driver,dataHTML["ticketreprinting"]["choice_Amonestacion"],By.XPATH)

def choice_CierreDeCajero(driver):
    return validateHTML(driver,dataHTML["ticketreprinting"]["choice_CierreDeCajero"],By.XPATH)

def btn_Lupa(driver):
    return validateHTML(driver,dataHTML["ticketreprinting"]["btn_Lupa"],By.XPATH)