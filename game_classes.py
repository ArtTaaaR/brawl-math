from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App
import random
import json
import os
import time

class RoundedButton(Button):
    """Кнопка з закругленими кутами"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()
    
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[20, 20, 20, 20]  # Закруглені кути
            )

# Імпорт pygame для аудіо
try:
    import pygame
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except:
    AUDIO_AVAILABLE = False

# Константи в стилі Brawl Stars (яскраві RGBA кольори)
BG = (0.0, 0.0, 0.0, 1.0)  # Чорний фон
TXT = (1.0, 1.0, 1.0, 1.0)  # Білий текст
BTN_BLUE = (0.0, 0.5, 1.0, 1.0)  # Яскраво-синій
BTN_ORANGE = (1.0, 0.5, 0.0, 1.0)  # Яскраво-помаранчевий
BTN_RED = (1.0, 0.0, 0.0, 1.0)  # Яскраво-червоний
BTN_GREEN = (0.0, 1.0, 0.0, 1.0)  # Яскраво-зелений
BTN_PURPLE = (0.5, 0.0, 1.0, 1.0)  # Фіолетовий
BTN_YELLOW = (1.0, 1.0, 0.0, 1.0)  # Яскраво-жовтий
BTN_PINK = (1.0, 0.0, 0.5, 1.0)  # Рожевий

# Додаткові кольори для ефектів
GRADIENT_START = (0.0, 0.5, 1.0, 1.0)  # Яскраво-синій
GRADIENT_END = (1.0, 0.0, 0.5, 1.0)  # Рожевий
SHADOW_COLOR = (0.0, 0.0, 0.0, 1.0)  # Тінь

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        # Примусове оновлення кольорів
        from kivy.core.window import Window
        Window.clearcolor = (0.0, 0.0, 0.0, 1.0)  # Чорний фон
        
        # Основний контейнер
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Заголовок в стилі Brawl Stars
        title = Label(
            text='[b]BRAWL MATH[/b]', 
            font_size='36sp', 
            color=(1.0, 1.0, 1.0, 1),  # Білий текст
            size_hint_y=0.25,
            halign='center',
            markup=True
        )
        title.bind(size=title.setter('text_size'))
        main_layout.add_widget(title)
        
        # Підзаголовок
        subtitle = Label(
            text='Battle of Numbers!', 
            font_size='18sp', 
            color=(0.8, 0.8, 0.8, 1),  # Світло-сірий
            size_hint_y=0.1,
            halign='center'
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        main_layout.add_widget(subtitle)
        
        # Кнопки в стилі Brawl Stars
        btn_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.6)
        
        # Кнопка GO (яскраво-зелена)
        go_btn = RoundedButton(
            text='GO BATTLE!', 
            font_size='26sp',
            size_hint_y=0.3,
            background_color=BTN_GREEN,  # Використовуємо константу
            color=(0, 0, 0, 1),  # Чорний текст
            bold=True
        )
        go_btn.bind(on_press=self.start_multiplication_mode)
        
        # Кнопка Difficult (яскраво-помаранчева)
        difficult_btn = RoundedButton(
            text='DIFFICULTY', 
            font_size='26sp',
            size_hint_y=0.3,
            background_color=BTN_ORANGE,  # Використовуємо константу
            color=(0, 0, 0, 1),  # Чорний текст
            bold=True
        )
        difficult_btn.bind(on_press=self.go_to_difficulty)
        
        # Кнопка Hiscore (яскраво-синя)
        hiscore_btn = RoundedButton(
            text='HISCORE', 
            font_size='26sp',
            size_hint_y=0.3,
            background_color=BTN_BLUE,  # Використовуємо константу
            color=(1, 1, 1, 1),  # Білий текст
            bold=True
        )
        hiscore_btn.bind(on_press=self.go_to_hiscore)
        
        btn_layout.add_widget(go_btn)
        btn_layout.add_widget(difficult_btn)
        btn_layout.add_widget(hiscore_btn)
        
        main_layout.add_widget(btn_layout)
        
        # Додаємо основний контейнер до екрану
        self.add_widget(main_layout)

    def go_to_difficulty(self, instance):
        self.manager.current = 'difficulty'
    
    def start_multiplication_mode(self, instance):
        """Запускає гру з налаштуваннями за замовчанням (вся таблиця)"""
        # Використовуємо всі числа таблиці множення
        selected_numbers = list(range(1, 11))
        
        # Переходимо до гри
        app = App.get_running_app()
        app.sm.current = 'game'
        app.sm.get_screen('game').set_difficulty(selected_numbers)

    def go_to_hiscore(self, instance):
        self.manager.current = 'hiscore'

class DifficultyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.difficulty_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.build()

    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Заголовок в стилі Brawl Stars
        title = Label(
            text='SELECT DIFFICULTY', 
            font_size='28sp', 
            color=(1.0, 1.0, 1.0, 1),  # Білий текст
            size_hint_y=0.15,
            halign='center',
            bold=True
        )
        title.bind(size=title.setter('text_size'))
        main_layout.add_widget(title)
        
        # Чекбокси в скролі
        scroll = ScrollView(size_hint=(1, 0.6))
        
        checkbox_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        checkbox_layout.bind(minimum_height=checkbox_layout.setter('height'))
        
        self.checkboxes = {}
        for i in range(1, 11):
            row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
            
            cb = CheckBox(active=True, size_hint_x=0.3)  # Всі активні по замовчанню
            self.checkboxes[i] = cb
            
            label = Label(
                text=f'Table {i}', 
                font_size='18sp', 
                color=(1.0, 1.0, 1.0, 1),  # Білий текст
                size_hint_x=0.7,
                halign='left',
                bold=True
            )
            label.bind(size=label.setter('text_size'))
            
            row.add_widget(cb)
            row.add_widget(label)
            checkbox_layout.add_widget(row)
        
        scroll.add_widget(checkbox_layout)
        main_layout.add_widget(scroll)
        
        # Кнопки
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.2)
        
        back_btn = RoundedButton(
            text='BACK', 
            font_size='22sp',
            background_color=BTN_RED,  # Використовуємо константу
            color=(1, 1, 1, 1),
            bold=True
        )
        back_btn.bind(on_press=self.go_back)
        
        start_btn = RoundedButton(
            text='START BATTLE!', 
            font_size='22sp',
            background_color=BTN_GREEN,  # Використовуємо константу
            color=(0, 0, 0, 1),  # Чорний текст
            bold=True
        )
        start_btn.bind(on_press=self.start_game)
        
        btn_layout.add_widget(back_btn)
        btn_layout.add_widget(start_btn)
        
        main_layout.add_widget(btn_layout)
        self.add_widget(main_layout)
        
        # Завантажуємо збережені налаштування складності
        self.load_difficulty_settings()

    def go_back(self, instance):
        self.manager.current = 'start'

    def start_game(self, instance):
        selected = [i for i, cb in self.checkboxes.items() if cb.active]
        if not selected:
            # Якщо нічого не вибрано, використовуємо всі числа
            selected = list(range(1, 11))
        
        # Зберігаємо налаштування складності
        self.save_difficulty_settings(selected)
        
        game_screen = self.manager.get_screen('game')
        game_screen.set_difficulty(selected)
        self.manager.current = 'game'
    
    def save_difficulty_settings(self, selected_numbers):
        """Зберігає налаштування складності в файл"""
        try:
            import json
            settings = {
                'selected_numbers': selected_numbers
            }
            with open('difficulty_settings.json', 'w') as f:
                json.dump(settings, f)
        except:
            pass
    
    def load_difficulty_settings(self):
        """Завантажує налаштування складності з файлу"""
        try:
            import json
            with open('difficulty_settings.json', 'r') as f:
                settings = json.load(f)
                selected_numbers = settings.get('selected_numbers', list(range(1, 11)))
                
                # Встановлюємо чекбокси
                for i in range(1, 11):
                    if i in self.checkboxes:
                        self.checkboxes[i].active = i in selected_numbers
        except:
            # Якщо файл не існує, залишаємо всі активними
            pass

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_task = 0
        self.total_tasks = 0
        self.mistakes = 0
        self.start_time = 0
        self.tasks = []
        self.difficulty_numbers = []
        self.build()
    
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Статус бар (як в оригіналі - зверху з жовтим фоном)
        self.status_layout = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=10)
        
        self.time_label = Label(text='⏱ 00:00', font_size='14sp', color=(1.0, 1.0, 1.0, 1), bold=True)  # Білий текст
        self.mistakes_label = Label(text='MISSES: 0', font_size='14sp', color=(1.0, 1.0, 1.0, 1), bold=True)  # Білий текст
        self.progress_label = Label(text='0/0', font_size='12sp', color=(1.0, 1.0, 1.0, 1), bold=True)  # Білий текст
        
        menu_btn = RoundedButton(text='MENU', font_size='12sp', background_color=BTN_BLUE, color=(1, 1, 1, 1), size_hint_x=0.3, bold=True)
        menu_btn.bind(on_press=self.go_to_menu)
        
        self.status_layout.add_widget(self.time_label)
        self.status_layout.add_widget(self.mistakes_label)
        self.status_layout.add_widget(self.progress_label)
        self.status_layout.add_widget(menu_btn)
        
        main_layout.add_widget(self.status_layout)
        
        # Завдання
        self.task_layout = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=20)
        
        self.task_label = Label(
            text='', 
            font_size='32sp', 
            color=BTN_GREEN,  # Зелений колір
            halign='center',
            bold=True
        )
        self.task_label.bind(size=self.task_label.setter('text_size'))
        
        self.answer_input = TextInput(
            text='', 
            font_size='24sp', 
            multiline=False, 
            size_hint_y=0.4,
            halign='center'
        )
        self.answer_input.bind(on_text_validate=self.submit_answer)
        
        self.task_layout.add_widget(self.task_label)
        self.task_layout.add_widget(self.answer_input)
        
        main_layout.add_widget(self.task_layout)
        
        # Клавіатура
        self.keypad_layout = GridLayout(cols=3, spacing=8, size_hint_y=0.5)
        
        # Цифри 1-9 (яскраво-сині кнопки в стилі Brawl Stars)
        for i in range(1, 10):
            btn = RoundedButton(
                text=str(i), 
                font_size='26sp',
                background_color=BTN_BLUE,  # Використовуємо константу
                color=(1, 1, 1, 1),  # Білий текст
                bold=True
            )
            btn.bind(on_press=self.append_digit)
            self.keypad_layout.add_widget(btn)
        
        # Кнопки внизу в стилі Brawl Stars
        clear_btn = RoundedButton(
            text='DEL', 
            font_size='20sp',  # Більший розмір
            background_color=BTN_RED,  # Використовуємо константу
            color=(1, 1, 1, 1),  # Білий текст
            bold=True
        )
        clear_btn.bind(on_press=self.clear_input)
        
        zero_btn = RoundedButton(
            text='0', 
            font_size='26sp',
            background_color=BTN_BLUE,  # Використовуємо константу
            color=(1, 1, 1, 1),  # Білий текст
            bold=True
        )
        zero_btn.bind(on_press=self.append_digit)
        
        enter_btn = RoundedButton(
            text='GO', 
            font_size='20sp',  # Більший розмір
            background_color=BTN_GREEN,  # Використовуємо константу
            color=(0, 0, 0, 1),  # Чорний текст
            bold=True
        )
        enter_btn.bind(on_press=self.submit_answer)
        
        self.keypad_layout.add_widget(clear_btn)
        self.keypad_layout.add_widget(zero_btn)
        self.keypad_layout.add_widget(enter_btn)
        
        main_layout.add_widget(self.keypad_layout)
        self.add_widget(main_layout)
    
    def set_difficulty(self, numbers):
        self.difficulty_numbers = numbers
        self.generate_tasks()
        self.start_game()
    
    def generate_tasks(self):
        self.tasks = []
        for A in self.difficulty_numbers:
            for _ in range(10):
                B = random.randint(1, 10)
                self.tasks.append((A, B, A * B))
        random.shuffle(self.tasks)
        self.total_tasks = len(self.tasks)
    
    def start_game(self):
        self.current_task = 0
        self.mistakes = 0
        self.start_time = time.time()
        self.show_task()
        self.update_timer()
    
    def show_task(self):
        if self.current_task < len(self.tasks):
            A, B, answer = self.tasks[self.current_task]
            self.task_label.text = f'{A} × {B} = ?'
            self.task_label.color = BTN_GREEN  # Зелений колір для питання
            self.answer_input.text = ''
            self.answer_input.focus = True
            self.update_progress()
    
    def append_digit(self, instance):
        digit = instance.text
        self.answer_input.text += digit
        if AUDIO_AVAILABLE:
            try:
                pygame.mixer.Sound("1 push.mp3").play()
            except:
                pass
    
    def clear_input(self, instance):
        self.answer_input.text = self.answer_input.text[:-1]
        if AUDIO_AVAILABLE:
            try:
                pygame.mixer.Sound("delete.mp3").play()
            except:
                pass
    
    def submit_answer(self, instance):
        try:
            answer = int(self.answer_input.text)
            A, B, correct = self.tasks[self.current_task]
            
            if answer == correct:
                # Правильна відповідь - без паузи, одразу наступне завдання
                self.current_task += 1
                self.update_progress()
                
                if self.current_task < len(self.tasks):
                    self.show_task()  # Одразу наступне завдання
                else:
                    self.end_game()
            else:
                # Помилка - пауза 5 секунд + показ правильної відповіді
                self.show_incorrect()
                self.mistakes += 1
                # НЕ збільшуємо current_task - завдання не зараховується як пройдене
                self.update_progress()
                
                # Додаємо це завдання в кінець списку для повторення
                A, B, correct = self.tasks[self.current_task]
                self.tasks.append((A, B, correct))
                
                Clock.schedule_once(lambda dt: self.show_task(), 5)  # Пауза 5 секунд
                
        except ValueError:
            pass
    
    def show_correct(self):
        self.task_label.text = 'PERFECT!'
        self.task_label.color = BTN_GREEN  # Використовуємо константу
        if AUDIO_AVAILABLE:
            try:
                pygame.mixer.Sound("answer.mp3").play()
            except:
                pass

    def show_incorrect(self):
        # Показуємо правильну відповідь
        A, B, correct = self.tasks[self.current_task]
        self.task_label.text = f'MISS! Correct: {A} × {B} = {correct}'
        self.task_label.color = BTN_RED  # Використовуємо константу
        if AUDIO_AVAILABLE:
            try:
                pygame.mixer.Sound("answer.mp3").play()
            except:
                pass
    
    def update_progress(self):
        self.progress_label.text = f'{self.current_task}/{self.total_tasks}'
        self.mistakes_label.text = f'MISSES: {self.mistakes}'
    
    def update_timer(self):
        if self.current_task < len(self.tasks):
            elapsed = time.time() - self.start_time
            
            # Прискорюємо час відповідно до складності
            accelerated_time = self.accelerate_time(elapsed)
            minutes = int(accelerated_time) // 60
            seconds = int(accelerated_time) % 60
            self.time_label.text = f'⏱ {minutes:02d}:{seconds:02d}'
            
            # Прискорюємо оновлення таймера відповідно до складності
            update_interval = self.get_update_interval()
            Clock.schedule_once(lambda dt: self.update_timer(), update_interval)
    
    def end_game(self):
        elapsed = time.time() - self.start_time
        
        # Розраховуємо справедливий час
        fair_time = self.calculate_fair_time(elapsed)
        minutes = int(fair_time) // 60
        seconds = int(fair_time) % 60
        
        result_text = f'BATTLE COMPLETE!\nTime: {minutes:02d}:{seconds:02d}\nMisses: {self.mistakes}'
        self.task_label.text = result_text
        self.task_label.color = BTN_ORANGE  # Використовуємо константу
        
        # Зберігаємо рекорд з справедливим часом
        self.save_high_score(fair_time)
        
        if AUDIO_AVAILABLE:
            try:
                pygame.mixer.Sound("End.mp3").play()
            except:
                pass
    
    def calculate_fair_time(self, real_time):
        """Розраховує справедливий час з урахуванням складності"""
        if not self.difficulty_numbers:
            return real_time
        
        # Коефіцієнт складності (кількість обраних чисел / 10)
        difficulty_coefficient = len(self.difficulty_numbers) / 10.0
        
        # Бонус за складність (середнє значення обраних чисел)
        complexity_bonus = sum(self.difficulty_numbers) / len(self.difficulty_numbers)
        
        # Формула: (Реальний час / коефіцієнт складності) - бонус за складність
        fair_time = (real_time / difficulty_coefficient) - complexity_bonus
        
        # Не може бути менше 0
        return max(0, fair_time)
    
    def accelerate_time(self, real_time):
        """Прискорює час відповідно до складності"""
        if not self.difficulty_numbers:
            return real_time
        
        # Коефіцієнт прискорення (кількість обраних чисел / 10)
        acceleration_coefficient = len(self.difficulty_numbers) / 10.0
        
        # Прискорюємо час
        accelerated_time = real_time / acceleration_coefficient
        
        return accelerated_time
    
    def get_update_interval(self):
        """Розраховує інтервал оновлення таймера відповідно до складності"""
        if not self.difficulty_numbers:
            return 1.0  # Звичайний інтервал
        
        # Коефіцієнт прискорення (кількість обраних чисел / 10)
        acceleration_coefficient = len(self.difficulty_numbers) / 10.0
        
        # Прискорюємо оновлення (менший інтервал = швидше оновлення)
        update_interval = 1.0 * acceleration_coefficient
        
        return max(0.1, update_interval)  # Мінімум 0.1 секунди
    
    def save_high_score(self, fair_time):
        """Зберігає рекорд з справедливим часом"""
        try:
            # Завантажуємо існуючі рекорди
            try:
                with open('leaderboard.json', 'r') as f:
                    scores = json.load(f)
            except:
                scores = []
            
            # Додаємо новий рекорд
            scores.append({
                'time': fair_time,
                'mistakes': self.mistakes,
                'difficulty': self.difficulty_numbers.copy() if self.difficulty_numbers else list(range(1, 11))
            })
            
            # Сортуємо за часом (кращі результати першими)
            scores.sort(key=lambda x: x['time'])
            
            # Зберігаємо тільки топ-10
            scores = scores[:10]
            
            # Зберігаємо в файл
            with open('leaderboard.json', 'w') as f:
                json.dump(scores, f)
                
        except:
            pass
    
    def go_to_menu(self, instance):
        self.manager.current = 'start'

class HiscoreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(
            text='HALL OF FAME', 
            font_size='28sp', 
            color=(1.0, 1.0, 1.0, 1),  # Білий текст
            size_hint_y=0.2,
            halign='center',
            bold=True
        )
        title.bind(size=title.setter('text_size'))
        main_layout.add_widget(title)
        
        self.scores_label = Label(
            text='No battles yet!', 
            font_size='20sp', 
            color=(1.0, 1.0, 1.0, 1),  # Білий текст
            size_hint_y=0.6,
            halign='center',
            bold=True
        )
        self.scores_label.bind(size=self.scores_label.setter('text_size'))
        main_layout.add_widget(self.scores_label)
        
        back_btn = RoundedButton(
            text='BACK TO BATTLE', 
            font_size='22sp',
            background_color=BTN_BLUE,  # Використовуємо константу
            color=(1, 1, 1, 1),  # Білий текст
            size_hint_y=0.2,
            bold=True
        )
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
        
        # Завантажуємо рекорди
        self.load_scores()

    def load_scores(self):
        """Завантажує та відображає рекорди"""
        try:
            with open('leaderboard.json', 'r') as f:
                scores = json.load(f)
            
            if not scores:
                self.scores_label.text = 'No battles yet!'
                return
            
            # Формуємо текст рекордів
            score_text = ""
            for i, score in enumerate(scores, 1):
                time_seconds = score['time']
                minutes = int(time_seconds) // 60
                seconds = int(time_seconds) % 60
                mistakes = score['mistakes']
                difficulty = score.get('difficulty', list(range(1, 11)))
                
                # Форматуємо складність
                if len(difficulty) == 10:
                    diff_text = "Full Table"
                else:
                    diff_text = f"Tables: {', '.join(map(str, sorted(difficulty)))}"
                
                score_text += f"{i}. {minutes:02d}:{seconds:02d} ({mistakes} misses) - {diff_text}\n"
            
            self.scores_label.text = score_text
            
        except:
            self.scores_label.text = 'No battles yet!'

    def go_back(self, instance):
        self.manager.current = 'start'