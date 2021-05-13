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

    acumular_precision=0
    acumular_recobrado=0
    acumular_medidaf=0
    acumular_medidaf1=0
    acumular_rpresicion=0
    acumular_fallout=0

    def EjecutaConsulta(num):
        
        new_consulta=Modelo.Retroalimentacion(pc.relevancia[str(num)],pc.ListQuery[num-1][2])
        Modelo.Ranking_Doc(new_consulta)
    
        
        st.warning("Procesando la query: "+str(num))
        
        Documentos_Procesados=[]
        count=1
        id_con=(num)
        rel=pc.relevancia[str(num)]
        #print("el len del ranking es: "+str(len(Modelo.Ranking)))
        #st.markdown("Se recuperaron los documentos:")
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
                #st.text(str(id_doc+1)+": "+str(pdc.ListDoc[id_doc][1]))
            
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
        #a=acumular_precision+presicion
        #acumular_precision=a
        recobrado=Evaluacion.Recobrado()
        #b=acumular_recobrado+recobrado
        #acumular_recobrado=b
        medidaf=Evaluacion.MedidaF(0)
        #c=acumular_medidaf+medidaf
        #acumular_medidaf=c
        medidaf1=Evaluacion.MedidaF1()
        #d=acumular_medidaf1+medidaf1
        #acumular_medidaf1=d
        rpresicion=Evaluacion.RPrecision(20)
        #e=acumular_rpresicion+rpresicion
        #acumular_rpresicion=e
        fallout=Evaluacion.Fallout(20)
        #f=acumular_fallout+fallout
        #cumular_fallout=f
        

        st.success("Evaluacion en la query: "+str(num))
        st.text("Esta es la precision: "+str(presicion))
        st.text("Esta es el Recobrado: "+str(recobrado))
        st.text("Esta es la MedidaF: "+str(medidaf))
        st.text("Esta es la MedidaF1: "+str(medidaf1))
        st.text("Esta es la RPresicion: "+str(rpresicion))
        st.text("Esta es la Fallout: "+str(fallout))
    
    for i in range(1,21):
        EjecutaConsulta(i)
    
    #promedio_presicion=acumular_precision/20
   # promedio_recobrado=acumular_recobrado/20
   # promedio_medidaf=acumular_medidaf/20
   # promedio_medidaf1=acumular_medidaf1/20
  #  promedio_rpresecion=acumular_rpresicion/20
  #  promedio_fallout=acumular_fallout/20

  #  st.success("Evaluacion del Modelo")
  #  st.text("Esta es la precision: "+str(promedio_presicion))
  #  st.text("Esta es el Recobrado: "+str(promedio_recobrado))
  #  st.text("Esta es la MedidaF: "+str(promedio_medidaf))
  #  st.text("Esta es la MedidaF1: "+str(promedio_medidaf1))
   # st.text("Esta es la RPresicion: "+str(promedio_rpresecion))
  #  st.text("Esta es la Fallout: "+str(promedio_fallout))


    

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


