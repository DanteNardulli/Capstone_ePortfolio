#Service layer for building MongoDB queries and handling filter logic.
#This separates backend query construction from the Dash UI callbacks.


def build_query(filter_type):
    if filter_type == "water":
        return {
            "$and": [
                {"breed": {"$in": [
                    "Labrador Retriever Mix",
                    "Chesapeake Bay Retriever",
                    "Newfoundland"
                ]}},
                {"sex_upon_outcome": "Intact Male"},
                {"age_upon_outcome_in_weeks": {"$lte": 104}}
            ]
        }

    elif filter_type == "mountain":
        return {
            "$and": [
                {"breed": {"$in": [
                    "German Shepherd",
                    "Alaskan Malamute",
                    "Old English Sheepdog",
                    "Siberian Husky",
                    "Rottweiler"
                ]}},
                {"sex_upon_outcome": "Intact Male"},
                {"age_upon_outcome_in_weeks": {"$lte": 104}}
            ]
        }

    elif filter_type == "disaster":
        return {
            "$and": [
                {"breed": {"$in": [
                    "Doberman Pinscher",
                    "German Shepherd",
                    "Golden Retriever",
                    "Bloodhound",
                    "Rottweiler"
                ]}},
                {"sex_upon_outcome": "Intact Male"},
                {"age_upon_outcome_in_weeks": {"$lte": 104}}
            ]
        }

    return {}
    
def validate_filter(filter_type):
    #Validate the selected filter value.
    valid_filters = {"all", "water", "mountain", "disaster"}
    return filter_type if filter_type in valid_filters else "all"