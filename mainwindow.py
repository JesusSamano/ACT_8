from ast import Str
from math import fabs
from multiprocessing import managers
from sqlite3 import Row
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow
from manager import Manager
from particula import Particula

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.manager = Manager()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.id = 0
        
        #Cuando el botón pushbutton es presionado, ejecuta la función click_agregar
        # self.ui.mostrar.clicked.connect(self.click_mostrar)
        self.ui.insertar_inicio.clicked.connect(self.click_insertar_inicio)
        self.ui.insertar_final.clicked.connect(self.click_insertar_final)
        self.ui.mostrar.clicked.connect(self.click_mostrar)

        self.ui.actionAbrir.triggered.connect(self.action_abrir_archivo)
        self.ui.actionGuardar.triggered.connect(self.action_guardar_archivo)

        self.ui.mostrar_tabla_pushButton.clicked.connect(self.mostrar_tabla)
        self.ui.buscar_pushButton.clicked.connect(self.buscar_titulo)

    @Slot()
    def buscar_titulo(self):
        id = self.ui.buscar_lineEdit.text() #str
        encontrado = False

        for particula in self.manager: 
            if str (id) == str(particula.id):
                self.ui.tabla.clear()
                self.ui.tabla.setRowCount(1)

                id_widget = QTableWidgetItem(str(particula.id))
                origen_x_widget = QTableWidgetItem(str(particula.origen_x))   
                origen_y_widget = QTableWidgetItem(str(particula.origen_y))   
                destino_x_widget = QTableWidgetItem(str(particula.destino_x))   
                destino_y_widget = QTableWidgetItem(str(particula.destino_y))   
                velocidad_widget = QTableWidgetItem(str(particula.velocidad))
                red_widget = QTableWidgetItem(str(particula.red))
                green_widget = QTableWidgetItem(str(particula.green))
                blue_widget = QTableWidgetItem(str(particula.blue))
                distancia_widget = QTableWidgetItem(str(particula.distancia))

                self.ui.tabla.setItem(0, 0, id_widget)
                self.ui.tabla.setItem(0, 1, origen_x_widget)
                self.ui.tabla.setItem(0, 2, origen_y_widget)
                self.ui.tabla.setItem(0, 3, destino_x_widget)
                self.ui.tabla.setItem(0, 4, destino_y_widget)
                self.ui.tabla.setItem(0, 5, velocidad_widget)
                self.ui.tabla.setItem(0, 6, red_widget)
                self.ui.tabla.setItem(0, 7, green_widget)
                self.ui.tabla.setItem(0, 8, blue_widget)
                self.ui.tabla.setItem(0, 9, distancia_widget)

                encontrado = True
                return
        if not encontrado:
            QMessageBox.warning(
                self,
                "Atencion",
                f'La particula con nombre "{id}" no fue encontrado'
                )
               

        


    @Slot()
    def mostrar_tabla(self):
        self.ui.tabla.setColumnCount(10)
        headers = ["ID", "Origen X", "Origen Y", "Destino X",
                   "Destino Y", "Velocidad", "Red", "Green", "Blue", "Distancia"]
        self.ui.tabla.setHorizontalHeaderLabels(headers)

        self.ui.tabla.setRowCount(len(self.manager))

        row = 0
        for particula in self.manager:
            id_widget = QTableWidgetItem(str(particula.id))
            origen_x_widget = QTableWidgetItem(str(particula.origen_x))   
            origen_y_widget = QTableWidgetItem(str(particula.origen_y))   
            destino_x_widget = QTableWidgetItem(str(particula.destino_x))   
            destino_y_widget = QTableWidgetItem(str(particula.destino_y))   
            velocidad_widget = QTableWidgetItem(str(particula.velocidad))
            red_widget = QTableWidgetItem(str(particula.red))
            green_widget = QTableWidgetItem(str(particula.green))
            blue_widget = QTableWidgetItem(str(particula.blue))
            distancia_widget = QTableWidgetItem(str(particula.distancia))

            self.ui.tabla.setItem(row, 0, id_widget)
            self.ui.tabla.setItem(row, 1, origen_x_widget)
            self.ui.tabla.setItem(row, 2, origen_y_widget)
            self.ui.tabla.setItem(row, 3, destino_x_widget)
            self.ui.tabla.setItem(row, 4, destino_y_widget)
            self.ui.tabla.setItem(row, 5, velocidad_widget)
            self.ui.tabla.setItem(row, 6, red_widget)
            self.ui.tabla.setItem(row, 7, green_widget)
            self.ui.tabla.setItem(row, 8, blue_widget)
            self.ui.tabla.setItem(row, 9, distancia_widget)

            row += 1

                 
    
    #Funcion que es llamada por x razón que imprime Click en Terminal.
    @Slot()
    # def click_mostrar(self):
    #     a

    @Slot()
    def action_abrir_archivo(self):
        #print("Abrir_archivo")
        ubicacion = QFileDialog.getOpenFileName(
            self,
            'Abrir Archivo',
            '.',
            'JSON (*.json)'
        ) [0]
        if self.manager.abrir(ubicacion):
            QMessageBox.information(
                self,
                "Éxito",
                "Se abrió el archivo" + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al abrir el archivo" + ubicacion 
            )


    @Slot()
    def action_guardar_archivo(self):
        #print("guardar_archivo")
        ubicacion = QFileDialog.getSaveFileName(
            self,
            'Guardar Archivo',
            '.',
            'JSON (*.json)'
        )[0]
        print(ubicacion)
        if self.manager.guardar(ubicacion):
            QMessageBox.information(
                self,
                "Exito",
                "Se pudo crear el archivi" + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo crear el archivo" + ubicacion
            )
        
    
    def click_insertar_inicio(self):
        self.id += 1
        aux = Particula(self.id, self.ui.ox.value(), self.ui.oy.value(), self.ui.dx.value(), self.ui.dy.value(), self.ui.velocidad.value(), self.ui.red.value(), self.ui.green.value(), self.ui.blue.value())
        self.manager.agregarInicio(aux)
        self.click_mostrar()
        
    def click_insertar_final(self):
        self.id += 1
        aux = Particula(self.id , self.ui.ox.value(), self.ui.oy.value(), self.ui.dx.value(), self.ui.dy.value(), self.ui.velocidad.value(), self.ui.red.value(), self.ui.green.value(), self.ui.blue.value())
        self.manager.agregarFinal(aux)
        self.click_mostrar()
        
    def click_mostrar(self):
        self.ui.lista_particulas.clear()
        self.ui.lista_particulas.insertPlainText(str(self.manager))