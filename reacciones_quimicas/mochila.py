import re

class BACKPACK:

#----- CONSTRUCTOR -----
    # SIZE    : cantidas de objetos
    # WEIGHT  : Peso maximo de la mochila
    # FILETXT : archivo txt
    def __init__(self,fileTxt) -> None:
        #self.weight   = weight
        self.fileTxt  = fileTxt
        self.backpack = []
    
#----- LEER ARCHIVO DE DATOS -----
    def ReadTxt(self):
        readFile = open(self.fileTxt)
    # --- caja de texto ---
        numWeight = ""
        numCost   = ""
        for line in readFile:
            for s in re.findall(r'-?\d+\.?\d*',line):
                if line.find('PESO:') != -1:
                    numWeight += s

                if line.find('COSTO:') != -1:
                    numCost += s
            
            if line.find(',') != -1:
                self.backpack.append([numWeight,numCost])
                numWeight = ""
                numCost   = ""
        readFile.close()
    
#----- GENERAR PESO Y COSTO DE LOS OBJETOS -----
    def Objects(self):
        list_objet = []
        flag       = False
        sum        = 0
        count      = 0

        while flag == False:
            list_objet = []
            count      = 0
            sum        = 0.0
            while count < len(self.backpack):#self.size:
                weight = self.backpack[count][0]
                cost   = self.backpack[count][1]
                sum    += round(float(weight),2)
                list_objet.append([weight,cost])
                count += 1

            #if sum == self.weight:
            #    flag = True
            flag = True
        return list_objet