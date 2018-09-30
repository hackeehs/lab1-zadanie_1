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

def RandUniqueRe(start, end, num, end2):
    #res = [[] for _ in range(num)]
    res = [[]]
    res[0] = [(random.randint(start, end2)),(random.randint(start, end2))]
    coord = [(random.randint(start, end2)), (random.randint(start, end2))]
    while len(res) < num-1:
        for i in range(len(res)):
            if (coord not in res) and (len(res) < 10):
                res.append(coord)
                coord = [(random.randint(start, end)), (random.randint(start, end2))]
                print(res)
                print(len(res))
            else:
                coord = [(random.randint(start, end)), (random.randint(start, end2))]
                
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

def Lin(arrays, num):
    sumx = 0
    sumy = 0
    sumx2 = 0
    sumxy = 0
    k = 0
    arrays_lin = arrays
    array_lin_y = []
    for i in range(1, 3):
        for j in range(num):
            if i == 1:
                if arrays[i][j] != '' and arrays[i+1][j] != '' :
                    k = k+1
                
                    sumx = sumx + arrays[i][j]
                    sumy = sumy + arrays[i+1][j]
                    sumx2 = sumx2 + ((arrays[i][j])**2)
                    sumxy = sumxy + arrays[i][j] * arrays[i+1][j]
    #print(sumx, sumy, sumx2, sumxy)	
    a = (k * sumxy - sumx * sumy)/(k * sumx2 - ((sumx)**2))
    b = (sumy - a * sumx)/k
    print(a, b, ' - Коэффициенты a, b для линейной аппроксимации')
    for i in range(1, 3):
        for j in range(num):
            if (arrays[i][j] == '') and (i==2):
                arrays_lin[i][j] = round(a*int(arrays[i-1][j])+b)
                wks.update_cell(j+1, i, str(arrays_lin[i][j]))
            else:
                if (arrays[i][j] == '') and (i==1):
                    arrays_lin[i][j] = round(((int(arrays[i+1][j]))-b)/a)
                    wks.update_cell(j+1, i, str(arrays_lin[i][j]))
            if (i == 2) and (arrays[i][j] != '') and (arrays[i-1][j] != '') :
                #print (arrays[i-1][j])
                array_lin_y.append(a*int(arrays[i-1][j])+b)
                
    return arrays_lin, array_lin_y

num = 18
start = 1
end = 30
j = 1
arrays = [[] for _ in range(j, 4)]
for i in range(1, 3):
    cell_list = wks.range(1, i, num, i)
    arrays[i] = Rand(start, end, num)
    print(arrays[i], ' - Набор случайных координат ' + str(i) )
    i=0
    for cell in cell_list:
	    cell.value = str(arrays[j][i])
	    i=i+1
    j=j+1
    wks.update_cells(cell_list)

cells_index = [[] for _ in range(10)]

arrx = Rand(1, 2, 10)
arry = RandUnique(1, 18, 10)
#arr_coord = RandUniqueRe(1, 18, 10, 2)
print(arrx, ' - Индексы пропусков по X')
print(arry, ' - Индексы пропусков по Y')
#print(arr_coord, ' - Координаты выпавших значений')
for i in range(10):
    x = arrx[i]
    y = arry[i]
    wks.update_cell(y, x, '')
    arrays[x][y-1] = ''
    #print(arrays)
    
print(arrays[1], ' - Набор координат X после потерь данных')
print(arrays[2], ' - Набор координат Y после потерь данных')

restore = input('Каким способам восстановить недостающие данные? 1 - линейная аппроксимация.\n')
if restore == '1':
    arrays_lin, array_lin_y = Lin(arrays, num)

for i in range(1, 3):
    print(arrays_lin[i], ' - Восстановленный набор ' + str(i))

#print(arrays_lin[1])
#print(array_lin_y)
plt.scatter(arrays_lin[1], arrays_lin[2])
plt.plot(arrays_lin[1], array_lin_y)
plt.show()
