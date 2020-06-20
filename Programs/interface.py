import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton,QLineEdit
from settings import main
from PyQt5.QtGui import QFont



class Example(QMainWindow):
    


    def __init__(self, x,y,z):
   
        super().__init__()
                
        self.qlabelx = QLabel(self)
        self.qlabelx.move(50,10)
        self.qlabelx.setText("Choose feature category:")
        self.qlabelx.setFixedSize(200,40)
        self.qlabelx.setFont(QFont('Ubuntu', 9, QFont.Bold))
    
      
      
        combo = QComboBox(self)
        combo.addItem("UNIGRAM")
        combo.addItem("BIGRAM")
        combo.addItem("HANDCRAFTED")
        combo.addItem("HANDCRAFTED_UNIGRAM")
        combo.addItem("HANDCRAFTED_BIGRAM")
        combo.addItem("UNIGRAM_BIGRAM")
        combo.addItem("HANDCRAFTED_UNIGRAM_BIGRAM")
        combo.move(50, 50)
        combo.setFixedSize(200,30)
        Feature_chosen = combo.currentText()

        
        self.qlabely = QLabel(self)
        self.qlabely.move(50,90)
        self.qlabely.setText("Choose Processing Unit:")
        self.qlabely.setFixedSize(200,40)
        self.qlabely.setFont(QFont('Ubuntu', 9, QFont.Bold))
        
        combo2 = QComboBox(self)
        combo2.addItem("FILE")
        combo2.addItem("FUNCTION")
        combo2.move(50, 130)
        combo2.setFixedSize(200,30)
        Processing_unit_chosen = combo2.currentText()

        self.qlabelz = QLabel(self)
        self.qlabelz.move(50,170)
        self.qlabelz.setText("Choose Measurement type:")
        self.qlabelz.setFixedSize(200,40)
        self.qlabelz.setFont(QFont('Ubuntu', 9, QFont.Bold))
        
        
        combo3 = QComboBox(self)
        combo3.addItem("IDENTIFICATION")
        combo3.addItem("VERIFICATION")
        combo3.move(50, 210)
        combo3.setFixedSize(200,30)
        Measurement_type_chosen = combo3.currentText()

        self.qlabeld = QLabel(self)
        self.qlabeld.move(50,310)
        self.qlabeld.setText("Precision:")
        self.qlabeld.setFixedSize(200,40)
        self.qlabeld.setFont(QFont('Ubuntu', 9, QFont.Bold))

        self.qlabele = QLabel(self)
        self.qlabele.move(50,350)
        f = open("C:/Users/Zsombi/Desktop/Allamvizsga/Programs/aux_res.txt",'r')
        txt = f.read()
        self.qlabele.setText(txt)
        self.qlabele.setFixedSize(200,40)
        self.qlabele.setFont(QFont('Ubuntu', 9, QFont.Bold))
        
        button_quit = QPushButton('Quit', self)
        button_quit.move(50,450)
        button_quit.clicked.connect(self.close)        
        
        button = QPushButton('Get result', self)
        button.setToolTip('This is an example button')
        button.move(50,250)
        button.clicked.connect(lambda: self.assign(combo.currentText(),combo2.currentText(),combo3.currentText()))

        self.qlabel2 = QLabel(self)
        self.qlabel2.move(350,0)
        #self.qlabel2.resize(200,40)
        self.qlabel2.setFixedSize(350,600)



        f = open("C:/Users/Zsombi/Desktop/Allamvizsga/Programs/aux_perm.txt",'r')
        txt = f.read()

        i = 0

        outptext = ""
        
        for line in txt.split("\n"):
            i+=1
            if i>10:
                outptext+=line+'\n'

        self.qlabel2.setText(outptext)
        self.qlabel2.setFont(QFont('Ubuntu', 9, QFont.Bold))
        self.qlabel = QLabel(self)
        self.qlabel.move(350,50)
        self.qlabel.setText("Permutation Importance")
        self.qlabel.setFixedSize(200,40)
        self.qlabel.setFont(QFont('Ubuntu', 13, QFont.Medium))
    
        self.setGeometry(50,50,320,200)
        self.setWindowTitle("App demo")
        self.show()
    def assign(self,x,y,z):
        
        global Feature_chosen
        global Processing_unit_chosen
        global Measurement_type_chosen     

        Feature_chosen = x
        Processing_unit_chosen = y
        Measurement_type_chosen = z
        w = open("C:/Users/Zsombi/Desktop/Allamvizsga/Programs/aux_file.txt",'w')
        w.truncate(0)
        w.write(Feature_chosen + "," + Processing_unit_chosen + "," + Measurement_type_chosen)
        w.close()
        main()
        exit(0)

    

        
        


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example("","","")
    sys.exit(app.exec_())