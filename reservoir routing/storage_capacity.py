# Author : Ashwin Kumar 
# Roll : CE21BTECH11008

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# Sample x and y values
x = np.array([0, 4, 9, 12, 16, 21, 24, 28, 33, 36, 40, 45, 48, 52, 57, 60, 
              64, 69, 72, 76, 81, 84, 88, 93, 96, 100, 105, 108, 112, 117, 
              120, 124, 129, 132, 136, 141, 144])

discharge = np.array([
    1050, 300, 50, 3000, 250, 40, 3500, 370, 90, 2000, 150, 120, 
    1200, 350, 65, 1400, 400, 100, 3600, 200, 80, 3000, 150, 120, 
    700, 210, 50, 800, 120, 80, 2400, 320, 120, 3200, 280, 80
])

y = [0]

prev =0
for i in range(len(discharge)):
    val = discharge[i]*24*36/1e6

    if i%3==0:
        prev = val*1.2+prev
        y.append(round(prev,4))
    elif i%3==1:
         prev = val*1.5+prev
         y.append(round(prev,4))
    else:
          prev = val*0.9+prev
          y.append(round(prev,4))

print(y)
print(len(y))


# Fit a smooth spline to the data
spl = UnivariateSpline(x, y, s=0.5)

# Fine set of points for plotting the smooth curve
x_fine = np.linspace(min(x), max(x), 1000)
y_fine = spl(x_fine)

# Derivative to find local maxima and minima
dy_fine = spl.derivative()(x_fine)

# Local maxima (derivative changes from positive to negative)
max_idx = (np.diff(np.sign(dy_fine)) < 0).nonzero()[0]
min_idx = (np.diff(np.sign(dy_fine)) > 0).nonzero()[0]

max_need = 0

# Plot the smooth curve
plt.figure(figsize=(20, 10))
plt.plot(x_fine, y_fine, label='Smooth curve')

# Loop through all local maxima and find the next local minima
for idx_max in max_idx:
    x_max = x_fine[idx_max]
    y_max = y_fine[idx_max]
    
    # Find the next local minima after the current maxima
    min_candidates = min_idx[min_idx > idx_max]
    if len(min_candidates) > 0:
        idx_min = min_candidates[0]
        x_min = x_fine[idx_min]
        y_min = y_fine[idx_min]

        # Tangent line at the local maximum: y = mx + c
        slope = 0.125  # this is the slope of demand line
        intercept = y_max - slope * x_max
        
        # Value for comparison
        diff = slope * x_min + intercept - y_min
        max_need = max(diff, max_need)

        # Highlight local maximum and minima
        plt.scatter([x_max], [y_max], color='red', label=f'Local Max (x={x_max:.2f}, y={y_max:.2f})')
        plt.scatter([x_min], [y_min], color='blue', label=f'Next Min (x={x_min:.2f}, y={y_min:.2f})')

        # Output coordinates and tangent line equation
        print(f"Max at: x = {x_max}, y = {y_max}")
        print(f"Tangent line: y = {slope}x + {intercept}")
        print(f"Next Min at: x = {x_min}, y = {y_min}")
        print('-' * 50)

print(f"Maximum need = {max_need}")

# Customize plot
plt.title('Smooth Curve with Local Maxima and Minima')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
