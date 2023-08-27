# for useing PyQt5, you need to install PyQt5
# pip install PyQt5

# Jjamppong Marble

import sys
import random
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QImage
from PyQt6.QtCore import QTimer

class DiceRollerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.setFixedSize(640, 550)

    def init_ui(self):
        self.setWindowTitle('주사위 던지기')

        self.background_image = QImage('board.png')  # 바탕 이미지 파일 경로
        self.dice_image = QPixmap('dice.png')
        self.dice_position = (100, 100)  # 주사위 시작 위치 (x, y)
        self.dice_size = (100, 100)  # 주사위 크기 (width, height)

        self.button = QtWidgets.QPushButton(self)
        self.button.setText('던지기')
        self.button.setMinimumWidth(150)
        self.button.setMinimumHeight(50)
        self.button.move(int(640 / 2 - 150 / 2), 480)
        self.button.clicked.connect(self.roll_animation)

        # layout = QVBoxLayout()
        # layout.addWidget(self.button)
        # self.setLayout(layout)

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_dice)
        self.animation_frames = []
        for i in range(1, 7):
            self.animation_frames.append(QPixmap(f'dice_{i}.png'))
        self.animation_index = 0

    def roll_animation(self):
        self.animation_index = 0
        self.animation_timer.start(100)  # 주사위 애니메이션 속도 (밀리초)

    def animate_dice(self):
        if self.animation_index < len(self.animation_frames):
            self.update()  # 화면 갱신을 요청하여 주사위 위치 업데이트
            self.animation_index += 1
        else:
            self.animation_timer.stop()
            self.show_result()

    def show_result(self):
        roll_result = random.randint(1, 6)
        self.result_dice_image = QPixmap(f'dice_{roll_result}.png')
        self.update()  # 화면 갱신을 요청하여 결과 주사위 이미지 표시

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.background_image)  # 바탕 이미지 표시

        if self.animation_index < len(self.animation_frames):
            frame = self.animation_frames[self.animation_index]
            painter.drawPixmap(*self.dice_position, *self.dice_size, frame)
        elif hasattr(self, 'result_dice_image'):
            painter.drawPixmap(*self.dice_position, *self.dice_size, self.result_dice_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiceRollerApp()
    window.show()
    # app.exec()
    sys.exit(app.exec())
