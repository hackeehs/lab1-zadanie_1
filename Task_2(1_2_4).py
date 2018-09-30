import gspread
import random
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Laboratory work 2-38370bd8641f.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Laboratory work 2').get_worksheet(1)

wks.clear()

def RandUnique(start, end, num): 
    res = [] 
    k=0
    res.append(random.randint(start, end))
    number = random.randint(start, end)
    while len(res) < num:
        number = random.randint(start, end)
        for i in range(len(res)):
            if number == res[i]:
                k=1
                break
        if k == 1:
            number = random.randint(start, end)
            k=0
        else:
            res.append(number)
            k=0
            number = random.randint(start, end)
            
    return res 

def RandUniqueRe(start, end, num):
    #res = [[] for _ in range(num)]
    res = [[]]
    res[0] = [(random.randint(start, end)),(random.randint(start, end))]
    coord = [(random.randint(start, end)), (random.randint(start, end))]
    while len(res) < num-1:
        for i in range(len(res)):
            if (coord not in res) and (len(res) < 10):
                res.append(coord)
                coord = [(random.randint(start, end)), (random.randint(start, end))]
                #print(res)
                #print(len(res))
                
    return res

def Rand(start, end, num): 
    res = [] 
    k=0
    res.append(random.randint(start, end))
    number = random.randint(start, end)
    while len(res) < num:
        number = random.randint(start, end)
        res.append(number)
            
    return res 

def Vin(arrays, num):
    arrays_vin = arrays
    for i in range(1, num+1):
        for j in range(num):
            if arrays[i][j] == '':
                if (j+1)<=num-1:
                    if (arrays[i][j+1]) != '':
                        arrays_vin[i][j] = arrays[i][j+1]
                        wks.update_cell(j+1, i, str(arrays[i][j+1]))
                else:
                    if (j-1)>=0:
                        if (arrays[i][j-1]) != '':
                            arrays_vin[i][j] = arrays[i][j-1]
                            wks.update_cell(j+1, i, str(arrays[i][j-1]))
                    else:
                        arrays_vin[i][j] = -999
                        wks.update_cell(j+1, i, -999)
    return arrays_vin

def Cor(arrays, num):
    cor_rows={}
    arrays_cor = arrays
    for i in range(1, num+1):
        for j in range(num):
            if arrays[i][j] == '':
                if j not in cor_rows:
                    cor_row = input('Введите номер коррелируемого ряда для ряда номер ' + str(j+1) + ' с утраченным значением: ')
                    cor_row = int(cor_row)-1
                    cor_rows[j] = cor_row
                k=1
                while arrays[i][j] == '':
                    if (i+k <= num-1) and (arrays_cor[i][int(cor_rows[j])]!='') and (arrays_cor[i+k][int(cor_rows[j])]!='') and (arrays_cor[i+k][j]!=''): 
                            arrays_cor[i][j] = round((arrays_cor[i+k][j])/(arrays_cor[i+k][int(cor_rows[j])])*(arrays_cor[i][int(cor_rows[j])]))
                            wks.update_cell(j+1, i, str(arrays_cor[i][j]))
                            #print ('+1', arrays_cor[i][j], k, arrays_cor[i+k][j], arrays_cor[i+k][int(cor_rows[j])], arrays_cor[i][int(cor_rows[j])])
                    else:    
                        if (i-k >= 0) and (arrays_cor[i][int(cor_rows[j])]!='') and (arrays_cor[i-k][int(cor_rows[j])]!='') and (arrays_cor[i-k][j]!=''): 
                            arrays_cor[i][j] = round((arrays_cor[i-k][j])/(arrays_cor[i-k][int(cor_rows[j])])*(arrays_cor[i][int(cor_rows[j])]))
                            wks.update_cell(j+1, i, str(arrays_cor[i][j]))
                            #print ('-1', arrays_cor[i][j], k, arrays_cor[i-k][j], arrays_cor[i-k][int(cor_rows[j])], arrays_cor[i][int(cor_rows[j])])
                        else:
                            k=k+1

    return arrays_cor
    
    
num = 18
start = 1
end = 30
j = 1
arrays = [[] for _ in range(j, num+2)]
for i in range(1, num+1):
    cell_list = wks.range(1, i, num, i)
    arrays[i] = Rand(start, end, num)
    print(arrays[i])
    #print(arrays[1][0])
    i=0
    for cell in cell_list:
	    cell.value = str(arrays[j][i])
	    i=i+1
    j=j+1
    wks.update_cells(cell_list)

cells_index = [[] for _ in range(10)]

#arrx = RandUniqueRe(1, 18, 10)
#arry = RandUniqueRe(1, 18, 10)
arr_coord = RandUniqueRe(1, 18, 10)
#print(arrx)
print(arr_coord,' - координаты утраченных значений')
#print(len(arr_coord))
for i in range(10):
    x = arr_coord[i][0]
    y = arr_coord[i][1]
    wks.update_cell(y, x, '')
    arrays[x][y-1] = ''
    #print(arrays[x])

restore = input('Каким способам восстановить недостающие данные? 1 - винзорирование, 2 - корреляционное восстановление.\n')
if restore == '1':
    arrays_vin = Vin(arrays, num)
    for i in range(1, num+1):
        print(arrays_vin[i])
    #print('Готово')
else:
    if restore == '2':
        arrays_cor = Cor(arrays, num)
        for i in range(1, num+1):
            print(arrays_cor[i])
        #print('Готово')


