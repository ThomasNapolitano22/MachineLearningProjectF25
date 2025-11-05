import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium as folium
import leafmap.foliumap as leafmap
import json
from folium import LayerControl, FeatureGroup
import seaborn as sns

cleanedData = pd.read_csv("../cleanedData/cleanedListings.csv")
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
#Box Plot Chart
##############################################################################

sns.boxplot(x=cleanedData['neighbourhood_cleansed'], y=cleanedData['price'])
plt.title("Boxplot of Price vs. Different Neighborhoods")
plt.xticks(rotation=90)
plt.xlabel("Neighborhoods")
plt.ylabel("Price per Night")
plt.tight_layout()
plt.savefig("../ModelsandDiagrams/BoxPlotOfPriceVs.DifferentNeighborhoods.png")
plt.show()

##############################################################################
#Scatter Plot Chart
##############################################################################
sns.boxplot(x=cleanedData['room_type'], y= cleanedData['price'])
plt.title("Relationship between Price and Room Type")
plt.xlabel("Room Type")
plt.ylabel("Price")
plt.tight_layout()
plt.savefig("../ModelsandDiagrams/BoxPlotOfPriceVs.RoomType.png")
plt.show()

##############################################################################
#Map Creation
##############################################################################

    ##############################################################################
    #Map Creation (Methods)
    ##############################################################################
        #Neighborhood Overlay

        #No Counts
neighborhoodNoCounts = "../cleanedData/bostonNeighborhoodBoundariesCleaned.geojson"
with open(neighborhoodNoCounts) as f:
    neighborhoodNoCounts_data = json.load(f)

        #EntireHome Counts
neighborhoodEntireHomeCounts = "../finalizedData/bostonNeighborhoodBoundariesEntireHomeCount.geojson"
with open(neighborhoodEntireHomeCounts) as f:
    neighborhoodEntireHomeCounts_data = json.load(f)

neighborhoodPrivateRoomCounts = "../finalizedData/bostonNeighborhoodBoundariesPrivateRoomCount.geojson"
with open(neighborhoodPrivateRoomCounts) as f:
    neighborhoodPrivateRoomCounts_data = json.load(f)

neighborhoodSharedRoomCounts = '../finalizedData/bostonNeighborhoodBoundariesSharedRoomCount.geojson'
with open(neighborhoodSharedRoomCounts) as f:
    neighborhoodSharedRoomCounts_data = json.load(f)


        #Counts for Everything
neighborhoodPathCounts = "../finalizedData/bostonNeighborhoodBoundariesEverythingCount.geojson"
with open(neighborhoodPathCounts) as f:
    neighborhoodData_test = json.load(f)

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
    in_geojson = neighborhoodPathCounts,
    layer_name = "Neighborhoods"
)
map1.add_labels(
    data = neighborhoodPathCounts,
    column = "name",
    font_size= "12pt",
    font_color = "Black",
    font_weight = "bold",
    font_family= "Times New Roman"
)

map1.add_title("Airbnb Boston Price Categorization")
map1.add_legend(title="Price Categorization", legend_dict=legend_dictionary)
LayerControl().add_to(map1)
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
    in_geojson = neighborhoodPrivateRoomCounts,
    layer_name = "Neighborhoods"
)
map2.add_labels(
    data = neighborhoodPrivateRoomCounts,
    column = "name",
    font_size= "12pt",
    font_color = "Black",
    font_weight = "bold",
    font_family="Times New Roman"

)


map2.add_title("Private Room Price Categorization")
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
    in_geojson = neighborhoodEntireHomeCounts,
    layer_name = "Neighborhoods"
)
map3.add_labels(
    data = neighborhoodEntireHomeCounts,
    column = "name",
    font_size= "12pt",
    font_color = "Black",
    font_weight = "bold",
    font_family="Times New Roman"

)

map3.add_title("Entire Home Price Categorization")
map3.add_legend(title="Price Categorization", legend_dict=legend_dictionary)
map3.save("../ModelsandDiagrams/mapOfDataCategoryDistribution(EntireHomeOrApt).html")
########################################################################################
#Fourth Map (Shared Rooms)
########################################################################################
map4 = leafmap.Map(location= [centerlatitude, centerlongitude], zoom_start= 10)

for listings, row in finalizedData.iterrows():
    if(row['room_type'] == "Shared room"):
        folium.CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=5,
            color=colorization(row['price_category']),
            fill=True,
            fill_opacity=0.7,
            opacity=1
        ).add_to(map4)



map4.add_geojson(
    in_geojson = neighborhoodSharedRoomCounts,
    layer_name = "Neighborhoods"
)
map4.add_labels(
    data = neighborhoodSharedRoomCounts,
    column = "name",
    font_size= "12pt",
    font_color = "Black",
    font_weight = "bold",
    font_family="Times New Roman"

)

map4.add_title("Shared Room Price Categorization")
map4.add_legend(title="Price Categorization", legend_dict=legend_dictionary)
map4.save("../ModelsandDiagrams/mapOfDataCategoryDistribution(SharedRoom).html")

########################################################################################
#Master Map (All the data but with layers?)
########################################################################################
map5 = leafmap.Map(center = [centerlatitude, centerlongitude], zoom_start= 10)

#featureGroups
featureGroupEntireHomeAptBudget = folium.FeatureGroup(name="Entire Home or Apartment - Budget")
featureGroupEntireHomeAptAverage = folium.FeatureGroup(name="Entire Home or Apartment - Average")
featureGroupEntireHomeAptExpensive = folium.FeatureGroup(name="Entire Home or Apartment - Expensive")

featureGroupPrivateRoomBudget = folium.FeatureGroup(name="Private Room - Budget")
featureGroupPrivateRoomAverage = folium.FeatureGroup(name="Private Room - Average")
featureGroupPrivateRoomExpensive = folium.FeatureGroup(name="Private Room - Expensive")

featureGroupSharedRoomBudget = folium.FeatureGroup(name="Shared Room - Budget")
featureGroupSharedRoomAverage = folium.FeatureGroup(name="Shared Room - Average")
featureGroupSharedRoomExpensive = folium.FeatureGroup(name="Shared Room - Expensive")

for listing, row in finalizedData.iterrows():
    priceCategory = row['price_category']
    roomType = row['room_type']

    circleMarker = folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color=colorization(row['price_category']),
        fill=True,
        fill_opacity=0.7,
        opacity=1
    )

    if(roomType == "Entire home/apt" and priceCategory == "Budget"):
        circleMarker.add_to(featureGroupEntireHomeAptBudget)
    elif(roomType == "Entire home/apt" and priceCategory == "Average"):
        circleMarker.add_to(featureGroupEntireHomeAptAverage)
    elif(roomType == "Entire home/apt" and priceCategory == "Expensive"):
        circleMarker.add_to(featureGroupEntireHomeAptExpensive)

    elif(roomType == "Private room" and priceCategory == "Budget"):
        circleMarker.add_to(featureGroupPrivateRoomBudget)
    elif (roomType == "Private room" and priceCategory == "Average"):
        circleMarker.add_to(featureGroupPrivateRoomAverage)
    elif (roomType == "Private room" and priceCategory == "Expensive"):
        circleMarker.add_to(featureGroupPrivateRoomExpensive)

    elif (roomType == "Shared room" and priceCategory == "Budget"):
        circleMarker.add_to(featureGroupSharedRoomBudget)
    elif (roomType == "Shared room" and priceCategory == "Average"):
        circleMarker.add_to(featureGroupSharedRoomAverage)
    elif (roomType == "Shared room" and priceCategory == "Expensive"):
        circleMarker.add_to(featureGroupSharedRoomExpensive)

map5.add_child(featureGroupEntireHomeAptBudget)
map5.add_child(featureGroupEntireHomeAptAverage)
map5.add_child(featureGroupEntireHomeAptExpensive)
map5.add_child(featureGroupPrivateRoomBudget)
map5.add_child(featureGroupPrivateRoomAverage)
map5.add_child(featureGroupPrivateRoomExpensive)
map5.add_child(featureGroupSharedRoomBudget)
map5.add_child(featureGroupSharedRoomAverage)
map5.add_child(featureGroupSharedRoomExpensive)



map5.add_geojson(
    in_geojson = neighborhoodNoCounts,
    layer_name = "Neighborhoods"
)

map5.add_labels(
    data = neighborhoodNoCounts,
    column = "name",
    font_size= "12pt",
    font_color = "Black",
    font_weight = "bold",
    font_family="Times New Roman"

)

map5.add_layer_control()
map5.add_title("Master Map Price Categorization")
map5.add_legend(title="Price Categorization", legend_dict=legend_dictionary)
map5.save("../ModelsandDiagrams/mapOfDataCategoryDistribution(MasterMap).html")

