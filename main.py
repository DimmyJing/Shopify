import pandas as pd


data = pd.read_csv('data.csv')
order_amount = data['order_amount']
total_items = data['total_items']
print(f'order amount mean   : {order_amount.mean()}')
print(f'order amount std    : {order_amount.std()}')
print(f'order amount median : {order_amount.median()}')
print(f'total items  mean   : {total_items.mean()}')
print(f'total items  std    : {total_items.std()}')
print(f'total items  median : {total_items.median()}')

print(data[total_items > 8])
print(data[data['user_id'] == 607])

print('after removing user 607')
order_amount = data[data['user_id'] != 607]['order_amount']
print(f'order amount mean   : {order_amount.mean()}')
print(f'order amount std    : {order_amount.std()}')
print(f'order amount median : {order_amount.median()}')
