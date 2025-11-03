import json
import pandas as pd

finalizedData = pd.read_csv('../finalizedData/FinalizedData.csv')

with open('../finalizedData/boston_neighborhood_boundaries.geojson', 'r') as file:
    bostonNeighborhoodBoundariesCleaned = json.load(file)

    propertiesToRemove = ["OBJECTID","acres","neighborhood_id","sqmiles","Shape_Length","Shape_Area","shape_wkt"]

    for feature in bostonNeighborhoodBoundariesCleaned["features"]:
        for property in propertiesToRemove:
            if property in feature["properties"]:
                del feature["properties"][property]

with open('../finalizedData/bostonNeighborhoodBoundariesCleanedNoCounts.geojson', 'w') as newfile:
    json.dump(bostonNeighborhoodBoundariesCleaned, newfile)

with open('../finalizedData/bostonNeighborhoodBoundariesCleanedNoCounts.geojson', 'r') as file:
    bostonNeighborhoodBoundariesEntireHomeCount = json.load(file)

with open('../finalizedData/bostonNeighborhoodBoundariesCleanedNoCounts.geojson', 'r') as file:
    bostonNeighborhoodBoundariesPrivateRoomCount = json.load(file)

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




with open('../finalizedData/bostonNeighborhoodBoundariesCleaned.geojson', 'w') as newfile:
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
countInNeighbourhoodRooms = (
    finalizedDataRooms.groupby(['neighbourhood_cleansed', 'price_category']).size().unstack(fill_value=0).reindex(columns = ["Budget", "Average", "Expensive"], fill_value=0)
)
countInNeighbourhoodRooms = countInNeighbourhoodRooms.rename(index={"Longwood Medical Area" : "Longwood"})
print(countInNeighbourhoodRooms)

for feature in bostonNeighborhoodBoundariesPrivateRoomCount["features"]:
     name = feature["properties"]["name"]
     if name in countInNeighbourhoodRooms.index:
         row = countInNeighbourhoodRooms.loc[name]
         feature["properties"] = {
             "name": name,
             "Budget": int(row["Budget"]),
             "Average": int(row["Average"]),
             "Expensive": int(row["Expensive"])
         }
with open('../finalizedData/bostonNeighborhoodBoundariesPrivateRoomCount.geojson', 'w') as newfile:
    json.dump(bostonNeighborhoodBoundariesPrivateRoomCount, newfile)
