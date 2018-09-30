import gspread
import random
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Laboratory work 2-38370bd8641f.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Laboratory work 2').sheet1

wks.clear()

def Rand(start, end, num): 
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


num = 18

startx = int(input('Введите минимальное значение X: '))
endx = int(input('Введите максимальное значение X: '))
arrx = Rand(startx, endx, num)

starty = int(input('Введите минимальное значение Y: '))
endy = int(input('Введите максимальное значение Y: '))
arry = Rand(starty, endy, num)

print(arrx, ' - значения X')
print(arry, ' - значения Y')

cell_listx = wks.range('A1:A'+str(num))
i=0
for cell in cell_listx:
	cell.value = str(arrx[i])
	i=i+1
wks.update_cells(cell_listx)

cell_listy = wks.range('B1:B'+str(num))
i=0
for cell in cell_listy:
	cell.value = str(arry[i])
	i=i+1
wks.update_cells(cell_listy)

sumx = 0
sumy = 0
sumx2 = 0
sumxy = 0

for i in range(num):
	sumx = sumx + arrx[i]
	sumy = sumy + arry[i]
	sumx2 = sumx2 + ((arrx[i])**2)
	sumxy = sumxy + arrx[i] * arry[i]
#print(sumx, sumy, sumx2, sumxy)	
a = (num * sumxy - sumx * sumy)/(num * sumx2 - ((sumx)**2))
b = (sumy - a * sumx)/num
print(a, b, ' - коэффициенты a, b аппроксимации')

arryy = []
for i in range(num):
	arryy.append(arrx[i]*a+b)

plt.plot(arrx, arryy)
plt.scatter(arrx, arry)
plt.show()
