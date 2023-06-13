import json

customer_id = "5001"

def catch_customer(customer_id):
    with open('recommendation_total.json', 'r') as f:
        datas = json.load(f)
        for data in datas:
            if data['customer_id'] == customer_id:
                return data['recommendations']

# print(catch_customer(customer_id))
