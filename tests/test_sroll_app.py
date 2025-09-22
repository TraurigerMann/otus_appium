from appium.webdriver.common.appiumby import AppiumBy


def test_scroll_to_calendar(driver, report):
    while True:
        elements = driver.find_elements(AppiumBy.ID, "com.csdroid.pkg:id/tv_title")

        driver.scroll(elements[1], elements[0])
        elements = driver.find_elements(AppiumBy.ID, "com.csdroid.pkg:id/tv_title")
        element_names = [name.text for name in elements]

        if 'Calendar' in element_names:
            driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Calendar']").click()
            driver.find_element(AppiumBy.ID, "android:id/button1").click()
            assert driver.find_element(AppiumBy.ID, "com.google.android.calendar:id/header").text == "Google Calendar"
            break
