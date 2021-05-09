# Question 1:

I first downloaded the data in google sheets as a csv, then I renamed it to `data.csv`.

I ran the following python script

```python
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
```

and the result is as follows:

```
order amount mean   : 3145.128
order amount std    : 41282.539348788036
order amount median : 284.0
total items  mean   : 8.7872
total items  std    : 116.32031980492447
total items  median : 2.0
```

I realized that the mean of total items is close to the median, but the std is very high.
This made me think that there are outliers in terms of total items bought. I checked the
specific values using the following:

```python
print(data[total_items > 8])
```

and the result is as follows:

```
      order_id  shop_id  user_id  order_amount  total_items payment_method          created_at
15          16       42      607        704000         2000    credit_card  2017-03-07 4:00:00
60          61       42      607        704000         2000    credit_card  2017-03-04 4:00:00
520        521       42      607        704000         2000    credit_card  2017-03-02 4:00:00
1104      1105       42      607        704000         2000    credit_card  2017-03-24 4:00:00
1362      1363       42      607        704000         2000    credit_card  2017-03-15 4:00:00
1436      1437       42      607        704000         2000    credit_card  2017-03-11 4:00:00
1562      1563       42      607        704000         2000    credit_card  2017-03-19 4:00:00
1602      1603       42      607        704000         2000    credit_card  2017-03-17 4:00:00
2153      2154       42      607        704000         2000    credit_card  2017-03-12 4:00:00
2297      2298       42      607        704000         2000    credit_card  2017-03-07 4:00:00
2835      2836       42      607        704000         2000    credit_card  2017-03-28 4:00:00
2969      2970       42      607        704000         2000    credit_card  2017-03-28 4:00:00
3332      3333       42      607        704000         2000    credit_card  2017-03-24 4:00:00
4056      4057       42      607        704000         2000    credit_card  2017-03-28 4:00:00
4646      4647       42      607        704000         2000    credit_card  2017-03-02 4:00:00
4868      4869       42      607        704000         2000    credit_card  2017-03-22 4:00:00
4882      4883       42      607        704000         2000    credit_card  2017-03-25 4:00:00
```

I realized that the user_id is the same for every order that exceeds 8 items. I then checked
the orders that specific user made:

```python
print(data[data['user_id'] == 607])
```

And the output is exactly the same as the previous script.

The program for the mean, std, and median after removing orders from that user is as follows:

```python
order_amount = data[data['user_id'] != 607]['order_amount']
print(f'order amount mean   : {order_amount.mean()}')
print(f'order amount std    : {order_amount.std()}')
print(f'order amount median : {order_amount.median()}')
```

And the result is as follows:

```
order amount mean   : 754.0919125025085
order amount std    : 5314.092293103258
order amount median : 284.0
```

a) What could be going wrong with the calculation is that there is one user that orders
significantly more items than other users, but the order amount for him is counted in
the mean. A solution is to remove the outlier, which is to remove all orders that user 607
made, before analyzing the data.

b) There are two metrics I would report for this dataset, since both of them contributes
to an overall understanding of the data. One is the AOV after removing the outliers, and
the other is the median value after removing the outliers. However, since the question
intends to perform analysis on the AOV, I would report the AOV after removing the outliers.

c) The AOV after removing the outliers is 754.09

# Question 2:

a) I first get the shipper id that corresponds to Speedy Express,
then I count the number of orders that has that shipper id.

```sql
SELECT COUNT(*)
FROM Orders
WHERE ShipperID = (
	SELECT ShipperID
	FROM Shippers
	WHERE ShipperName = "Speedy Express"
);
```

54 orders were shipped by Speedy Express in total

b) I first get a table of employee id and the number of orders they
have done. Then I find the maximum row within that table. Then
I select the employee id from that row. Then I select the LastName
field from the Employees table that matches the EmployeeID.

```sql
SELECT LastName
FROM Employees
WHERE EmployeeID IN (
	SELECT EmployeeID
    FROM (
    	SELECT EmployeeID, MAX(CNT)
        FROM (
        	SELECT EmployeeID, COUNT(*) AS CNT
            FROM Orders
            GROUP BY EmployeeID
        )
    )
);
```

The last name of the employee with the most orders is Peacock

c) I first get the CustomerIDs that correspond to the customers in Germany.
Then I get all the orders that originated from those customers by matching the
customer id. Then I create a new table from the orders that matches the OrderID.
The new table consists of ProductID and the sum of their quantities. Then I
find the maximum row in that table. Then I find the product id from that row.
Then I get the product name from the product id that is found.

```sql
SELECT ProductName
FROM Products
WHERE ProductID IN (
	SELECT ProductID
	FROM (
		SELECT ProductID, MAX(QUANT)
		FROM (
			SELECT ProductID, SUM(Quantity) AS QUANT
			FROM OrderDetails
			WHERE OrderID IN (
				SELECT OrderID
				FROM Orders
				WHERE CustomerID IN (
					SELECT CustomerID
					FROM Customers
					WHERE Country = "Germany"
				)
			)
			GROUP BY ProductID
		)
	)
);
```

Boston Crab Meat was ordered the most by customers in Germany
