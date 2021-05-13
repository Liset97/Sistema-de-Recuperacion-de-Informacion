import numpy as np
import math as mt

#
# Tendremos una lista de tuplas, las cuales significan:
# <id_doc, recuperado o no(0,1), ranking, relevancia(0,1),id_consulta>
#



class Evaluacion:
    def __init__(self, list_docs):
        self.Documentos_Info=list_docs
        self.Recuperados_Relevantes=0
        self.Recuperados_Irrelevantes=0
        self.No_Recuperados_Relevantes=0
        self.No_Recuperados_Irrelevantes=0
        self.Recuperados=0
        self.Relevantes=0
        self.Irrelevantes=0
        self.LlenaVariables()


    def LlenaVariables(self):
        for i in self.Documentos_Info:
            if i[1]==1:
                self.Recuperados+=1
                if i[3]==1:
                    #print("Entre doble")
                    self.Recuperados_Relevantes+=1
                    self.Relevantes+=1
                else:
                    self.Recuperados_Irrelevantes+=1
                    self.Irrelevantes+=1
            else:
                if i[3]==1:
                    self.No_Recuperados_Relevantes+=1
                    self.Relevantes+=1
                else:
                    self.No_Recuperados_Irrelevantes+=1
                    self.Irrelevantes+=1

    def Presicion(self):
        presicion=float(self.Recuperados_Relevantes)/float(self.Recuperados)
        return presicion

    def Recobrado(self):
        if(self.Relevantes==0):
            return 0
        recobrado=self.Recuperados_Relevantes/self.Relevantes
        return recobrado
    
    def MedidaF(self,beta):
        p=self.Presicion()
        r=self.Recobrado()
        if(p==0 or r==0):
            return 0
        med=((1+mt.pow(beta,2))*p*r)/((mt.pow(beta,2)*p)+r)
        return med
    
    def MedidaF1(self):
        p=self.Presicion()
        r=self.Recobrado()
        if(p==0 or r==0):
            return 0
        med= (2*p*r)/(p+r)
        return med

    def RPrecision(self,R):
        cant_relevantes=0
        for i in self.Documentos_Info:
            if i[2]>=1 and i[2]<=R and i[3]==1:
                cant_relevantes+=1
        
        return cant_relevantes/R

    def Fallout(self,R):
        cant_irrelevantes=0
        for i in self.Documentos_Info:
            if i[2]>=1 and i[2]<=R and i[3]==0:
                cant_irrelevantes+=1

        return cant_irrelevantes/self.Irrelevantes                
    


    
