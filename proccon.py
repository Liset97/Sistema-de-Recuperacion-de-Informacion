import json
import numpy as np 
import procdoc as pd
#Realmente esto no lo hare asi, sino q para utilizar el modulo este tenga que mandar el diccionario de terminos


#
#En ListQuery guardare tuplas de la forma <id_q,text,[vector con todas las palabras]>
#
ListQuery=[]

def Query(query,list_term):
    with open('datasets/'+query+'.json') as file:
        data = json.load(file)

        print(len(list_term))
        for i in data:
            text=data[i]["text"].lower()

            new=text.split(' ')
            for j in range(0,len(new)):
                temp=new[j]
                temp1=temp.split(',')
                temp2=temp1[0].split('.')
                temp3=temp2[0].split('?')
                new[j]=temp3[0]

            agregar=[]
            for t in new:
                if(not(pd.inutiles.__contains__(t))):
                    agregar.append(t)

            tupla=(data[i]["id"],agregar,[0 for x in range(0,len(list_term))])
            ListQuery.append(tupla)


    count=0
    for term in list_term:
        for consulta in ListQuery:
            suma=len([1 for x in consulta[1] if term==x])
            consulta[2][count]=suma
                
        count+=1


def PreparaQuery(text_consulta,id_new,lon_ter,list_term):
    text_new=text_consulta.lower()
    new=text_new.split(' ')
    for j in range(0,len(new)):
        temp=new[j]
        temp1=temp.split(',')
        temp2=temp1[0].split('.')
        temp3=temp2[0].split('?')
        new[j]=temp3[0]
    
    agregar=[]
    for t in new:
        if(not(pd.inutiles.__contains__(t))):
            agregar.append(t)

    tupla=(id_new,agregar,[0 for x in range(0,lon_ter)])

    count=0
    for term in list_term:
        suma=len([1 for x in agregar if term==x])
        tupla[2][count]=suma
                
        count+=1
    
    return tupla

    

    
    





print(len(ListQuery))

relevancia={}
def Carga_Relevancia(rel):

    with open('datasets/'+rel+'.json') as file:
        data = json.load(file)
        for i in data:
            relevantes=[]
            for j in data[i]:
                relevantes.append(int(j))
            
            relevancia[i]=relevantes
        
#print(relevancia)

