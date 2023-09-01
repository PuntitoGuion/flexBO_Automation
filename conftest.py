import pytest
import pytest_html
import datetime
from selenium import webdriver
import os

now = datetime.datetime.now()
report_name= "test_results - " + now.strftime("%H.%M.%S")
report_direct = "./ReportesEjecucion/"
folderImages = "./ReportesEjecucion/Imagenes"
if not os.path.exists(folderImages):
    os.makedirs(folderImages)

path_screenshot = []

def save_path_screenshot(path):
    path_screenshot.append(path)


def pytest_html_report_title(report):
    report.title = report_name

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not config.option.htmlpath:
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        test_name = config.getoption("-k") or report_name
        #html_path = f"{report_direct}{test_name}_{timestamp}.html"
        html_path = f"{report_direct}{test_name}.html"
        config.option.htmlpath = html_path

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #Si no existe creamos carpeta para guardar las screen separadas por casos de prueba
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        feature_request = item.funcargs['request']
        driver = feature_request.getfixturevalue('driver')
        driver.save_screenshot(report_direct+'/Imagenes/scr'+timestamp+'.png')
        #extra.append(pytest_html.extras.image('./Reportes/Imagenes/scr'+timestamp+'.png'))
        # always add url to report
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            extra.append(pytest_html.extras.image('file:Imagenes/scr'+timestamp+'.png'))
            #extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
        for screenshot_path in path_screenshot:
            extra.append(pytest_html.extras.image(f"file:{screenshot_path}"))

        report.extra = extra
        path_screenshot.clear()