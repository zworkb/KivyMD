"""
MDDropDownItem
==============

Copyright (c) 2015 Andrés Rodríguez and KivyMD contributors -
    KivyMD library up to version 0.1.2
Copyright (c) 2019 Ivanov Yuri and KivyMD contributors -
    KivyMD library version 0.1.3 and higher

For suggestions and questions:
<kivydevelopment@gmail.com>

This file is distributed under the terms of the same license,
as the Kivy framework.

Example
-------

from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.lang import Builder

from kivymd.theming import ThemeManager

Builder.load_string(
    '''
#:import toast kivymd.toast.toast
#:import MDComboBox kivymd.uix.combobox.MDComboBox


<MyRoot@BoxLayout>
    orientation: 'vertical'

    MDToolbar:
        title: "Test MDDropDownItem"
        md_bg_color: app.theme_cls.primary_color
        elevation: 10
        left_action_items: [['menu', lambda x: x]]

    FloatLayout:

        MDComboBox:

            id: dropdown_item
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            size_hint:(None, None)
            items: app.items
            # dropdown_bg: [1, 1, 1, 1]

        MDRaisedButton:
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            text: 'Check Item'
            on_release: toast(dropdown_item.text)
''')


class Test(MDApp):

    def build(self):
        self.items = [f"Item {i}" for i in range(50)]
        return Factory.MyRoot()


Test().run()
"""

import copy

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dropdownitem import MDDropDownItemBehavior
from kivymd.uix.menu import MDDropdownMenu

Builder.load_string("""
<MDComboBox>:
    label_item:label_item
    canter:False
    MDTextField:
        id:label_item
        width:root.width
        pos:root.pos
""")


class MDComboBox(MDDropDownItemBehavior, BoxLayout):
    """"""
    items_unfiltered = ListProperty()
    """
    all items without filter before filtering
    """

    case_sensitive = BooleanProperty(False)
    """shall the matching between edit field
    and the menu items be case sensitive?
    """

    def __init__(self,  **kw):
        super().__init__(**kw)
        self.dropdown_bg = App.get_running_app().theme_cls.bg_normal
        Clock.schedule_once(self.after_init)

    def after_init(self, *a):
        self.label_item.bind(text=self.on_text)
        self.items_unfiltered = copy.copy(self.items)

    def on_text(self, _, text):
        # self._drop_list.filter = text
        if self.case_sensitive:
            self.items = [item for item in self.items_unfiltered if item.startswith(text)]
        else:
            self.items = [item for item in self.items_unfiltered if item.lower().startswith(text)]


    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if (self.collide_point(touch.x, touch.y) or self.label_item.collide_point(*touch.pos)) \
                and self._list_menu:

            self._drop_list = MDDropdownMenu(
                _center=False,
                items=self._list_menu,
                background_color=self.dropdown_bg,
                max_height=self.dropdown_max_height,
                width_mult=self.dropdown_width_mult,
                width_rectangle=1,
                anim_duration=0,
            )
            self._drop_list.open(self)

    def on_items(self, instance, value):
        _list_menu = []
        for name_item in value:
            _list_menu.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": name_item,
                    "text_color": self.theme_cls.text_color,
                    "theme_text_color": "Custom",
                    "on_release": lambda x=name_item: self.set_item(x),
                }
            )
        self._list_menu = _list_menu
        self.current_item = self.ids.label_item.text
        if self._drop_list is not None:
            self._drop_list.items = self._list_menu
            self._drop_list.display_menu(self)
