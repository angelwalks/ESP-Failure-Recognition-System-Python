# -*- coding: utf-8 -*-
"""
Created on Sat May 13 09:32:06 2017

@author: angel
"""

import numpy as np
import pylab as py
#import matplotlib.pyplot as py
import Load_And_Form_Data as imp
from numpy import random




"""-------------------------------------------------------------------------"""
"""(a)-------CREAR EL FORMATO DE UNA CARTA AMPERIMETRICA--------------------"""
def plantilla(escala=1,op=0,titulo_op=0,size_num=7,size_nombre=10,num_chart="default"):
    
#(2.1)codigo que define condiciones de ploteo
    muestras_minuto=1
    muestreo=24*muestras_minuto*60
    angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
    #py.figure(figsize=(7*escala, 7*escala))
    #py.grid(True)
    py.xlim(xmin=-(14*escala), xmax=(14*escala))
    py.ylim(ymin=-(14*escala), ymax=(14*escala))
    py.xticks(np.arange(1),(''))
    py.yticks(np.arange(1),(''))
    titulo=["Carta:\noperacion\nNormal","Carta:\npicos de corriente","Carta:\n apagado por gas\nen bomba",
            "Carta:\ngas libre\nen bomba","Carta:\ncorriente en\nbaja carga",
            "Carta:\ncorriente en\nsobrecarga","Carta:\ndescarga de fluido",
            "Carta:\nbajo nivel de\nfluido con gas","Carta:\ncon bajo nivel de\nfluido sin gas",
            "Carta:\nnumero excesivo\nde arranques","Carta:\nexcesivos ciclos\nde operacion",
            "Carta:\nemulsiones o\ncargas","Carta:\nsolidos en\n la bomba"]
    if op==1:
        py.text(0, 0, titulo[titulo_op]+"\n"+num_chart, horizontalalignment='center',
            verticalalignment='center',fontsize=size_nombre,color='k')

    
#fin codigo que define condiciones de ploteo
    

    for i in range(4,12,1):
         radio=i
         x=radio*np.cos(angle)
         y=radio*np.sin(angle)
         py.plot(x,y,color="c")
         #print(x.shape,y.shape)
               

    angle_step=np.pi/12
    rmax=11
    rmin=4
    #l=D.arange(0,rmax,0.1)
    hours=["06 pm","05 pm","04 pm","03 pm","02 pm","01 pm",
           "12 pm","11 am","10 am","09 am","08 am","07 am",
           "06 am","05 am","04 am","03 am","02 am","01 am",
           "12 am","11 am","10 pm","09 pm","08 pm","07 pm",]
    for j in range(24):
        yf=rmax*np.sin(angle_step*j-np.pi/2)
        xf=rmax*np.cos(angle_step*j-np.pi/2)
        yi=rmin*np.sin(angle_step*j-np.pi/2)
        xi=rmin*np.cos(angle_step*j-np.pi/2)
        y=np.linspace(yi,yf,100)
        x=np.linspace(xi,xf,100)
        
        hy=(rmax+1.5)*np.sin(angle_step*j-np.pi/2)
        hx=(rmax+1.5)*np.cos(angle_step*j-np.pi/2)
        py.plot(y,x,color="c")
        if op==1:
            py.text(hx,hy,hours[j],horizontalalignment='center',
            verticalalignment='center',fontsize=size_num,color='k')
"""----------------------fin de (a)----------------------------------------"""




"""-------------------------------------------------------------------------"""
"""(b)-----------------CARGA EL FORMATO DE LA CARTA AMPERIMETRICA---(NO USADA--
Load_format() carga los ficheros generados por la funcion (1) y grafica de manera
 instantanea el formato de la carta amperimetrica debido a que no necesita
realizar calculos
"""        
def Load_format():
    
    XC=imp.Load_Data("XC.txt",0,"todas",False)
    YC=imp.Load_Data("YC.txt",0,"todas",False)
    xe=imp.Load_Data("xe.txt",0,"todas",False)
    ye=imp.Load_Data("ye.txt",0,"todas",False)
    escala=1
    py.figure(figsize=(8*escala, 8*escala))
    py.grid(True)
    py.xlim(xmin=-(9*escala), xmax=(9*escala))
    py.ylim(ymin=-(9*escala), ymax=(9*escala))
    
    for i in range(0,8,1):
        py.plot(XC[i],YC[i],color='k')
        py.plot(XC[i],-YC[i],color='k')
    
    py.plot((xe[0:398]),(ye[0:398]),color="k");
    for i in range(24):
        a=(400+i*400)
        b=(800+i*400)
        py.plot((xe[a:b]),(ye[a:b]),color="k");
    print(np.size(XC))
"""----------------------fin de (b)-----------------------------------------"""

    
    
    
"""-------------------------------------------------------------------------"""    
"""(1)--------------GENERAR CARTAS AMPERIMETRICAS EN OPERACION NORMAL----------
sim_current_bomb_normal(In,k): recibe In que es el valor de la corriente nominal
y k que es el error en torno al cual oscilará esta corriente de manera aleatoria
"""
def sim_current_pump_normal(In=4,k=0.3,plotear=1,default="a"):
    try:
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)
        p_start=random.randint(1,240*muestras_minuto)       
        radio[p_start]=2*In
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        print("carta comportamiento normal de corriente generada")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='y',linewidth=2)
        radio=np.array(radio)
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    return radio
"""----------------------fin de (1)-----------------------------------------"""




"""-------------------------------------------------------------------------"""
"""(2)--------GENERAR CARTAS AMPERIMETRICAS CON PICOS DE CORRIENTE-------------
sim_current_bomb_peaks(In,k): recibe In que es el valor de la corriente nominal
y k que es el error en torno al cual oscilará esta corriente de manera aleatoria
aparte me generará valores aleatorios de:
num_peaks-> numero de picos que tendra la carta
start_peak-> posicion del tren de datos de corriente donde se generará el pico
value_peak->amplitud del error que tendrá el pico
este metodo genera un tren de datos de operacion normal, luego con los valores
aleatorios generados borrara el valor en las posiciones correspondientes y escribirá
en dichas posiciones el valor del pico, asi genera un comportamiento de sobrecargas
"""
def sim_current_pump_peaks(In=4,k=0.3,plotear=1,default="a"):
    try:       
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)
        time_peak=4
        num_peaks=random.randint(5,10) #valor aleatorio entre 2 y 9
        for i in range(num_peaks):
            start_peak=random.randint(0,muestreo) 
            for j in range(time_peak):
                value_peak=random.uniform(1.5,2)
                aux=start_peak+j
                if aux==1440:
                    start_peak=0
                    aux=0
                radio[aux]=In+value_peak
        p_start=random.randint(1,240*muestras_minuto)       
        radio[p_start]=2*In
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        print("carta falla por picos de corriente generada")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='b',linewidth=2) 
        radio=np.array(radio)
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    return radio
"""---------------,-------fin de (2)-----------------------------------------"""




"""-------------------------------------------------------------------------"""    
"""(3)--------GENERAR CARTAS AMPERIMETRICAS GAS LIBRE EN LA BOMBA-------------- 
sim_current_pump_gas_free_in_pump(In,k): recibe el valor de la corriente nominal(In)
y el valor en que puede oscilar la misma en condiciones normales (k) 
p_start-> indica el inicio o arranque aleatorio de la bomba segun condiciones o limites
de tiempo, a partir de alli trabaja en operacion normal durante  un lapso aleatorio, 
luego los valores de corriente empiezn a oscilar mas alla del valor de k
"""
def sim_current_pump_gas_free_in_pump(In=4,k=0.3,plotear=1,default="a"):
    try:    
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]
        #num_blocks=random.randint(1,4) #valor aleatorio 
        num_blocks=2
        mult=1
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)                 
            p=int(r)                                  
            intervalo.append(random.randint(0,p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        #print("N intervalos", num_blocks)                                           
        #print(intervalo)
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
        #print(len(ranks))  
        #print(ranks)          
        g=0;
        a1=In;b1=k;a2=In;b2=1;a3=4;b3=0;aux_arranque=1
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
            if g==0:
                Ina=a1
                ka=b1            
                g=1
                aux_arranque=1;
            elif g==1:
                Ina=a2
                ka=b2
                g=2
            elif g==2:
                Ina=a3
                ka=b3
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
                
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla gas libre en la bomba")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='r',linewidth=2) 
        radio=np.array(radio)
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    
    return radio
"""----------------------fin de (3)-----------------------------------------"""    
   



"""-------------------------------------------------------------------------"""    
"""(4)--------GENERAR CARTAS AMPERIMETRICAS CON BLOQUEO POR GAS ---------------
sim_current_block_gas(In,k): recibe el valor de la corriente nominal(In)
y el valor en que puede oscilar la misma en condiciones normales (k) 
p_start-> indica el inicio o arranque aleatorio de la bomba segun condiciones o limites
de tiempo, a partir de alli trabaja en operacion normal durante  un lapso aleatorio, 
luego los valores de corriente empiezan a oscilar mas alla del valor de k otro
lapso aleatorio para finalmente caer a cero o condicion de apagado; se repetira 
este comportamiento de arranque->funcionamiento normal->oscilacion por gas ->apagado
un numero de veces definido aleatoriamente. 
"""
def sim_current_block_gas(In=4,k=0.3,plotear=1,default="a"):
    try:    
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]
        num_blocks=random.randint(1,4) #valor aleatorio 
        mult=3
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)                 
            p=int(r)                                  
            intervalo.append(random.randint(0.8*p,p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        #print("N intervalos", num_blocks)                                           
        #print(intervalo)
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
            
        g=0;
        a1=In;b1=k;a2=In;b2=1;a3=4;b3=0;aux_arranque=1
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
                
            if i==(len(ranks)-1):
                g=2
                    
            if g==0:
                Ina=a1
                ka=b1            
                g=1
                aux_arranque=1;
            elif g==1:
                Ina=a2
                ka=b2
                g=2
            elif g==2:
                Ina=a3
                ka=b3
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
               
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por apagado gas en la bomba")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='k',linewidth=2) 
        radio=np.array(radio)
        
    except:
       radio=np.loadtxt(default)
       radio=np.array(radio)
       
    
    return radio
"""----------------------fin de (4)-----------------------------------------"""    
   
   
   
   
"""-------------------------------------------------------------------------"""   
"""(5)--------GENERAR CARTAS AMPERIMETRICAS CON BAJA CARGA---------------------
sim_current_pump_low_load(In,k): recibe el valor de la corriente nominal(In)
y el valor en que puede oscilar la misma en condiciones normales (k) 
p_start-> indica el inicio o arranque aleatorio de la bomba segun condiciones o limites
de tiempo, a partir de alli trabaja en operacion normal durante  un lapso aleatorio, 
luego los valores de corriente nominal empiezan a disminuir otro lapso aleatorio para
finalmente caer a cero o condicion de apagado; 
"""
def sim_current_pump_low_load(In=6,k=0.3,plotear=1,default="a"):
    try:        
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]
        #num_blocks=random.randint(1,4) #valor aleatorio 
        num_blocks=4
        mult=1
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)        
            #r=rango         
            p=int(r)                                  
            intervalo.append(random.randint(0.5*p,p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
            
        g=0;
        a1=In;b1=k;a2=In;b2=k;a3=(In-1);b3=k;a4=4;b4=0;aux_arranque=1
        #try:
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
                #  print(len(ranks[i]))
            if i==(len(ranks)-1):
                    g=3
            if g==0:
                Ina=a1
                ka=b1            
                g=1
                aux_arranque=1;
                
                
            elif g==1:
                Ina=a2
                Ina=((a3-a2)/len(ranks[i]))*(np.array(list(ranks[i]))-inicio)+a2
                #print(len(Ina))
                ka=b2
                g=2
                
            elif g==2:
                Ina=a3
                ka=b3
                g=3
                
            elif g==3:
                Ina=a4
                ka=b4
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
               
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por baja carga")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='g',linewidth=2) 
        radio=np.array(radio)
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    return radio
  
"""----------------------fin de (5)-----------------------------------------"""




"""-------------------------------------------------------------------------"""
"""(6)--------GENERAR CARTAS AMPERIMETRICAS CON SOBRE CARGA--------------------
sim_current_pump_over_load(In,k): recibe el valor de la corriente nominal(In)
y el valor en que puede oscilar la misma en condiciones normales (k) 
p_start-> indica el inicio o arranque aleatorio de la bomba segun condiciones o limites
de tiempo, a partir de alli trabaja en operacion normal durante  un lapso aleatorio, 
luego los valores de corriente nominal empiezan a aumentar otro lapso aleatorio para
finalmente caer a cero o condicion de apagado;
"""
def sim_current_pump_over_load(In=6,k=0.3,plotear=1,default="a"):
    try:        
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]
        #num_blocks=random.randint(1,4) #valor aleatorio 
        num_blocks=4
        mult=1
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)        
            #r=rango         
            p=int(r)                                  
            intervalo.append(random.randint(0.5*p,p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
            
        g=0;
        a1=In;b1=k;a2=In;b2=k;a3=(In+1);b3=k;a4=4;b4=0;aux_arranque=1
        #try:
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
                #  print(len(ranks[i]))
            if i==(len(ranks)-1):
                    g=3
            if g==0:
                Ina=a1
                ka=b1            
                g=1
                aux_arranque=1;
                
                
            elif g==1:
                Ina=a2
                Ina=((a3-a2)/len(ranks[i]))*(np.array(list(ranks[i]))-inicio)+a2
                #print(len(Ina))
                ka=b2
                g=2
                
            elif g==2:
                Ina=a3
                ka=b3
                g=3
                
            elif g==3:
                Ina=a4
                ka=b4
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
               
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por sobrecarga")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='c',linewidth=2) 
        radio=np.array(radio)
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    return radio
"""----------------------fin de (6)-----------------------------------------""" 
 
 


"""-------------------------------------------------------------------------"""  
"""(7)--------GENERAR CARTAS AMPERIMETRICAS DESCARGA DE FLUIDO-----------------
sim_current_pump_download_fluid(In,k): recibe el valor de la corriente nominal(In)
y el valor en que puede oscilar la misma en condiciones normales (k) 
p_start-> indica el inicio o arranque aleatorio de la bomba segun condiciones o limites
de tiempo, a partir de alli empieza con un valor de corriente superior que disminuye
 hasta estabilizarse en el valor nominal;
"""
def sim_current_pump_download_fluid(In=4,k=0.3,plotear=1,default="a"):
    try:        
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]    
        #num_blocks=random.randint(1,4) #valor aleatorio 
        num_blocks=3
        mult=1
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)        
            #r=rango         
            p=int(r)                                  
            intervalo.append(random.randint(0.1*p,0.5*p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))  
        
        g=0;
        a1=(In+1);b1=k;a2=(In+1);b2=k;a3=(In);b3=k;a4=In;b4=k;aux_arranque=1
        #try:
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
            
            if g==0:
                Ina=a1
                ka=b1            
                g=1
                aux_arranque=1;
                
            elif g==1:
                Ina=a2
                Ina=((a3-a2)/len(ranks[i]))*(np.array(list(ranks[i]))-inicio)+a2
                #print(len(Ina))
                ka=b2
                g=2
                
            elif g==2:
                Ina=a3
                ka=b3
                g=3
                
            elif g==3:
                Ina=a4
                ka=b4
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
               
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por descarga de fluido")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='g',linewidth=2) 
        radio=np.array(radio)
        
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
        
    return radio
"""----------------------fin de (7)-----------------------------------------"""




"""-------------------------------------------------------------------------"""
"""(8)--------GENERAR CARTAS AMPERIMETRICAS CON BAJO NIVEL FLUIDO (CASO 1) ----
"""
def sim_current_low_level_fluid_1(In=6,k=0.3,plotear=1,default="a"):
    try:    
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]
        num_blocks=random.randint(1,4) #valor aleatorio 
        mult=3
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)                 
            p=int(r)                                  
            intervalo.append(random.randint(0.8*p,p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
        #    
        g=0;
        a1=In;b1=k;a2=(In-1);b2=1;a3=4;b3=0;aux_arranque=1
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
            
            if i==(len(ranks)-1):
                g=2
                
            if g==0:
                Ina=a1
                Ina=a2
                Ina=((a2-a1)/len(ranks[i]))*(np.array(list(ranks[i]))-inicio)+a1
                ka=b1            
                g=1
                aux_arranque=1;
            elif g==1:
                Ina=a2
                ka=b2
                g=2
            elif g==2:
                Ina=a3
                ka=b3
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
               
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por bajo nivel de fluido con gas en la bomba")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='k',linewidth=2) 
        radio=np.array(radio)   
    
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    
    return radio
"""----------------------fin de (8)-----------------------------------------"""




"""-------------------------------------------------------------------------"""    
"""(9)--------GENERAR CARTAS AMPERIMETRICAS CON BAJO NIVEL FLUIDO (CASO 2) ----
"""
def sim_current_low_level_fluid_2(In=4,k=0.3,plotear=1,default="a"):
    try:
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]
        num_blocks=random.randint(1,4) #valor aleatorio 
        #num_blocks=3
        mult=2
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)                 
            p=int(r)                                  
            intervalo.append(random.randint(0.8*p,p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
        
        g=0;
        a1=In;b1=k;a2=(In-1.4);a3=4;b3=0;aux_arranque=1
    
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
            
            if i==(len(ranks)-1):
                g=2 
                
            if g==0:
                Ina=a1
                Ina=a2
                Ina=((a2-a1)/len(ranks[i]))*(np.array(list(ranks[i]))-inicio)+a1
                ka=b1            
                g=1
                aux_arranque=1;
                
            elif g==1:
                Ina=a2
                ka=b1
                g=2
          
            elif g==2:
                Ina=a3
                ka=b3
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
               
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por bajo nivel de fluido sin gas en la bomba")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='y',linewidth=2) 
        radio=np.array(radio)   
    
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    
    return radio
"""----------------------fin de (9)-----------------------------------------"""




"""-------------------------------------------------------------------------"""                                                    
"""(10)---GENERAR CARTAS AMPERIMETRICAS CON EXCESIVOS INTENTOS DE ARRANQUE ----
"""
def sim_current_pump_excesive_starts(In=6,k=0,plotear=1,default="a"):
    try:       
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)
        time_start=2
        num_starts=random.randint(3,6) #valor aleatorio entre 2 y 9
        lim=random.randint(0,muestreo-240)
        for i in range(num_starts):
            start=random.randint(lim,lim+240) 
            for j in range(time_start):
                value_start=2*In
                aux=start+j
                if aux>1440:
                    start=0
                    aux=0
                radio[aux]=value_start
        p_start=random.randint(1,240*muestras_minuto)       
        radio[p_start]=value_start
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        print("carta falla por numero excesivo de arranques generada")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='r',linewidth=2)
        radio=np.array(radio)
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    return radio
"""----------------------fin de (10)----------------------------------------"""




"""-------------------------------------------------------------------------"""    
"""(11)-----GENERAR CARTAS AMPERIMETRICAS CON EXCESIVOS CICLOS DE OPERACION ---
"""
def sim_current_excesive_operate_cicles(In=4,k=0.3,plotear=1,default="a"):
    try:    
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]   
        num_blocks=random.randint(7,10) #valor aleatorio 
        #num_blocks=10
        mult=2
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)                 
            p=int(r)                                  
            intervalo.append(random.randint(0.8*p,p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
        
        g=0;
        a1=In;b1=k;a2=In*0.7;a3=4;b3=0;aux_arranque=1
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
                
            if i==(len(ranks)-1):
                g=2
                
            if g==0:
                Ina=a1
                Ina=a2
                Ina=((a2-a1)/len(ranks[i]))*(np.array(list(ranks[i]))-inicio)+a1
                ka=b1            
                g=2
                aux_arranque=1;
              
            elif g==2:
                Ina=a3
                ka=b3
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
               
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por excesivos ciclos de operacion generada")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='y',linewidth=2) 
        radio=np.array(radio)    
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    
    return radio
"""----------------------fin de (11)----------------------------------------"""




"""-------------------------------------------------------------------------"""
"""(12)---GENERAR CARTAS AMPERIMETRICAS EMULSIONES O CARGAS EN SUPERFICIE------
"""
def sim_current_pump_surface_load(In=4,k=0.3,plotear=1,default="a"):
    try:
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]
        #num_blocks=8
        num_blocks=random.randint(7,10)
        mult=1
        rango=muestreo
        acum=0;aux_arranque=0;
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)        
            #r=rango         
            p=int(r)                                  
            intervalo.append(random.randint(0.5*p,p))  
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        #p_start=1
        aux_ini=p_start
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
    
        g=1;
        a1=In;b1=k;a2=In;b2=k;a3=(In+1);b3=k;a4=4;b4=0;aux_arranque=1
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
    
            if i==(len(ranks)-1):
                    g=3
            if g==0:
                Ina=a1
                ka=b1            
                g=1
                aux_arranque=1;
                
                
            elif g==1:
                Ina=a2
                Ina=((a3-a2)/len(ranks[i]))*(np.array(list(ranks[i]))-inicio)+a2
                ka=b2
                #g=2
                
            elif g==2:
                Ina=a3
                ka=b3
                g=3
                
            elif g==3:
                Ina=a4
                ka=b4
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
               
            if aux_arranque==1 and i < (len(ranks)-2):
                radio[inicio]=6
                radio[inicio]=2*In
                aux_arranque=0
    
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por emulsiones o cargas en superficie") 
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='m',linewidth=2)
        radio=np.array(radio)
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    return radio
"""----------------------fin de (12)----------------------------------------"""
                                              
    
    
    
"""-------------------------------------------------------------------------"""    
"""(13)--------GENERAR CARTAS AMPERIMETRICAS CON SOLIDOS EN LA BOMBA-----------

"""
def sim_current_solid_in_pump(In=4,k=0.3,plotear=1,default="a"):
    try:        
        muestras_minuto=1
        muestreo=24*muestras_minuto*60
        angle=np.arange(0,2*np.pi,(2*np.pi)/muestreo)
        ruidos=random.uniform(0,1,(muestreo))
        radio=np.array(In+k*ruidos-k/2)  
        intervalo=[]
        ranks=[]
        num_blocks=random.randint(5,10) #valor aleatorio
        #num_blocks=8
        mult=2
        rango=muestreo
        acum=0;aux_arranque=0;
        t=0
        for i in range((mult*num_blocks-1)):
            r=rango/(mult*num_blocks-i)                 
            p=int(r)
            if t==0:                                  
                intervalo.append(random.randint(0.9*p,p)) 
                t=1
            else:
                intervalo.append(random.randint(0.2*p,p*0.4)) 
                t=0
            rango=rango-intervalo[i]                
            acum=acum+intervalo[i]    
        intervalo.append(muestreo-acum)                
        #print("N intervalos", num_blocks)                                           
        #print(intervalo)
        p_start=random.randint(1,240*muestras_minuto) # primer arranque del dia primeras 4 horas del dia
        aux_ini=p_start
        
        for i in range((mult*num_blocks-1)):                  
            p_end=p_start+intervalo[i]
            if  p_end>=muestreo:
                ranks.append(range(p_start,muestreo))
                p_end=(intervalo[i]-(muestreo-p_start))-1
                ranks.append(range(0,p_end))  
            else:
                ranks.append(range(p_start,p_end)) 
            p_start=p_end
        if(aux_ini<p_start):
            ranks.append(range(p_start,muestreo))
            ranks.append(range(0,aux_ini))
        else:
            ranks.append(range(p_start,aux_ini))
            
        g=0;
        a1=In;b1=k;a2=In;b2=2;a3=4;b3=0;aux_arranque=1
        aux_arranque=1;
        for i in range(len(ranks)-0):
            inicio=ranks[i][0]
            fin=ranks[i][-1]+1
            ruidos=random.uniform(0,1,(len(ranks[i])-0))
            
            if i==(mult*num_blocks-1):
                g=0
                
            if i==(len(ranks)-1):
                g=0
                
            if g==0:
                Ina=a1
                ka=b1            
                g=1
                aux_arranque=1;
            elif g==1:
                Ina=a2
                ka=b2
                g=0
            elif g==2:
                Ina=a3
                ka=b3
                g=0
                    
            radio[inicio:fin]=(Ina+ka*ruidos-ka/2 )
            radio[aux_ini]=2*In
               
        x=-radio*np.cos(angle)
        y=radio*np.sin(angle)
        len(radio)
        print("carta falla por solidos en la bomba")
        print("tiene:",len(x),"valores, una muestra tomada cada ",muestras_minuto, "minutos" )
        print("\n")
        if plotear==1:
            py.plot(x,y,color='k',linewidth=2) 
        radio=np.array(radio)
    except:
        radio=np.loadtxt(default)
        radio=np.array(radio)
    
    return radio
"""----------------------fin de (13)-----------------------------------------"""  
