### Author : Ashwin Kumar 
### Roll : CE21BTECH11008 

import pandas as pd
import math
import sys
import matplotlib.pyplot as plt

# Read data from CSV
df = pd.read_csv("data.csv")

# Converting the first column to datetime
df['Timestamp'] = pd.to_datetime(df.iloc[:, 0])

# Input and conversion
year_no = int(input("Enter the year: "))
month_no = int(input("Enter the month: "))

# Leap year calculation
def is_leap_year(year):
    return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)

J = 366 if is_leap_year(year_no) else 365

# Extract data for the specific month
month_data = df[(df['Timestamp'].dt.year == year_no) & (df['Timestamp'].dt.month == month_no)]

if month_data.empty:
    print("The DataFrame is empty. No data for the specified month and year.")
    sys.exit()

phi_deg = float(input("Enter the latitude in degrees: "))
# Height above sea level
z = float(input("Enter the height above sea level in meters: "))

# Calculate the number of days in the given month
days_in_month = pd.Period(f'{year_no}-{month_no}', freq='M').days_in_month
date_range = pd.date_range(start=f'{year_no}-{month_no:02d}-01', periods=days_in_month, freq='D')

day_no = list(range(1, days_in_month + 1))
evaporation_val = [0] * days_in_month

# Loop over the dates in the month
for i, day in enumerate(date_range):
    day_data = month_data[month_data['Timestamp'].dt.day == day.day]
    
    if day_data.empty:
        continue
    # Extract required data
    Tmax = day_data.iloc[:, 2].max()
    Tmin = day_data.iloc[:, 2].min()
    RH_max = day_data.iloc[:, 3].max()
    RH_min = day_data.iloc[:, 3].min()
    uavg = day_data.iloc[:, 6].mean()
    R_s_watt = day_data.iloc[:, -1].mean()

    R_s = R_s_watt * 0.0864  # Convert to MJ/m²/day

    T_mean = (Tmax + Tmin) / 2
    delta = 4098 * 0.6108 * math.exp((17.27 * T_mean) / (T_mean + 237.3)) / ((T_mean + 237.3) ** 2)

    P = 101.3 * ((293 - 0.0065 * z) / 293) ** 5.26
    gamma = 0.000665 * P

    DT = delta / (delta + gamma * (1 + 0.34 * uavg))
    PT = gamma / (delta + gamma * (1 + 0.34 * uavg))
    TT = 900 * uavg / (T_mean + 273)

    e_Tmax = 0.6108 * math.exp((17.27 * Tmax) / (Tmax + 237.3))
    e_Tmin = 0.6108 * math.exp((17.27 * Tmin) / (Tmin + 237.3))
    e_s = (e_Tmax + e_Tmin) / 2

    d_r = 1 + 0.033 * math.cos((2 * math.pi / 365) * J)
    d_t = 0.409 * math.sin((2 * math.pi / 365) * J - 1.39)

    sigma = 4.903e-9  # Stefan-Boltzmann constant in MJ/K^4/m²
    T_max_K = Tmax + 273.16
    T_min_K = Tmin + 273.16

    e_a = (e_Tmin * RH_max + e_Tmax * RH_min) / 200

    alpha = 0.23
    phi = math.radians(phi_deg)
    G_sc = 0.0820
    omg_s = math.acos(-math.tan(phi) * math.tan(d_t))

    R_a = (24 * 60 / math.pi) * G_sc * d_r * (omg_s * math.sin(phi) * math.sin(d_t) + math.cos(phi) * math.cos(d_t) * math.sin(omg_s))
    R_so = (0.75 + 2e-5 * z) * R_a

    R_ns = (1 - alpha) * R_s
    R_nl = sigma * ((T_max_K**4 + T_min_K**4) / 2) * (0.34 - 0.14 * math.sqrt(e_a)) * (1.35 * (R_s / R_so) - 0.35)

    R_n = R_ns - R_nl
    R_ng = 0.408 * R_n

    ET_rad = DT * R_ng
    ET_wind = PT * TT * (e_s - e_a)

    ETo = ET_wind + ET_rad
    evaporation_val[i] = ETo

# Plotting the results
plt.figure(figsize=(10, 5))
plt.plot(day_no, evaporation_val, marker='o', linestyle='-', color='red')

# Adding labels and title
plt.xlabel('Day')
plt.ylabel('Evapotranspiration (mm/day)')
plt.title('Evapotranspiration over Days')
plt.grid(True)

# Display the plot
plt.show()

# sys.exit()
