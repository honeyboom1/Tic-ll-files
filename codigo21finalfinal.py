import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import convolve2d
import matplotlib.animation as animation
import serial
import time

class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setup_ui()
        self.setup_game()
        self.setup_serial()

    def setup_ui(self):
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


        self.temperature_textedit = QTextEdit()
        self.layout.addWidget(self.temperature_textedit)

        # Crear lienzo para mostrar el juego de la vida
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

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
        self.ani = animation.FuncAnimation(self.figure, self.update, frames=10, interval=100, fargs=(self.img, self.grid, self.N,))
        self.canvas.draw()

    def stop_game(self):
        self.ani.event_source.stop()

    
        
    def update(self, frame, img, grid, N):
        
        

        # Definimos el kernel
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        
        # Usamos convolve2d para aplicar el kernel a la grilla, considerando condiciones de frontera periódicas
        convolved = convolve2d(grid, kernel, mode='same', boundary='wrap')
        
        # Aplicamos las reglas del Juego de la Vida de Conway
        birth = (convolved == 3) & (grid == 0)  # Una célula muerta con exactamente 3 vecinos vivos "nace"
        survive = ((convolved == 2) | (convolved == 3)) & (grid == 1)  # Una célula viva con 2 o 3 vecinos vivos sobrevive
        grid[:, :] = 0  # Primero, seteamos todas las células a "muertas"
        grid[birth | survive] = 1  # Luego, actualizamos las células que deben "nacer" o sobrevivir
        
        
        # Actualizamos la imagen con el nuevo estado
        img.set_data(grid)
        img.autoscale()
         # Contar la cantidad de células vivas
        alive_cells = np.sum(self.grid)

        # Imprimir las células vivas en consola
        print("Número de células vivas:", alive_cells)

        # Enviar comandos a Arduino según el número de células vivas
        if alive_cells >= 1000:
            self.serial_port.write(b'S')  # Envía el comando para el color azul
        elif 600 <= alive_cells <= 999:
            self.serial_port.write(b'C')  # Envía el comando para el color verde
        else:
            self.serial_port.write(b'E')  # Envia 
    def reinicio_programa(self):
        print("Reiniciar")
        self.N = 100
        self.grid = np.random.choice([0, 1], self.N*self.N, p=[0.8, 0.2]).reshape(self.N, self.N)


        self.timer.start()
    def leerreglas_puerto_serial(self):
        mensaje = self.serial_port.readall().decode('utf-8').strip()
        
        if mensaje == "Reiniciar":
            print("Se ha iniciado el reinicio")
            self.reinicio_programa()
        
        # Enviamos la cantidad de células vivas por el puerto serial cada 10 segundos
        
            
            # Leemos la respuesta de Arduino y actualizamos la interfaz
            response = self.serial_port.readline().decode().strip()
            if response:
                self.temperature_textedit.append(response)
            self.serial_port.write(f'{live_cells}\n'.encode())
            # Leer datos del puerto serial de manera no bloqueante
         
            # Leer datos del puerto serial de manera no bloqueante
    
        
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec())
