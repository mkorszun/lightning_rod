class Aggregator():
    PIPELINE = [
        {
            "$group": {
                "_id": {
                    "name": "$name",
                    "email": "$email"
                },
                "messages": {
                    "$addToSet": {
                        "msg": "$message",
                        "timestamp": "$timestamp"
                    }
                },
                "to_delete": {
                    "$addToSet": "$_id"
                }
            }
        }
    ]

    collection = None

    def __init__(self, collection):
        self.collection = collection

    def collect(self):
        return list(self.collection.aggregate(self.PIPELINE))
