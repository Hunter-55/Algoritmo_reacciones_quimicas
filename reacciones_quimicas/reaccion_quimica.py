import random
import os
from mochila import BACKPACK

class BackPackCreate:
#----- CONSTRUCTOR -----
    def __init__(self,sizeOfParticle) -> None:
        self.sizeOfParticle = sizeOfParticle # cantidad de objeto de la molecula
        self.particle       = []             # lista de la particula

#----- GENERA '0,1' de energia potencial y sinetica en la particula -----
    def GegerateParticle(self):
        self.particle = [random.randint(0,1) for i in range(self.sizeOfParticle)]
        return self.particle



class Methods:
     #----- CONSTRUCTOR -----
    def __init__(self,backPackList) -> None:
        self.backPackList = backPackList

    # [[1,0,1,1],ptencial,sinetica]
#----- Calcular Energía Potencial de la estructura molecular -----
    def CalculatePotentialEnergyOfMolecule(self,newMolecule):
        sum_cost     = 0
        sum_weight   = 0
        for i in range(len(newMolecule)):
            if newMolecule[i] == 1:
                #sum_cost   += float(self.backPackList[i][1])
                sum_weight += float(self.backPackList[i][0])
                #sum_cost    = round(sum_cost,2)
                sum_weight  = round(sum_weight,2)
        return [newMolecule,sum_weight,sum_cost]

#----- Mutaciones -----
    def Mutations(self,molecule):
        numberOfMutation   = random.randint(1,len(molecule))
        positionOfMutation = 0
        for i in range(numberOfMutation):
            positionOfMutation = random.randint(0,len(molecule)-1)
            binary = random.randint(0,1)
            molecule[positionOfMutation] = binary
        return molecule
    
#----- Mutaciones para la colisión de SINTESIS #4 -----
    def MutationsSintesis4(self,molecule1,molecule2):
        half1    = len(molecule1)  // 2
        half2    = len(molecule2) // 2
        return molecule1[:half1] + molecule2[half2:]



class PopulationOfParticles:
    #----- CONSTRUCTOR -----
    def __init__(self,populationSize,backPackList) -> None:
        self.populationSize            = populationSize # Tamaño de la población de particulas
        self.backPackList              = backPackList   # tamaño de la lista de la mochila
        self.listPopulationParticle    = []             # lista de la población de moleculas
        self.listPopulationParticleAux = []
        self.potentialEnergyTotal      = 0              # almacena la enegia potencial total del sistema
        self.buffer                    = 0              # almacena una parte de la energia
        self.objects                   = Methods(self.backPackList)

#----- GENERA TAMAÑO DE LA POBLACIÓN -----
    def GeneratePopulation(self):
        for i in range(self.populationSize):
            particleObject    = BackPackCreate(len(self.backPackList))
            particleIndividuo = particleObject.GegerateParticle()
            self.listPopulationParticle.append(particleIndividuo)

#----- Calculo de la energia potencial de cada molecula y Ke = 0 -----
    def CalculatePotentialEnergysListOfMolecules(self):
        sum_cost     = 0
        sum_weight   = 0
        self.listPopulationParticleAux = []
        for molecule in self.listPopulationParticle:
            for i in range(len(molecule)):
                if molecule[i] == 1:
                    sum_cost   += round(float(self.backPackList[i][1]),2) 
                    sum_weight += round(float(self.backPackList[i][0]),2)
            sum_weight = sum_cost / sum_weight
            self.listPopulationParticleAux.append([molecule,sum_weight,0])
            sum_cost   = 0
            sum_weight = 0
        self.listPopulationParticle = []
        self.listPopulationParticle = self.listPopulationParticleAux

#----- Calcular Energía Potencial total del sistema -----
    def CalculatePotentialEnergyTotal(self,percentage):
        for populationParticle in self.listPopulationParticle:
            self.potentialEnergyTotal += populationParticle[1]
            self.potentialEnergyTotal  = round(self.potentialEnergyTotal,2)
        self.buffer = round(self.potentialEnergyTotal * percentage)

#----- retorna la mejor solución -----
    def Major(self,listMolecule):
        listMolecule = sorted(listMolecule, key=lambda molecule: molecule[0][1])
        listMolecule = sorted(listMolecule, key=lambda molecule: molecule[0][2],reverse=True)
        return listMolecule[0]

#----- Filtra por la cantidad permitida de peso y costo -----
    def Filtter(self,listMolecule,pe,ke):
        listMoleculeFitter = []
        for molecule in listMolecule:
            if (molecule[0][1] <= pe and ke <= molecule[0][2]):
                listMoleculeFitter.append(molecule)
        return listMoleculeFitter


#----- colición ineficaz contra la pared #1 -----
    def IneffectiveCollisionAgainstTheWall(self,positionOfMolecule):
        molecule        = self.listPopulationParticle[positionOfMolecule]
        newMolecule     = self.objects.Mutations(molecule[0])#-----CHECAR
        newMoleculePEKE = self.objects.CalculatePotentialEnergyOfMolecule(newMolecule)#----CHECAR
        if molecule[1] + molecule[2] >= newMoleculePEKE[1]:
            q                  = round(random.uniform(0,1), 2)  #-------CHECAR
            newMoleculeKE      = (molecule[1] + molecule[2] - newMoleculePEKE[1]) * q
            newMoleculePEKE[2] = round(newMoleculeKE,2)
            self.buffer        = self.buffer + (molecule[1] + molecule[2] - newMoleculePEKE[1]) * (1 - q)
            self.buffer        = round(self.buffer,2)
            self.listPopulationParticle[positionOfMolecule] = newMoleculePEKE
            return [1,newMoleculePEKE,self.buffer,self.potentialEnergyTotal]
        return 0

#----- Descomposición #2 -----
    def Decomposition(self,positionOfMolecule):
        molecule         = self.listPopulationParticle[positionOfMolecule]
        newMolecule1     = self.objects.Mutations(molecule[0])#-----CHECAR
        newMolecule2     = self.objects.Mutations(molecule[0])#-----CHECAR
        newMoleculePEKE1 = self.objects.CalculatePotentialEnergyOfMolecule(newMolecule1)#----CHECAR
        newMoleculePEKE2 = self.objects.CalculatePotentialEnergyOfMolecule(newMolecule2)#----CHECAR
        temp1            = molecule[1] + molecule[2] #- newMolecule1[1] - newMolecule2[1]
        success          = False
        if temp1 >= 0:
            success = True
            k = round(random.uniform(0,1), 2)
            newMoleculeKE1 = temp1 * k
            newMoleculeKE2 = temp1 * (1 - k)
            # se crean las nuevas moleculas
            newMoleculePEKE1[2] = round(newMoleculeKE1,2)
            newMoleculePEKE2[2] = round(newMoleculeKE2,2)
            self.listPopulationParticle[positionOfMolecule] = newMoleculePEKE1
            #self.listPopulationParticle[positionOfMolecule] = newMoleculePEKE2
            return [1 , newMoleculePEKE1,self.buffer,self.potentialEnergyTotal]
        elif temp1 + self.buffer >= 0:
            success = True
            m1      = round(random.uniform(0,1), 2)
            m2      = round(random.uniform(0,1), 2)
            m3      = round(random.uniform(0,1), 2)
            m4      = round(random.uniform(0,1), 2)
            newMoleculeKE1 = (temp1 + self.buffer) * m1 * m2
            newMoleculeKE2 = (temp1 + self.buffer - newMolecule1) * m3 * m4
            self.buffer    = temp1 + self.buffer - newMolecule1 - newMolecule2 # actualiza buffer
            self.buffer    = round(self.buffer,2)
            # se crean las nuevas moleculas
            newMoleculePEKE1[2] = newMoleculeKE1
            newMoleculePEKE2[2] = newMoleculeKE2
            
            #self.listPopulationParticle[positionOfMolecule] = newMoleculePEKE1
            self.listPopulationParticle[positionOfMolecule] = newMoleculePEKE2
            return [1 , newMoleculePEKE2,self.buffer,self.potentialEnergyTotal]

#----- Colisión Intermolecular ineficaz #3 -----
    def IneffectiveIntermolecularCollision(self,positionOfMolecule,positionOfMolecule2):
        molecule         = self.listPopulationParticle[positionOfMolecule]
        molecule2        = self.listPopulationParticle[positionOfMolecule2]
        newMolecule1     = self.objects.Mutations(molecule[0])#-----CHECAR
        newMolecule2     = self.objects.Mutations(molecule2[0])#-----CHECAR
        newMoleculePEKE1 = self.objects.CalculatePotentialEnergyOfMolecule(newMolecule1)#----CHECAR
        newMoleculePEKE2 = self.objects.CalculatePotentialEnergyOfMolecule(newMolecule2)#----CHECAR
        temp2            = (molecule[1] + molecule2[1] + molecule[2] + molecule2[2]) #- (newMolecule1[1] + newMolecule2[1])
        if temp2 >= 0:
            p = round(random.uniform(0,1), 2)
            newMoleculeKE1 = temp2 * p 
            newMoleculeKE2 = temp2 * (1 - p)
            # se crean las nuevas moleculas
            newMoleculePEKE1[2] = round(newMoleculeKE1,2)
            newMoleculePEKE2[2] = round(newMoleculeKE2,2)
            self.listPopulationParticle[positionOfMolecule]  = newMoleculePEKE1
            #self.listPopulationParticle[positionOfMolecule2] = newMoleculePEKE2
            return [1 , newMoleculePEKE1,self.buffer,self.potentialEnergyTotal]

#----- Síntesis #4 -----
    def Synthesis(self,positionOfMolecule,positionOfMolecule2):
        molecule1       = self.listPopulationParticle[positionOfMolecule]
        molecule2       = self.listPopulationParticle[positionOfMolecule2]
        newMolecule     = self.objects.MutationsSintesis4(molecule1[0],molecule2[0])
        newMoleculePEKE = self.objects.CalculatePotentialEnergyOfMolecule(newMolecule)#----CHECAR
        success         = False
        if (molecule1[1] + molecule2[1] + molecule1[2] + molecule2[2]) >= newMoleculePEKE[1]:
            success            = True
            newMoleculeKE      = (molecule1[1] + molecule2[1] + molecule1[2] + molecule2[2]) - newMoleculePEKE[1]
            newMoleculePEKE[2] = round(newMoleculeKE,2)
            self.listPopulationParticle[positionOfMolecule] = newMoleculePEKE
            return [1 , newMoleculePEKE,self.buffer,self.potentialEnergyTotal]


def main():
    populationSize     = 1000                                  # tamaño de población para el sistema
    counterCollisions  = 0                                    # contador de coliciones
    numberOfCollisions = 1000                                  # Cantidad de coliciones a simular
    percentage         = 0.15                                 # porcentaje para el calculo del buffer
    fileTxt            = 'mochila.txt'                        # archivo a leer
    solution           = []
    pe                 = 2.0
    ke                 = 6000

# SE CREA EL OBJETO Y TODA LA MOCHILA
    backPack     = BACKPACK(fileTxt)
    backPack.ReadTxt()
    backPackList = backPack.Objects()

# SE CREA EL OBJETO DE LA POBLACION DE LA MOLECULA
    populationMolecule = PopulationOfParticles(populationSize,backPackList)
    populationMolecule.GeneratePopulation()
    populationMolecule.CalculatePotentialEnergysListOfMolecules()
    populationMolecule.CalculatePotentialEnergyTotal(percentage)

    while counterCollisions <= numberOfCollisions:
        selectionMolecule  = random.randint(0,populationSize - 1) # obtener molecula random
        selectionMolecule2 = random.randint(0,populationSize - 1) # obtener molecula random
        typeOfCollisions   = random.randint(1,4)                  # obtener el tipo de colición
        match typeOfCollisions:
            case 1:
               result = populationMolecule.IneffectiveCollisionAgainstTheWall(selectionMolecule)
               if result != 0:
                    counterCollisions += result[0]
                    solution.append([result[1],counterCollisions,result[2],result[3]])
            case 2:
                result = populationMolecule.Decomposition(selectionMolecule)
                if result != 0:
                    counterCollisions += result[0]
                    solution.append([result[1],counterCollisions,result[2],result[3]])
            case 3:
                result = populationMolecule.IneffectiveIntermolecularCollision(selectionMolecule,selectionMolecule2)
                if result != 0:
                    counterCollisions += result[0]
                    solution.append([result[1],counterCollisions,result[2],result[3]])
            case 4:
                result = populationMolecule.Synthesis(selectionMolecule,selectionMolecule2)
                if result != 0:
                    counterCollisions += result[0]
                    solution.append([result[1],counterCollisions,result[2],result[3]])
            case _:
                print("Colición no encontrada")

    solution = populationMolecule.Filtter(solution,pe,ke)
    if solution:
        r        = populationMolecule.Major(solution)
        print("MOLECULA: ",r[0][0],"\nPOTENCIAL: ",r[0][1],"\nSINETICA: ",r[0][2],"\nCOLISION: ",r[1],"\nBUFFER: ",r[2],"\nPOTENCIAL TOTAL: ",r[3])

if __name__ == "__main__":
    main()




