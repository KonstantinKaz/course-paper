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
    def get_category(self,instance):
        try:
            conn = pymysql.connect(
                host='sql7.freesqldatabase.com',
                port=3306,
                user='sql7593829',
                password='iTM51TCuM4',
                database='sql7593829',
                cursorclass=pymysql.cursors.DictCursor)
            with conn.cursor() as cursor:
                select = "SELECT * FROM `trash`"
                cursor.execute(select)
                rows = cursor.fetchall()
                papper = []
                glass = []
                metal = []
                plastic = []
                food = []
                hygenic = []
                for row in rows:
                    papper.append(row['papper'])
                    glass.append(row['glass'])
                    metal.append(row['metal'])
                    plastic.append(row['plastic'])
                    food.append(row['food'])
                    hygenic.append(row['hygenic'])
                if self.trash_input.text.lower() in papper:
                    self.lbl_category.text = 'Макулатура'
                elif self.trash_input.text.lower() in glass:
                    self.lbl_category.text = 'Стекло'
                elif self.trash_input.text.lower() in metal:
                    self.lbl_category.text = 'Металл'
                elif self.trash_input.text.lower() in plastic:
                    self.lbl_category.text = 'Пластик'
                elif self.trash_input.text.lower() in food:
                    self.lbl_category.text = 'Пищевые отходы'
                elif self.trash_input.text.lower() in hygenic:
                    self.lbl_category.text = 'Средства личной гигиены'
                else:
                    self.lbl_category.text = 'Информация о категории мусора не найденa\nВы можете добавить её самостоятельно'
        except Exception as ex:
            self.lbl_category.text = 'Не удалось подключиться к базе данных\nПроверье подключение к интернету'
    def add_trash(self,instance):
        if self.trash_category_input.text.lower() == 'пластик':
            category = 'plastic'
        elif self.trash_category_input.text.lower() == 'макулатура':
            category = 'papper'
        elif self.trash_category_input.text.lower() == 'стекло':
            category = 'glass'
        elif self.trash_category_input.text.lower() == 'металл':
            category = 'metal'
        elif self.trash_category_input.text.lower() == 'средства личной гигиены':
            category = 'hygenic'
        elif self.trash_category_input.text.lower() == 'пищевые отходы':
            category = 'food'
        if self.trash_category_input.text.lower() in ['пластик', 'макулатура', 'стекло', 'средства личной гигиены',
                                                      'металл', 'пищевые отходы']:
            try:
                conn = pymysql.connect(
                    host='sql7.freesqldatabase.com',
                    port=3306,
                    user='sql7593829',
                    password='iTM51TCuM4',
                    database='sql7593829',
                    cursorclass=pymysql.cursors.DictCursor)
                with conn:
                    with conn.cursor() as cursor:
                        # Create a new record
                        sql = f"INSERT INTO `trash` ({category}) VALUES (%s)"
                        cursor.execute(sql, (self.trash_input.text.lower()))

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                    conn.commit()
            except Exception as ex:
                self.lbl_category.text = 'Не удалось подключиться к базе данных\nПроверьте работу VPN'
        else:
            self.lbl_category.text = 'Укажите правильно категорию'

    def build(self):
        mainbl = BoxLayout(orientation='horizontal',spacing=15,padding=25)
        bl_map = BoxLayout(orientation = 'vertical',padding=25, spacing=15)
        bl_sort = BoxLayout(orientation='vertical', padding=25, spacing=15)
        bl_labels = BoxLayout(orientation = 'vertical')
        bl_inputs = BoxLayout(orientation = 'horizontal',size_hint=(1,.15), spacing = 10)
        bl_buttons = BoxLayout(orientation = 'vertical', spacing = 5)
        bl_labels_trash = BoxLayout(orientation = 'vertical')
        bl_inputs_trash = BoxLayout(orientation='horizontal', size_hint=(1, .15), spacing=10)
        bl_buttons_trash = BoxLayout(orientation = 'vertical', spacing = 5)
        self.lbl_category = Label(text='Введите название мусора')
        self.lbl_status = Label(text='',font_size=32, halign='center')
        self.lbl_categories = Label(text='Доступные категории:•макулатура\n•стекло\n•металл\n•пластик\n•пищевые•отходы\n•средства личной гигиены', font_size=16)
        bl_labels.add_widget(self.lbl_status)
        bl_labels.add_widget(self.lbl_categories)
        self.lat_input = TextInput(text='', hint_text='Широта')
        self.lon_input = TextInput(text='', hint_text='Долгота')
        self.trash_input = TextInput(text='', hint_text='Мусор')
        self.trash_category_input = TextInput(text='', hint_text='Категория')
        self.category_input = TextInput(text='', hint_text='Пластик, стекло...')
        bl_inputs.add_widget(self.lat_input)
        bl_inputs.add_widget(self.lon_input)
        bl_inputs.add_widget(self.category_input)
        self.add_button = Button(text='Добавить координаты', on_press=self.add_cordinates)
        self.open_map_btn = Button(text='Открыть карту', on_press=self.parse_coordinates)
        self.add_trash_btn = Button(text='Добавить вид мусора', on_press=self.add_trash)
        self.get_category_btn = Button(text='Узнать категорию', on_press=self.get_category)
        bl_buttons.add_widget(self.add_button)
        bl_buttons.add_widget(self.open_map_btn)
        bl_buttons_trash.add_widget(self.get_category_btn)
        bl_buttons_trash.add_widget(self.add_trash_btn)
        bl_map.add_widget(bl_labels)
        bl_map.add_widget(bl_inputs)
        bl_map.add_widget(bl_buttons)
        bl_labels_trash.add_widget(self.lbl_category)
        bl_inputs_trash.add_widget(self.trash_input)
        bl_inputs_trash.add_widget(self.trash_category_input)
        bl_sort.add_widget(bl_labels_trash)
        bl_sort.add_widget(bl_inputs_trash)
        bl_sort.add_widget(bl_buttons_trash)
        mainbl.add_widget(bl_map)
        mainbl.add_widget(bl_sort)

        return mainbl
if __name__ == "__main__":
    MyApp().run()