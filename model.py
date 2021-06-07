#Morgan Jones
#Requires the two datasets qhi_temp_2017.csv and qhi_cover_ITEX_1999_2017.csv
#To Run: 'Python model.py'

from scipy.stats import linregress
import pandas as pd
import matplotlib.pyplot as plt

temp_data = pd.read_csv('QikiqtarukHub-master/data/qhi_temp_2017.csv', delimiter=',', header=0)
plot_data = pd.read_csv('QikiqtarukHub-master/data/qhi_cover_ITEX_1999_2017.csv', delimiter=',', header=0)
plot_data.columns =[column.replace(" ", "_") for column in plot_data.columns]

#find average summer temp for year
temp_data.loc[(temp_data['month'] >= 6) & (temp_data['month'] < 9), 'season'] = 'summer'
# https://weatherspark.com/y/145110/Average-Weather-at-Herschel-Island-Automatic-Weather-Reporting-System-Canada-Year-Round#:~:text=The%20warm%20season%20lasts%20for,low%20of%2044%C2%B0F.
average_summer_temp_by_year = temp_data.groupby(['year', 'season'])['temp'].mean()
print(average_summer_temp_by_year)

#find average cover for each species in plots
sp_cover = plot_data.groupby(['year', 'name'])['cover'].mean().to_frame().reset_index()
plot_data_temp = pd.merge(sp_cover, average_summer_temp_by_year, on='year', how='inner')

plt.title("Percentage of plot covering vs summer temprature in two plant species on Qikiqtaruk Island", fontsize=16)
plt.xlabel("Temprature (°C)", fontsize=12)
plt.ylabel("Percentage covering in plots 1-6", fontsize=12)

#plot for Eriophorum vaginatum
al = plot_data_temp.query('name == "Eriophorum vaginatum"', inplace = False)
x = al.temp
y = al.cover
stats = linregress(x, y)
m = stats.slope
b = stats.intercept
plt.scatter(x, y, color='#F0D9AF')
plt.plot(x, m * x + b, color='#F3A81F')

#plot for Salix pulchra
al = plot_data_temp.query('name == "Salix pulchra"', inplace = False)
x = al.temp
y = al.cover
stats = linregress(x, y)
m = stats.slope
b = stats.intercept
plt.scatter(x, y, color='#B6E5A7')
plt.plot(x, m * x + b, color='#72CE55')

plt.gca().legend(('Eriophorum vaginatum','Salix pulchra'))

plt.savefig("temp_data.png")
plt.show()
