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
