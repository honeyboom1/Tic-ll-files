import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from PyQt6.QtCore import QTimer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import convolve2d
import matplotlib.animation as animation
import serial
import time
from playsound import playsound


class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setup_ui()
        self.setup_game()
        self.setup_serial()

    def setup_ui(self):
        # Configuración de la interfaz de usuario
        self.setWindowTitle("Game of Life")
        self.setGeometry(100, 100, 800, 600)
        

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_game)
        self.layout.addWidget(self.stop_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        self.temperature_textedit = QTextEdit()
        self.layout.addWidget(self.temperature_textedit)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.n_1_button = QPushButton("Nuke")
        self.n_1_button.clicked.connect(self.n_1)
        self.layout.addWidget(self.n_1_button)

        self.h_1_button = QPushButton("Heal")
        self.h_1_button.clicked.connect(self.h_1)
        self.layout.addWidget(self.h_1_button)

        self.n_1_button.clicked.connect(self.n_1)
        self.h_1_button.clicked.connect(self.h_1)

    def setup_game(self):
        # Configuración inicial del juego
        self.N = 100  # Tamaño de la grilla NxN
        self.grid = np.random.choice([0,1], self.N*self.N, p=[0.8, 0.2]).reshape(self.N, self.N)  # Inicialización aleatoria
        self.img = plt.imshow(self.grid, interpolation='nearest')

    def setup_serial(self):
        # Configuración de la comunicación serial con Arduino
        self.serial_port = serial.Serial('COM5', 9600, timeout=0)
        time.sleep(2)  # Espera para asegurar la conexión

    def start_game(self):
        self.ani = animation.FuncAnimation(self.figure, self.update, frames=10, interval=100, fargs=(self.img,))
        self.canvas.draw()


    def stop_game(self):
        self.ani.event_source.stop()

    def reset_game(self):
        self.N = 100
        self.grid = np.random.choice([0,1], self.N*self.N, p=[0.8, 0.2]).reshape(self.N, self.N)
        self.img.set_data(self.grid)
        self.img.autoscale()
    
    
        

    def update(self, frame, img):
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

        convolved = convolve2d(self.grid, kernel, mode='same', boundary='wrap')


    # Aplicar las modificaciones específicas adicionales
        nuevo_grid = np.where((self.grid > 0) & ((convolved < 2) | (convolved > 3)), self.grid - 30, self.grid)

# Regla para renacimiento de células muertas
        nuevo_grid = np.where((self.grid == 0) & (convolved == 3), 100, nuevo_grid)
        nuevo_grid = np.where((nuevo_grid < 0), 0, nuevo_grid)
        self.grid = np.where((self.grid > 100), 100, nuevo_grid)

        self.grid = nuevo_grid
        img.set_data(nuevo_grid)
        img.autoscale()

    # Contar la cantidad de células vivas
        alive_cells = np.sum(self.grid)
        print("Número de células vivas:", alive_cells)
        


        if alive_cells >= 1000:
                self.serial_port.write(b'S')  # Envía el comando para el color azul
        elif 600 <= alive_cells <= 999:
                self.serial_port.write(b'C')  # Envía el comando para el color verde
        else:
                self.serial_port.write(b'E')  # Envia
    #sonas cuando la cuenta es 0 crashea el codigo pero funciona
        if alive_cells == 0:
            playsound("C:/Users/Pablo/Desktop/plinplin.mp3")

       

        self.serial_port.write(str(alive_cells).encode())


    def h_1(self, event= None):
        print("healing")

        x = np.random.randint(0, self.N - 21)
        y = np.random.randint(0, self.N - 21)

        for i in range(x, x + 21):
            for j in range(y, y + 21):
                if self.grid[i, j] == 0:  # Revivir células muertas
                    self.grid[i, j] = np.random.choice([0, 1], p=[0.2, 0.8])  # Probabilidad de 0.8 para células vivas
                elif 1 <= self.grid[i, j] <= 50:
                    self.grid[i, j] = min(self.grid[i, j] + 50, 100)  # Aumentar el estado de las células vivas
                else:
                    pass  # No hacer nada si la célula está en su estado máximo


    def n_1(self, event=None):
        print("Send a nuke")

        x = np.random.randint(0, self.N - 21)
        y = np.random.randint(0, self.N - 21)

        for i in range(x, x + 21):
            for j in range(y, y + 21):
                if 0 <= self.grid[i, j] <= 100:
                    self.grid[i, j] = 0

        
    def leer_puerto(self):
    # Leer datos del puerto serial de manera no bloqueante
        while self.serial_port.in_waiting > 0:
            mensaje = self.serial_port.readline().decode().strip()

        if mensaje == "Reiniciar":
            print("reiniciando")
            self.reset_game()

        elif mensaje == "h_1":
            print("Mensaje de Bomba sanadora recibido")
            self.h_1()
        elif mensaje == "n_1":
            print("Mensaje de Bomba atómica recibido")
            self.n_1()

               


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec())