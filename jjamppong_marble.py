# This game needs PyQt6
# pip install PyQt6

# Jjamppong Marble
import sys
import random
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QDialog
from PyQt6.QtGui import QPixmap, QPainter, QImage
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class PopupDiceWindow(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)

    self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)  # 타이틀 없는 창으로 설정

    popup_width = 200
    popup_height = 100

    parent_geometry = parent.geometry() if parent else QApplication.desktop().availableGeometry()

    popup_x = (parent_geometry.width() - popup_width) // 2 + parent_geometry.left()
    popup_y = (parent_geometry.height() - popup_height) // 2 + parent_geometry.top() - 40

    self.setGeometry(popup_x, popup_y, popup_width, popup_height)

    layout = QVBoxLayout(self)
    label = QLabel(self)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    font = QFont("Arial", 36, QFont.Weight.Bold)
    label.setFont(font)

    self.dice_number = random.randint(1, 6)

    random_number = str(self.dice_number)
    label.setText(random_number)  # 랜덤한 숫자 설정

    layout.addWidget(label)

    # 타이머 설정
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.on_close)
    self.timer.start(2000)  # 2초 (2000 밀리초) 후에 타이머가 만료됨
    
  def on_close(self):
    self.close()
    self.parent().on_dice_number(self.dice_number)

class PopupShowingCardImageWindow(QDialog):
  def __init__(self, pixmap, parent=None):
    super().__init__(parent)

    self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)  # 타이틀 없는 창으로 설정

    popup_width = pixmap.width()
    popup_height = pixmap.height()

    parent_geometry = parent.geometry() if parent else QApplication.desktop().availableGeometry()

    popup_x = (parent_geometry.width() - popup_width) // 2 + parent_geometry.left()
    popup_y = (parent_geometry.height() - popup_height) // 2 + parent_geometry.top() - 40

    self.setGeometry(popup_x, popup_y, popup_width, popup_height)

    layout = QVBoxLayout(self)
    label = QLabel(self)
    
    label.setPixmap(pixmap)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(label)

    confirm_button = QPushButton("확인", self)
    confirm_button.clicked.connect(self.close)
    layout.addWidget(confirm_button)

class PopupShowingWinderWindow(QDialog):
  def __init__(self, pixmap, parent=None):
    super().__init__(parent)

    self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)  # 타이틀 없는 창으로 설정

    popup_width = 300
    popup_height = 200

    parent_geometry = parent.geometry() if parent else QApplication.desktop().availableGeometry()

    popup_x = (parent_geometry.width() - popup_width) // 2 + parent_geometry.left()
    popup_y = (parent_geometry.height() - popup_height) // 2 + parent_geometry.top() - 40

    self.setGeometry(popup_x, popup_y, popup_width, popup_height)

    layout = QVBoxLayout(self)

    text_label = QLabel(self)
    text_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    font = QFont("Arial", 36, QFont.Weight.Bold)
    text_label.setFont(font)
    text_label.setText("우승!")  # 랜덤한 숫자 설정
    layout.addWidget(text_label)
    
    image_label = QLabel()
    image_label.setPixmap(pixmap)
    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(image_label)

    confirm_button = QPushButton("확인", self)
    confirm_button.clicked.connect(self.close)
    layout.addWidget(confirm_button)

class JjamppongMarbleApp(QWidget):
  def __init__(self):
    super().__init__()

    self.setFixedSize(640, 550)

    self.board_size = {
      'cx': 640,
      'cy': 445
    }

    # Game Data
    self.board_table_position = [
      [85,	75], [175,	68], [235, 110], [309, 100], [380, 98], 
      [450, 102], [506, 102], [578, 107], [518, 169], [513, 213], 
      [438, 225], [352, 242], [280, 241], [222, 222], [163, 213], 
      [108, 208], [122, 279], [111, 337], [162, 352], [220, 371], 
      [281, 319], [347, 358], [409, 367], [461, 358], [546, 320]
    ]

    self.card_infos = [
      None, QPixmap('images/003.png'), QPixmap('images/004.png'), QPixmap('images/005.png'), None, 
      QPixmap('images/006.png'), QPixmap('images/007.png'), QPixmap('images/008.png'), QPixmap('images/009.png'), None, 
      QPixmap('images/010.png'), QPixmap('images/011.png'), QPixmap('images/012.png'), None, None,
      QPixmap('images/013.png'), QPixmap('images/015.png'), None, None, QPixmap('images/016.png'),
      QPixmap('images/014.png'), None, QPixmap('images/002.png'), QPixmap('images/001.png'), None
    ]

    self.player_images = [
      QPixmap('images/player1.png'), QPixmap('images/player2.png'), QPixmap('images/player3.png')
    ]

    self.player_position = [
      0, 0, 0
    ]

    self.max_player_num = 3
    self.current_player = 0

    self.init_ui()

  def reset_game(self):
    self.current_player = 0
    
    self.player_position = [
      0, 0, 0
    ]

  def init_ui(self):
    self.setWindowTitle('주사위 던지기')

    self.background_image = QImage('images/board.png')  # 바탕 이미지 파일 경로
    self.dice_image = QPixmap('dice.png')
    self.dice_position = (100, 100)  # 주사위 시작 위치 (x, y)
    self.dice_size = (100, 100)  # 주사위 크기 (width, height)

    self.current_player_label = QLabel(self)
    self.current_player_label.setText("현재 플레이어: ")
    self.current_player_label.move(20, 495)

    self.throw_dice_button = QtWidgets.QPushButton(self)
    self.throw_dice_button.setText('던지기')
    self.throw_dice_button.setStyleSheet("background-color: green; font-weight: bold;")  # 버튼 색상 변경
    self.throw_dice_button.setMinimumWidth(150)
    self.throw_dice_button.setMinimumHeight(50)
    self.throw_dice_button.move((self.board_size['cx'] // 2 - 150 // 2), 480)
    self.throw_dice_button.clicked.connect(self.on_throw_dice)

    self.restart_button = QtWidgets.QPushButton(self)
    self.restart_button.setText('다시 시작')
    self.restart_button.setStyleSheet("background-color: #A30000; color: white; font-weight: bold;")  # 버튼 색상 변경
    self.restart_button.setMinimumWidth(150)
    self.restart_button.setMinimumHeight(50)
    self.restart_button.move((self.board_size['cx'] // 2 - 150 // 2) + 200, 480)
    self.restart_button.clicked.connect(self.on_restart_game)

  def on_restart_game(self):
    self.reset_game()
    self.update()

  def on_throw_dice(self):
    if self.player_position[0] == len(self.board_table_position):
      # Game over
      return

    popup = PopupDiceWindow(self)
    popup.exec()  # 모달 다이얼로그로 표시

  def on_dice_number(self, dice_number):
    self.player_position[self.current_player] = self.player_position[self.current_player] + dice_number

    if self.player_position[self.current_player] >= len(self.board_table_position):
        self.player_position[self.current_player] = len(self.board_table_position) - 1

        popup = PopupShowingWinderWindow(self.player_images[self.current_player], self)
        popup.exec()

        self.reset_game()
    else:
      if self.card_infos[self.player_position[self.current_player]] != None:
        popup = PopupShowingCardImageWindow(self.card_infos[self.player_position[self.current_player]], self)
        popup.exec()

      self.current_player = (self.current_player + 1) % self.max_player_num

    self.update()

  def draw_background(self, painter):
    painter.drawImage(0, 0, self.background_image)  # 바탕 이미지 표시

  def draw_players(self, painter):
    offset_pos = [
      [-6, -1], [0, -4], [4, 2]
    ]
    for i, player in enumerate(self.player_position):
      draw_pos = self.board_table_position[player]

      painter.drawPixmap(
        draw_pos[0] - self.player_images[i].width() // 2 + offset_pos[i][0],
        draw_pos[1] - self.player_images[i].height() // 2 + offset_pos[i][1], 
        self.player_images[i].width(), self.player_images[i].height(), self.player_images[i])
      
      painter.drawPixmap(
        100, 480, 
        self.player_images[self.current_player].width(), self.player_images[self.current_player].height(), 
        self.player_images[self.current_player])

  def paintEvent(self, event):
    painter = QPainter(self)

    self.draw_background(painter)
    self.draw_players(painter)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = JjamppongMarbleApp()
  window.show()

  # app.exec()
  sys.exit(app.exec())
