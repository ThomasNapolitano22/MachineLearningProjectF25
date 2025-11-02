import pandas as pd
import json

finalizedData = pd.read_csv('../finalizedData/FinalizedData.csv')
countInNeighbourhood = (
    finalizedData.groupby(['neighbourhood_cleansed', 'price_category']).size().unstack(fill_value=0).reindex(columns = ["Budget", "Average", "Expensive"], fill_value=0)
)

countInNeighbourhood = countInNeighbourhood.rename(index={"Longwood Medical Area" : "Longwood"})
print(countInNeighbourhood)

countInNeighbourhood.to_csv("../finalizedData/categoryCountsPerNeighbourhood.csv")

neighborhoodData = json.load(open("../finalizedData/boston_neighborhood_boundaries.geojson"))

neighborhoodDataCleaned = neighborhoodData
for feature in neighborhoodDataCleaned.get('features'):
    name = feature.get('properties').get('name')
    if name in countInNeighbourhood.index:
        row = countInNeighbourhood.loc[name]
        feature["properties"] = {
            "name": name,
            "Budget": int(row["Budget"]),
            "Average": int(row["Average"]),
            "Expensive": int(row["Expensive"]),
        }


with open("../finalizedData/boston_neighborhood_boundaries.geojson", 'w') as file:
    json.dump(neighborhoodDataCleaned, file)