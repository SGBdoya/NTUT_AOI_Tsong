import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QProgressDialog
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap, QMouseEvent
from Ui_ts_hw2 import Ui_Form  # 匯入您的 UI 檔案
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 選擇微軟正黑體
        plt.rcParams['axes.unicode_minus'] = False  # 用來正常顯示負號

        # 初始化影片播放器屬性
        self.cap = None
        self.is_paused = False
        self.start_point = None
        self.end_point = None
        self.drawing = False
        self.roi_selected = False
        self.roi = None
        self.total_frames = 0
        self.saving_video = False
        self.video_writer = None

        self.ui.interval_label.hide()

        # 將按鈕和滑塊連線到功能
        self.ui.play_button.clicked.connect(self.toggle_play)
        self.ui.progress_slider.sliderMoved.connect(self.set_position)
        self.ui.select_video_button.clicked.connect(self.select_video)
        self.ui.mode_slider.valueChanged.connect(self.update_display_mode)
        self.ui.mode_slider.valueChanged.connect(self.update_histogram)
        self.ui.interval_slider.valueChanged.connect(self.update_histogram)
        self.ui.new_video_button.clicked.connect(self.save_new_video)

        # 定時器用於更新影片幀
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_frame)

        # 初始化 matplotlib 畫布
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.ui.interval_label.layout().addWidget(self.canvas)

    def select_video(self):
        """打開影片檔案並設定影片源"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "選擇影片檔案", "", "影片檔案 (*.mp4 *.avi *.mov)")
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            if not self.cap.isOpened():
                print("無法打開影片檔案")
                return
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.ui.progress_slider.setMaximum(self.total_frames - 1)
            self.timer.start(30)  # 開始定時器

    def toggle_play(self):
        self.is_paused = not self.is_paused
        self.ui.play_button.setText("播放" if self.is_paused else "暫停")

    def display_frame(self):
        if not self.is_paused and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:  # 到達影片結尾，重置影片位置
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.saving_video = False  # 停止儲存影片
                if self.video_writer:
                    self.video_writer.release()  # 釋放 video_writer
                    self.video_writer = None
                    print("影片儲存完成")
                return

            # 更新進度條
            self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.ui.progress_slider.setValue(self.current_frame)

            # 儲存原始幀，用於在新增文字時重新整理
            self.original_frame = frame.copy()
            self.frame = self.original_frame.copy()
            self.display_image(self.ui.video_label, self.frame)

            # 如果有選中的 ROI，顯示非零畫素數和 RGB 通道
            if self.roi_selected:
                self.extract_and_display_roi()
                self.update_new_video_frame()  # 處理新影片幀

                # 如果正在儲存影片，將處理后的幀寫入檔案
                if self.saving_video and self.video_writer:
                    self.video_writer.write(self.frame)

                # 更新 new_video_label 顯示
                self.update_new_video_label()
                self.update_histogram()

    def display_image(self, label, frame):
        """將影片幀或影像顯示在指定的 QLabel 上"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(rgb_image.data, width, height,
                         bytes_per_line, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(q_image))

    def set_position(self, position):
        """設定影片播放位置"""
        if self.cap:
            # 設定影片的當前幀為新的位置
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

            # 在暫停狀態下讀取新幀
            if self.is_paused:
                ret, frame = self.cap.read()
                if ret:
                    # 更新原始幀和可修改的當前幀
                    self.original_frame = frame.copy()
                    self.frame = self.original_frame.copy()

                    # 顯示新的幀內容
                    self.display_image(self.ui.video_label, self.frame)

                    # 如果已選擇 ROI，重新繪製 ROI 框
                    if self.roi_selected:
                        self.extract_and_display_roi()
                        self.update_new_video_label()  # 更新合成後的幀顯示
                        self.update_histogram()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.is_paused:
            # 獲取 video_label 的偏移位置
            label_x = self.ui.video_label.geometry().x()
            label_y = self.ui.video_label.geometry().y()

            # 轉換滑鼠座標到 video_label 內的相對座標
            self.start_point = (int(event.position().x() - label_x),
                                int(event.position().y() - label_y))
            self.drawing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing and self.is_paused:
            # 獲取 video_label 的偏移位置
            label_x = self.ui.video_label.geometry().x()
            label_y = self.ui.video_label.geometry().y()

            # 轉換滑鼠座標到 video_label 內的相對座標
            self.end_point = (int(event.position().x() - label_x),
                              int(event.position().y() - label_y))

            temp_frame = self.frame.copy()
            cv2.rectangle(temp_frame, self.start_point,
                          self.end_point, (0, 255, 0), 2)
            self.display_image(self.ui.video_label, temp_frame)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.drawing:
            # 獲取 video_label 的偏移位置
            label_x = self.ui.video_label.geometry().x()
            label_y = self.ui.video_label.geometry().y()

            # 轉換滑鼠座標到 video_label 內的相對座標
            self.end_point = (int(event.position().x() - label_x),
                              int(event.position().y() - label_y))

            self.drawing = False
            self.roi_selected = True
            self.extract_and_display_roi()
            self.update_new_video_label()

    def extract_and_display_roi(self):

        x1, y1 = self.start_point
        x2, y2 = self.end_point
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        # 提取 ROI
        self.roi = self.frame[y1:y2, x1:x2].copy()
        self.non_zero_pixel()

        # 分割 RGB 通道
        b_img = self.roi.copy()
        b_img[:, :, 1] = 0
        b_img[:, :, 2] = 0

        g_img = self.roi.copy()
        g_img[:, :, 0] = 0
        g_img[:, :, 2] = 0

        r_img = self.roi.copy()
        r_img[:, :, 0] = 0
        r_img[:, :, 1] = 0

        # 顯示 RGB 通道和原始 ROI
        self.display_image(self.ui.red_channel_label, r_img)
        self.display_image(self.ui.green_channel_label, g_img)
        self.display_image(self.ui.blue_channel_label, b_img)
        self.display_image(self.ui.original_roi_label, self.roi)
        self.ui.ROI_Frame.setMaximumSize(
            self.ui.ROI_Frame.maximumSize().width(), 16777215)

    def non_zero_pixel(self):
        # 重置 self.frame 為無文字的原始幀
        self.frame = self.original_frame.copy()

        non_zero_b = cv2.countNonZero(self.roi[:, :, 0])
        non_zero_g = cv2.countNonZero(self.roi[:, :, 1])
        non_zero_r = cv2.countNonZero(self.roi[:, :, 2])

        # 在原始幀上顯示計數
        cv2.putText(self.frame, f"B nonZero = {non_zero_b}", (
            10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.putText(self.frame, f"G nonZero = {non_zero_g}", (
            10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(self.frame, f"R nonZero = {non_zero_r}", (
            10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        self.display_image(self.ui.video_label, self.frame)  # 更新顯示

    def process_and_display_new_video(self):
        if self.roi is None:
            print("請先選擇一個 ROI 區域")
            return

        # 計算 ROI 範圍內的 R、G、B 平均值
        avg_b = int(np.mean(self.roi[:, :, 0]))
        avg_g = int(np.mean(self.roi[:, :, 1]))
        avg_r = int(np.mean(self.roi[:, :, 2]))
        print(f"R 平均值: {avg_r}, G 平均值: {avg_g}, B 平均值: {avg_b}")

        # 建立一個新的 ROI 區域，將 R、G、B 通道的平均值填充到該區域中
        avg_roi = np.zeros_like(self.roi)
        avg_roi[:, :, 0] = avg_b
        avg_roi[:, :, 1] = avg_g
        avg_roi[:, :, 2] = avg_r

        # 合成新的影片幀，將填充平均值的 ROI 區域覆蓋到原始幀的對應位置
        new_frame = self.frame.copy()
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        new_frame[y1:y2, x1:x2] = avg_roi

        # 顯示處理後的新幀到 new_video_label
        self.display_image(self.ui.new_video_label, new_frame)

    def update_new_video_label(self):
        if self.roi is None:
            return

        # 計算 ROI 範圍內的 R、G、B 平均值
        avg_b = int(np.mean(self.roi[:, :, 0]))
        avg_g = int(np.mean(self.roi[:, :, 1]))
        avg_r = int(np.mean(self.roi[:, :, 2]))

        # 建立一個新的 ROI 區域，將 R、G、B 通道的平均值填充到該區域中
        avg_roi = np.zeros_like(self.roi)
        avg_roi[:, :, 0] = avg_b
        avg_roi[:, :, 1] = avg_g
        avg_roi[:, :, 2] = avg_r

        # 合成新的幀，更新 ROI 區域
        new_frame = self.frame.copy()
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        new_frame[y1:y2, x1:x2] = avg_roi

        # 將處理后的 new_frame 顯示到 new_video_label
        self.display_image(self.ui.new_video_label, new_frame)

    def update_new_video_frame(self):
        if self.roi is None:
            return

        # 計算 ROI 範圍內的 R、G、B 平均值
        avg_b = int(np.mean(self.roi[:, :, 0]))
        avg_g = int(np.mean(self.roi[:, :, 1]))
        avg_r = int(np.mean(self.roi[:, :, 2]))

        # 建立一個新的 ROI 區域，將 R、G、B 通道的平均值填充到該區域中
        avg_roi = np.zeros_like(self.roi)
        avg_roi[:, :, 0] = avg_b
        avg_roi[:, :, 1] = avg_g
        avg_roi[:, :, 2] = avg_r

        # 將填充后的 ROI 區域覆蓋到 self.frame 的對應位置
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        self.frame[y1:y2, x1:x2] = avg_roi

    def update_display_mode(self):
        mode = self.ui.mode_slider.value()

        # 更新 mode_label 顯示的文字
        if mode == 0:
            self.ui.mode_label.setText("全部")
            # 顯示所有的 RGB 通道和原始 ROI
            self.ui.original_roi_label.show()
            self.ui.blue_channel_label.show()
            self.ui.green_channel_label.show()
            self.ui.red_channel_label.show()
            # 隱藏 interval_label
            self.ui.interval_label.hide()

        elif mode == 1:
            self.ui.mode_label.setText("藍色")
            # 只顯示藍色通道，並保留 original_roi_label 顯示
            self.ui.original_roi_label.show()
            self.ui.blue_channel_label.show()
            self.ui.green_channel_label.hide()
            self.ui.red_channel_label.hide()
            # 顯示 interval_label
            self.ui.interval_label.show()

        elif mode == 2:
            self.ui.mode_label.setText("綠色")
            # 只顯示綠色通道，並保留 original_roi_label 顯示
            self.ui.original_roi_label.show()
            self.ui.blue_channel_label.hide()
            self.ui.green_channel_label.show()
            self.ui.red_channel_label.hide()
            # 顯示 interval_label
            self.ui.interval_label.show()

        elif mode == 3:
            self.ui.mode_label.setText("紅色")
            # 只顯示紅色通道，並保留 original_roi_label 顯示
            self.ui.original_roi_label.show()
            self.ui.blue_channel_label.hide()
            self.ui.green_channel_label.hide()
            self.ui.red_channel_label.show()
            # 顯示 interval_label
            self.ui.interval_label.show()

    def save_new_video(self):
        # 彈出檔案儲存路徑對話方塊
        file_path, _ = QFileDialog.getSaveFileName(
            self, "儲存處理后的影片", "", "AVI 檔案 (*.avi);;MP4 檔案 (*.mp4)")

        # 如果使用者取消了檔案儲存，則返回
        if not file_path:
            return

        # 設定儲存影片的格式、尺寸和幀率
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        # 建立影片寫入對像
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 可以根據需要改成 'MP4V' 等格式
        video_writer = cv2.VideoWriter(
            file_path, fourcc, fps, (frame_width, frame_height))

        # 建立進度條
        progress_dialog = QProgressDialog(
            "正在儲存影片...", "取消", 0, self.total_frames, self)
        progress_dialog.setWindowTitle("儲存進度")
        progress_dialog.setWindowModality(Qt.WindowModal)

        # 逐幀處理影片
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重置影片到起始幀
        for frame_idx in range(self.total_frames):
            ret, frame = self.cap.read()
            if not ret:
                break

            # 更新進度條
            progress_dialog.setValue(frame_idx)
            if progress_dialog.wasCanceled():
                break

            # 如果有選中的 ROI，應用處理后的 ROI 區域
            if self.roi_selected:
                self.apply_roi_to_frame(frame)

            # 將處理后的幀寫入影片
            video_writer.write(frame)

        # 釋放資源
        video_writer.release()
        progress_dialog.setValue(self.total_frames)  # 完成進度條
        print(f"影片已成功儲存到: {file_path}")

    def apply_roi_to_frame(self, frame):
        """將處理后的 ROI 區域應用到指定幀上"""
        if self.roi is None:
            return

        # 確定 ROI 區域的邊界
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        # 提取目前幀的 ROI
        current_roi = frame[y1:y2, x1:x2]

        # 計算 ROI 範圍內的 R、G、B 平均值
        avg_b = int(np.mean(current_roi[:, :, 0]))
        avg_g = int(np.mean(current_roi[:, :, 1]))
        avg_r = int(np.mean(current_roi[:, :, 2]))

        # 建立一個新的 ROI 區域，將 R、G、B 通道的平均值填充到該區域中
        avg_roi = np.zeros_like(current_roi)
        avg_roi[:, :, 0] = avg_b
        avg_roi[:, :, 1] = avg_g
        avg_roi[:, :, 2] = avg_r

        # 將填充后的 ROI 區域覆蓋到 frame 的對應位置
        frame[y1:y2, x1:x2] = avg_roi

    def update_histogram(self):
        """更新目前 ROI 通道的畫素分佈直方圖，並在 video_label 上顯示級距信息"""
        if self.roi is None:
            return

        # 獲取目前通道的畫素數據
        mode = self.ui.mode_slider.value()
        if mode == 1:  # 藍色通道
            channel_data = self.roi[:, :, 0].flatten()
            self.ui.mode_label.setText("藍色")
        elif mode == 2:  # 綠色通道
            channel_data = self.roi[:, :, 1].flatten()
            self.ui.mode_label.setText("綠色")
        elif mode == 3:  # 紅色通道
            channel_data = self.roi[:, :, 2].flatten()
            self.ui.mode_label.setText("紅色")
        else:
            self.ui.mode_label.setText("全部")
            self.ax.clear()
            self.canvas.draw()
            return

        # 獲取分割的級距數
        intervals = self.ui.interval_slider.value()
        self.ui.interval_text_label.setText(f"級距: {intervals}")

        # 計算每個級距的範圍
        bin_ranges = np.linspace(0, 256, intervals + 1, dtype=int)
        bin_counts, _ = np.histogram(channel_data, bins=bin_ranges)

        # 繪製直方圖
        self.ax.clear()
        self.ax.hist(channel_data, bins=intervals, range=(0, 256),
                     color='blue' if mode == 1 else 'green' if mode == 2 else 'red')
        self.ax.set_title(f"通道畫素分佈（級距數：{intervals}）")
        self.ax.set_xlabel("畫素值")
        self.ax.set_ylabel("畫素數量")
        self.canvas.draw()

        # 在 video_label 上顯示級距信息
        self.frame = self.original_frame.copy()
        y_offset = 90  # 起始的 Y 位置
        for i, count in enumerate(bin_counts):
            bin_range_text = f"{bin_ranges[i]}-{bin_ranges[i+1]-1}: {count} px"
            cv2.putText(self.frame, bin_range_text, (10, y_offset + i * 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if mode == 3 else (0, 255, 0) if mode == 2 else (255, 0, 0), 1)

        # 更新 video_label 顯示
        self.display_image(self.ui.video_label, self.frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
