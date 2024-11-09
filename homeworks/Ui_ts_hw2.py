# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ts_hw2.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1075, 643)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_frmae = QFrame(Form)
        self.main_frmae.setObjectName(u"main_frmae")
        self.main_frmae.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_frmae.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.main_frmae)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.video_widget = QWidget(self.main_frmae)
        self.video_widget.setObjectName(u"video_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_widget.sizePolicy().hasHeightForWidth())
        self.video_widget.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.video_widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.video_label = QLabel(self.video_widget)
        self.video_label.setObjectName(u"video_label")
        sizePolicy.setHeightForWidth(self.video_label.sizePolicy().hasHeightForWidth())
        self.video_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.video_label)

        self.new_video_label = QLabel(self.video_widget)
        self.new_video_label.setObjectName(u"new_video_label")

        self.horizontalLayout_3.addWidget(self.new_video_label)


        self.verticalLayout_3.addWidget(self.video_widget, 0, Qt.AlignmentFlag.AlignTop)

        self.tool_frame = QFrame(self.main_frmae)
        self.tool_frame.setObjectName(u"tool_frame")
        self.tool_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.tool_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.tool_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.select_video_button = QPushButton(self.tool_frame)
        self.select_video_button.setObjectName(u"select_video_button")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.select_video_button.setFont(font)

        self.horizontalLayout.addWidget(self.select_video_button)

        self.play_button = QPushButton(self.tool_frame)
        self.play_button.setObjectName(u"play_button")
        self.play_button.setFont(font)

        self.horizontalLayout.addWidget(self.play_button)

        self.progress_slider = QSlider(self.tool_frame)
        self.progress_slider.setObjectName(u"progress_slider")
        self.progress_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.progress_slider)

        self.new_video_button = QPushButton(self.tool_frame)
        self.new_video_button.setObjectName(u"new_video_button")
        self.new_video_button.setFont(font)

        self.horizontalLayout.addWidget(self.new_video_button)


        self.verticalLayout_3.addWidget(self.tool_frame, 0, Qt.AlignmentFlag.AlignBottom)

        self.ROI_Frame = QFrame(self.main_frmae)
        self.ROI_Frame.setObjectName(u"ROI_Frame")
        self.ROI_Frame.setMaximumSize(QSize(16777215, 0))
        self.ROI_Frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ROI_Frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.ROI_Frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ROI_channel_Frame = QFrame(self.ROI_Frame)
        self.ROI_channel_Frame.setObjectName(u"ROI_channel_Frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ROI_channel_Frame.sizePolicy().hasHeightForWidth())
        self.ROI_channel_Frame.setSizePolicy(sizePolicy1)
        self.ROI_channel_Frame.setMaximumSize(QSize(16777215, 16777215))
        self.ROI_channel_Frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ROI_channel_Frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.ROI_channel_Frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.original_roi_label = QLabel(self.ROI_channel_Frame)
        self.original_roi_label.setObjectName(u"original_roi_label")

        self.horizontalLayout_2.addWidget(self.original_roi_label)

        self.blue_channel_label = QLabel(self.ROI_channel_Frame)
        self.blue_channel_label.setObjectName(u"blue_channel_label")

        self.horizontalLayout_2.addWidget(self.blue_channel_label)

        self.green_channel_label = QLabel(self.ROI_channel_Frame)
        self.green_channel_label.setObjectName(u"green_channel_label")

        self.horizontalLayout_2.addWidget(self.green_channel_label)

        self.red_channel_label = QLabel(self.ROI_channel_Frame)
        self.red_channel_label.setObjectName(u"red_channel_label")

        self.horizontalLayout_2.addWidget(self.red_channel_label)

        self.interval_label = QWidget(self.ROI_channel_Frame)
        self.interval_label.setObjectName(u"interval_label")
        self.horizontalLayout_6 = QHBoxLayout(self.interval_label)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.horizontalLayout_2.addWidget(self.interval_label)


        self.verticalLayout.addWidget(self.ROI_channel_Frame)

        self.ROI_tool_Widget = QWidget(self.ROI_Frame)
        self.ROI_tool_Widget.setObjectName(u"ROI_tool_Widget")
        self.horizontalLayout_4 = QHBoxLayout(self.ROI_tool_Widget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.mode_label = QLabel(self.ROI_tool_Widget)
        self.mode_label.setObjectName(u"mode_label")
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        self.mode_label.setFont(font1)

        self.horizontalLayout_4.addWidget(self.mode_label)

        self.mode_slider = QSlider(self.ROI_tool_Widget)
        self.mode_slider.setObjectName(u"mode_slider")
        self.mode_slider.setMaximum(3)
        self.mode_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.mode_slider)


        self.verticalLayout.addWidget(self.ROI_tool_Widget, 0, Qt.AlignmentFlag.AlignBottom)

        self.interval_widget = QWidget(self.ROI_Frame)
        self.interval_widget.setObjectName(u"interval_widget")
        self.interval_widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_5 = QHBoxLayout(self.interval_widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.interval_text_label = QLabel(self.interval_widget)
        self.interval_text_label.setObjectName(u"interval_text_label")
        self.interval_text_label.setFont(font)

        self.horizontalLayout_5.addWidget(self.interval_text_label)

        self.interval_slider = QSlider(self.interval_widget)
        self.interval_slider.setObjectName(u"interval_slider")
        self.interval_slider.setMinimum(1)
        self.interval_slider.setMaximum(10)
        self.interval_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.interval_slider)


        self.verticalLayout.addWidget(self.interval_widget)


        self.verticalLayout_3.addWidget(self.ROI_Frame)


        self.verticalLayout_2.addWidget(self.main_frmae)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.video_label.setText("")
        self.new_video_label.setText("")
        self.select_video_button.setText(QCoreApplication.translate("Form", u"\u9078\u64c7\u5f71\u7247", None))
        self.play_button.setText(QCoreApplication.translate("Form", u"\u66ab\u505c", None))
        self.new_video_button.setText(QCoreApplication.translate("Form", u"\u7b2c\u4e09\u984c", None))
        self.original_roi_label.setText("")
        self.blue_channel_label.setText("")
        self.green_channel_label.setText("")
        self.red_channel_label.setText("")
        self.mode_label.setText(QCoreApplication.translate("Form", u"\u5168\u90e8", None))
        self.interval_text_label.setText(QCoreApplication.translate("Form", u"\u7d1a\u8ddd", None))
    # retranslateUi

