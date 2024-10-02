# Author : Ashwin Kumar 
# Roll : CE21BTECH11008
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
data = pd.read_csv("/home/ash/Desktop/water resource eng/reservoir routing/flow.csv")
print(data)

outflow = data.iloc[:,1]
storage = data.iloc[:,2]

outflow1 = 2*storage*(10**6)/(6*3600) + outflow
outflow2 = 2*storage*(10**6)/(6*3600) - outflow 

# print(outflow1)
T=  [0, 6, 12, 18, 24, 30, 36, 42, 48, 54,60, 66, 72, 78, 84, 90, 96, 102, 108, 114,120, 126, 132, 138, 144, 150, 156, 162]
I = [0, 50, 130, 250, 350, 540, 735, 1215, 1800, 1400, 1050, 900, 740, 620, 510, 420, 320, 270, 200, 150, 100, 72, 45, 25, 10, 0, 0, 0]

# for i in I:
#     print(i)


plt.figure(figsize=(8,6))
plt.plot(outflow1, outflow, marker='o', color='b', label="Outflow vs Outflow1 ")
plt.plot(outflow2, outflow, marker='o', color='g', label="Outflow vs Outflow2 ")

coeff_outflow1 = np.polyfit(outflow1, outflow, 1)  
coeff_outflow2 = np.polyfit(outflow2, outflow, 1)

print(coeff_outflow1)
print(coeff_outflow2)

slope1 = coeff_outflow1[0]
slope2 = coeff_outflow2[0]
incept1 = coeff_outflow1[1]
incept2 = coeff_outflow2[1]
print(slope1)

plt.xlabel("Outflow (cumencs)")
plt.ylabel("Storage (m3) x 10^6")
plt.title("Outflow vs Storage Graph")
plt.grid(True)
plt.legend()
plt.show()




xcord2=0
O=[0]

for i in range(0,len(I)-1):
    I1= I[i]
    I2= I[i+1]
    xcord1 = I1+I2 + xcord2
    ycord1 = xcord1*slope1 +incept1
    O.append(ycord1)
    ycord2 = ycord1 
    xcord2 = (ycord2-incept2)/slope2


print(O)


plt.figure(figsize=(8,6))
plt.plot(T, I, marker='o', color='r', label="Inflow vs time ")
plt.plot(T, O, marker='o', color='g', label="outflow vs time ")
plt.ylabel("Outflow (cumecs)")
plt.xlabel("Time(in hrs)")
plt.title("Resevoir Routing ")
plt.grid(True)
plt.legend()
plt.show()

max1 = max(O)
max2 = max(I)
time1 = O.index(max1)
time2 = I.index(max2)

peak_diff = max2-max1
print(f"{round(peak_diff)} cumecs")

lag = T[time1]-T[time2]
print(f" {lag} Hours")

