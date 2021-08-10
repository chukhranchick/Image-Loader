from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import os
from win10toast import ToastNotifier


class ImageLoader(object):

    def __init__(self, target_dir_name='images'):
        self.target_dir_name = target_dir_name

        if not os.path.exists(target_dir_name):
            os.mkdir(target_dir_name)

    def load_images(self, image_names, images_per_request):
        for image_name in image_names:
            self._load_image(image_name, images_per_request)

    def _load_image(self, image_name, images_per_request):
        raise NotImplementedError


class SeleniumImageLoader(ImageLoader):
    LOADER_URL = 'https://images.google.com/?hl=ru'

    def __init__(self, driver_path='D:\Download\chromedriver.exe', target_dir_name='images'):
        super().__init__(target_dir_name)
        self.browser = webdriver.Chrome(executable_path=driver_path)

    def __open_loader_url(self):
        self.browser.get('https://images.google.com/?hl=ru')
        sleep(random.randint(2, 3))

    def __close_browser(self):
        self.browser.close()

    def __fill_search_input(self, image_name):
        self.browser.find_element_by_xpath("//input[@title='Поиск']").click()
        self.browser.find_element_by_xpath("//input[@title='Поиск']").send_keys(image_name)
        sleep(random.randint(1, 2))
        self.browser.find_element_by_xpath("//input[@title='Поиск']").send_keys(Keys.ENTER)
        sleep(random.randint(1, 2))

    def __choose_hi_res_images_filter(self):
        self.browser.find_element_by_xpath("//div[contains(text(), 'Инструменты')]").click()
        sleep(random.randint(1, 2))
        self.browser.find_element_by_xpath("//div[contains(text(), 'Размер')]").click()
        sleep(random.randint(1, 2))
        self.browser.find_element_by_xpath("//span[contains(text(), 'Большой')]").click()
        sleep(random.randint(1, 2))

    def _load_image(self, image_name, images_per_request):
        self.__open_loader_url()

        self.__fill_search_input(image_name)
        self.__choose_hi_res_images_filter()

        search_images_table = self.browser.find_element_by_class_name('islrc')
        search_images = search_images_table.find_elements_by_class_name('islir')

        for i in range(0, images_per_request):
            try:
                self.__save_image(str(image_name) + str(i + 1), search_images[i])
            except Exception as e:
                print(e)
                toaster = ToastNotifier()
                toaster.show_toast("Attention", str(e), icon_path=None, duration=100)


    def __save_image(self, image_name, target_element):
        target_element.click()
        sleep(3)
        src = self.browser.find_element_by_xpath(
            '/html/body/div[2]/c-wiz/div[4]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img'
            # TODO '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img'
        ).get_attribute(
            "src")
        img_data = requests.get(src).content
        with open(str(self.target_dir_name) + '/' + str(image_name) + '.jpg', 'wb') as img:
            img.write(img_data)


def load_images(self, image_names, images_per_request):
    super().load_images(image_names, images_per_request)
    self.__close_browser()
