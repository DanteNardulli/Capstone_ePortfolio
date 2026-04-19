"""Query-building helpers for the Grazioso Salvare dashboard.

This module isolates rescue filter logic from the Dash callbacks so the
application can be extended and tested more easily.
"""

from __future__ import annotations

from typing import Dict, List

import pandas as pd

FILTER_ALL = "all"
FILTER_WATER = "water"
FILTER_MOUNTAIN = "mountain"
FILTER_DISASTER = "disaster"

VALID_FILTERS = {
    FILTER_ALL,
    FILTER_WATER,
    FILTER_MOUNTAIN,
    FILTER_DISASTER,
}

RESCUE_QUERIES: Dict[str, Dict] = {
    FILTER_WATER: {
        "$and": [
            {"breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]}},
            {"sex_upon_outcome": "Intact Male"},
            {"age_upon_outcome_in_weeks": {"$lte": 104}},
        ]
    },
    FILTER_MOUNTAIN: {
        "$and": [
            {"breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]}},
            {"sex_upon_outcome": "Intact Male"},
            {"age_upon_outcome_in_weeks": {"$lte": 104}},
        ]
    },
    FILTER_DISASTER: {
        "$and": [
            {"breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]}},
            {"sex_upon_outcome": "Intact Male"},
            {"age_upon_outcome_in_weeks": {"$lte": 104}},
        ]
    },
}


def validate_filter(filter_type: str | None) -> str:
    """Return a safe filter value for downstream query generation."""
    if filter_type in VALID_FILTERS:
        return filter_type
    return FILTER_ALL



def build_rescue_query(filter_type: str | None) -> Dict:
    """Create the MongoDB query for the selected rescue category."""
    safe_filter = validate_filter(filter_type)
    return RESCUE_QUERIES.get(safe_filter, {})



def prepare_dataframe(records: List[Dict]) -> pd.DataFrame:
    """Convert MongoDB records into a dashboard-safe DataFrame."""
    dataframe = pd.DataFrame.from_records(records)
    if "_id" in dataframe.columns:
        dataframe = dataframe.drop(columns=["_id"])
    return dataframe
