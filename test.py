#  {
#      "customer_first_name": "client3",
#      "customer_last_name": "clientos3",
#      "customer_phone": "994502702564",
#      "customer_email": "client3@gmail.com",
#      "complete": "false",
#      "order_items":[
#          {
#              "quantity": 5,
#              "order": 1,
#              "meal": 2
#          },
#          {
#              "quantity": 5,
#              "order": 1,
#              "meal": 2
#          },
#          {
#              "quantity": 5,
#              "order": 1,
#              "meal": 2
#          }
#      ]
#  }

test_data = {
    'customer_first_name': 'client4',
    'customer_last_name': 'clientos4',
    'customer_phone': '994502702564',
    'customer_email': 'client4@gmail.com',
    'complete': 'false',
    'order_items': [
        {'quantity': 5, 'order': 1, 'meal': 1},
        {'quantity': 5, 'order': 1, 'meal': 2},
        {'quantity': 5, 'order': 1, 'meal': 3}
        ]
    }
meal_id = None
order_item_data = test_data['order_items']
for i in order_item_data:
    meal_id = i['meal']
    print(i)
print("meal_id: ", meal_id)
# print(order_
# item_data)