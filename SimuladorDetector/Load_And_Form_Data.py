# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 14:57:25 2017
@author: angel
"""
import numpy as D

"""
(1)----------------CARGAR DATA DESDE UN FICHERO con extension .txt-------------
Load_Data(nfile,skip_rows,use_cols,un_pack) recibe los siguientes parametros;

a) nfile= nombre del fichero a cargar; ejemplo -> Datos.txt

b) skip_rows= indica las filas del archivo que se va a saltar; si se quieren leer
   todas las filas skip_rows=0, si quiero saltarme la primera fila skip_rows=1. etc

c) use_cols= indica cuales columnas del fichero quiero cargar, se deben especificar
   de la forma (a,b,c); ejemplo: si solo quiero cargar los valores de las 
   filas 2, 5 y 7 -> use_cols=(2,5,7)

d) un_pack=indica la manera en que se representará la Data
   si un_pack=TRUE  --> las filas del documento seran columnas en el narray
                        las columnas del documento seran filas en el narray
   si un_pack=FALSE --> las filas del documento seran filas en el narray
                        las columnas del documento seran columnas en el narray
                        
La funcion devuelve el valor de Data que es tipo array, indica las condiciones
en que se cargo y la dimension de Data. es importante acotar que los valores
que contenga el fichero a cargar deben ser numericos y, en caso de contener
palabras o comentarios en algunas de sus filas especificar cuales son para
saltarselas.
"""
def Load_Data(nfile,skip_rows,use_cols,un_pack):#
    Data="fallo la carga, estoy vacio"
    
    if (use_cols=="todas"):
        
        try:
            Data=D.loadtxt(nfile,skiprows=skip_rows,unpack=un_pack)
        except:
             b=open(nfile)
             c=b.read() 
             b.close()
             d=c.split()
             Data=D.array(d)
             print("no se saltó las filas indicadas, se cargan todos los valores del fichero ")
               
    else:
        try:
            Data=D.loadtxt(nfile,skiprows=skip_rows,usecols=use_cols,unpack=un_pack)
        except:
             b=open(nfile)
             c=b.read() 
             b.close()
             d=c.split()
             Data=D.array(d)
             print("hubo una inconsistencia en la eleccion de columnas a cargar, por tanto se cargan todos los valores del fichero ")
    
    print("se cargo el archivo ", nfile," exitosamente y contiene", Data.size, "valores" ) 
   
    return Data
"""----------------------fin de (1)----------------------------------------"""

"""
(2)----------------------------DAR FORMA A LA DATA-----------------------------
Form_Data(number_rows,number_cols,data) recibe los siguientes parametros:
number_rows= numero de filas que quiero tenga el nuevo array
number_cols= numero de columnas que quiero tenga el nuevo array
data= array original al que quiero reordenar

si pudo reordenar la data retorna el valor de data 
si no pudo reorderdenar la data indica un mensaje y retorna el valor de data =None
"""
    
def Form_Data(number_rows,number_cols,data):
    if data.size==number_rows*number_cols:
        Data=data.reshape(number_rows,number_cols)
        return Data
    else:
        print("las dimensiones de la data no permiten reordenar de esta manera,"   
        "intente con una combinacion de filas y columnas cuyo producto sea igual a ", data.size)
"""----------------------------fin de (2)-----------------------------------"""