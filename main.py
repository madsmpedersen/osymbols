from kivy.metrics import cm
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from language import text
from data import ISOM2017_2, symbols, ISSprOM2019, get_image_path
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.graphics import BorderImage
from kivy.core.window import Window
from kivy.app import App
import kivy
import os
import random
import sys

w, h = 1280, 1720

w, h, dpi = 1080, 2160, 427  # fairphone 3
# w, h, dpi = 1200, 1920, 224  # samsung tablet
#w, h = 1440, 2960
#dpi = 427
#size = '1280x1720'
#dpi = 529
s1 = 2.2
s2 = 2.2
if sys.argv[0] == 'C:\\mmpe\\Privat\\okr\\OSynbols\\main.py':
    sys.argv += [f'--size={int(w/s1)}x{int(h/s1)}', f'--dpi={dpi/s2}']


kivy.require('1.9.0')
Window.clearcolor = (1, 1, 1, 1)
# print(Window.height)
#Window.size = (1000, max(800, Window.height))


Window.top = 50
Window.left = 50


class Settings():
    def __init__(self):
        self.language = 'Dansk'
        self.wrong_again = True


settings = Settings()


class Answer(BoxLayout):
    status_source = StringProperty('graphics/white.png')
    symbol_source = StringProperty('graphics/white.png')

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Answer, self).__init__(orientation='horizontal', **kwargs)

    def set_nr(self, norm, nr):
        self.nr = nr
        self.text = text[settings.language]['Symbol names'][norm].get(nr, 'Mangler')
        self.ids.symbolImage.source = get_image_path(norm, nr)
        self.set_status(None, False)

    def set_status(self, status, show_text):
        if status is None:
            self.ids.statusImage.source = 'graphics/white.png'
        else:
            self.ids.statusImage.source = ['graphics/wrong.png', 'graphics/correct.png'][status]
        self.ids.symbolLabel.text = ("", self.text)[show_text]


class ResultContents(FloatLayout):
    def __init__(self, result, **kwargs):
        FloatLayout.__init__(self, **kwargs)
        self.ids.resultLabel.text = 'Du har svaret rigtigt på\n %d ud af %d' % result


class QuizScreen(Screen):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(QuizScreen, self).__init__(**kwargs)
        self.answers = [self.ids[f'answer{i}'] for i in range(1, 6)]

    def start(self, language, norm, nr_lst):
        self.nr_lst = nr_lst
        self.ids['quiz_ProgressBar'].max = len(nr_lst)
        self.ids['quiz_ProgressBar'].value = 0
        self.norm = norm
        self.set_result(0, 0)
        self.next_question()

    def next_question(self):
        if self.nr_lst:

            norm = self.norm
            self.nr = nr = self.nr_lst.pop()
            self.ids.questionLabel.text = text[settings.language]['Symbol names'][norm][nr]
            # let's add a Widget to this layout
            alternatives = list(set(symbols[norm][nr]) - {nr})
            random.shuffle(alternatives)
            alternatives = alternatives[:4] + [nr]
            random.shuffle(alternatives)

            for alternative, answer in zip(alternatives, self.answers):
                answer.set_nr(norm, alternative)
                # if alternative == nr:
                #    self.correct_answer = answer
            self.ids.nextButton.disabled = True
            self.ids.nextButton.opacity = 0
        else:
            self.show_result()

    def show_result(self):
        resultContents = ResultContents(self.result)  # Create a new instance of the P class

        popupWindow = Popup(
            title="Velkommen i mål", content=resultContents,
            title_size=NumericProperty(14),
            size_hint=(None, None), size=(cm(4), cm(3)))

        resultContents.ids.closeButton.bind(on_press=popupWindow.dismiss)
        popupWindow.bind(on_dismiss=self.back)

        popupWindow.open()  # show the popup

    def back(self, *args, **kwargs):
        self.manager.current = 'settings'

    def on_touch_down(self, touch):
        if self.ids.nextButton.disabled:
            for answer in self.answers:
                if answer.ids.symbolImage.collide_point(touch.x, touch.y):
                    for an in self.answers:
                        if an == answer:
                            self.set_result(self.result[0] + int(an.nr == self.nr), self.result[1] + 1)
                            if an.nr != self.nr and settings.wrong_again:
                                self.nr_lst.insert(0, self.nr)
                        if an.nr == self.nr:
                            an.set_status(True, True)
                        elif an == answer:
                            an.set_status(False, True)
                        else:
                            an.set_status(None, True)
                    self.ids.nextButton.disabled = False
                    self.ids.nextButton.opacity = 1
                    return
        Screen.on_touch_down(self, touch)

    def set_result(self, correct, total):
        self.result = (correct, total)
        # self.ids.resultLabel.text = f'%d/%d' % self.result
        self.ids['quiz_ProgressBar'].value = self.result[0]


class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        self.set_categories()

    def set_categories(self):
        txt = self.ids.normSpinner.text
        categories = list(text[settings.language]['Categories'][txt].keys())
        self.ids.categorySpinner.text = categories[0]
        self.ids.categorySpinner.values = categories

    def set_N_options(self):
        norm = self.ids.normSpinner.text
        txt = self.ids.categorySpinner.text
        self.ids.nSpinner.disabled = (txt == 'Vælg')
        if txt != 'Vælg':
            max_N = len(text[settings.language]['Categories'][norm][txt])
            if max_N > 20:
                n_lst = [5] + sorted(list(range(10, max_N + 1, 10)) + [max_N])
            else:
                n_lst = sorted(list(range(5, max_N + 1, 5)) + [max_N])
            self.ids.nSpinner.values = map(str, n_lst)
            self.ids.nSpinner.text = str(n_lst[0])

    def start(self, *args, **kwargs):
        self.manager.current = 'quiz'
        language = self.ids.languageSpinner.text
        norm = self.ids.normSpinner.text
        category = self.ids.categorySpinner.text
        N = int(self.ids.nSpinner.text)
        nr_lst = text[language]['Categories'][norm][category]
        random.shuffle(nr_lst)
        nr_lst = nr_lst[:N]
        self.manager.quiz.start(language, norm, nr_lst)



class OSymbolsApp(App):

    def build(self):
        sm = ScreenManager()
        sm.settings = SettingsScreen(name='settings')
        sm.add_widget(sm.settings)
        sm.quiz = QuizScreen(name='quiz')
        sm.add_widget(sm.quiz)

        # sm.current = 'quiz'
        # sm.quiz.start(language='Dansk', norm=ISOM2017_2, nr_lst=[408])
        return sm


if __name__ == '__main__':
    OSymbolsApp().run()
