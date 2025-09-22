import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.remote.command import Command


options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "Pixel 9 Pro",
    "appium:app": "/home/vladimir-iliev/develop/otus_appium/app/pnv_486875_ece65f-582630-edb363.apk"
})

appium_server_url = 'http://localhost:4723'

class ReportCommand(Command):
    GET_REPORT: str = "getReport"
    DELETE_REPORT: str = "deleteReport"
    SET_TEST_INFO: str = "setTestInfo"


@pytest.fixture()
def driver():
    android_driver = webdriver.Remote(appium_server_url, options=options)
    android_driver.command_executor._commands = {
        **android_driver.command_executor._commands,
        ReportCommand.GET_REPORT: ("GET", "/getReport"),
        ReportCommand.DELETE_REPORT: ("DELETE", "/deleteReportData"),
        ReportCommand.SET_TEST_INFO: ("POST", "/setTestInfo"),
        }
    android_driver.execute(ReportCommand.DELETE_REPORT)
    yield android_driver
    android_driver.quit()


@pytest.fixture()
def report(driver, request):
    yield
    test_name = request.node.name
    test_status = request.node.get_closest_marker('status').kwargs.get('status', 'unknown')

    driver.execute(
        ReportCommand.SET_TEST_INFO,
        {"sessionId": driver.session_id, "testName": test_name, "testStatus": test_status}
    )
    html = driver.execute(ReportCommand.GET_REPORT)
    with open("report.html", "wt") as r:
        r.write(html['value'])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call':
        item.add_marker(pytest.mark.status(status=rep.outcome))