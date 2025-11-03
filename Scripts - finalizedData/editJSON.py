import json
import pandas as pd

finalizedData = pd.read_csv('../finalizedData/FinalizedData.csv')

with open('../originalData/boston_neighborhood_boundaries.geojson', 'r') as file:
    bostonNeighborhoodBoundariesCleaned = json.load(file)

    propertiesToRemove = ["OBJECTID","acres","neighborhood_id","sqmiles","Shape_Length","Shape_Area","shape_wkt"]

    for feature in bostonNeighborhoodBoundariesCleaned["features"]:
        for property in propertiesToRemove:
            if property in feature["properties"]:
                del feature["properties"][property]

with open('../cleanedData/bostonNeighborhoodBoundariesCleaned.geojson', 'w') as newfile:
    json.dump(bostonNeighborhoodBoundariesCleaned, newfile)

with open('../cleanedData/bostonNeighborhoodBoundariesCleaned.geojson', 'r') as file:
    bostonNeighborhoodBoundariesEntireHomeCount = json.load(file)

with open('../cleanedData/bostonNeighborhoodBoundariesCleaned.geojson', 'r') as file:
    bostonNeighborhoodBoundariesPrivateRoomCount = json.load(file)

with open('../cleanedData/bostonNeighborhoodBoundariesCleaned.geojson', 'r') as file:
    bostonNeighborhoodBoundariesSharedRoomCount = json.load(file)

countInNeighbourhood = (
    finalizedData.groupby(['neighbourhood_cleansed', 'price_category']).size().unstack(fill_value=0).reindex(columns = ["Budget", "Average", "Expensive"], fill_value=0)
)
countInNeighbourhood = countInNeighbourhood.rename(index={"Longwood Medical Area" : "Longwood"})
print(countInNeighbourhood)



for feature in bostonNeighborhoodBoundariesCleaned["features"]:
     name = feature["properties"]["name"]
     if name in countInNeighbourhood.index:
         row = countInNeighbourhood.loc[name]
         feature["properties"] = {
             "name": name,
             "Budget": int(row["Budget"]),
             "Average": int(row["Average"]),
             "Expensive": int(row["Expensive"])
         }




with open('../finalizedData/bostonNeighborhoodBoundariesEverythingCount.geojson', 'w') as newfile:
    json.dump(bostonNeighborhoodBoundariesCleaned, newfile)

finalizedDataEntireHomes = finalizedData[finalizedData['room_type'] == "Entire home/apt"]
countInNeighbourhoodEntireHomes = (
    finalizedDataEntireHomes.groupby(['neighbourhood_cleansed', 'price_category']).size().unstack(fill_value=0).reindex(columns = ["Budget", "Average", "Expensive"], fill_value=0)
)
countInNeighbourhoodEntireHomes = countInNeighbourhoodEntireHomes.rename(index={"Longwood Medical Area" : "Longwood"})
print(countInNeighbourhoodEntireHomes)

for feature in bostonNeighborhoodBoundariesEntireHomeCount["features"]:
     name = feature["properties"]["name"]
     if name in countInNeighbourhoodEntireHomes.index:
         row = countInNeighbourhoodEntireHomes.loc[name]
         feature["properties"] = {
             "name": name,
             "Budget": int(row["Budget"]),
             "Average": int(row["Average"]),
             "Expensive": int(row["Expensive"])
         }

with open('../finalizedData/bostonNeighborhoodBoundariesEntireHomeCount.geojson', 'w') as newfile:
    json.dump(bostonNeighborhoodBoundariesEntireHomeCount, newfile)

finalizedDataRooms = finalizedData[finalizedData['room_type'] == "Private room"]
countInNeighbourhoodPrivateRooms = (
    finalizedDataRooms.groupby(['neighbourhood_cleansed', 'price_category']).size().unstack(fill_value=0).reindex(columns = ["Budget", "Average", "Expensive"], fill_value=0)
)
countInNeighbourhoodPrivateRooms = countInNeighbourhoodPrivateRooms.rename(index={"Longwood Medical Area" : "Longwood"})
print(countInNeighbourhoodPrivateRooms)

for feature in bostonNeighborhoodBoundariesPrivateRoomCount["features"]:
     name = feature["properties"]["name"]
     if name in countInNeighbourhoodPrivateRooms.index:
         row = countInNeighbourhoodPrivateRooms.loc[name]
         feature["properties"] = {
             "name": name,
             "Budget": int(row["Budget"]),
             "Average": int(row["Average"]),
             "Expensive": int(row["Expensive"])
         }
with open('../finalizedData/bostonNeighborhoodBoundariesPrivateRoomCount.geojson', 'w') as newfile:
    json.dump(bostonNeighborhoodBoundariesPrivateRoomCount, newfile)

finalizedDataSharedRooms = finalizedData[finalizedData['room_type'] == "Shared room"]
countInNeighbourhoodSharedRooms = (
    finalizedDataSharedRooms.groupby(['neighbourhood_cleansed', 'price_category']).size().unstack(fill_value=0).reindex(columns = ["Budget", "Average", "Expensive"], fill_value=0)
)
countInNeighbourhoodSharedRooms = countInNeighbourhoodSharedRooms.rename(index={"Longwood Medical Area" : "Longwood"})
print(countInNeighbourhoodSharedRooms)

for feature in bostonNeighborhoodBoundariesSharedRoomCount["features"]:
     name = feature["properties"]["name"]
     if name in countInNeighbourhoodSharedRooms.index:
         row = countInNeighbourhoodSharedRooms.loc[name]
         feature["properties"] = {
             "name": name,
             "Budget": int(row["Budget"]),
             "Average": int(row["Average"]),
             "Expensive": int(row["Expensive"])
         }

with open('../finalizedData/bostonNeighborhoodBoundariesSharedRoomCount.geojson', 'w') as newfile:
    json.dump(bostonNeighborhoodBoundariesSharedRoomCount, newfile)

