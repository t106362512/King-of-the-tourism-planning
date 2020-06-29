[
    {
        "$group": {
            "_id": "$device_id",
            "gateway_id": {"$last":"$gateway_id"},
                "data": {"$last": '$data'},
                "date": {"$last": '$Observations'},
        }
    },
    {
        "$project": {
            "Location": 1,
            "ObservatoryName": 1,
            "description": 1,
            "name": 1,
            "station": 1,
            "Observations": {
                "$filter": {
                    "input": "$Observations",
                    "as": "observation",
                    "cond": { 
                        # "$eq": [ "$$observation.phenomenonTime", "1593316015000" ] 
                        "$sort:": {"$$observation.phenomenonTime": -1}
                    }
                }
            }
        } 
    } 
] 

station = "sta"
loc_for_mongo = "bnbb"
[
    {
        "$match": {
            "station" : station,
            "Location": loc_for_mongo
        } 
    },
    {
        "$project": {
            '_id': False,
            "Location": 1,
            "ObservatoryName": 1,
            "description": 1,
            "name": 1,
            "station": 1,
            "Observations": {
                "$filter": {
                    "input": "$Observations",
                    "cond": { 
                        "$eq": [
                            {
                                "$max": "$Observations.phenomenonTime"
                            },
                            "$$this.phenomenonTime"
                        ]
                    }
                },
                "$map": {
                    "input": "$Observations",
                    "in": {
                        "phenomenonTime": {
                            "$dateToString":{"format":"%Y%m%dT%H%M", "date":"$$this.phenomenonTime"}
                        }
                    }
                }
            }
        } 
    }
] 