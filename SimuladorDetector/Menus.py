# -*- coding: utf-8 -*-
"""
Created on Tue May 30 08:36:04 2017

@author: angel
"""

import Generate_Ammeter_Charts as amp 
import pylab as py
#import matplotlib.pyplot as py
import numpy as D
import Manage_Files as mf
import os as opt
import Training_Set as tr
import pickle as pick
#C=1
#gamma=0.001




"""-------------------------------------------------------------------------"""
"""(1)----------------------------MENU PRINCIPAL-------------------------------
donde se muestra el membrete del programa y las distintas opciones que ofrece
al usuario. 
"""
def menu_main(NC=5,Ngamma=0.001):
    C=NC
    gamma=Ngamma

    clear_shell()
    #--------------------------------MEMBRETE----------------------------------
    print("\n\n \tSIMULACION Y RECONOCIMIENTO DE PATRONES DE FALLA EN EL SISTEMA BES ")
    print("\n\tAngel Leonardo Duarte Montes")
    print("\tV-19134002")
    print("\tUniversidad Nacional Experimental del Táchira UNET")
    print("\tPDVSA, AIT Corportativo, DST Merida-Venezuela ")
    print("\n \n \n")
    #----------------------------FIN MEMBRETE----------------------------------
    
    #------------------------OPCIONES DE SELECCION----------------------------
    print("\t!BIENVENIDO!!, que desea hacer? \n")
    flag=0
    while(flag==0):
        print("\t1)Generar escenarios de fallas (cartas amperimetricas) en el sistema BES" )
        print("\t2)Consultar numero de cartas existentes actualmente")
        print("\t3)Graficar cartas")    
        print("\t4)Entrenar el modelo de Reconocimiento")
        print("\t5)Estimar tipo de falla con el modelo d Reconomiento")
        print("\t6)Graficas ROC para Maquina Soporte Vectorial")
        print("\t7)Curva de Aprendizaje")
        print("\t8)Calcular parametros C y gamma para MSV")
        print("\t9)Salir")
        resp=input("\n\t")
        
        clear_shell()
        
        if resp=="1":
            menu_1(rows=3,columns=4)
            flag=1
        elif resp=="2":
            #print("2 En construccion") 
            menu_2()
            flag=1            
        elif resp=="3":
            #print("3 En construccion")  
            menu_3()
            flag=1
        elif resp=="4":
            menu_4(C,gamma)
            flag=1
        elif resp=="5":
            menu_5(C,gamma)
            flag=1
        elif resp=="6":
            menu_6(C,gamma)
            flag=1
        elif resp=="7":
            menu_7(C,gamma)
            flag=1    
        elif resp=="8":
            menu_8() 
            flag=1         
        elif resp=="9":
            print("Adios!!") 
            flag=1         
            break
            
        else:
            print("Debe seleccionar una opcion valida (1 al 9), intente de nuevo.\n")
    #-----------------------FIN OPCIONES DE SELECCION--------------------------            
"""(1)---------------------FIN DE MENU PRINCIPAL----------------------------"""




"""-------------------------------------------------------------------------"""
"""(2)-----------------------LIMPIAR CONSOLA-----------------------------------
imprime cierta cantidad de espacios en blanco o "saltos de carro" que dan la
sensacion de que se limpia la consola
"""
def clear_shell():
    for n in range(100):
        print("\n")
"""(2)--------------------FIN DE LIMPIAR CONSOLA----------------------------"""
        



"""-------------------------------------------------------------------------"""
"""(3)-----------------MENU GENERAR CARTAS AMPERIMETRICAS----------------------
presenta las multiples opciones de cartas que puede generar el usuario, asi como
una serie de submenus que permiten decidir si se agregan nuevas cartas, se borran
las existentes o se conservan. ademas da la opcion de imprimir las cartas generadas
una vez se han terminado de crear (no se recomienda imprimirlas si el numero de
cartas generadas es alto (quizas mayor a veinte) )
"""
def menu_1(rows=3,columns=4):   
    n_plots=columns*rows
    opcion=0
    
    #-------------------OPCIONES DE SELECCION----------------------------------
    while opcion==0:
        sel=0
        while sel==0:
            #clear_shell()
            print("\tOPCION 1: Que tipo de carta desea generar  \n ")
            print("\t1) Operacion normal" )                                        
            print("\t2)  Falla picos de corriente  ")
            print("\t3)  Falla apagado por gas en la bomba  ")                       
            print("\t4)  Falla por gas libre en la bomba  ")
            print("\t5)  Falla por corriente en bajacarga  ")                        
            print("\t6)  Falla por corriente en sobrecarga  ")
            print("\t7)  Falla por descarga de fluido  ")                           
            print("\t8)  Falla por bajo nivel de fluido con gas en la bomba ")
            print("\t9)  Falla por bajo nivel de fluido sin gas en la bomba ")      
            print("\t10) Falla por numero excesivo de arranques  ")
            print("\t11) Falla por excesivos ciclos de operacion ")                 
            print("\t12) Falla por emulsiones o cargas en superficie ")
            print("\t13) Falla por solidos en la bomba " )
            print("\t14) Generar cartas de todos los tipos")
            print("\t15) Regresar al menu anterior " )
            
            try:
                resp=input("\n\t")
                aux=int(resp)
                if aux>0 and aux<16 :
                    sel=1
                else:
                    print("\n\tingreso una opcion no valida, intente de nuevo")
            except:
                print("\n\tingreso una opcion no valida, intente de nuevo")
                
            print("\n")
            
        [flag, n_plots, init,carpt]=mf.manage_dirs_charts(tipo=resp) 
        if(flag==3):
            break            
    #----------------------FIN OPCIONES DE SELECCION---------------------------
        
    #-----------------------OPCIONES PARA  MOSTRAR GRAFICAS--------------------        
        """ Decidi quitar la parte de mostrar las graficas en la creacion para
            hacer mas sencillo y rapido el proceso y dejar la parte de la visualizacion
            en un menu aparte
        print("\tquiere mostrar las graficas s/n")
        mt=input("\n\t")
        ft=0
        if mt=="s":
            mostrar=1
            while ft==0:
                print("\ten cuantas filas ")
                f=input("\t")
                rows=int(f)
                print("\ten cuantas columnas ")
                c=input("\t")
                columns=int(c)
                if(columns*rows!=n_plots):
                    print("\tel numero de filas por columnas debe ser igual a", n_plots,"intente de nuevo")
                else:
                    ft=1                         
        elif mt=="n":
            mostrar=0
        """
        mostrar=0     
        if mostrar==1:     
            
            escala=1
            muestras_minuto=1
            muestreo=24*muestras_minuto*60
            angle=D.arange(0,2*D.pi,(2*D.pi)/muestreo)
            py.figure(figsize=(7*escala, 7*escala))
            py.grid(True)
            py.xlim(xmin=-(10*escala), xmax=(10*escala))
            py.ylim(ymin=-(10*escala), ymax=(10*escala))
        
        for i in range(n_plots):
            print("procesando el ejemplo",i+1+init, "de ",n_plots+init)
            n=i+1+init
            print("\n")
            
            if mostrar==1:
                py.subplot(rows,columns,i) 
    #------------------FIN OPCIONES PARA  MOSTRAR GRAFICAS---------------------     
                
                #----------impresion de planillas de fondo--------------------               
                for i in range(1,9,1): #circunferencias de la plantilla
                    radio=i
                    x=radio*D.cos(angle)
                    y=radio*D.sin(angle)
                    py.plot(x,y,color="k")    
                angle_step=D.pi/12
                
                rmax=8    
                for j in range(24): #radios de la plantilla
                    yf=rmax*D.sin(angle_step*j-D.pi/2)
                    xf=rmax*D.cos(angle_step*j-D.pi/2)
                    y=D.linspace(0,yf,100)
                    x=D.linspace(0,xf,100)
                    py.plot(y,x,color="k")
                #--------------fin impresion planillas de fondo----------------
        
            #-llama a funciones que crean los tipos de carta segun sea el caso-        
            if resp=="1":
                name_chart=opt.getcwd()+carpt+"/1_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/1_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_pump_normal(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                #1
                D.savetxt(name_chart,(radio))
                
            elif resp=="2":
                name_chart=opt.getcwd()+carpt+"/2_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/2_carta_"+str(n-1)+".txt"
                radio=amp.sim_current_pump_peaks(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                 #2
                D.savetxt(name_chart,(radio))
                
            elif resp=="3":
                name_chart=opt.getcwd()+carpt+"/3_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/3_carta_"+str(n-1)+".txt"
                radio=amp.sim_current_block_gas(In=6,k=0.3,plotear=mostrar,default=name_chart_default)                  #3
                D.savetxt(name_chart,(radio))    
                
            elif resp=="4":
                name_chart=opt.getcwd()+carpt+"/4_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/4_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_pump_gas_free_in_pump(In=6,k=0.3,plotear=mostrar,default=name_chart_default)      #4
                D.savetxt(name_chart,(radio))
                
            elif resp=="5":
                name_chart=opt.getcwd()+carpt+"/5_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/5_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_pump_low_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)              #5
                D.savetxt(name_chart,(radio))
                
            elif resp=="6":
                name_chart=opt.getcwd()+carpt+"/6_carta_"+str(n)+".txt"   
                name_chart_default=opt.getcwd()+carpt+"/6_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_pump_over_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)             #6
                D.savetxt(name_chart,(radio))
                
            elif resp=="7":
                name_chart=opt.getcwd()+carpt+"/7_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/7_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_pump_download_fluid(In=6,k=0.3,plotear=mostrar,default=name_chart_default)        #7
                D.savetxt(name_chart,(radio))
                
            elif resp=="8":
                name_chart=opt.getcwd()+carpt+"/8_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/8_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_low_level_fluid_1(In=6,k=0.3,plotear=mostrar,default=name_chart_default)          #8
                D.savetxt(name_chart,(radio))
                
            elif resp=="9":
                name_chart=opt.getcwd()+carpt+"/9_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/9_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_low_level_fluid_2(In=6,k=0.3,plotear=mostrar,default=name_chart_default)  
                D.savetxt(name_chart,(radio))#9
                
            elif resp=="10":
                name_chart=opt.getcwd()+carpt+"/10_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/10_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_pump_excesive_starts(In=4,k=0,plotear=mostrar,default=name_chart_default)        #10
                D.savetxt(name_chart,(radio))
                
            elif resp=="11":
                name_chart=opt.getcwd()+carpt+"/11_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/11_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_excesive_operate_cicles(In=6,k=0.3,plotear=mostrar,default=name_chart_default)   #11
                D.savetxt(name_chart,(radio))
                
            elif resp=="12":
                name_chart=opt.getcwd()+carpt+"/12_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/12_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_pump_surface_load(In=6,k=0.3,plotear=mostrar,default=name_chart_default)         #12
                D.savetxt(name_chart,(radio))
                
            elif resp=="13":
                name_chart=opt.getcwd()+carpt+"/13_carta_"+str(n)+".txt"
                name_chart_default=opt.getcwd()+carpt+"/13_carta_"+str(n-1)+".txt" 
                radio=amp.sim_current_solid_in_pump(In=6,k=0.5,plotear=mostrar,default=name_chart_default)             #13
                D.savetxt(name_chart,(radio))
            #-fin llama a funciones que crean los tipos de carta segun sea e lcaso-  
    
        if resp!="14" and resp!="15" :   
            print("\tdesea generar otro tipo de carta? s/n")
            resp=input("\n\t")
    
            if resp=="n":
                opcion=1
                print("fin ¡¡")		
                
                if mostrar==1:
                    py.show()
                else:
                    menu_main()
                    
            else:
                clear_shell()
        
"""(3)-------------FIN MENU GENERAR CARTAS AMPERIMETRICAS-------------------"""


  
          
"""-------------------------------------------------------------------------"""
"""(4)-----------------MENU CONSULTAR CARTAS EXISTENTES------------------------
Recorre cada una de las carpetas en donde se almacenan las cartas generadas y
cuenta el numero de archivos existentes en ellas
"""
def menu_2():
    consult=["/1_operacion_normal","/2_con_picos","/3_apagado_por_gas",
       "/4_gas_en_bomba","/5_bajacarga","/6_sobrecarga","/7_descarga_fluido",
       "/8_bajo_nivel_fluido_a","/9_bajo_nivel_fluido_b","/10_arranques_excesivos",
       "/11_excesivos_ciclos_operacion","/12_cargas_en_superficie","/13_presencia_de_solidos"]
       
    info=["Operacion normal","Falla picos de corriente","Falla apagado por gas en la bomba",                       
            "Falla por gas libre en la bomba","Falla por corriente en bajacarga",                        
            "Falla por corriente en sobrecarga","Falla por descarga de fluido",                           
            "Falla por bajo nivel de fluido con gas en la bomba","Falla por bajo nivel de fluido sin gas en la bomba ",      
            "Falla por numero excesivo de arranques","Falla por excesivos ciclos de operacion",                 
            "Falla por emulsiones o cargas en superficie","Falla por solidos en la bomba " ]
    
    
    print("\n \n\t OPCION 2: NUMERO DE CARTAS EXISTENTES\n \n")
    
    for i in range(len(consult)):           
         dt=opt.getcwd()+consult[i]
         c=opt.listdir(dt)
         print("\t",i+1,") existen ", len(c), "cartas de ",info[i])
         print("\talmacenadas en ", dt)
         print("\n")
    print("\n\tpresione ENTER para volver al menu principal")
    input("\n\t")
    menu_main()
"""(4)-----------------FIN MENU CONSULTAR CARTAS EXISTENTES-----------------"""




"""-------------------------------------------------------------------------"""
"""(5)----------------MENU CARGAR Y MOSTRAR CARTAS-----------------------------
"""
def menu_3():
    cont_fig=1
    opcion=0
    while opcion==0:
        print("\n\tOPCION 3: GRAFICAR CARTAS\n")
        print("\tque tipo de carta desea graficar?\n")
        sel=0
        while sel==0:
            print("\t1) Operacion normal" )                                        
            print("\t2)  Falla picos de corriente  ")
            print("\t3)  Falla apagado por gas en la bomba  ")                       
            print("\t4)  Falla por gas libre en la bomba  ")
            print("\t5)  Falla por corriente en bajacarga  ")                        
            print("\t6)  Falla por corriente en sobrecarga  ")
            print("\t7)  Falla por descarga de fluido  ")                           
            print("\t8)  Falla por bajo nivel de fluido con gas en la bomba ")
            print("\t9)  Falla por bajo nivel de fluido sin gas en la bomba ")      
            print("\t10) Falla por numero excesivo de arranques  ")
            print("\t11) Falla por excesivos ciclos de operacion ")                 
            print("\t12) Falla por emulsiones o cargas en superficie ")
            print("\t13) Falla por solidos en la bomba " )
            print("\t14) Fallas Mixtas (no implementado) " )
            print("\t15) Volver al menu anterior " )
            try:
                resp=input("\n\t")
                aux=int(resp)
                if aux>0 and aux<15 :
                    sel=1
                    #print("\tparte de mostrar y cargar cartas")
                    mf.manage_plot_charts(aux,cont_fig)
                elif aux==15:
                    clear_shell()
                    sel=1
                    opcion=1
                    menu_main()
                    break
                else:
                    #print(aux)
                    clear_shell()
                    print("\n\tingreso una opcion no valida, intente de nuevo")
                    
            except:
                clear_shell()
                print("\n\tingreso una opcion no valida, intente de nuevo")
                menu_3()
            
           
        if aux!=15:       
            print("\n\tdesea cargar y ver  otro tipo de carta? s/n")
            print("\t(Todas las cartas se mostraran al final)")
            resp=input("\n\t")
            clear_shell()
            if resp=="n":
                opcion=1
                py.show()
                menu_main()
		
            else:
                clear_shell()
                cont_fig=cont_fig+1             
"""(5)------------------FIN MENU CARGAR Y MOSTRAR CARTAS--------------------"""




"""-------------------------------------------------------------------------"""
"""(6)------------------MENU DE ENTRENAMIENTO-------------------------------"""
def menu_4(C,gamma):   
    
    a=opt.getcwd() #me da directorio actual
    dt=a+"/Archivos_training" #creo la ruta del directorio que quiero crear
    b=opt.access(dt,opt.F_OK) #reviso si existe o no la carpeta
    if b==True:    #la carpeta existe
        c=opt.listdir(dt)
    else:
        opt.mkdir(dt) #cree la carpeta
        c=opt.listdir(dt) #cuente el numero de archivos (cero)
    
    print("\n\tPASO 1: Definir el set de datos.\n" )
    [data_random,resultado_r]=tr.generate_data_set(n_examples_d=50)
    D.savetxt(dt+"/Data.txt",(data_random))
    D.savetxt(dt+"/resultados.txt",(resultado_r))
    
    print("\n\t PASO 1 ejecutado exitosamente!!\n\n")
    
    print("\n\tPASO 2: Definir el set de entrenamiento\n")
  
    [training_set,training_results,valid_set,valid_results ]=tr.generate_training_set(data_random,resultado_r)
    print("\n\t PASO 2 ejecutado exitosamente!!\n\n")    
    
    resp=0
    while resp==0:
        
        print("\n\tPASO 3: Elegir Maquina de Aprendizaje y entrenar\n")
        [clf,opt_ma]=tr.select_and_training_Machine_learning(training_set,training_results,valid_set,valid_results,C,gamma)
        print("\n\t PASO 3 ejecutado exitosamente!!\n\n")
         
        print("\n\tPASO 4: Validar Resultados\n")
        [clf,n_ejemplos,prub_valid]=tr.validate(clf,valid_results,valid_set,data_random,resultado_r,opt_ma,C,gamma)
  
        output = open((dt+'/clf_SVM.pkl'), 'wb')
        pick.dump(clf, output)
       
        s=(dt+"/n_ejemplo.txt")
       
        n_ejemplo=D.array([n_ejemplos,prub_valid,opt_ma])
        D.savetxt(s,(n_ejemplo))
        print("\n\t PASO 4 ejecutado exitosamente!! \n\n")
        
        print("\tDesea entrenar la data con otra Maquina? s/n ")
        op=input("\t")
        if op=="n":
            resp=1
            menu_main()  
"""(6)--------------FIN MENU DE ENTRENAMIENTO-------------------------------"""



            
"""(7)----------------------------------------------------------------------"""
"""------------------------------------MENU ESTIMAR----------------------------
"""            
def menu_5(C,gamma):
    
    a=opt.getcwd() #me da directorio actual
    dt=a+"/Archivos_training" #creo la ruta del directorio que quiero crear
    b=opt.access(dt,opt.F_OK) #reviso si existe o no la carpeta
    if b==True:    #la carpeta existe
        c=opt.listdir(dt)
    else:
        opt.mkdir(dt) #cree la carpeta
 
    clf=actual_machine()
    print("esta de acuerdo estimar con ella? s/n")
    resp=input("")
    if resp=="s":
        #print("codigo de probar")
        mf.probe_charts_unknow(32,clf)
        menu_main()
    else:
        menu_main()             
"""(7)-----------------------FIN MENU ESTIMAR-------------------------------"""      
 



"""-------------------------------------------------------------------------"""
"""(8)----------------------MENU GRAFICAS ROC----------------------------------
"""      
def menu_6(C,gamma):
    
    actual_machine()
   # a=opt.getcwd() #me da directorio actual
    try:
        
        print("\n\nGenerando graficas ROC, espere ...") 
        tr.graphs_ROC()
        print("\n\tGraficas Generadas, presione ENTER ")
        input("\t")
        menu_main()
    except:
        print("esta maquina no es valida, la opcion de graficas ROC solo", 
        "esta disponible para la Maquina de soporte vectorial (SVM), presione ENTER para continuar")
        input("")
        menu_main()
"""(8)---------------------FIN MENU GRAFICAS ROC----------------------------"""     




"""-------------------------------------------------------------------------"""
"""(9)---------------------MENU CURVAS DE APRENDIZAJE--------------------------
"""  
def menu_7(C,gamma):
   
    clf=actual_machine()
    a=opt.getcwd() #me da directorio actual
    print("\tClasificador cargado\n")
    data=a+"/Archivos_training/Data.txt"
    resultado=a+"/Archivos_training/resultados.txt"
    #clasificador=a+"/Archivos_training/clf_SVM.pkl"
    
    X=D.loadtxt(data)
    print("\tData cargada")
    y=D.loadtxt(resultado)
    print("\tResultados cargados")

   
    print("\tEn proceso ...") 
    title="Curva de aprendizaje:"
    
    tr.plot_learning_curve(clf, title, X, y, ylim=None, cv=None,
    n_jobs=4, train_sizes=D.linspace(.1, 1.0, 10))        
    
    print("\n\tGraficas Generadas, presione ENTER")
    input("\t")
    menu_main()
"""(9)------------------FIN MENU CURVAS DE APRENDIZAJE----------------------"""    




"""-------------------------------------------------------------------------"""
"""(10)----------------------MENU CALCULO  PARAMETROS C Y GAMMA----------------
"""
def menu_8 ():
   
    actual_machine()
    a=opt.getcwd() #me da directorio actual
    data=a+"/Archivos_training/Data.txt"
    resultado=a+"/Archivos_training/resultados.txt"
    #clasificador=a+"/Archivos_training/clf_SVM.pkl"
    X=D.loadtxt(data)
    print("\tData cargada")
    y=D.loadtxt(resultado)
    print("\tResultados cargados")
   
    print("\tEn proceso ...") 
    print("\t Calcular los parametros optimos  de C y Gamma en la MSV")
    param_grid = {'C': [1, 2, 5, 10, 15 , 20],#, 50, 100, 500],
    'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01]}# ,0.001, 0.005, 0.01, 0.05 , 0.1
    [C,gamma]=tr.best_param(X,y,param_grid)
    print("\n\tGraficas Generadas, presione ENTER")
    input("\t")
    menu_main()
"""(10)------------------FIN MENU CALCULO  PARAMETROS C Y GAMMA-------------"""




"""-------------------------------------------------------------------------""" 
"""(11)---------------INFORMACION ULTIMA MAQUINA ENTRENADA---------------------
"""       
def actual_machine():
    
    a=opt.getcwd() #me da directorio actual
    dt=a+"/Archivos_training" #creo la ruta del directorio que quiero crear
    nmv=D.loadtxt(dt+"/n_ejemplo.txt")
    pkl_file = open((dt+'/clf_SVM.pkl'), 'rb')
    clf = pick.load(pkl_file)
    print("La ultima maquina entrenada es: \n")
    
    if nmv[2]==1:
        print("Maquina de soporte vectorial")
        print("C=",clf.get_params([True])['C'])
        print("gamma=",clf.get_params([True])['gamma'])
        
    elif nmv[2]==2:
        print("Arbol de decision")
        
    elif nmv[2]==3:
        print("Nayve Bayes")
        
    print("\nEntrenada con:",nmv[0],"ejemplos")
    print("Acierto del",nmv[1],"%") 

    return clf          
"""(11)-----------FIN INFORMACION ULTIMA MAQUINA ENTRENADA------------------"""
