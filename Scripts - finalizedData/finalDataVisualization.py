import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium as folium
finalizedData = pd.read_csv('../finalizedData/finalizedData.csv')
centerlatitude = finalizedData['latitude'].mean()
centerlongitude = finalizedData['longitude'].mean()

##############################################################################
#Pie Chart
##############################################################################

labels = ['Budget', 'Average', 'Expensive']
plt.pie(finalizedData['price_category'].value_counts(), labels=finalizedData['price_category'].value_counts().index, autopct='%1.1f%%')
plt.title("Finalized Data - Categorization Distribution")
plt.savefig("../ModelsandDiagrams/PieChartDistributionPriceCategories.png")
plt.show()

##############################################################################
#Map Creation
##############################################################################
map = folium.Map(location= [centerlatitude, centerlongitude], zoom_start= 10)


def colorization(category):
    if category == 'Budget':
        return "green"
    elif category == 'Average':
        return "yellow"
    elif category == 'Expensive':
        return "red"

for listings, row in finalizedData.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color=colorization(row['price_category']),
        fill=True,
        fill_opacity=0.7,
        opacity=1
    ).add_to(map)



map.save("../ModelsandDiagrams/mapOfDataCategoryDistribution.html")
