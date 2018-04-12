# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 17:31:28 2017

@author: angel
"""
import numpy as D
from numpy import random
import Menus as shw
import os as opt
import math as mat
from sklearn import svm
import matplotlib.pyplot as plt
import pickle as pick
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
#from sklearn import linear_model
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from scipy import interp
from itertools import cycle
from sklearn.model_selection import learning_curve
from sklearn.model_selection import GridSearchCV




"""-------------------------------------------------------------------------"""
"""1)------------------- GENERAR EL SET DE DATOS-------------------------------
"""
def generate_data_set(n_examples_d=50):
    nc=0
    muestras_minuto=1
    muestreo=24*muestras_minuto*60
    tipos_c=["/1_operacion_normal","/2_con_picos","/3_apagado_por_gas",
    "/4_gas_en_bomba","/5_bajacarga","/6_sobrecarga","/7_descarga_fluido",
    "/8_bajo_nivel_fluido_a","/9_bajo_nivel_fluido_b","/10_arranques_excesivos",
    "/11_excesivos_ciclos_operacion","/12_cargas_en_superficie","/13_presencia_de_solidos"]  
    dir_raiz=opt.getcwd()
    num=n_examples_d
    data=D.zeros(muestreo+1)
    data_c=D.zeros(muestreo+1)
    r=0    
    
    while r==0:
        try:
            print("\tcuantas cartas de cada tipo de falla ha de tener el set de datos?")
            num=int(input("\t"))
            print("\tel set de datos tendra ", 13*num,"ejemplos, esta de acuerdo? s/n")
            aux=input("\t")
            if aux=="s" or aux=="S":
                r=1
            elif aux=="n" or aux=="N":
                r=0
            else:
                print("\tla respuesta debe ser s ó n ")
            print("\n")
        except:
            print("\tIngreso datos invalidos,intente de nuevo\n\n")
    
    for i in tipos_c :
        nc=nc+1
        print("\n")
        
        for j in range(num):
            carta_p=dir_raiz+i+"/"+str(nc)+"_carta_"+str(j+1)+".txt"
            data_aux1=D.loadtxt(carta_p)
            data_aux=D.hstack((10*nc,data_aux1))
            data_c=D.vstack((data_c,data_aux))
            print("\tSe ha cargado: ",carta_p)
    
    data_c=data_c[1:,:]
    
    for i in range(100):
        random.shuffle(data_c) 
   
    data=data_c[:,1:]
    resultado_r=data_c[:,0]
    data_random=D.copy(data)
    
    print("\n\tLa matriz del set de datos fue creada y tiene ",data_random.shape[0],
          "ejemplos  (",data_random.shape[0]," filas",
            " y " ,data_random.shape[1], "columnas) ")
        
    return data_random,resultado_r
"""1)----------------FIN GENERAR EL SET DE DATOS----------------------------"""  
 



"""-------------------------------------------------------------------------"""
"""2)------------------- GENERAR EL SET DE ENTRENAMIENTO-----------------------
""" 
def generate_training_set(data_random,resultado_r):    
    sel=0
    while sel==0:
        try:
            print("\tCuantos ejemplos para el set de entrenamiento? (en porcentaje)")
            r_set=int(input(""));  n_set=int((r_set/100)*data_random.shape[0])
            if r_set<1 or r_set>100:
                print("\n\tEl porcentaje debe estar entre 1% y 99%\n\n")
            else:
                sel=1
        except:
            print("\tDatos no validos, intente de nuevo\n\n")
            
    print("\tEl set de entrenamiento tendrá ",n_set,"ejemplos de entrenamiento")
    print("\tQuedan disponibles para validar",data_random.shape[0]-n_set," ejemplos" )

    training_set=data_random[0:(n_set-1),:]
    training_results=resultado_r[0:(n_set-1)]
    vi=(n_set);vf=(data_random.shape[0]-1)
    valid_set=data_random[vi:vf,:]
    valid_results=resultado_r[vi:vf]
   
    return training_set,training_results,valid_set,valid_results    
"""2)----------------FIN GENERAR EL SET DE ENTRENAMIENTO--------------------"""




"""-------------------------------------------------------------------------"""
"""3)-----------ELEGIR Y ENTRENAR LA MAQUINA APRENDIZAJE-----------------------
"""    
def select_and_training_Machine_learning(training_set,training_results,valid_set,valid_results,C,gamma):
    #print("\n\tPASO 3: Definir La Maquina de Aprendizaje\n")
    
   
    try:  
        sel=0   
        while sel==0:
            print("\tQue tipo de maquina de aprendizaje quiere entrenar?")
            print("\t\t1)Maquina Soporte Vectorial")
            print("\t\t2)Clasificador por arbol de decision")
            print("\t\t3) Naive Bayes Gaussiano")
           
            opt_ma=int(input("\t"))
            
            if opt_ma==1:
                sel=1
                print("\tEntrenando la MSV, por favor espere ...\n")
                clf=svm.SVC(C=C,gamma=gamma,  probability=True, shrinking=False,kernel='rbf')
                a=clf.fit(training_set,training_results)
               # print(a)    
               
            elif opt_ma==2:
                sel=1
                print("\tEntrenando el clasificador por arbol de decision, por favor espere ...\n")
                clf=tree.DecisionTreeClassifier()
                a=clf.fit(training_set,training_results)
                print(clf)
                
            elif opt_ma==3:
                sel=1
                print("\tEntrenando por Naive Bayes Gaussiano, por favor espere ...\n ")
                clf=GaussianNB()
                clf.fit(training_set,training_results)
                print(clf)

            #elif opt_ma==4:
            #    sel=1
            #    print("\tEntrenando por Regresion Logistica, por favor espere ...\n")
            #    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15,), random_state=1)                
                #clf = linear_model.LogisticRegression(C=1e10,solver='newton-cg')
            #    a=clf.fit(training_set,training_results)
                #print(clf)
                #pkl_file = open('clf_SVM.pkl', 'rb')
                #clf = pick.load(pkl_file)
             
            else:
                print("\topciones no validas, intente de nuevo \n\n")
    except:
        print("\topciones no validas, intente de nuevo \n\n")
    return clf,opt_ma
"""3)--------FIN ELEGIR Y ENTRENAR LA MAQUINA APRENDIZAJE--------------------""" 




"""-------------------------------------------------------------------------"""
"""4)------------------------OPCIONES DE VALIDACION----------------------------
"""       
def validate(clf,valid_results,valid_set,data_random,resultado_r,opt_ma,C,gamma):  
    
    sel=0    
    while sel==0:
        try:
            print("\tQue tipo de validacion?")
            print("\t\t1) Simple")
            print("\t\t2) Cruzada")
            print("\t\t3) Uno afuera")
            print("\t\t4) Bootstrap")
            r_tval=int(input("\t"))
            shw.clear_shell()
            
            #------------------VALIDACION SIMPLE-------------------------------
            if r_tval==1:
                sel=1
                print("\tValidacion simple\n")
                
                #suma=0
                st=0    
                m_confusion=D.zeros((13,13),int)
                for i in range(len(valid_results)):
                     #-----------PARA MATRIZ CONFUSION--------------------------
                    f=int(valid_results[i]/10)-1
                    c=int(clf.predict(valid_set[i])/10)-1
                    m_confusion[f][c]=m_confusion[f][c]+1
                    #-------------------------------------

                    #if valid_results[i]!=clf.predict(valid_set[i]):
                      #  print("\tvalor real: ",valid_results[i]/10,"     valor estimado: ", 
                       #       clf.predict(valid_set[i])/10," mal claificados")
                    if valid_results[i]==clf.predict(valid_set[i]):
                        st=st+1                    
                confusion_matrix(m_confusion)
                print("acierto de un ", 100*(st/len(valid_results)), "%") 
                return clf,(len(resultado_r)-len(valid_results)),100*(st/len(valid_results))                             
            #---------------FIN VALIDACION SIMPLE-------------------------------
            
            
            #------------------VALIDACION CRUZADA------------------------------
            elif r_tval==2:
                sel=1
                #print("\tValidacion cruzada\n")
                sel=0
                while sel==0:
                    try:
                        print("\tValidacion cruzada\n\n")
                        print("\tPara la validacion cruzada es necesario re-entrenar la\n",
                              "\tmaquina de aprendizaje varias veces; dependiendo de\n", 
                              "\tla cantidad de partes en que desee dividir el set de\n",
                              "\tdatos y la cantidad de ejemplos que tenga puede tardar\n",
                              "\tvarios minutos, esta de acuerdo? s/n\n\n")
                        resp=input("\t")
                        if resp=="n":
                            print("\tvolver al menu principal")
                            shw.menu_main()
                            sel=1
                        elif resp=="s":
                            print("\tEn cuantas partes desea dividir el set de datos?\n",
                                  "\t(valores tipicos entre 5 y 10)")
                            num_div=int(input("\t"))
                            sel=1
                        else:
                            print("\tValores no validos, intente de nuevo\n\n")                            
                    except:
                        print("\tValores no validos, intente de nuevo\n\n")
                        sel=0
                   
                    [clf,prob_valid]=cross_validate(num_div,data_random,resultado_r,opt_ma,r_tval,C,gamma)#,long_valid)#long_training)
                    return clf,int((len(resultado_r)/num_div)*(num_div-1)),prob_valid
            #--------------FIN VALIDACION CRUZADA------------------------------
           
           
            #--------------VALIDACION UNO AFUERA-------------------------------
            elif r_tval==3:
                sel=1
                sel=0
                while sel==0:
                    try:
                        print("\tValidacion Uno Afuera\n\n")
                        print("\tPara la validacion Uno Afuera es necesario re-entrenar la\n",
                              "\tmaquina de aprendizaje",len(resultado_r)," veces; esta validacion\n",
                              "\tpuede tardar considerablemente, esta de acuerdo? s/n\n\n")
                        resp=input("\t")
                        if resp=="n":
                            print("\tvolver al menu principal")
                            shw.menu_main()
                            sel=1
                        elif resp=="s":
                            num_div=len(resultado_r)
                            sel=1
                        else:
                            print("\tValores no validos, intente de nuevo\n\n")                            
                    except:
                        print("\tValores no validos, intente de nuevo\n\n")
                        sel=0
                    #long_valid=int(len(resultado_r)/num_div)
                    #long_training=examples_valid*(num_div-1)
                    [clf,prob_valid]=cross_validate(num_div,data_random,resultado_r,opt_ma,r_tval,C, gamma)#,long_valid)#long_training)
                    return clf,(len(resultado_r)-1),prob_valid
                
            #----------FIN VALIDACION UNO AFUERA-------------------------------
                
                
            #---------------------BOOTSTRAP------------------------------------
            elif r_tval==4:
                sel=1
                sel=0
                while sel==0:
                    try:
                        print("\tBootstrap\n\n")
                        print("\tPara la validacion Bootstrap es necesario re-entrenar la\n",
                              "\tmaquina de aprendizaje varias veces; esta validacion\n",
                              "\tpuede tardar considerablemente, esta de acuerdo? s/n\n\n")
                        resp=input("\t")
                        if resp=="n":
                            print("\tvolver al menu principal")
                            shw.menu_main()
                            sel=1
                        elif resp=="s":
                            print("\tcuantas veces quiere aplicarla?\n",
                                  "\t(se recomienda entre 1 y 10 maximo)")
                            nv=int(input("\t"))
                            sel=1
                        else:
                            print("\tValores no validos, intente de nuevo\n\n")                            
                    except:
                        print("\tValores no validos, intente de nuevo\n\n")
                        sel=0
                    #long_valid=int(len(resultado_r)/num_div)
                    #long_training=examples_valid*(num_div-1)
                    [clf,prob_valid]=botstrap(nv,data_random,resultado_r,opt_ma,C,gamma)#,long_valid)#long_training)
                    return clf,len(resultado_r),prob_valid
        except:
            print("\tOpcion no valida, intente de nuevo\n\n")
            
"""4)-------------------FIN OPCIONES DE VALIDACION--------------------------"""       
    
    


"""-------------------------------------------------------------------------"""    
"""5)------------------------VALIDACION BOTSTRAP----------------------------
"""       
    
def botstrap(nv,data_random,resultado_r,opt_ma,C,gamma):

    acum_v=0
    acum_d=0
    for k in range(nv):    
        print("Botstrap numero",k+1, "de",nv)
            #----------parte que crea el conjunto de entrenamiento
        ejemplos_training=D.zeros(len(resultado_r))
        b_data=D.zeros((data_random.shape[0],data_random.shape[1]),float)
        b_resultado=D.zeros(len(resultado_r))
        b_data_valid=D.zeros((data_random.shape[0],data_random.shape[1]),float)
        b_resultado_valid=D.zeros(len(resultado_r))
              
        for i in range(len(resultado_r)):
            rand=random.randint(0,len(resultado_r))
            ejemplos_training[i]=rand
            b_data[i]=data_random[rand]
            b_resultado[i]=resultado_r[rand]
            #----------fin parte que crea el conjunto de entrenamiento  
                
            #----------parte que crea el conjunto de prueba
        c_v=0
        for i in range (len(resultado_r)):
            flag=0
            for j in ejemplos_training:
                if i==j:
                    #no lo tomo para la validacion
                    flag=1
            if flag==0:
                b_data_valid[c_v]=data_random[i]
                b_resultado_valid[c_v]=resultado_r[i]
                c_v=c_v+1
        b_data_valid= b_data_valid[0:c_v,:]
        b_resultado_valid=b_resultado_valid[0:c_v]
            #----------fin parte que crea el conjunto de prueba
        """
        """
        
        if opt_ma==1:
            clf=svm.SVC(C=C,gamma=gamma,  probability=True, shrinking=False,kernel='rbf')
            clf.fit(b_data,b_resultado)
        elif opt_ma==2:
            clf=tree.DecisionTreeClassifier()
            clf.fit(b_data,b_resultado)
        elif opt_ma==3:
            clf=GaussianNB()
            clf.fit(b_data,b_resultado)
        """
        elif opt_ma==4:
            clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15,), random_state=1)                
                #clf = linear_model.LogisticRegression(C=1e10,solver='newton-cg')
            a=clf.fit(training_set,training_results)
        """     
            
        print("a) Acierto pesimita")
        acum_a=valid_s(clf,b_data_valid,b_resultado_valid)
        print("\n\nb) Acierto optimista")
        acum_b=valid_s(clf,data_random,resultado_r)
       
        acum_v=acum_v+acum_a
        
        acum_d=acum_d+acum_b
        print("\n\nacierto botstrap 0.636: ",0.636*acum_a+0.364*acum_b )
        print("validacion exitosa")
        #print("\tEntrenando para validacion ", j+1,"el set de entrenamiento es \n",data_tr[:,0:4],"\t",res_tr)
        #print("\ny el de validacion \n",data_valid[:,0:4],res_valid)
        print("\n\n")     
    print("VALIDACION BOTSTRAP ARROJO UN ACIERTO PESIMISTA DE", (acum_v/nv),"%\n")
    print("VALIDACION BOTSTRAP ARROJO UN OPTIMISTA DE", (acum_d/nv),"%\n")
    print("VALIDACION BOTSTRAP 0.636 ARROJO UN ACIERTO DE", 0.636*(acum_v/nv)+0.364*(acum_d/nv),"%\n")
    
    return clf,0.636*(acum_v/nv)+0.364*(acum_d/nv)
  
"""5)------------------------FIN VALIDACION BOTSTRAP-----------------------""" 




"""-------------------------------------------------------------------------"""      
"""6)------------------------VALIDACION CRUZADA-------------------------------
"""    
def cross_validate(num_div,data_random,resultado_r,opt_ma,r_tval,C,gamma):
   
    long_valid=int(len(resultado_r)/num_div)
    data_tr=D.zeros(data_random.shape[1])
    vi=0 
    acum_v=0
    shw.clear_shell()
    print("\n\tInicio proceso de validacion\n\n")    
    for j in range(num_div):
        vi=0 
        data_tr=D.zeros(data_random.shape[1])
        res_tr=D.zeros(len(resultado_r))
        for i in range(num_div):
             vf=vi+(long_valid-1)+1
             sub_data=data_random[vi:vf,:]
             sub_res=resultado_r[vi:vf]
             if i!=j:
                 data_tr=D.vstack((data_tr,sub_data))
                 res_tr=D.hstack((res_tr,sub_res))
             elif i==j:
                 data_valid=data_random[vi:vf,:]
                 res_valid=resultado_r[vi:vf]
             vi=vf
        
        if len(resultado_r)>vf:
            data_tr=D.vstack((data_tr,data_random[(vf):len(resultado_r),:]))
            res_tr=D.hstack((res_tr,resultado_r[(vf):len(resultado_r)]))            

        data_tr=data_tr[1:,:]
        res_tr=res_tr[len(resultado_r):]
        print("Entrenando para validacion ", j+1," de",num_div," por favor espere...\n")
        
        if opt_ma==1:
            clf=svm.SVC(C=C,gamma=gamma,  probability=True, shrinking=False,kernel='rbf')
            clf.fit(data_tr,res_tr)
        elif opt_ma==2:
            clf=tree.DecisionTreeClassifier()
            clf.fit(data_tr,res_tr)
        elif opt_ma==3:
            clf=GaussianNB()
            clf.fit(data_tr,res_tr)
        """    
        elif opt_ma==4:
            clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(15,), random_state=1)                
                #clf = linear_model.LogisticRegression(C=1e10,solver='newton-cg')
            #a=clf.fit(training_set,training_results)
            #clf = linear_model.LogisticRegression(C=1e5,solver='newton-cg')
            clf.fit(data_tr,res_tr)
        """
        acum_a=valid_s(clf,data_valid,res_valid)
        acum_v=acum_v+acum_a
        print("validacion exitosa")
        #print("\tEntrenando para validacion ", j+1,"el set de entrenamiento es \n",data_tr[:,0:4],"\t",res_tr)
        #print("\ny el de validacion \n",data_valid[:,0:4],res_valid)
        print("\n\n")     
    if r_tval==2:
        print("LA VALIDACION CRUZADA ARROJO UN ACIERTO DE  ",(acum_v/num_div),"% !!")
    elif r_tval==3:
        print("LA VALIDACION UNO AFUERA ARROJO UN ACIERTO DE  ",(acum_v/num_div),"% !!")    
    return clf,(acum_v/num_div)
"""6)---------------------FIN VALIDACION CRUZADA----------------------------"""      



    
"""-------------------------------------------------------------------------"""    
"""7)------------------- AUXILIAR DE VALIDACION -------------------------------
"""     
def valid_s (clf,data_valid,res_valid):
    cont=0
    cont1=0
    m_confusion=D.zeros((13,13),int)
    for i in range(len(res_valid)):
        #-----------PARA MATRIZ CONFUSION--------------------------
        f=int(res_valid[i]/10)-1
        c=int(clf.predict(data_valid[i])/10)-1
        m_confusion[f][c]=m_confusion[f][c]+1
        #-------------------------------------
        if res_valid[i]==clf.predict(data_valid[i]):
            cont=cont+1
        else:
            cont1=cont1+1
           # print("\tvalor real: ",res_valid[i]/10,"     valor estimado: ",
            #      clf.predict(data_valid[i])/10,"mal estimados")
        #print("\tvalor real: ",res_valid[i]/10,"     valor estimado: ", clf.predict(data_valid[i])/10)
    p_acierto=100*(cont/len(res_valid))
    confusion_matrix(m_confusion)
    print("\nAcierto: de un ",p_acierto, "%")
    
    return p_acierto
"""7)-----------------FIN AUXILIAR DE VALIDACION ---------------------------"""




"""-------------------------------------------------------------------------"""
"""8)-------------------MATRIZ DE CONFUSION------------------------------------
"""   
def confusion_matrix(m_confusion):
    
   # f=[["/"],["F1"],["F2"],["F3"],["F4"],["F5"],["F6"],["F7"],
    #   ["F8"],["F9"],["F10"],["F11"],["F12"],["F13"]]
    """    
    c=D.arange(13)+1
    f=D.arange(14)    
    f=f.reshape(14,1)
    a=m_confusion.reshape(13,13)
    data_aux=D.vstack((c,a))
    data_aux=D.hstack((f,data_aux))
    print(data_aux,"\n")
    """
    a=m_confusion.reshape(13,13)
    print("Matriz de Confusion:")
    print(a)
"""8)-------------------FIN MATRIZ DE CONFUSION-----------------------------""" 



  
"""-------------------------------------------------------------------------"""
"""9)------------------- FUNCIONES DE SIMILITUD GAUSSIANAS---------------------
"""
def generate_similitude_functions(X):#esta funcion se probo y esta bien
    #X=D.array([[1,2,3],[4,5,6],[7,8,9]])
    n_examples=X.shape[0]
    sigma=20
    denom=2*(sigma**2)
    print("se calcularan", n_examples, "funciones de similitud, presione cualquier tecla para continuar")
    input("")    
    #print(n_examples)
    #f=D.zeros(n_examples)
    funciones=D.zeros((n_examples,n_examples),float)
    #print("longitud de f ",len(f))
    #print(f)
    for j in range(n_examples):
        print("calculando funciones de similitud para ejemplo ",j+1, "de", n_examples)
        for i in range(n_examples):
            dif=(X[j]-X[i])**2
            #print (dif)
            
            #sum_total=dif.sum()
            #print(sum_total)
            #print("\n")
            #print(dif)
            sum_fila=dif.sum(axis=0)
            funciones[j][i]=mat.exp(-sum_fila/denom)
        print(funciones[j])
        print("\n")
    print(funciones.shape)
"""9)---------------FIN FUNCIONES DE SIMILITUD GAUSSIANAS-------------------"""
   



"""-------------------------------------------------------------------------"""
"""10)------------------- GRAFICAS ROC-----------------------------------------
FUNCION EDITADA DE EJEMPLO DEL MANUAL SCIKIT.LEARN
"""        
def graphs_ROC():#data_random,resultado_r,valid_set,valid_results):
    a=opt.getcwd() #me da directorio actual
    data=a+"/Archivos_training/Data.txt"
    resultado=a+"/Archivos_training/resultados.txt"
    clasificador=a+"/Archivos_training/clf_SVM.pkl"
    
    data_random=D.loadtxt(data)
    print("\tData cargada")
    resultado_r=D.loadtxt(resultado)
    print("\tResultados cargados")
    pkl_file = open(clasificador, 'rb')
    clf = pick.load(pkl_file)
    print("\tClasificador cargado")
    print("\tEn proceso ...") 
    resultado_r = label_binarize(resultado_r, classes=[10, 20,30,40,50,60,70,80,90,100,110,120,130])
    
    n_classes = resultado_r.shape[1]
   
    
    X_train, X_test, y_train, y_test = train_test_split(data_random,resultado_r, test_size=0.4,random_state=0)
    classifier = OneVsRestClassifier(clf)#,random_state=random_state))
    
    y_score = classifier.fit(X_train, y_train).decision_function(X_test)
   
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])    
    lw = 2    
   
    # Compute macro-average ROC curve and ROC area
    # First aggregate all false positive rates
    all_fpr = D.unique(D.concatenate([fpr[i] for i in range(n_classes)]))
    # Then interpolate all ROC curves at this points
    mean_tpr = D.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])
    # Finally average it and compute AUC
    mean_tpr /= n_classes
    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    
    #--------------------------------------------------------------------------
    # Plot all ROC curves
    plt.figure()
    plt.rc('font', size = 8)
    for k in range(3):
        
        plt.subplot(2,2,k+1)
       
        colors = cycle(['r', 'darkorange', 'b' ,'y'])
        for i, color in zip(range(3), colors):
            plt.plot(fpr[i+k*3], tpr[i+k*3], color=color, lw=lw,
            label='Curva ROC clase {0} (area = {1:0.2f})'
            ''.format(i+k*3+1, roc_auc[i+k*3]))
        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        plt.xlim([-0.05, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Rata de Falsos Positivos')
        plt.ylabel('Rata de Aciertos Positivos')
        titulo="Graficas ROC de la clase "+ str(k*3+1)+" a la clase "+str(k*3+3)
        plt.title(titulo)
        plt.legend(loc="lower right")
    #-------------------------------------------------------------------------
    
    plt.subplot(2,2,4)
      
    colors = cycle(['r', 'darkorange', 'b' ,'y'])
    for i, color in zip(range(4), colors):
        
        plt.plot(fpr[i+9], tpr[i+9], color=color, lw=lw,
        label='Curva ROC clase {0} (area = {1:0.2f})'
        ''.format(i+10, roc_auc[i+9]))
    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Rata de Falsos Positivos')
    plt.ylabel('Rata de Aciertos Positivos')
    titulo="Graficas ROC de la clase "+ str(10)+" a la clase "+str(13)
    plt.title(titulo)
    plt.legend(loc="lower right")
        #----------------------------------------------------------------------
    plt.figure()
    plt.rc('font', size = 8)
    plt.plot(fpr["micro"], tpr["micro"],
    label='micro-average ROC curve (area = {0:0.2f})'
    ''.format(roc_auc["micro"]),
    color='deeppink', linestyle='-', linewidth=4)
    plt.plot(fpr["macro"], tpr["macro"],
    label='macro-average ROC curve (area = {0:0.2f})'
    ''.format(roc_auc["macro"]),
    color='navy', linestyle='-', linewidth=4)
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    titulo="Graficas ROC Promedio, minima y maxima"
    plt.title(titulo)
    plt.legend(loc="lower right")
    plt.show()    
"""10)---------------FIN GRAFICAS ROC---------------------------------------"""




"""-------------------------------------------------------------------------"""
"""11)------------------ CURVA DE APRENDIZAJE----------------------------------
FUNCION EDITADA DE EJEMPLO DEL MANUAL SCIKIT.LEARN
"""
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
n_jobs=1, train_sizes=D.linspace(.1, 1.0, 5)):   
    
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Ejemplos de entrenamiento")
    plt.ylabel("Puntuacion")
    train_sizes, train_scores, test_scores = learning_curve(
    estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = D.mean(train_scores, axis=1)
    train_scores_std = D.std(train_scores, axis=1)
    test_scores_mean = D.mean(test_scores, axis=1)
    test_scores_std = D.std(test_scores, axis=1)
    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
    train_scores_mean + train_scores_std, alpha=0.1,
    color="b")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
    test_scores_mean + test_scores_std, alpha=0.1, color="y")
    
    plt.plot(train_sizes, train_scores_mean, 'o-', color="b",
    label="Puntuacion de entrenamiento",linewidth=3)
    plt.plot(train_sizes, test_scores_mean, 'o-', color="y",    
    label="Puntuacion con validacion cruzada",linewidth=3)
    plt.legend(loc="best")
    plt.show()  
    return plt
    
    plt.show()    
"""11)--------------FIN CURVA DE APRENDIZAJE-------------------------------"""




"""-------------------------------------------------------------------------"""
"""12)-----------------ELEGIR PARAMETROS C Y GAMMA-----------------------------
FUNCION EDITADA DE EJEMPLO DEL MANUAL SCIKIT.LEARN
"""

def best_param(X_train,y_train,param_grid ):
    
    
    print("En proceso, espere ...")
    clf = GridSearchCV(svm.SVC(kernel='rbf', class_weight='balanced'), param_grid)
    clf = clf.fit(X_train, y_train)
    print("Los valores optimos encontrados para un set de datos de",len(y_train)," son:\n")
    print("C=",clf.best_estimator_.get_params([True])['C'])
    print("gamma=",clf.best_estimator_.get_params([True])['gamma'])
    g=clf.cv_results_['param_gamma']
    c=clf.cv_results_['param_C']
    x=D.array(g).reshape(len(param_grid['C']),len(param_grid['gamma']))
    y=D.array(c).reshape(len(param_grid['C']),len(param_grid['gamma']))
    Z = clf.cv_results_['mean_test_score']
    z=D.array(Z).reshape(len(param_grid['C']),len(param_grid['gamma']))
    plt.figure("Grafica C en funcion de gamma")
    plt.pcolor(x, y, z); plt.colorbar(); plt.show()
    C=0;gamma=1
    return C,gamma
"""12)-------------FIN ELEGIR PARAMETROS C Y GAMMA--------------------------"""
           
