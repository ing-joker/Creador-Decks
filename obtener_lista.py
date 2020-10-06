import os
import sqlite3
from PIL import Image,ImageTk
import cv2 as cv
import re,base64
from unicodedata import normalize
def  consulta(query, parameters=()):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

def  consulta2(query, parameters=()):
    with sqlite3.connect(db2) as conn2:
        cursor = conn2.cursor()
        result = cursor.execute(query, parameters)
        conn2.commit()
    return result


#directorio= 'C:/Users/Scarlett/Desktop/sr'
#directorio='C:/Users/Scarlett/Pictures/Uplay'
directorio='C:/Users/Scarlett//Documents/Programacion/Creador de Mazos/cartas'
db='C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/database2.db'
db2='C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/db_creador.db'
lista = os.listdir(directorio)
#print(lista)
#j=[None]*len(lista)
#h=0
'''
query='SELECT * FROM cartas ORDER BY nombre DESC'
records=consulta(query)

for i in records:
    print(i)
    query='INSERT INTO cartas VALUES(NULL,?,?,?,?,?,?,?,?)'
    parameters=(i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],)
    consulta2(query,parameters)'''









'''
for i in lista:
    #f=open('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas/'+ i,"rb")
    #photo_Color = cv.imread('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas/'+ i)
    #img=base64.encodestring(f.read())
    #print("f")
    #print(f.read())
    #print("f")
    #query='DELETE FROM cartas WHERE nombre = ?'
    #consulta(query,(i,))
    j[h]=i.replace('.png','')
    print(j[h])
    h+=1
    
    #query = 'INSERT INTO cartas VALUES(NULL,NULL, ?,NULL,NULL,NULL,?,NULL,NULL)'
    #parameters=(j,4)
    #consulta(query,parameters)

query = 'SELECT * FROM cartas ORDER BY nombre ASC' #ascedente ASC

db_columnas = consulta(query)
records=db_columnas.fetchall()'''
'''
h=0
for i in lista:
    print(i)
    j=i.replace('.png','')
    jj=j.replace('_',' ')
    x=cv.imread('C:\\Users\\Scarlett\\Documents\\Programacion\\Creador de Mazos\\con creador\\' + i,1)
    d = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", i), 0, re.I)
    g = normalize( 'NFC', d)
    p=g.replace(' ','_')
    os.rename(directorio+'/'+ i,'C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas3/'+ p )
    #cv.imwrite('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas3/'+ i,x)
    query = 'INSERT INTO cartas VALUES(NULL,NULL,?, ?,?,NULL,?,?,?)'
    parameters=(jj,4,'N',p)
    consulta(query,parameters)
    
    print(d)
    print(g)'''
    #h+=1
'''
for i in lista:
    j=i.replace('_',' ')
    k=j.replace('.png','')
    query='UPDATE cartas SET nombre = ? WHERE archivo = ?'
    parameters=(k,i)
    consulta(query,parameters)'''


'''
xd='espa'
#SELECT * FROM COMPANY WHERE ADDRESS  LIKE '%-%';
query = 'SELECT * FROM cartas WHERE nombre LIKE ? and atributo = ?'
parameters=('%'+xd+'%','Fuego')
rows=consulta(query,(parameters))
#print(rows.fetchall())
for row in rows:
    print(row[2])'''


'''
nw=[None]*len(lista)
for i in range(len(lista)):
    nw[i]=[None, 'ojito' , lista[i] , None , None ,None, 4,None]
print(nw)

def take_second(elem):
    return elem[2]

parameters=()
with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        result = cursor.execute('DELETE FROM cartas', parameters)
        conn.commit()'''

for i in lista:
    print(i)
    image2 = Image.open('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas/'+i)
    image2.thumbnail([55,80], Image.ANTIALIAS)
    image2.save('C:/Users/Scarlett/Documents/Programacion/Creador de Mazos/cartas2/'+i)

'''
query = 'SELECT * FROM videos ORDER BY id DESC' #ascedente DESC
db_columnas = consulta(query)
records=db_columnas.fetchall()
query='DELETE FROM videos'
consulta(query)
for i in records:
    print(i[2])
    query = 'INSERT INTO videos VALUES(NULL, ?,?)'
    parameters =  (i[1],i[2])
    consulta(query,parameters)'''
    

'''
print(len(records))
print(type(records))
print(records[0])
xs=records[0]
print(xs[2])

records.extend(nw)
print(len(records))
print(records[500:560])
xs=records[530]
print(xs[2])

nueva= sorted(records, key=take_second)
print(nueva)

query='DELETE FROM cartas'
consulta(query)
for i in nueva:
    query = 'INSERT INTO cartas VALUES(NULL, ?,?,?,?,?,?)'
    parameters =  (i[1],i[2],i[3],i[4],i[5],i[6])
    consulta(query,parameters)'''
'''
query= 'UPDATE users SET phone = ? WHERE id = ? '
parameters=(newphone, userid)
consulta(query,parameters)'''