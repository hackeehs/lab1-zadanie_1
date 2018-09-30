import gspread
import random
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Laboratory work 2-94b4ef54a7fa.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Laboratory work 2').get_worksheet(2)

wks.clear()

def Rand(start, end, num): 
    res = [] 
    k=0
    res.append(random.randint(start, end))
    number = random.randint(start, end)
    while len(res) < num:
        number = random.randint(start, end)
        res.append(number)
            
    return res 

def Mat(arrays, num):
    arrays_mat = arrays
    mats=[0 for _ in range(1, num+1)]
    dis=[0 for _ in range(1, num+1)]
    for i in range(1, num+1):
        for j in range(num):
            ver = arrays_mat[i][j]/100
            mats[j] = mats[j] + (round(arrays_mat[i][j]*ver))
            dis[j] = dis[j] + (round((arrays_mat[i][j]**2)*ver))
            #print(dis)
            #print(dis[j])
    for j in range(num):
        #print(dis[j])
        dis[j] = dis[j] - (mats[j]**2)   
    
    return mats, dis

def Corr(arrays, mats, dis, num):
    arrays_mat = arrays
    cov = [[0 for _ in range(num)] for _ in range(num)]
    mats2 = [[0 for _ in range(num)] for _ in range(num)]
    for i in range(1, num+1):
        for j in range(num):
            if (i != j+1) and (j+1 < num):		
                ver = (arrays_mat[i][j+1]/100 + arrays_mat[i][j+1]/100) /2
                mats2[i-1][j] = mats2[i-1][j] + (round(arrays_mat[i][j]*arrays_mat[i][j+1]*ver))
    ver2 = input ('Введите допустимый процент погрешности: ')
    ver2 = int(ver2)/100
    for i in range(1, num+1):
        for j in range(num):
            if (i != j+1) and (j+1 < num):
                print(cov)
                print(cov[i-1][j])	
                print(mats[j+1])	
                cov[i-1][j] = round((mats2[i-1][j] - (mats[j]*mats[j+1]))/(dis[j]*dis[j+1])**(1/2))
            else:
                cov[i-1][j]=0
                print(cov)
    return cov
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



#mats, dis = Mat(arrays, num)
#print(mats, ' - Математическое ожидание для каждого ряда')
#print(dis, ' - Дисперсия для каждого ряда')

arrays_t = [[] for _ in range(1, num+2)]
for i in range(1, num+1):
    for j in range(num):
        arrays_t[j+1].append(arrays[i][j])
        #print (arrays_t[j])

mats_np=[0 for _ in range(1, num+1)]
dis_np=[0 for _ in range(1, num+1)]
cor_np=[[] for _ in range(1, num+1)]

#print(mats_np)	
#cov = Corr(arrays, mats, dis, num)

for i in range(1, num+1):
    #print(arrays_t[i])
    mats_np[i-1] = round(np.mean(arrays_t[i]))
    dis_np[i-1] = round(np.var(arrays_t[i]))
    for j in range(1, num+1):
        #print(arrays_t[i])
        #print(arrays_t[j])
        temp = np.correlate(arrays_t[i], arrays_t[j])
        cor_np[i-1].append(temp)
        #print(cor_np[i-1][j-1])
    
    

print(mats_np, ' - Математическое ожидание для каждого ряда')
print(dis_np, ' - Дисперсия для каждого ряда')

for i in range(1, num+1):
    #wks.update_cell(i, num+1, mats[i-1])
    #wks.update_cell(i, num+3, dis[i-1])
    wks.update_cell(i, num+1, mats_np[i-1])
    wks.update_cell(i, num+2, dis_np[i-1])
    #print(cor_np[i-1])
    #print(cov[i-1])
    
#for i in range(1, num+1):
    #for j in range(num):
        #arrays_t[j][i] = arrays[i][j]
        #print (arrays_t[j])
	
