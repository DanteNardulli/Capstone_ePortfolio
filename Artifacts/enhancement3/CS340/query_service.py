from __future__ import annotations

from typing import Any

import pandas as pd

# Rescue configuration keeps category rules in one place so the filter logic
# is easier to read, maintain, and extend.
RESCUE_FILTERS: dict[str, dict[str, Any]] = {
    "all": {},
    "water": {
        "breed": {
            "$in": [
                "Labrador Retriever Mix",
                "Chesapeake Bay Retriever",
                "Newfoundland",
            ]
        },
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": {"$lte": 104},
    },
    "mountain": {
        "breed": {
            "$in": [
                "German Shepherd",
                "Alaskan Malamute",
                "Old English Sheepdog",
                "Siberian Husky",
                "Rottweiler",
            ]
        },
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": {"$lte": 104},
    },
    "disaster": {
        "breed": {
            "$in": [
                "Doberman Pinscher",
                "German Shepherd",
                "Golden Retriever",
                "Bloodhound",
                "Rottweiler",
            ]
        },
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": {"$lte": 104},
    },
}

#Return a safe filter value for dashboard requests.
def validate_filter(filter_type: str | None) -> str:
    if filter_type in RESCUE_FILTERS:
        return filter_type
    return "all"

#Build a MongoDB query from the selected rescue category.
def build_rescue_query(filter_type: str | None) -> dict[str, Any]: 
    validated_filter = validate_filter(filter_type)
    query = RESCUE_FILTERS[validated_filter]
    return dict(query)

#Convert database records into a clean DataFrame for the dashboard.
def prepare_dataframe(records: list[dict[str, Any]] | None) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    dataframe = pd.DataFrame.from_records(records)
    dataframe.drop(columns=["_id"], inplace=True, errors="ignore")
    return dataframe

#Retrieve and normalize records for the selected rescue category.
def fetch_filtered_animals(database: Any, filter_type: str | None) -> pd.DataFrame:
    query = build_rescue_query(filter_type)
    records = database.read(query)
    return prepare_dataframe(records)

def build_aggregation_pipeline(filter_type: str | None) -> list[dict[str, Any]]:
    #Aggregation pipeline that filters records by rescue category and summarizes the results by breed.

    query = build_rescue_query(filter_type)

    return [
        {"$match": query},
        {
            "$group": {
                "_id": "$breed",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]
