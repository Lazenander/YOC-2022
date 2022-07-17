from selenium import webdriver

option = webdriver.ChromeOptions()
#option.add_argument("headless")
path = "./chromedriver"
browser = webdriver.Chrome(path, options=option)

browser.get('https://s.weibo.com/weibo?q=%E7%81%B5%E6%B4%BB%E7%94%A8%E5%B7%A5')
browser.get_screenshot_as_file('截图.png')