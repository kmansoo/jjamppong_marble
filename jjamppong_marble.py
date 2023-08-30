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
    popup_y = (parent_geometry.height() - popup_height) // 2 + parent_geometry.top()

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
    self.player_position = [
      0, 0, 0
    ]

  def init_ui(self):
    self.setWindowTitle('주사위 던지기')

    self.background_image = QImage('images/board.png')  # 바탕 이미지 파일 경로
    self.dice_image = QPixmap('dice.png')
    self.dice_position = (100, 100)  # 주사위 시작 위치 (x, y)
    self.dice_size = (100, 100)  # 주사위 크기 (width, height)

    self.start_button = QtWidgets.QPushButton(self)
    self.start_button.setText('다시 시작')
    self.start_button.setMinimumWidth(150)
    self.start_button.setMinimumHeight(50)
    self.start_button.move(int(self.board_size['cx'] / 2 - 150 / 2) - 200, 480)
    self.start_button.clicked.connect(self.on_start_game)

    self.throw_dice_button = QtWidgets.QPushButton(self)
    self.throw_dice_button.setText('던지기')
    self.throw_dice_button.setMinimumWidth(150)
    self.throw_dice_button.setMinimumHeight(50)
    self.throw_dice_button.move(int(self.board_size['cx'] / 2 - 150 / 2), 480)
    self.throw_dice_button.clicked.connect(self.roll_animation)

    self.animation_timer = QTimer(self)
    self.animation_timer.timeout.connect(self.animate_dice)
    self.animation_frames = []

    for i in range(1, 7):
      self.animation_frames.append(QPixmap(f'dice_{i}.png'))

    self.animation_index = 0

  def on_start_game(self):
    self.reset_game()

  def roll_animation(self):
    if self.player_position[0] == len(self.board_table_position):
      # Game over
      return

    popup = PopupDiceWindow(self)
    popup.exec()  # 모달 다이얼로그로 표시

  def on_dice_number(self, dice_number):
    self.player_position[self.current_player] = self.player_position[self.current_player] + dice_number

    self.current_player = (self.current_player + 1) % self.max_player_num
    
    self.update()

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

  def draw_background(self, painter):
    painter.drawImage(0, 0, self.background_image)  # 바탕 이미지 표시

  def draw_players(self, painter):
    for i, player in enumerate(self.player_position):
      draw_pos = self.board_table_position[player]

      draw_pos[0] = draw_pos[0] - self.player_images[i].width() // 2
      draw_pos[1] = draw_pos[1] - self.player_images[i].height() // 2

      painter.drawPixmap(*draw_pos, 
      self.player_images[i].width(), self.player_images[i].height(), self.player_images[i])

  def draw_dice(self, painter):
    painter.drawPixmap(*self.dice_position, *self.dice_size, self.dice_image)

  def draw_cards(self, painter):
    player_pos = self.player_position[0]
    board_pos = self.board_table_position[player_pos]

    if self.card_infos[player_pos] != None:
      x = int(self.board_size['cx'] / 2 - self.card_infos[player_pos].width() / 2)
      y = int(self.board_size['cy'] / 2 - self.card_infos[player_pos].height() / 2)

      painter.drawPixmap(x, y, self.card_infos[player_pos].width(), self.card_infos[player_pos].height(), self.card_infos[player_pos])
    pass

  def paintEvent(self, event):
    painter = QPainter(self)

    self.draw_background(painter)
    self.draw_players(painter)
    self.draw_dice(painter)
    self.draw_cards(painter)

    # painter.drawImage(0, 0, self.background_image)  # 바탕 이미지 표시

    # if self.animation_index < len(self.animation_frames):
    #   frame = self.animation_frames[self.animation_index]
    #   painter.drawPixmap(*self.dice_position, *self.dice_size, frame)
    # elif hasattr(self, 'result_dice_image'):
    #   painter.drawPixmap(*self.dice_position, *self.dice_size, self.result_dice_image)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = JjamppongMarbleApp()
  window.show()

  # app.exec()
  sys.exit(app.exec())
