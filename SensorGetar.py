from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
from pyqtgraph import mkPen
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
from datetime import datetime
import pandas as pd
import os


class SensorPlotWidget(PlotWidget):
    def __init__(self, parent=None):
        super(SensorPlotWidget, self).__init__(parent)
        self.curve = self.plot(pen=mkPen('b'))
        self.x_data = np.array([])
        self.y_data = np.array([])

    def update_plot(self):
        self.curve.setData(self.x_data, self.y_data)


class SensorThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, selected_port, ui_dialog):
        super().__init__()
        self.selected_port = selected_port
        self.ui_dialog = ui_dialog
        self.ser = None

    def run(self):
        try:
            self.ser = serial.Serial(self.selected_port, 9600)
            print(f"Sensor terhubung di port {self.selected_port}")
            print(f"Apakah serial terbuka? {self.ser.is_open}")
            while True:
                if self.ser.is_open:
                    data = self.ser.readline().decode("utf-8").strip()
                    print("Data yang diterima:", data)
                    self.ui_dialog.update_graph_data(data)

        except serial.SerialException as e:
            print(f"Error membuka port serial: {e}")
            print("Pastikan sensor terhubung dan coba lagi.")
            self.quit()
        except Exception as e:
            print(f"Error tak terduga: {e}")
            self.quit()
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(672, 402)
        self.nilai_getaran = QtWidgets.QLabel(Dialog)
        self.nilai_getaran.setGeometry(QtCore.QRect(180, 80, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nilai_getaran.setFont(font)
        self.nilai_getaran.setObjectName("nilai_getaran")
        self.peringatan = QtWidgets.QLabel(Dialog)
        self.peringatan.setGeometry(QtCore.QRect(180, 120, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.peringatan.setFont(font)
        self.peringatan.setObjectName("peringatan")
        self.lcd_NilaiGetaran = QtWidgets.QLCDNumber(Dialog)
        self.lcd_NilaiGetaran.setGeometry(QtCore.QRect(310, 80, 111, 23))
        self.lcd_NilaiGetaran.setObjectName("lcd_NilaiGetaran")
        self.lb_peringatan = QtWidgets.QLabel(Dialog)
        self.lb_peringatan.setGeometry(QtCore.QRect(310, 120, 181, 16))
        self.lb_peringatan.setText("")
        self.lb_peringatan.setObjectName("lb_peringatan")
        self.GvGetaran = QtWidgets.QGraphicsView(Dialog)
        self.GvGetaran.setGeometry(QtCore.QRect(120, 180, 521, 211))
        self.GvGetaran.setObjectName("GvGetaran")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 10, 421, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(220, 40, 211, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 671, 401))
        self.label_3.setStyleSheet("background-color: rgb(170, 170, 127);\n"
                                   "background-color: rgb(85, 170, 127);\n"
                                   "border-radius: 10px")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.LePeringatan = QtWidgets.QLineEdit(Dialog)
        self.LePeringatan.setEnabled(False)
        self.LePeringatan.setGeometry(QtCore.QRect(310, 120, 113, 20))
        self.LePeringatan.setObjectName("LePeringatan")
        self.PbSimpanData = QtWidgets.QPushButton(Dialog)
        self.PbSimpanData.setGeometry(QtCore.QRect(20, 220, 75, 23))
        self.PbSimpanData.setObjectName("PbSimpanData")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(300, 160, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 60, 671, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_3.raise_()
        self.nilai_getaran.raise_()
        self.peringatan.raise_()
        self.lcd_NilaiGetaran.raise_()
        self.lb_peringatan.raise_()
        self.GvGetaran.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.LePeringatan.raise_()
        self.PbSimpanData.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.line.raise_()

        # Tambahkan atribut instance untuk SensorThread
        self.sensor_thread = SensorThread("COM4", self)
        self.sensor_thread.data_received.connect(self.update_graph_data)
        self.sensor_thread.start()

        # Tambahkan timer untuk pembaruan GUI setiap 1000 milidetik (1 detik)
        self.gui_update_timer = QTimer(Dialog)
        self.gui_update_timer.timeout.connect(self.update_gui)
        self.gui_update_timer.start(1000)

        # Tambahkan MatplotlibWidget untuk menampilkan grafik
        self.sensor_plot_widget = SensorPlotWidget(Dialog)
        self.sensor_plot_widget.setGeometry(QtCore.QRect(120, 180, 521, 211))

        # Inisialisasi DataFrame
        self.df = pd.DataFrame(
            columns=['Timestamp', 'Nilai Getaran', 'Peringatan'])

        # Tambahkan metode ini untuk menyimpan data ke dalam file Excel
        self.PbSimpanData.clicked.connect(self.save_data_to_excel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.nilai_getaran.setText(_translate("Dialog", "Nilai Getaran :"))
        self.peringatan.setText(_translate("Dialog", "Peringatan :"))
        self.label.setText(_translate(
            "Dialog", "SIstem Pendeteksi Getaran Pada Mesin/Alat Di Dunia Kerja "))
        self.label_2.setText(_translate(
            "Dialog", "Dengan Menggunakan Metode Fuzzy"))
        self.PbSimpanData.setText(_translate("Dialog", "Klik"))
        self.label_4.setText(_translate("Dialog", "Simpan Data :"))
        self.label_5.setText(_translate("Dialog", "Grafik Getaran :"))

    def update_graph_data(self, new_data):
        try:
            # Split data berdasarkan titik dua
            data_parts = new_data.split(':')
            if len(data_parts) == 2:
                label = data_parts[0].strip()
                value = data_parts[1].strip()

                if label == "Getaran":
                    try:
                        numeric_value = float(value)
                        print("Data yang diterima:", new_data)

                        # Tambahkan nilai baru
                        self.sensor_plot_widget.x_data = np.append(
                            self.sensor_plot_widget.x_data, self.sensor_plot_widget.x_data[-1] + 1) if len(self.sensor_plot_widget.x_data) > 0 else np.array([1])
                        self.sensor_plot_widget.y_data = np.append(self.sensor_plot_widget.y_data, numeric_value) if len(
                            self.sensor_plot_widget.y_data) > 0 else np.array([numeric_value])

                        # Hapus elemen pertama jika sudah mencapai batas tertentu
                        if len(self.sensor_plot_widget.y_data) > 20:
                            self.sensor_plot_widget.x_data = self.sensor_plot_widget.x_data[1:]
                            self.sensor_plot_widget.y_data = self.sensor_plot_widget.y_data[1:]

                        # Memperbarui data pada grafik dengan membuat garis yang menghubungkan semua titik
                        self.sensor_plot_widget.update_plot()

                        # Tampilkan nilai getaran pada LCD Number
                        self.lcd_NilaiGetaran.display(numeric_value)

                        # Tambahkan baris berikut untuk menentukan peringatan
                        if numeric_value > 5.0:  # Atur ambang batas sesuai kebutuhan
                            peringatan = "Bahaya"
                            self.LePeringatan.setText("Buzzer Menyala")
                        else:
                            peringatan = "Aman"
                            self.LePeringatan.setText("Buzzer Mati")

                        # Tampilkan peringatan di QLabel
                        self.lb_peringatan.setText(peringatan)

                        # Tambahkan data baru ke DataFrame
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        new_row = {
                            'Timestamp': timestamp, 'Nilai Getaran': numeric_value, 'Peringatan': peringatan}
                        self.df = self.df.append(new_row, ignore_index=True)

                        # Tambahkan baris berikut untuk memperbarui grafik getaran
                        self.GvGetaran.update_plot(
                            self.df['Timestamp'], self.df['Nilai Getaran'])

                    except ValueError as e:
                        print(
                            f"Error: {e}. Nilai Getaran tidak dapat diubah menjadi float.")
                else:
                    print(f"Label tidak dikenali: {label}")
            else:
                print("Format data tidak sesuai.")

        except Exception as e:
            print(f"Error: {e}. Data yang diterima tidak valid.")

    def save_data_to_excel(self):
        try:
            # Tentukan nama file Excel dengan menggunakan path yang ditentukan
            excel_filename = f'data_getaran_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
            script_path = os.path.dirname(os.path.abspath(__file__))
            excel_filepath = os.path.join(script_path, excel_filename)

            # Simpan DataFrame ke dalam file Excel di direktori aplikasi
            self.df.to_excel(excel_filepath, index=False)

            print(
                f"Data Getaran Disimpan dalam bentuk excel: {excel_filepath}")

        except Exception as e:
            print(f"Error: {e}. Gagal menyimpan data ke file Excel.")

    def update_gui(self):
        # Tambahkan baris berikut jika Anda ingin menampilkan status port terhubung
        # (Anda mungkin perlu mengubah port_name sesuai dengan port yang benar-benar digunakan)
        port_name = "4"
        port_status = "Terhubung" if port_name in [
            port.device for port in serial.tools.list_ports.comports()] else "Tidak Terhubung"
        print(f"Status Port {port_name}: {port_status}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
