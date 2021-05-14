import streamlit as st 
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


import numpy as np
import procdoc as pdc





import proccon as pc 



import modelo as md
import evalmodelo as em


#pdc.Cargar('CRAN.ALL')
#pc.Query('CRAN.QRY',pdc.ListTerm)
#pc.Carga_Relevancia('CRAN.REL')

#Matriz=[]
#for terms in pdc.ListTerm:
#    Matriz.append(pdc.ListTerm[terms])
####
#print(len(Matriz))
###
#print(pc.ListQuery[2][1])
#Modelo=md.Vectorial(Matriz,pdc.ListMaxDoc)


def main():
    st.title("Sistema de Recuperación de Información")

    juego_datos=st.text_input("Introduzca el nombre del set de datos a utilizar","Set")

    #if(st.button("Procesar")):
    if(st.checkbox("Procesar las consultas del set de datos")):

        pdc.ListDoc=[]
        pdc.ListTerm={}
        pdc.ListTermAux=[]
        pdc.ListMaxDoc=[]
        pc.ListQuery=[]
        pc.relevancia={}

        pdc.Cargar(juego_datos+'.ALL')
        pc.Query(juego_datos+'.QRY',pdc.ListTerm)
        pc.Carga_Relevancia(juego_datos+'.REL')

        EjecutaModelo()
    
    if(st.checkbox("Realizar una consulta nueva sobre el set de datos")):
        consulta_usuario=st.text_input("Introduzca que consulta desea realizar sobre el set anterior","Consulta")
        if(st.button("Procesar")):
            pdc.ListDoc=[]
            pdc.ListTerm={}
            pdc.ListTermAux=[]
            pdc.ListMaxDoc=[]
            pc.ListQuery=[]
            pc.relevancia={}
            cant_consultas=1
            pdc.Cargar(juego_datos+'.ALL')
            query=pc.PreparaQuery(consulta_usuario,cant_consultas,len(pdc.ListTerm),pdc.ListTerm)
            Consulta_Usuario(query,cant_consultas)



    

        
    
    



def EjecutaModelo():
    Matriz=[]
    for terms in pdc.ListTerm:
        Matriz.append(pdc.ListTerm[terms])
    print(len(Matriz))
    Modelo=md.Vectorial(Matriz,pdc.ListMaxDoc)

    Promedio={}
    Promedio["precision"]=0
    Promedio["recobrado"]=0
    Promedio["medidaf"]=0
    Promedio["medidaf1"]=0
    Promedio["rpresicion"]=0
    Promedio["fallout"]=0

    def EjecutaConsulta(num):
        try:
            new_consulta=Modelo.Retroalimentacion(pc.relevancia[str(num)],pc.ListQuery[num-1][2])
            Modelo.Ranking_Doc(new_consulta)
        except:
            Modelo.Ranking_Doc(pc.ListQuery[num-1][2])
        
        st.warning("Procesando la query: "+str(num))
        
        Documentos_Procesados=[]
        count=1
        id_con=(num)
        try:
            rel=pc.relevancia[str(num)]
        except:
            rel=[]
        #print("el len del ranking es: "+str(len(Modelo.Ranking)))
        st.markdown("Se recuperaron los documentos:")
        for i in Modelo.Ranking:
            #print(str(i[1])+" el ranking es: "+str(i[0]))
            id_doc=i[1]
            ranking=i[0]
            doc_rel=0
            rec=0
            if(rel.__contains__(id_doc)):
                doc_rel=1
                
            if count<=20:
                rec=1
                if count <=10:
                    st.text(str(id_doc+1)+": "+str(pdc.ListDoc[id_doc][1]))
            
            tupla=(id_doc,rec,count,doc_rel,id_con)
            
            #print(tupla)
            Documentos_Procesados.append(tupla)
            #if(count<=40):
            #    print(tupla)
            count+=1

        #print("el len de doc_procesados es: "+str(len(Documentos_Procesados)))
        Evaluacion=em.Evaluacion(Documentos_Procesados)
        #Evaluacion.LlenaVariables()

        presicion=Evaluacion.Presicion()
        Promedio["precision"]+=presicion
        recobrado=Evaluacion.Recobrado()
        Promedio["recobrado"]+=recobrado
        medidaf=Evaluacion.MedidaF(0)
        Promedio["medidaf"]+=medidaf
        medidaf1=Evaluacion.MedidaF1()
        Promedio["medidaf1"]+=medidaf1
        rpresicion=Evaluacion.RPrecision(20)
        Promedio["rpresicion"]+=rpresicion
        fallout=Evaluacion.Fallout(20)
        Promedio["fallout"]+=fallout
        

        #st.success("Evaluacion en la query: "+str(num))
        #st.text("Esta es la precision: "+str(presicion))
        #st.text("Esta es el Recobrado: "+str(recobrado))
        #st.text("Esta es la MedidaF: "+str(medidaf))
        #st.text("Esta es la MedidaF1: "+str(medidaf1))
        #st.text("Esta es la RPresicion: "+str(rpresicion))
        #st.text("Esta es la Fallout: "+str(fallout))
    
    for i in range(1,11):
        EjecutaConsulta(i)

    promedio_presicion=Promedio["precision"]/10
    promedio_recobrado=Promedio["recobrado"]/10
    promedio_medidaf=Promedio["medidaf"]/10
    promedio_medidaf1=Promedio["medidaf1"]/10
    promedio_rpresecion=Promedio["rpresicion"]/10
    promedio_fallout=Promedio["fallout"]/10

    st.success("Evaluacion del Modelo")
    st.text("Esta es la precision: "+str(promedio_presicion))
    st.text("Esta es el Recobrado: "+str(promedio_recobrado))
    st.text("Esta es la MedidaF: "+str(promedio_medidaf))
    st.text("Esta es la MedidaF1: "+str(promedio_medidaf1))
    st.text("Esta es la RPresicion: "+str(promedio_rpresecion))
    st.text("Esta es la Fallout: "+str(promedio_fallout))


    

def Consulta_Usuario(query_user,num):
    Matriz=[]
    for terms in pdc.ListTerm:
        Matriz.append(pdc.ListTerm[terms])
    print(len(Matriz))
    Modelo=md.Vectorial(Matriz,pdc.ListMaxDoc)

    Modelo.Ranking_Doc(query_user[2])
    
    
    
    st.success("Procesando la consulta realizada por el usuario")
    
    Documentos_Procesados=[]
    count=1
    id_con=(num)
    #print("el len del ranking es: "+str(len(Modelo.Ranking)))
    st.markdown("Se recuperaron los documentos:")
    for i in Modelo.Ranking:
        #print(str(i[1])+" el ranking es: "+str(i[0]))
        id_doc=i[1]
        ranking=i[0]
        doc_rel=0
        rec=0
        
                
        if count<=20:
            rec=1
            st.text(str(id_doc)+": "+str(pdc.ListDoc[id_doc][1]))
        else:
            break    

        count+=1

     

    


    

#for i in range(1,20):
#    EjecutaConsultas(i)
    

if __name__=='__main__':
    main()


