# BS - Test

## Questions about the python code.

1 - In order to improve the get orders from backend.py script, we want to put it under version control (e.g., GitHub). Therefore, we need to remove the credentials from the code while still making them available when the script runs.

• What methods can you propose to achieve this? Provide at least two solutions, outlining the advantages and disadvantages of each.

> I see that we can have 2 alternatives here:
>
>a - We can use a parameter store / vault to save the credentials
>Example: Use the Azure Key Vault / AWS Systems Manager Parameter Store
>The good: is that it will be completely isolated from the code, so no problem to just call the variables into the .py file and upload it to the git that we are using, also increasing the security of the company.
>The ugly: Well, you need to do more configurations, so creating a new key vault, configure the variables, give the permissions and call the vault on your code.
>
>b- We can use env variables
>Example: We can use the os.environ.get('DATABASE_KEY') for example or the decouple import config (its the same, but more organized)
>The good: Really easy, you just need to add the environment variables into the machines and devolpers can have a .env file in their PCS
>The ugly: This is not a good idea if you are using terraform, since you will expose the password the same way, and there will be the need of a copy with all the access for each developer.
>
>Worth to mention:
>We also could use a Managed Identity, this way we just connect to the database creating roles into our database/machines, but i did not added it because i think that not every database that you are going to use will have this resource available.


2 - We want to schedule this script to run periodically in an automated manner.

• How would you modify the script to easily verify successful execution?

>I think we have 2 ways to manage it
>
>a - Adding some logs, saying that that piece of the code is working perfectly - this way we can trace what is going well when where it stopped
>b - Configuring some sys.exit(0) codes. So if you receive the 0 for example, it can means "success".

• How would you change the script to simplify diagnosing any failures?

>For me the best way would be creting try-catchs into the pieces that can run into problems, as the connection with the database, reaching the API and its response and doing the commit. 
>I would also add a sys.exit(1) for example, saying that the output of the code was an error.

• Which methods or tools can be used to schedule such jobs? Provide at least two options, including their advantages and disadvantages.

>a - I am a big fan of airflow, so this would be my first option.
>
>The good: It solves 2 of the problems that we mentioned here - Triggering the code and have a parameter store / Connection store that we can use - Also its really well mantained by the comunity and companies like Astronomer.
>The ugly: Its a new system to monitorize and it can be complex to create some dags, depending of what you want. Scaling is easy, but maybe if can not be the optimal cost.
>
>b - Also, as you are into the Azure environment, you could use the Azure Functions with CRON.
>
>The good: Serverless and auto scalable. Also really easy to connect with any other tool inside the Azure environment.
>The bad: bad for big applications, it creates a lock in situation into the cloud that you are using and you really depends on the azure plan that you have.


3 - We will soon need to write another script to access the backend API and generate a PDF report. Should we copy the existing script and modify it, or are there better alternatives? What other approaches could we take?

>Well, i would try to decouple the maximum that i can.
>If the backend api its a commom used connection, we could create a class for it, and you just use its methods into any other class/scrips that you need.
>Creating just one big file, just makes it harder to debug, conflicts on git and creates tons of responsability to the same code.
>If you take a look in the code, we could easly decouple the database and API connection.
>Also we need to have a configuration file, because imagine changing the same URL across different files, instead of just one.
>Another alternative is to get all the necessary data from the API, save into a datalake, and read the data from the datalake to create the report, but i would still do the first option first.

4 - We aim to adopt a development approach based on continuous integration. 

• How would you improve the script to make it suitable for a continuous
integration environment, ensuring it runs on developers’ machines,
staging environments, production environments, and the CI system?

>I would do a containerization - put everything in containers. Its the best way to isolate everything and guarantee that the same thing is going to run everywhere. 
>This way we could run the code into the developer machines, run the tests, lints, code coverage or whatever needed, and make it available to create a image to run into the container orchestrator.

• What building blocks and tools would you include in such an envi-
ronment?

>Git
>Docker - to create the containers / Images
>Gitlab CI/Azure DevOps
>Pytest for the tests
>Great expectations - if we need to test the data
>If necessary - SonarQube to check the code files.
>Terraform
>Kubernetes - to run the containers
>Prometheus/Granafa or Elasticsearch/Kibana - for log checking.



## Code exercise - Financial Data Conversion

how to run:

clone the repo 

and add your fixer.io KEY into the **.env** file.

<code>docker compose up</code>

After the compose is up, you are free to try the 2 functionalitis

The command to fecht and store the data from the API into a SQLite database

<code>docker run --rm --env-file .env -v ./data:/app/data bs_test-exchange_rate_app python /app/scripts/main.py --fetch_and_store --base_currency EUR --start_date 2023-01-01 --end_date 2023-01-02</code>

And the one if you just want to see the average

<code>docker run --rm --env-file .env -v ./data:/app/data bs_test-exchange_rate_app python /app/scripts/main.py --print_avg --currency USD --start_date 2023-01-01 --end_date 2023-01-02</code>

When you are done, just use the 

<code>docker compose down</code>

If you want to delete everything that is docker from your machine :

<code>docker system prune -a --volumes</code>


What could be improved here:

1. Connection pool;

2. fixed values to to a configuration file (like the default value of days);

3. Better configuration and naming for the API calls.


## SQL Exercises:


1 - Join the tables to list order details: Write a query to join the ‘orders‘ and ‘order items‘ tables on ‘customer id‘ and ‘timestamp‘ to list down all the order details such as customer ID, timestamp, purchase revenue, number of items, purchase price, and item status.

```
SELECT 
	distinct
    o.customer_id, 
    o.timestamp, 
    o.purchase_revenue, 
    oi.number_items, 
    oi.purchase_price, 
    oi.item_status
FROM orders o
JOIN order_items oi 
    ON o.customer_id = oi.customer_id 
    AND o.timestamp = oi.timestamp;
```

2 - Calculate the total revenue and total items sold per customer: Write a query to calculate the total revenue and the total number of items sold for each customer. Sort the results by total revenue in descending order.

```
SELECT oi.customer_id,
       SUM(oi.number_items) AS total_items_sold,
       SUM(o.purchase_revenue) AS total_revenue
FROM orders o
JOIN (select distinct customer_id, timestamp, number_items, purchase_price,item_status from order_items)
oi ON oi.customer_id = o.customer_id AND oi.timestamp = o.timestamp
WHERE oi.item_status = 'sold'
GROUP BY oi.customer_id
```

3 - Show the running sales by day: Write a query which shows the total sales, returns and sales after returns by day. We also want to have a running sum of all three values giving the total sales, returns and sales after returns for all time up to this day.

```
 WITH daily_summary AS (
    SELECT 
        timestamp AS sale_date,
        SUM(purchase_price * qtt_sold) AS total_sales,
        SUM(purchase_price * qtt_returned) AS total_returns,
        SUM(purchase_price * qtt_sold) - SUM(purchase_price * qtt_returned) AS net_sales
    FROM 
        (SELECT distinct
      oi.customer_id,
      oi.timestamp,
      oi.purchase_price,
      SUM(CASE WHEN oi.item_status = 'returned' THEN 1 ELSE 0 END) AS qtt_returned,
      SUM(CASE WHEN oi.item_status = 'sold' THEN 1 ELSE 0 END) AS qtt_sold,
      COUNT(1) AS qtt_products
  FROM 
      order_items oi
  GROUP BY 
      oi.customer_id, oi.timestamp,oi.purchase_price) a
    GROUP BY 
        timestamp
)
SELECT 
    sale_date,
    total_sales,
    total_returns,
    net_sales,
    SUM(total_sales) OVER (ORDER BY sale_date) AS running_total_sales,
    SUM(total_returns) OVER (ORDER BY sale_date) AS running_total_returns,
    SUM(net_sales) OVER (ORDER BY sale_date) AS running_net_sales
FROM 
    daily_summary
ORDER BY 
    sale_date;
```

4 - Improving the Dataset: Given the current structure of the ‘orders‘ and ‘order items‘ tables, suggest improvements to the schema or data organization that could simplify queries and enhance data integrity. Explain the rationale behind your suggestions.

>If we are talking about transactional databases - and its day by day:
>
>The best thing we could do its to normalize the tables into the 3NF, splitting into smaller and only one resposability per table.
>
>I would create a products table, so this way into the order_itens, i dont need to describe the product in the order_itens table, just use its ID. There is other stuff that we could do, like using ENUMS into the column "item_status".
>
>Other thing in the order_itens, i am not sure if we should keep the number_items , since we can make a count of each of them, there is no need to repeat the same data across diferente lines.
>
>with this changes, the need of doing some of the select DISTINCT above would be not necessary anymore, already making the queries faster ,easier joins and just needing to bring the data that i really need.
>
>Also, talking about performance, i would add indexes into the customer_id, product_id and timestamp, since we are basically using them everywhere.
>
>Talking about the last querie, we could also add a materialized view into the "daily_summary" CTE - this way if i need to making a running total and the result already exists, it would be much faster.
>
>If we are talking about a reporting/processing tool, create bigger tables with everything would be the best case scenario, doing denormalization.
