import numpy as np
import math as mt
import random as rd

#
#La clase Vectorial hace referencia al modelo de Recuperacion de Informacion Vectorial
#La variable que se recibe como iniciadora matriz_ter_doc es una matriz con la frecuencia fij de los terminos ti(fila) en los documentos dj(columna)
#
class Vectorial:
    def __init__(self,matriz_ter_doc,listamax):
        #la Matriz_Ter_Doc no se modifica, pues son las frecuencias originales de los terminos
        self.Matriz_Ter_Doc=np.array(matriz_ter_doc)
        filas,columnas=self.Matriz_Ter_Doc.shape
        self.Transpuesta=self.Matriz_Ter_Doc.T
        self.Consulta=[]
        self.Frecuencia_Normalizada=np.zeros((filas,columnas))
        self.IDf=np.zeros(filas)
        self.Pesos_Terminos=np.zeros((filas,columnas))
        self.Pesos_Consulta=np.zeros(filas)
        self.ni=np.zeros(filas)
        self.Ranking=[]
        self.Maximos_doc=listamax
        self.LlenaFN()
        self.LlenaIDf()
        self.LlenaPesosTerminos()

    def MaximoDoc(self,j):
        array=[]
        transpuesta=self.Matriz_Ter_Doc.T
        maximo=max(transpuesta[j])       
        return maximo

    def LlenaFN(self): 
        index=0
        fila,columna=self.Matriz_Ter_Doc.shape
        #transpuesta=self.Matriz_Ter_Doc.T
        for i in range(0,fila):
            for j in range(0,columna):
                tfij=0
                fij=self.Matriz_Ter_Doc[i][j]
                maxfreqj=self.Maximos_doc[j]
                #print(maxfreqj)
                #maxfreqj=5
                if(fij==0):
                    tfij=0
                else:
                    tfij=fij/maxfreqj
                self.Frecuencia_Normalizada[i][j]=tfij

    
    def LlenaIDf(self):
        T,N=self.Matriz_Ter_Doc.shape

        for i in range(0,T):
            array=self.Matriz_Ter_Doc[i]
            l=[x for x in array if x != 0]
            self.ni[i]=len(l)
            self.IDf[i]=mt.log(N/(len(l)))
    
    def LlenaPesosTerminos(self):
        fila,columna=self.Matriz_Ter_Doc.shape

        for i in range(0,fila):
            for j in range(0,columna):
                self.Pesos_Terminos[i][j]=self.Frecuencia_Normalizada[i][j]*self.IDf[i]
    
    def LLenaPesosConsulta(self,alpha,consulta):
        self.Consulta=np.array(consulta)
        fila, =self.Consulta.shape
        _,N=self.Matriz_Ter_Doc.shape
        #print(N)
        maximofila=max(self.Consulta)
        for i in range(0,fila):
            if(self.Consulta[i]==0):
                self.Pesos_Consulta[i]=0
            else:
                self.Pesos_Consulta[i]=(alpha+((1-alpha)*(self.Consulta[i]/maximofila)))*mt.log(N/(self.ni[i]))

    def Similitud_Doc_Consulta(self,j):
        fila,columna=self.Matriz_Ter_Doc.shape

        numerador=0
        pesos_terminos_cuadrados_suma=0
        pesos_consulta_cuadrados_suma=0

        for i in range(0,fila):
            numerador+=self.Pesos_Terminos[i][j]*self.Pesos_Consulta[i]
            pesos_terminos_cuadrados_suma+=mt.pow(self.Pesos_Terminos[i][j],2)
            pesos_consulta_cuadrados_suma+=mt.pow(self.Pesos_Consulta[i],2)
        
        similitud=float(numerador/(mt.sqrt(pesos_terminos_cuadrados_suma)*mt.sqrt(pesos_consulta_cuadrados_suma)))

        return similitud

    def Ranking_Doc(self,consulta):
        self.Ranking=[]
        alpha=0.5
        print(alpha)
        self.LLenaPesosConsulta(alpha,consulta)

        fila,columna=self.Matriz_Ter_Doc.shape

        for j in range(0,columna):
            sim=self.Similitud_Doc_Consulta(j)
            self.Ranking.append((sim,j+1))
        self.Ranking.sort(reverse=True)
    
    def Retroalimentacion(self,list_rel,consulta_original):
        fila,columna=self.Matriz_Ter_Doc.shape
        alpha=1
        beta=0.75
        cita=0.15
        #Transpuesta=self.Matriz_Ter_Doc.T
        print("transpuesta")
        vector1=np.zeros(fila)
        vector2=np.zeros(fila)

        for i in range(0,columna):
            if(list_rel.__contains__(i)):
                vector1=np.add(vector1,self.Transpuesta[i])
            else:
                vector2=np.add(vector2,self.Transpuesta[i])
            
        vector1=np.dot(vector1,beta/len(list_rel))
        vector2=np.dot(vector2,cita/(columna-len(list_rel)))
        vector3=np.dot(alpha,consulta_original)
        new_consulta=np.subtract(np.add(vector3,vector1),vector2)

        for i in range(0,len(new_consulta)):
            if new_consulta[i]<0:
                new_consulta[i]=0

        print(new_consulta)
        return new_consulta
        







        




print(mt.sqrt(49))

#matriz=[[1,2,3],[4,5,6]]
#frecuencia=np.array(matriz)

#print(frecuencia.shape)
#a,b=frecuencia.shape
#print("esto es a:"+str(a))
#print("esto es b:"+str(b))

ejemplo=[[3,3,1,3,0],[0,1,1,3,0],[0,0,1,0,1]]

#Prueba=Vectorial(ejemplo,[3,2,0])
#Prueba.LlenaFN()
#print(Prueba.Frecuencia_Normalizada)
#Prueba.LlenaIDf()
#print(Prueba.IDf)
#Prueba.LlenaPesosTerminos()
#print(Prueba.Pesos_Terminos)
#Prueba.LLenaPesosConsulta(0.4)
#print(Prueba.Pesos_Consulta)
#print(Prueba.Similitud_Doc_Consulta(2))
#Prueba.Ranking_Doc()
#print(Prueba.Ranking)

#print("Hola?".split("?"))

#array1=np.array([1,2,3])
#array2=np.array([4,5,6])

#no
#array1.append(array2)

#print(array1)












