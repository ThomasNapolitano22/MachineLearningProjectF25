import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium as folium
import leafmap.foliumap as leafmap
import json

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

    ##############################################################################
    #Map Creation (Methods)
    ##############################################################################
        #Neighborhood Overlay
neighborhoodPath = "../finalizedData/boston_neighborhood_boundaries.geojson"
with open(neighborhoodPath) as f:
    neighborhood_data = json.load(f)

        #Colorization Method
def colorization(category):
    if category == 'Budget':
        return "green"
    elif category == 'Average':
        return "yellow"
    elif category == 'Expensive':
        return "red"

legend_dictionary = {
    "Budget": "green",
    "Average": "yellow",
    "Expensive": "red"
}
##############################################################################
#First Map (Overview of all the categories)
##############################################################################

map1 = leafmap.Map(location= [centerlatitude, centerlongitude], zoom_start= 10)

for listings, row in finalizedData.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color=colorization(row['price_category']),
        fill=True,
        fill_opacity=0.7,
        opacity=1
    ).add_to(map1)

map1.add_geojson(
    in_geojson = neighborhoodPath,
    layer_name = "Neighborhoods"
)
map1.add_labels(
    data = neighborhoodPath,
    column = "name",
    font_size= "12pt",
    font_color = "Black",
    font_weight = "bold",
    font_family= "Times New Roman"
)


map1.add_legend(title="Price Categorization", legend_dict=legend_dictionary)
map1.save("../ModelsandDiagrams/mapOfDataCategoryDistribution.html")

##############################################################################
#Second Map (Just Private Rooms)
##############################################################################
map2 = leafmap.Map(location= [centerlatitude, centerlongitude], zoom_start= 10)

for listings, row in finalizedData.iterrows():
    if(row['room_type'] == "Private room"):
        folium.CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=5,
            color=colorization(row['price_category']),
            fill=True,
            fill_opacity=0.7,
            opacity=1
        ).add_to(map2)



map2.add_geojson(
    in_geojson = neighborhoodPath,
    layer_name = "Neighborhoods"
)
map2.add_labels(
    data = neighborhoodPath,
    column = "name",
    font_size= "12pt",
    font_color = "Black",
    font_weight = "bold",
    font_family="Times New Roman"

)


map2.add_legend(title="Price Categorization", legend_dict=legend_dictionary)

map2.save("../ModelsandDiagrams/mapOfDataCategoryDistribution(PrivateRooms).html")

##############################################################################
#Third Map (Entire Homes/Apts)
##############################################################################
map3 = leafmap.Map(location= [centerlatitude, centerlongitude], zoom_start= 10)

for listings, row in finalizedData.iterrows():
    if(row['room_type'] == "Entire home/apt"):
        folium.CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=5,
            color=colorization(row['price_category']),
            fill=True,
            fill_opacity=0.7,
            opacity=1
        ).add_to(map3)



map3.add_geojson(
    in_geojson = neighborhoodPath,
    layer_name = "Neighborhoods"
)
map3.add_labels(
    data = neighborhoodPath,
    column = "name",
    font_size= "12pt",
    font_color = "Black",
    font_weight = "bold",
    font_family="Times New Roman"

)

map3.add_legend(title="Price Categorization", legend_dict=legend_dictionary)
map3.save("../ModelsandDiagrams/mapOfDataCategoryDistribution(EntireHomeOrApt).html")
########################################################################################


