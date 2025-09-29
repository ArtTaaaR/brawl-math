from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from game_classes import StartScreen, DifficultyScreen, GameScreen, HiscoreScreen

class MultiplicationGame(App):
    def build(self):
        self.title = "BRAWL MATH - Battle of Numbers!"
        
        # Примусове оновлення кольорів
        Window.clearcolor = (0.0, 0.0, 0.0, 1.0)  # Чорний фон
        
        self.sm = ScreenManager()
        
        # Створюємо екрани
        self.start_screen = StartScreen(name='start')
        self.difficulty_screen = DifficultyScreen(name='difficulty')
        self.game_screen = GameScreen(name='game')
        self.hiscore_screen = HiscoreScreen(name='hiscore')
        
        # Додаємо екрани до менеджера
        self.sm.add_widget(self.start_screen)
        self.sm.add_widget(self.difficulty_screen)
        self.sm.add_widget(self.game_screen)
        self.sm.add_widget(self.hiscore_screen)
        
        return self.sm

if __name__ == '__main__':
    MultiplicationGame().run()