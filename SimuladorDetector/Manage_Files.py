# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 16:23:14 2017

@author: angel
"""

import Generate_Ammeter_Charts as amp 
import pylab as py
import numpy as np
from numpy import random
import Menus as shw
import os as opt
import shutil as shu
import Menus as shi




"""-------------------------------------------------------------------------"""
"""(1)------------MANEJA LAS CARPETAS DE CARTAS Y SUS ARCHIVOS-----------------
dependiendo del valor que reciba del parametro "tipo" (numeros del 1 al 14)
trata el respectivo caso de tipo de falla en donde:
verifica existencia de carpetas, cuenta el numero de archivos en las mismas ,
crea nuevos archivos (cartas), borra existentes para reemplazarlos por nuevos
o regresa al menu principal
"""
def manage_dirs_charts(tipo):
    flag=0
    n_cartas=0
    carpt="a" #valor por defecto nunca usado
    
    # define la extension que se le agregara al directorio actual para crear ,
    # modificar o leer una carpeta dentro de el
    if tipo=="1":
        carpt="/1_operacion_normal"
    if tipo=="2":    
        carpt="/2_con_picos"
    if tipo=="3":
        carpt="/3_apagado_por_gas"
    if tipo=="4":
        carpt="/4_gas_en_bomba"
    if tipo=="5":
        carpt="/5_bajacarga"
    if tipo=="6":
        carpt="/6_sobrecarga"
    if tipo=="7":
        carpt="/7_descarga_fluido"
    if tipo=="8":
        carpt="/8_bajo_nivel_fluido_a"
    if tipo=="9":
        carpt="/9_bajo_nivel_fluido_b"
    if tipo=="10":
        carpt="/10_arranques_excesivos"
    if tipo=="11":
        carpt="/11_excesivos_ciclos_operacion"
    if tipo=="12":
        carpt="/12_cargas_en_superficie"
    if tipo=="13":
        carpt="/13_presencia_de_solidos"
    #if tipo=="14":
     #   generate_all_charts()
    if tipo=="15":
        shw.menu_main()
    
    #print(tipo)
    if tipo!="14" and tipo!="15":
        a=opt.getcwd() #me da directorio actual
        dt=a+carpt #creo la ruta del directorio que quiero crear
        b=opt.access(dt,opt.F_OK) #reviso si existe o no la carpeta
       
        if b==True:    #la carpeta existe
             c=opt.listdir(dt) #si la carpeta existe cuente cuantos archivos tiene
             flag=0
             #print(type(c),len(c))
             while flag==0:
                 print("\tel fichero", carpt,"contiene ", len(c),"cartas ")
                 print("\ta) si desea agregar mas cartas al fichero inserte 1")
                 print("\tb) si desea borrar las cartas existentes y crear un nuevo set presione 2")
                 print("\tc) si desea dejar el set de cartas actual y salir presione 3")
                 
                 resp=input("\t")
             
                 if resp=="1":
                     print("\tcuantas cartas nuevas desea agregar? ")
                     n_cartas=int(input("\t"))
                     flag=1
                     
                 elif resp=="2":
                     #print(dt)
                     shu.rmtree(dt)#PELIGRO CON ESTE COMANDO, ME BORRA EL DIRECTORIO Y TODO SU CONTENIDO, OJO A QUE DIRECTORIO SE HACE REFERENCIA
                     opt.mkdir(dt)#crea un nuevo directorio vacio
                     print("\tset de cartas borrados, cuantas cartas desea que tenga el nuevo set?")
                     flag=2
                     resp=input("\t")
                     n_cartas=int(resp)
                     flag=1
                     
                 elif resp=="3":#regresa al menu principal
                     shi.menu_main()
                     #print("Adios!")
                     flag=3
                     
                 else:   #si ninguna de las opciones es 1,2 o 3 pide datos nuevamente
                     print("\n")
                     print ("\tlos valores de eleccion deben ser 1,2,3; intente de nuevo")
                     
                 
        else:     #la carpeta no existe
            print("\tel fichero",carpt," no existe, desea crearlo? s/n")
            resp=input("\t")
            if resp =="s":    #si la respuesta es si
                opt.mkdir(dt) #cree la carpeta
                c=opt.listdir(dt) #cuente el numero de archivos (cero)
                print("\tel fichero",carpt,"fue creado exitosamente!")
                print("\tsi desea crear un set de cartas presione 1" ) 
                print("\tsi desea salir presione 2 " ) 
                resp=input("\t")
                if resp =="1": #si la respuesta es si pregunte y defina el numero de
                    flag=2     #cartas que tendra la carpeta
                    print("\tcuantas cartas desea que tenga el set")
                    resp=input("\t")
                    n_cartas=int(resp)
               
            else:
                print("\tel fichero",carpt," no fue creado")
        
        c=opt.listdir(dt)
        return flag, n_cartas,len(c),carpt
    
    elif tipo=="14":
        #print("aqui deberia construir mi funcion")
        generate_all_charts()
        print("\tCartas generadas con exito!, presione enter para continuar")
        input("\t")        
        shi.menu_main()
    return 3,0,0,0
"""(1)--------FIN MANEJA LAS CARPETAS DE CARTAS Y SUS ARCHIVOS--------------"""




"""-------------------------------------------------------------------------"""
"""(2)-----MANEJA LAS CARTAS Y LA MANERA EN QUE SE MOSTRARAN----------------"""
def manage_plot_charts(op,cont_fig):
    op=op-1
    
    muestras_minuto=1
    muestreo=24*muestras_minuto*60
    angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
    color=["k","y","b","r","g","m"]    
    plot_chart=["/1_operacion_normal","/2_con_picos","/3_apagado_por_gas",
       "/4_gas_en_bomba","/5_bajacarga","/6_sobrecarga","/7_descarga_fluido",
       "/8_bajo_nivel_fluido_a","/9_bajo_nivel_fluido_b","/10_arranques_excesivos",
       "/11_excesivos_ciclos_operacion","/12_cargas_en_superficie","/13_presencia_de_solidos"]    
   
    titulo=["Cartas de operacion normal","Cartas de falla picos de corriente",
            "Cartas de falla apagado por gas en la bomba","Cartas de falla gas libre en la bomba",
            "Cartas de falla corriente en baja carga","Cartas de falla corriente en sobrecarga",
            "Cartas de falla descarga de fluido","Cartas de falla bajo nivel de fluido con gas en la bomba",
            "Cartas de falla bajo nivel de fluido sin gas en la bomba","Cartas de falla con numero excesivo de arranques",
            "Cartas de falla con excesivos ciclos de operacion","Cartas de falla emulsiones o cargas en la superficie",
            "Cartas de falla con solidos en la bomba"]   
   #shi.clear_shell()
    print("\n\n")
    a=opt.getcwd() #me da directorio actual
    dt=a+plot_chart[op] #creo la ruta del directorio que quiero leer
    c=len(opt.listdir(dt))
    sel=0    
    while sel==0:
        print("\t¿Cuantas cartas de" ,plot_chart[op],"desea mostrar?")
        print("\n\t1)una carta\n\t2)varias cartas")
        resp=int(input("\n\t"))
        try:        
            if resp==1:
                sel2=0
                while sel2==0:
                    print("\n\tQue numero de carta (",plot_chart[op],") desea graficar?")
                    print("\t entre 1 y ", c )
                    ng=int(input("\n\t"))
                    long=ng
                    if ng>c:
                        print("\n\tEl numero de carta no existe, intente de nuevo")
                    else:
                        sel2=1
                        sel=1 
                        
                sel=1
            elif resp==2:
                sel1=0
                while sel1==0:
                    print("\n\tCual es el valor inicial (",plot_chart[op],") que desea graficar")
                    print("\t(recuerde que la carpeta tiene ", c , "cartas")            
                    vi=int(input("\t"))
                    print("\tCual es el valor final de carta ",plot_chart[op],"que desea graficar")
                    vf=int(input("\t"))
                    long=vf-vi
                    if vi>=vf:
                        #shi.clear_shell()
                        print("\n\tel valor inicial no puede ser mayor al valor final")
                        
                    else:
                        sel1=1
                        sel=1
            else:
                print("\n\tlas opciones son 1 o 2")
            #------------------------------------------------------------------
            if resp==2:
                c_color=0
                py.figure(titulo[op],figsize=(7, 7))
                #py.grid(False)
                print("ingrese el numero de filas")
                rows=int(input("\t"))
                print("ingrese el numero de columnas")
                columns=int(input("\t"))
                for i in range(long+1):
                    py.subplot(rows,columns,i+1)
                    chart=dt+"/"+str(op+1)+"_carta_"+str(i+vi)+".txt"
                    print(chart)                    
                    radio=np.loadtxt(chart)
                    x=-radio*np.cos(angle)
                    y=radio*np.sin(angle)
                    amp.plantilla(1,1,op,6,7,str(i+vi))
                    py.plot(x,y,color=color[c_color],linewidth=1)
                    #print("\t",chart)
                    c_color=c_color+1
                    if c_color>5:
                        c_color=0
            elif resp==1:
                a=color[random.randint(0,4)]
                py.figure(titulo[op],figsize=(5, 5))
                #py.grid(True)
                chart=dt+"/"+str(op+1)+"_carta_"+str(long)+".txt"
                print(chart)                
                radio=np.loadtxt(chart)
                x=-radio*np.cos(angle)
                y=radio*np.sin(angle)
                amp.plantilla(1,1,op,7,10,str(long))
                py.plot(x,y,color=a,linewidth=1)
                #print("\t",chart)
                
            #------------------------------------------------------------------            
        except:
            print("\talgunos de los datos son erroneos, por favor intente e nuevo")
            shi.clear_shell()
"""(2)------FIN MANEJA LAS CARTAS Y LA MANERA EN QUE SE MOSTRARAN-----------"""




"""-------------------------------------------------------------------------"""
"""(3)------GENERA TODOS LOS TIPOS DE CARTAS--------------------------------"""
def generate_all_charts():
    
    
    
    carpets_chart=["/1_operacion_normal","/2_con_picos","/3_apagado_por_gas",
       "/4_gas_en_bomba","/5_bajacarga","/6_sobrecarga","/7_descarga_fluido",
       "/8_bajo_nivel_fluido_a","/9_bajo_nivel_fluido_b","/10_arranques_excesivos",
       "/11_excesivos_ciclos_operacion","/12_cargas_en_superficie","/13_presencia_de_solidos"]  
    a=opt.getcwd()
    
    sel=0
    while sel==0:
        print("\tSe vaciaran todas las carpetas y se crearan nuevas cartas, esta de acuerdo? s/n")
        r=input("\t")
        if r=="s":
            sel=1
            for i in carpets_chart:
                
                #print(i)
                
                dtt=a+i
                if opt.access(dtt,opt.F_OK)==True:
                    shu.rmtree(dtt)#PELIGRO CON ESTE COMANDO, ME BORRA EL DIRECTORIO Y TODO SU CONTENIDO, OJO A QUE DIRECTORIO SE HACE REFERENCIA
                    opt.mkdir(dtt)#crea un nuevo directorio vacio
                else:
                    opt.mkdir(dtt)
                    
            sel1=0
           
            print("\tcartas borradas")
            while sel1==0  : 
                 
                 print("\tCuantas cartas desea que contenga cada carpeta?")    
                 try:
                    n_c=int(input("\t"))
                    sel1=1
                 except:
                    print("\tdebe ingresar un numero entero")
            
            #------------------------------------------------------------------
             
            a=opt.getcwd()
            for pos, i in enumerate(carpets_chart):
                for j in range(n_c):
                    name_chart=a+i+"/"+str(pos+1)+"_carta_"+str(j+1)+".txt"
                    name_chart_default=a+i+"/"+str(pos+1)+"_carta_"+str(j)+".txt"
                    
                    print("\tse ha creado ", name_chart)
                    resp=str(pos+1)  
                    mostrar=0
                    if resp=="1":
                        radio=amp.sim_current_pump_normal(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                #1
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="2":
                        radio=amp.sim_current_pump_peaks(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                 #2
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="3":
                        radio=amp.sim_current_block_gas(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                  #3
                        np.savetxt(name_chart,(radio))    
                        
                    elif resp=="4":
                        radio=amp.sim_current_pump_gas_free_in_pump(In=6,k=0.3,plotear=mostrar,default=name_chart_default)      #4
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="5":
                        radio=amp.sim_current_pump_low_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)              #5
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="6":
                        radio=amp.sim_current_pump_over_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)             #6
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="7":
                        radio=amp.sim_current_pump_download_fluid(In=6,k=0.3,plotear=mostrar,default=name_chart_default)        #7
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="8":
                        radio=amp.sim_current_low_level_fluid_1(In=6,k=0.3,plotear=mostrar,default=name_chart_default)          #8
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="9":
                        radio=amp.sim_current_low_level_fluid_2(In=6,k=0.3,plotear=mostrar,default=name_chart_default)  
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="10":
                        radio=amp.sim_current_pump_excesive_starts(In=6,k=0,plotear=mostrar,default=name_chart_default)        #10
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="11":
                        radio=amp.sim_current_excesive_operate_cicles(In=6,k=0.3,plotear=mostrar,default=name_chart_default)   #11
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="12":
                        radio=amp.sim_current_pump_surface_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)         #12
                        np.savetxt(name_chart,(radio))
                        
                    elif resp=="13":
                        radio=amp.sim_current_solid_in_pump(In=6,k=0.3,plotear=mostrar,default=name_chart_default)             #13
                        np.savetxt(name_chart,(radio))
                print("\n")
            
        elif r=="n":
            sel=1
            shi.menu_main()
            
        else:
            print("Opcion no valida intente de nuevo (n/s)")
"""(3)----------------FIN GENERA TODOS LOS TIPOS DE CARTAS------------------"""    
    



"""-------------------------------------------------------------------------"""
"""(4)--------------CARTAS DESCONOCIDAS A ESTIMAR---------------------------"""     
def probe_charts_unknow(k,clf):
    a=opt.getcwd() #me da directorio actual
    dt=a+"/Archivos_a_estimar/" #creo la ruta del directorio que quiero crear
    b=opt.access(dt,opt.F_OK) #reviso si existe o no la carpeta
    if b==True:    #la carpeta existe
        c=opt.listdir(dt)
    else:
        opt.mkdir(dt) #cree la carpeta
        c=opt.listdir(dt) #cuente el numero de archivos (cero)
    py.figure()
    #k=15;
    op=0
    prediccion=np.zeros(k)
    real=np.zeros(k)
    predicciones=[]
    for i in range(k):
        #amp.plantilla(1,1,op,6,7,str(i))
                        
        h=i+1
        py.subplot(4,8,h)
       
        mostrar=1
        name_chart=dt+str(i+1)+"_carta.txt"
        resp=random.randint(1,14)
        name_chart_default=dt+str(i-1)+"carta.txt"
        
        if resp==1:
            radio=amp.sim_current_pump_normal(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                #1
            np.savetxt(name_chart,(radio))
                        
        elif resp==2:
            radio=amp.sim_current_pump_peaks(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                 #2
            np.savetxt(name_chart,(radio))
                        
        elif resp==3:
            radio=amp.sim_current_block_gas(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                  #3
            np.savetxt(name_chart,(radio))    
                        
        elif resp==4:
            radio=amp.sim_current_pump_gas_free_in_pump(In=6,k=0.3,plotear=mostrar,default=name_chart_default)      #4
            np.savetxt(name_chart,(radio))
                        
        elif resp==5:
            radio=amp.sim_current_pump_low_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)              #5
            np.savetxt(name_chart,(radio))
                        
        elif resp==6:
            radio=amp.sim_current_pump_over_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)             #6
            np.savetxt(name_chart,(radio))
                    
        elif resp==7:
            radio=amp.sim_current_pump_download_fluid(In=6,k=0.3,plotear=mostrar,default=name_chart_default)        #7
            np.savetxt(name_chart,(radio))
                        
        elif resp==8:
            radio=amp.sim_current_low_level_fluid_1(In=6,k=0.3,plotear=mostrar,default=name_chart_default)          #8
            np.savetxt(name_chart,(radio))
                        
        elif resp==9:
            radio=amp.sim_current_low_level_fluid_2(In=6,k=0.3,plotear=mostrar,default=name_chart_default)  
            np.savetxt(name_chart,(radio))
                        
        elif resp==10:
            radio=amp.sim_current_pump_excesive_starts(In=4,k=0,plotear=mostrar,default=name_chart_default)        #10
            np.savetxt(name_chart,(radio))
                        
        elif resp==11:
            radio=amp.sim_current_excesive_operate_cicles(In=6,k=0.3,plotear=mostrar,default=name_chart_default)   #11
            np.savetxt(name_chart,(radio))
                        
        elif resp==12:
            radio=amp.sim_current_pump_surface_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)         #12
            np.savetxt(name_chart,(radio))
                        
        elif resp==13:
            radio=amp.sim_current_solid_in_pump(In=6,k=0.3,plotear=mostrar,default=name_chart_default)             #13
            np.savetxt(name_chart,(radio))
        
        real[i]=resp
        prediccion[i]=clf.predict(radio)
        
        if clf.predict(radio)/10==resp:
            ticket="ACIERTO"
        else:
            ticket="ERROR"
            
        amp.plantilla(1,0,resp,4,4,str(i+1))
        py.text(0, 0, "FALLA "+str(resp)+"\n"+ticket, horizontalalignment='center',
                verticalalignment='center',fontsize=6,color='k')
        
        aux=str(i+1)+ ") Falla " + str(prediccion[i]/10) 
        predicciones.append(aux)  
   
    print("Valores Estimados\n")
    shi.clear_shell()   
    predicciones=np.array(predicciones)
    predicciones.reshape(8,4)
    print(predicciones)
      
    py.show()
"""(4)----------FIN CARTAS DESCONOCIDAS A ESTIMAR---------------------------"""
