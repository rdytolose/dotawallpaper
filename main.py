import sys
import os
import shutil
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QHBoxLayout, QFileDialog, QLineEdit, QLabel, QProgressBar
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from moviepy.video.io.VideoFileClip import VideoFileClip


class FileDialogApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("dota2wallpaper")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout()

        self.file_path = QLineEdit(self)
        self.layout.addWidget(self.file_path)

        self.file_button = QPushButton("Обзор (видео файл)", self)
        self.file_button.clicked.connect(self.showFileDialog)
        self.layout.addWidget(self.file_button)

        self.folder_path = QLineEdit(self)
        self.layout.addWidget(self.folder_path)

        self.folder_button = QPushButton("Обзор (папка с игрой)", self)
        self.folder_button.clicked.connect(self.showFolderDialog)
        self.layout.addWidget(self.folder_button)

        language_layout = QHBoxLayout()

        self.toggle_button = QPushButton("Английский", self)
        self.toggle_button.clicked.connect(self.toggleLanguage)
        self.toggle_button.setFixedWidth(100)
        self.toggle_button.setFixedHeight(30)
        language_layout.addWidget(self.toggle_button)

        self.run_button = QPushButton("Запуск", self)
        self.run_button.clicked.connect(self.runAction)
        self.run_button.setFixedWidth(100)
        self.run_button.setFixedHeight(30)
        language_layout.addWidget(self.run_button)

        self.layout.addLayout(language_layout)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.image_label = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(sys.argv[0]), "img01.png"))
        pixmap = pixmap.scaled(510, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)
    def toggleLanguage(self):
        if self.toggle_button.text() == "Английский":
            self.toggle_button.setText("Русский")
        else:
            self.toggle_button.setText("Английский")
    def showFileDialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите видео файл", "",
                                                   "Видео файлы (*.mp4 *.avi *.mov *.mkv *.webm)")
        if file_name:
            self.file_path.setText(file_name)

    def showFolderDialog(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_name:
            self.folder_path.setText(folder_name)

    def rename_and_move_file(self, directory):
        original_file = os.path.join(directory, "pak01_dir.vpk")

        if os.path.exists(original_file):
            renamed_file = os.path.join(directory, "pak01_000.vpk")

            try:
                os.remove(os.path.join(directory, "pak01_000.vpk"))
                os.rename(original_file, renamed_file)
            except Exception as e:
                print(e)
                return
        else:
            print(5)
            return

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def remove_audio_from_video(self, video_file, output_file):
        try:
            video = VideoFileClip(video_file)
            video_without_audio = video.without_audio()
            video_without_audio.write_videofile(output_file, codec="libvpx-vp9", audio=False, bitrate="2M", fps=30)
            video_without_audio.close()
        except Exception as e:
            print(e)

    def runAction(self):
        video_file = self.file_path.text()
        output_folder = "pak01_dir/123"

        if not video_file or not output_folder:
            return

        file_extension = os.path.splitext(video_file)[1].lower()
        self.update_progress(20)
        if file_extension == ".webm":
            new_location = os.path.join(output_folder, '123.webm')
            try:
                shutil.copy(video_file, new_location)
                print(f"Файл перемещен в папку: {new_location}")
                self.remove_audio_from_video(new_location, new_location)
                print(f"Аудио удалено из файла: {new_location}")
            except Exception as e:
                print(f"Ошибка при перемещении или удалении аудио: {e}")
                return
        else:
            try:
                output_webm = os.path.join(output_folder, "123.webm")
                video = VideoFileClip(video_file)
                video.write_videofile(output_webm, codec="libvpx-vp9",audio=False, bitrate="2M", fps=30)
                print(f"Конвертация завершена: {output_webm}")
            except Exception as e:
                return
        try:
            vpk_command = f"vpk.exe pak01_dir"
            subprocess.run(vpk_command, check=True, shell=True)
            print(f"Команда выполнена: {vpk_command}")
        except subprocess.CalledProcessError as e:
            return
        self.update_progress(80)


        destination_folder = self.folder_path.text()
        if not destination_folder:
            return
        if self.toggle_button.text() == 'Английский':
            destination_folder += '/game/dota_123'
        else:
            destination_folder += '/game/dota_russian'
            self.rename_and_move_file(destination_folder)


        if not os.path.exists(destination_folder):
            try:
                os.makedirs(destination_folder)
                print(f"Папка {destination_folder} была создана.")
            except Exception as e:
                return

        program_dir = os.path.dirname(sys.argv[0])
        vpk_files = ["pak01_dir.vpk", "pak02_dir.vpk"]

        for vpk_filename in vpk_files:
            vpk_file = os.path.join(program_dir, vpk_filename)

            if os.path.exists(vpk_file):
                try:
                    destination_path = os.path.join(destination_folder, vpk_filename)
                    shutil.copy(vpk_file, destination_path)
                    print(f"Файл {vpk_filename} перемещен в папку: {destination_path}")
                except Exception as e:
                    return
                self.update_progress(100)
            else:
                return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileDialogApp()
    window.show()
    sys.exit(app.exec())

