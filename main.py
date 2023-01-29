import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import pymysql
from folium import *
from contextlib import contextmanager
import sys

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MyApp(App):
    def add_cordinates(self, instance):
        try:
            conn = pymysql.connect(
                host='sql7.freesqldatabase.com',
                port=3306,
                user='sql7593829',
                password='iTM51TCuM4',
                database='sql7593829',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.lbl_status.text = 'Успешно подключено'
        except Exception as ex:
            self.lbl_status.text = 'Не удалось подключиться'
        categories = ['макулатура', 'стекло', 'металл', 'пластик', 'пищевые отходы', 'средства личной гигиены']
        ok = True
        for i in self.category_input.text.split(', '):
            if i.lower() not in categories:
                ok = False
                break
        if ok:
            try:
                try:
                    if 0 <= float(self.lat_input.text) <= 90 and 0 <= float(self.lon_input.text) <= 180:
                        with conn.cursor() as cursor:
                            sql = "INSERT INTO `categories`(`lat`, `lon`, `category`) VALUES ({},{},'{}')".format(float(self.lat_input.text), float(self.lon_input.text), self.category_input.text)
                            cursor.execute(sql)
                            conn.commit()
                    else:
                        self.lbl_status.text = 'Широта от 0 до 90, долгота от 0 до 180'
                except ValueError:
                    self.lbl_status.text = 'Координаты должны быть типа float'
            except Exception as ex:
                self.lbl_status.text = 'Не удалось подключиться к базе данных\nПроверьте работу VPN'
        else:
            self.lbl_status.text = 'Неправильно введены данные'
    def parse_coordinates(self,instance):
        try:
            conn = pymysql.connect(
                host='sql7.freesqldatabase.com',
                port=3306,
                user='sql7593829',
                password='iTM51TCuM4',
                database='sql7593829',
                cursorclass=pymysql.cursors.DictCursor)
            with conn.cursor() as cursor:
                select = "SELECT * FROM `categories`"
                cursor.execute(select)
                rows = cursor.fetchall()
                m = Map(location=[55.752004, 37.617734], zoom_start=11)
                for marker in rows:
                    Marker([marker['lat'], marker['lon']], popup=marker['category'], tooltip='Посмотреть категорию').add_to(m)
                m.save('output.html')
                os.startfile('output.html')
            self.lbl_status.text = 'Успешно добавлено'
        except Exception as ex:
            self.lbl_status.text = 'Не удалось подключиться к базе данных\nПроверьте работу VPN'

    def build(self):
        bl = BoxLayout(orientation = 'vertical',padding=25, spacing=15)
        bl_labels = BoxLayout(orientation = 'vertical')
        bl_inputs = BoxLayout(orientation = 'horizontal',size_hint=(1,.15), spacing = 10)
        bl_buttons = BoxLayout(orientation = 'vertical', spacing = 5)
        self.lbl_status = Label(text='',font_size=32, halign='center')
        self.lbl_categories = Label(text='Доступные категории:•макулатура\n•стекло\n•металл\n•пластик\n•пищевые•отходы\n•средства личной гигиены', font_size=16)
        bl_labels.add_widget(self.lbl_status)
        bl_labels.add_widget(self.lbl_categories)
        self.lat_input = TextInput(text='', hint_text='Широта')
        self.lon_input = TextInput(text='', hint_text='Долгота')
        self.category_input = TextInput(text='', hint_text='Пластик, стекло...')
        bl_inputs.add_widget(self.lat_input)
        bl_inputs.add_widget(self.lon_input)
        bl_inputs.add_widget(self.category_input)
        self.add_button = Button(text='Добавить координаты', on_press=self.add_cordinates)
        self.open_map_btn = Button(text='Открыть карту', on_press=self.parse_coordinates)
        bl_buttons.add_widget(self.add_button)
        bl_buttons.add_widget(self.open_map_btn)
        bl.add_widget(bl_labels)
        bl.add_widget(bl_inputs)
        bl.add_widget(bl_buttons)

        return bl
if __name__ == "__main__":
    MyApp().run()