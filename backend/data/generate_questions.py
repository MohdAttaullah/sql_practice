"""Script to generate the full questions.json bank."""
import json, os

Q = []
def q(id,title,diff,tags,stmt,tables,hint,expl,sql,pyspark,cols,rows,order=False):
    Q.append({"id":id,"title":title,"difficulty":diff,"tags":tags,"problem_statement":stmt,"tables_used":tables,"hint":hint,"explanation":expl,"solution_sql":sql,"pyspark_equivalent":pyspark,"expected_output_columns":cols,"expected_row_count":rows,"requires_order":order})

# 1
q(1,"Total Delivered Revenue by Seller","Easy",
  ["aggregations","joins","PySpark SQL"],
  "Calculate the total revenue for each seller considering only delivered orders. Return seller_id, seller name, and total_revenue sorted by revenue descending.",
  ["orders","sellers"],
  "JOIN orders and sellers, filter status='delivered', GROUP BY seller.",
  "Basic JOIN + aggregation + filter pattern.",
  "SELECT s.seller_id, s.name AS seller_name, SUM(o.amount) AS total_revenue FROM orders o JOIN sellers s ON o.seller_id = s.seller_id WHERE o.status = 'delivered' GROUP BY s.seller_id, s.name ORDER BY total_revenue DESC",
  "orders.join(sellers,'seller_id').filter(F.col('status')=='delivered').groupBy('seller_id',sellers['name']).agg(F.sum('amount').alias('total_revenue')).orderBy(F.desc('total_revenue'))",
  ["seller_id","seller_name","total_revenue"],8,True)

# 2
q(2,"Top Product by Region","Medium",
  ["window functions","ranking","joins","PySpark SQL"],
  "Find the top-selling product by total quantity in each seller region (delivered orders only). Return region, product_name, total_qty.",
  ["orders","sellers","products"],
  "Aggregate then use ROW_NUMBER() OVER(PARTITION BY region ORDER BY total_qty DESC).",
  "Top-N per group using window functions.",
  "WITH ps AS (SELECT s.region, p.name AS product_name, SUM(o.quantity) AS total_qty FROM orders o JOIN sellers s ON o.seller_id=s.seller_id JOIN products p ON o.product_id=p.product_id WHERE o.status='delivered' GROUP BY s.region, p.name), rk AS (SELECT *, ROW_NUMBER() OVER(PARTITION BY region ORDER BY total_qty DESC) AS rn FROM ps) SELECT region, product_name, total_qty FROM rk WHERE rn=1 ORDER BY region",
  "w=Window.partitionBy('region').orderBy(F.desc('total_qty'))\ndf=orders.join(sellers,'seller_id').join(products,'product_id').filter(F.col('status')=='delivered').groupBy('region',products['name'].alias('product_name')).agg(F.sum('quantity').alias('total_qty')).withColumn('rn',F.row_number().over(w)).filter(F.col('rn')==1).drop('rn')",
  ["region","product_name","total_qty"],4)

# 3
q(3,"Repeat Customers","Easy",
  ["aggregations","PySpark SQL"],
  "Find customers with more than 2 distinct orders. Return customer_id, name, order_count desc.",
  ["orders","customers"],
  "GROUP BY customer_id, HAVING COUNT(DISTINCT order_id) > 2.",
  "HAVING clause for filtering aggregates.",
  "SELECT c.customer_id, c.name, COUNT(DISTINCT o.order_id) AS order_count FROM orders o JOIN customers c ON o.customer_id=c.customer_id GROUP BY c.customer_id, c.name HAVING COUNT(DISTINCT o.order_id) > 2 ORDER BY order_count DESC",
  "orders.join(customers,'customer_id').groupBy('customer_id','name').agg(F.countDistinct('order_id').alias('order_count')).filter(F.col('order_count')>2).orderBy(F.desc('order_count'))",
  ["customer_id","name","order_count"],14,True)

# 4
q(4,"Customers With No Delivered Orders","Easy",
  ["joins","PySpark SQL"],
  "Find customers who have never had a delivered order. Return customer_id and name.",
  ["customers","orders"],
  "LEFT JOIN with status filter, or NOT EXISTS / LEFT ANTI join.",
  "Anti-join pattern for finding missing matches.",
  "SELECT c.customer_id, c.name FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id AND o.status='delivered' WHERE o.order_id IS NULL ORDER BY c.customer_id",
  "delivered=orders.filter(F.col('status')=='delivered').select('customer_id').distinct()\ndf=customers.join(delivered,'customer_id','left_anti')",
  ["customer_id","name"],0)

# 5
q(5,"Latest Order Per Customer","Medium",
  ["window functions","deduplication","PySpark SQL"],
  "For each customer find their most recent order. Return customer_id, name, order_id, order_date, amount.",
  ["orders","customers"],
  "ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC).",
  "Latest record per key — essential deduplication pattern.",
  "WITH rk AS (SELECT o.*, c.name, ROW_NUMBER() OVER(PARTITION BY o.customer_id ORDER BY o.order_date DESC) AS rn FROM orders o JOIN customers c ON o.customer_id=c.customer_id) SELECT customer_id, name, order_id, order_date, amount FROM rk WHERE rn=1 ORDER BY customer_id",
  "w=Window.partitionBy('customer_id').orderBy(F.desc('order_date'))\ndf=orders.join(customers,'customer_id').withColumn('rn',F.row_number().over(w)).filter(F.col('rn')==1).drop('rn')",
  ["customer_id","name","order_id","order_date","amount"],20)

# 6
q(6,"Duplicate Order Detection","Easy",
  ["deduplication","data quality","PySpark SQL"],
  "Find duplicate order_ids in the orders table. Return order_id and occurrence_count.",
  ["orders"],
  "GROUP BY order_id HAVING COUNT(*) > 1.",
  "Duplicate detection — critical for data quality.",
  "SELECT order_id, COUNT(*) AS occurrence_count FROM orders GROUP BY order_id HAVING COUNT(*)>1",
  "orders.groupBy('order_id').agg(F.count('*').alias('occurrence_count')).filter(F.col('occurrence_count')>1)",
  ["order_id","occurrence_count"],1)

# 7
q(7,"Seller Target vs Actual Sales","Medium",
  ["aggregations","joins","PySpark SQL"],
  "Compare seller target_revenue vs actual delivered revenue. Return seller_id, name, target_revenue, actual_revenue, met_target boolean.",
  ["sellers","orders"],
  "LEFT JOIN sellers to aggregated orders, COALESCE for nulls.",
  "KPI comparison pattern common in reporting.",
  "SELECT s.seller_id, s.name, s.target_revenue, COALESCE(SUM(o.amount),0) AS actual_revenue, CASE WHEN COALESCE(SUM(o.amount),0)>=s.target_revenue THEN true ELSE false END AS met_target FROM sellers s LEFT JOIN orders o ON s.seller_id=o.seller_id AND o.status='delivered' GROUP BY s.seller_id, s.name, s.target_revenue ORDER BY s.seller_id",
  "actual=orders.filter(F.col('status')=='delivered').groupBy('seller_id').agg(F.sum('amount').alias('actual_revenue'))\ndf=sellers.join(actual,'seller_id','left').fillna(0,subset=['actual_revenue']).withColumn('met_target',F.col('actual_revenue')>=F.col('target_revenue'))",
  ["seller_id","name","target_revenue","actual_revenue","met_target"],8,True)

# 8
q(8,"Products With No Sales","Easy",
  ["joins","PySpark SQL"],
  "Find products never ordered. Return product_id and name.",
  ["products","orders"],
  "LEFT JOIN products to orders, WHERE order_id IS NULL.",
  "Anti-join for gap detection.",
  "SELECT p.product_id, p.name FROM products p LEFT JOIN orders o ON p.product_id=o.product_id WHERE o.order_id IS NULL ORDER BY p.product_id",
  "ordered=orders.select('product_id').distinct()\ndf=products.join(ordered,'product_id','left_anti')",
  ["product_id","name"],1)

# 9
q(9,"Daily GMV Trend","Easy",
  ["aggregations","date functions","PySpark SQL"],
  "Calculate daily GMV (total amount all statuses) per order_date, sorted by date.",
  ["orders"],
  "GROUP BY order_date, SUM(amount).",
  "Basic date-level aggregation.",
  "SELECT order_date, SUM(amount) AS daily_gmv FROM orders GROUP BY order_date ORDER BY order_date",
  "orders.groupBy('order_date').agg(F.sum('amount').alias('daily_gmv')).orderBy('order_date')",
  ["order_date","daily_gmv"],39,True)

# 10
q(10,"Running Total by Date","Medium",
  ["window functions","PySpark SQL"],
  "Calculate running total of delivered revenue by date. Return order_date, daily_revenue, running_total.",
  ["orders"],
  "SUM() OVER(ORDER BY order_date ROWS UNBOUNDED PRECEDING).",
  "Cumulative window function pattern.",
  "WITH daily AS (SELECT order_date, SUM(amount) AS daily_revenue FROM orders WHERE status='delivered' GROUP BY order_date) SELECT order_date, daily_revenue, SUM(daily_revenue) OVER(ORDER BY order_date) AS running_total FROM daily ORDER BY order_date",
  "w=Window.orderBy('order_date').rowsBetween(Window.unboundedPreceding,Window.currentRow)\ndaily=orders.filter(F.col('status')=='delivered').groupBy('order_date').agg(F.sum('amount').alias('daily_revenue'))\ndf=daily.withColumn('running_total',F.sum('daily_revenue').over(w))",
  ["order_date","daily_revenue","running_total"],37,True)

# 11
q(11,"Top 3 Customers by Spend Per Region","Hard",
  ["window functions","ranking","joins","PySpark SQL"],
  "Find top 3 customers by total spend in each region (delivered only). Return region, customer_name, total_spend, rank.",
  ["orders","customers"],
  "Aggregate then RANK() OVER(PARTITION BY region ORDER BY total_spend DESC).",
  "Top-N per group with RANK.",
  "WITH cs AS (SELECT c.region, c.name AS customer_name, SUM(o.amount) AS total_spend FROM orders o JOIN customers c ON o.customer_id=c.customer_id WHERE o.status='delivered' GROUP BY c.region, c.name), rk AS (SELECT *, RANK() OVER(PARTITION BY region ORDER BY total_spend DESC) AS rnk FROM cs) SELECT region, customer_name, total_spend, rnk FROM rk WHERE rnk<=3 ORDER BY region, rnk",
  "w=Window.partitionBy('region').orderBy(F.desc('total_spend'))\ndf=orders.filter(F.col('status')=='delivered').join(customers,'customer_id').groupBy('region','name').agg(F.sum('amount').alias('total_spend')).withColumn('rnk',F.rank().over(w)).filter(F.col('rnk')<=3)",
  ["region","customer_name","total_spend","rnk"],12)

# 12
q(12,"Identify Late-Arriving Data","Medium",
  ["date functions","data quality","PySpark SQL"],
  "Find orders where delivery_date is more than 7 days after order_date. Return order_id, order_date, delivery_date, days_to_deliver.",
  ["orders"],
  "Use DATE_DIFF or date subtraction, filter > 7.",
  "Late-arriving data detection for SLA monitoring.",
  "SELECT order_id, order_date, delivery_date, delivery_date - order_date AS days_to_deliver FROM orders WHERE delivery_date IS NOT NULL AND (delivery_date - order_date) > 7 ORDER BY days_to_deliver DESC",
  "df=orders.filter(F.col('delivery_date').isNotNull()).withColumn('days_to_deliver',F.datediff('delivery_date','order_date')).filter(F.col('days_to_deliver')>7)",
  ["order_id","order_date","delivery_date","days_to_deliver"],0)

# 13
q(13,"Changed Records Between Source and Target","Medium",
  ["CDC","data quality","PySpark SQL"],
  "Find transactions where the amount differs between source and target system for the same txn_id. Return txn_id, source_amount, target_amount, difference.",
  ["transactions"],
  "Self-join on txn_id filtering by system.",
  "Change detection — core CDC concept.",
  "SELECT s.txn_id, s.amount AS source_amount, t.amount AS target_amount, t.amount - s.amount AS difference FROM transactions s JOIN transactions t ON s.txn_id = t.txn_id WHERE s.system = 'source' AND t.system = 'target' AND s.amount != t.amount",
  "src=transactions.filter(F.col('system')=='source').select('txn_id',F.col('amount').alias('source_amount'))\ntgt=transactions.filter(F.col('system')=='target').select('txn_id',F.col('amount').alias('target_amount'))\ndf=src.join(tgt,'txn_id').filter(F.col('source_amount')!=F.col('target_amount')).withColumn('difference',F.col('target_amount')-F.col('source_amount'))",
  ["txn_id","source_amount","target_amount","difference"],1)

# 14
q(14,"SCD Type 2 Current Active Rows","Easy",
  ["SCD","PySpark SQL"],
  "Get the current active record for each customer from the SCD table. Return customer_id, name, region, segment.",
  ["scd_customers"],
  "Filter WHERE is_current = true.",
  "SCD Type 2 basic — select current version.",
  "SELECT customer_id, name, region, segment FROM scd_customers WHERE is_current = true ORDER BY customer_id",
  "df=scd_customers.filter(F.col('is_current')==True).select('customer_id','name','region','segment')",
  ["customer_id","name","region","segment"],12,True)

# 15
q(15,"Rank Sellers by Revenue","Easy",
  ["ranking","window functions","PySpark SQL"],
  "Rank all sellers by their total delivered revenue using DENSE_RANK. Return seller_id, name, total_revenue, revenue_rank.",
  ["orders","sellers"],
  "Aggregate then DENSE_RANK() OVER(ORDER BY total_revenue DESC).",
  "Ranking pattern with DENSE_RANK.",
  "SELECT s.seller_id, s.name, SUM(o.amount) AS total_revenue, DENSE_RANK() OVER(ORDER BY SUM(o.amount) DESC) AS revenue_rank FROM sellers s JOIN orders o ON s.seller_id=o.seller_id WHERE o.status='delivered' GROUP BY s.seller_id, s.name ORDER BY revenue_rank",
  "df=orders.filter(F.col('status')=='delivered').join(sellers,'seller_id').groupBy('seller_id','name').agg(F.sum('amount').alias('total_revenue')).withColumn('revenue_rank',F.dense_rank().over(Window.orderBy(F.desc('total_revenue'))))",
  ["seller_id","name","total_revenue","revenue_rank"],8,True)

# 16
q(16,"7-Day Rolling Average Sales","Hard",
  ["window functions","date functions","PySpark SQL"],
  "Calculate 7-day rolling average of daily delivered revenue. Return order_date, daily_revenue, rolling_avg_7d.",
  ["orders"],
  "Use AVG() OVER(ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW).",
  "Rolling window — common in time-series analytics.",
  "WITH daily AS (SELECT order_date, SUM(amount) AS daily_revenue FROM orders WHERE status='delivered' GROUP BY order_date) SELECT order_date, daily_revenue, ROUND(AVG(daily_revenue) OVER(ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_avg_7d FROM daily ORDER BY order_date",
  "w=Window.orderBy('order_date').rowsBetween(-6,Window.currentRow)\ndaily=orders.filter(F.col('status')=='delivered').groupBy('order_date').agg(F.sum('amount').alias('daily_revenue'))\ndf=daily.withColumn('rolling_avg_7d',F.round(F.avg('daily_revenue').over(w),2))",
  ["order_date","daily_revenue","rolling_avg_7d"],37,True)

# 17
q(17,"Null Primary Key Detection","Easy",
  ["data quality","PySpark SQL"],
  "Find rows in orders where order_id, customer_id, or product_id is NULL. Return the full row.",
  ["orders"],
  "WHERE order_id IS NULL OR customer_id IS NULL OR product_id IS NULL.",
  "Data quality check — NULL PKs break downstream.",
  "SELECT * FROM orders WHERE order_id IS NULL OR customer_id IS NULL OR product_id IS NULL",
  "df=orders.filter(F.col('order_id').isNull() | F.col('customer_id').isNull() | F.col('product_id').isNull())",
  ["order_id","customer_id","seller_id","product_id","quantity","amount","status","order_date","delivery_date"],0)

# 18
q(18,"Invalid Status Detection","Easy",
  ["data quality","PySpark SQL"],
  "Find orders with a status NOT in ('delivered','shipped','cancelled','returned'). Return order_id and status.",
  ["orders"],
  "WHERE status NOT IN (...).",
  "Referential integrity / domain validation.",
  "SELECT order_id, status FROM orders WHERE status NOT IN ('delivered','shipped','cancelled','returned')",
  "valid=['delivered','shipped','cancelled','returned']\ndf=orders.filter(~F.col('status').isin(valid)).select('order_id','status')",
  ["order_id","status"],0)

# 19
q(19,"Unmatched Foreign Keys","Medium",
  ["data quality","joins","PySpark SQL"],
  "Find orders referencing a customer_id that doesn't exist in the customers table. Return order_id and customer_id.",
  ["orders","customers"],
  "LEFT JOIN orders to customers, WHERE customers.customer_id IS NULL.",
  "Referential integrity check across tables.",
  "SELECT o.order_id, o.customer_id FROM orders o LEFT JOIN customers c ON o.customer_id=c.customer_id WHERE c.customer_id IS NULL",
  "df=orders.join(customers,'customer_id','left_anti').select('order_id','customer_id')",
  ["order_id","customer_id"],0)

# 20
q(20,"Reconcile Transaction Totals","Medium",
  ["data quality","aggregations","PySpark SQL"],
  "For each account_id, compare total amounts between source and target systems. Return account_id, source_total, target_total, difference. Only show mismatched accounts.",
  ["transactions"],
  "Aggregate by account_id and system, then pivot/join.",
  "Reconciliation check between two systems.",
  "WITH src AS (SELECT account_id, SUM(amount) AS source_total FROM transactions WHERE system='source' GROUP BY account_id), tgt AS (SELECT account_id, SUM(amount) AS target_total FROM transactions WHERE system='target' GROUP BY account_id) SELECT COALESCE(s.account_id, t.account_id) AS account_id, COALESCE(s.source_total,0) AS source_total, COALESCE(t.target_total,0) AS target_total, COALESCE(t.target_total,0) - COALESCE(s.source_total,0) AS difference FROM src s FULL OUTER JOIN tgt t ON s.account_id=t.account_id WHERE COALESCE(s.source_total,0) != COALESCE(t.target_total,0) ORDER BY account_id",
  "src=transactions.filter(F.col('system')=='source').groupBy('account_id').agg(F.sum('amount').alias('source_total'))\ntgt=transactions.filter(F.col('system')=='target').groupBy('account_id').agg(F.sum('amount').alias('target_total'))\ndf=src.join(tgt,'account_id','full').fillna(0).withColumn('difference',F.col('target_total')-F.col('source_total')).filter(F.col('difference')!=0)",
  ["account_id","source_total","target_total","difference"],3)

# 21-30
q(21,"Employee Salary Above Department Average","Medium",
  ["window functions","aggregations","PySpark SQL"],
  "Find employees earning above their department average. Return employee name, department_id, salary, dept_avg_salary.",
  ["employees"],
  "Use AVG() OVER(PARTITION BY department_id) and filter.",
  "Window function for comparative analysis.",
  "SELECT name, department_id, salary, ROUND(AVG(salary) OVER(PARTITION BY department_id), 2) AS dept_avg_salary FROM employees WHERE salary > (SELECT AVG(e2.salary) FROM employees e2 WHERE e2.department_id = employees.department_id) ORDER BY department_id, salary DESC",
  "w=Window.partitionBy('department_id')\ndf=employees.withColumn('dept_avg',F.avg('salary').over(w)).filter(F.col('salary')>F.col('dept_avg'))",
  ["name","department_id","salary","dept_avg_salary"],7)

q(22,"Month-over-Month Revenue Growth","Hard",
  ["window functions","date functions","PySpark SQL"],
  "Calculate month-over-month revenue growth for delivered orders. Return month, monthly_revenue, prev_month_revenue, growth_pct.",
  ["orders"],
  "Extract month, aggregate, then use LAG().",
  "MoM growth — core business metric with LAG window function.",
  "WITH monthly AS (SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS monthly_revenue FROM orders WHERE status='delivered' GROUP BY DATE_TRUNC('month', order_date)) SELECT month, monthly_revenue, LAG(monthly_revenue) OVER(ORDER BY month) AS prev_month_revenue, ROUND(100.0*(monthly_revenue - LAG(monthly_revenue) OVER(ORDER BY month)) / LAG(monthly_revenue) OVER(ORDER BY month), 2) AS growth_pct FROM monthly ORDER BY month",
  "monthly=orders.filter(F.col('status')=='delivered').withColumn('month',F.date_trunc('month','order_date')).groupBy('month').agg(F.sum('amount').alias('monthly_revenue'))\nw=Window.orderBy('month')\ndf=monthly.withColumn('prev_month_revenue',F.lag('monthly_revenue').over(w)).withColumn('growth_pct',F.round(100*(F.col('monthly_revenue')-F.col('prev_month_revenue'))/F.col('prev_month_revenue'),2))",
  ["month","monthly_revenue","prev_month_revenue","growth_pct"],3,True)

q(23,"Customer Lifetime Value","Hard",
  ["aggregations","joins","date functions","PySpark SQL"],
  "Compute CLV per customer: total spend, order count, avg order value, first and last order dates (delivered only). Return customer_id, name, total_spend, order_count, avg_order_value, first_order, last_order.",
  ["orders","customers"],
  "Aggregate on customer with multiple aggregate functions.",
  "CLV calculation — multi-metric aggregation.",
  "SELECT c.customer_id, c.name, SUM(o.amount) AS total_spend, COUNT(DISTINCT o.order_id) AS order_count, ROUND(SUM(o.amount)/COUNT(DISTINCT o.order_id),2) AS avg_order_value, MIN(o.order_date) AS first_order, MAX(o.order_date) AS last_order FROM orders o JOIN customers c ON o.customer_id=c.customer_id WHERE o.status='delivered' GROUP BY c.customer_id, c.name ORDER BY total_spend DESC",
  "df=orders.filter(F.col('status')=='delivered').join(customers,'customer_id').groupBy('customer_id','name').agg(F.sum('amount').alias('total_spend'),F.countDistinct('order_id').alias('order_count'),F.round(F.sum('amount')/F.countDistinct('order_id'),2).alias('avg_order_value'),F.min('order_date').alias('first_order'),F.max('order_date').alias('last_order')).orderBy(F.desc('total_spend'))",
  ["customer_id","name","total_spend","order_count","avg_order_value","first_order","last_order"],20,True)

q(24,"Pipeline Failure Rate","Easy",
  ["aggregations","PySpark SQL","ETL"],
  "Calculate the failure rate per pipeline. Return pipeline_name, total_runs, failed_runs, failure_rate_pct.",
  ["pipeline_run_log"],
  "GROUP BY pipeline and use conditional counts.",
  "Pipeline monitoring KPI.",
  "SELECT pipeline_name, COUNT(*) AS total_runs, SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) AS failed_runs, ROUND(100.0*SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END)/COUNT(*), 2) AS failure_rate_pct FROM pipeline_run_log GROUP BY pipeline_name ORDER BY failure_rate_pct DESC",
  "df=pipeline_run_log.groupBy('pipeline_name').agg(F.count('*').alias('total_runs'),F.sum(F.when(F.col('status')=='failed',1).otherwise(0)).alias('failed_runs')).withColumn('failure_rate_pct',F.round(100*F.col('failed_runs')/F.col('total_runs'),2)).orderBy(F.desc('failure_rate_pct'))",
  ["pipeline_name","total_runs","failed_runs","failure_rate_pct"],5,True)

q(25,"Recon Mismatches","Easy",
  ["data quality","PySpark SQL"],
  "Find all source-target reconciliation mismatches. Return recon_date, table_name, source_count, target_count, count_diff.",
  ["source_target_recon"],
  "Filter status='mismatched' and compute diff.",
  "Recon monitoring.",
  "SELECT recon_date, table_name, source_count, target_count, source_count - target_count AS count_diff FROM source_target_recon WHERE status = 'mismatched' ORDER BY recon_date",
  "df=source_target_recon.filter(F.col('status')=='mismatched').withColumn('count_diff',F.col('source_count')-F.col('target_count')).select('recon_date','table_name','source_count','target_count','count_diff')",
  ["recon_date","table_name","source_count","target_count","count_diff"],2,True)

q(26,"SCD2 History for a Customer","Medium",
  ["SCD","PySpark SQL"],
  "Show the full change history for customer_id=6 from the SCD table, ordered by effective_start. Return all columns.",
  ["scd_customers"],
  "Simple filter + ORDER BY.",
  "SCD Type 2 history traversal.",
  "SELECT * FROM scd_customers WHERE customer_id=6 ORDER BY effective_start",
  "df=scd_customers.filter(F.col('customer_id')==6).orderBy('effective_start')",
  ["scd_id","customer_id","name","region","segment","effective_start","effective_end","is_current"],3,True)

q(27,"SCD2 Point-in-Time Lookup","Hard",
  ["SCD","date functions","PySpark SQL"],
  "Find each customer's region as of 2022-06-01 from the SCD table. Return customer_id, name, region.",
  ["scd_customers"],
  "Filter effective_start <= date AND effective_end > date.",
  "Point-in-time query on SCD — important for historical analytics.",
  "SELECT customer_id, name, region FROM scd_customers WHERE effective_start <= '2022-06-01' AND effective_end > '2022-06-01' ORDER BY customer_id",
  "df=scd_customers.filter((F.col('effective_start')<='2022-06-01') & (F.col('effective_end')>'2022-06-01')).select('customer_id','name','region')",
  ["customer_id","name","region"],10,True)

q(28,"Inventory Depletion Rate","Hard",
  ["window functions","date functions","PySpark SQL"],
  "Calculate inventory depletion rate per product across snapshots. Return product_id, snapshot_date, qty_on_hand, prev_qty, depletion.",
  ["inventory_snapshots"],
  "Use LAG() to get previous snapshot and compute difference.",
  "Inventory analytics with window functions.",
  "SELECT product_id, snapshot_date, qty_on_hand, LAG(qty_on_hand) OVER(PARTITION BY product_id ORDER BY snapshot_date) AS prev_qty, LAG(qty_on_hand) OVER(PARTITION BY product_id ORDER BY snapshot_date) - qty_on_hand AS depletion FROM inventory_snapshots ORDER BY product_id, snapshot_date",
  "w=Window.partitionBy('product_id').orderBy('snapshot_date')\ndf=inventory_snapshots.withColumn('prev_qty',F.lag('qty_on_hand').over(w)).withColumn('depletion',F.col('prev_qty')-F.col('qty_on_hand'))",
  ["product_id","snapshot_date","qty_on_hand","prev_qty","depletion"],30,True)

q(29,"Missing Transactions in Target","Medium",
  ["CDC","joins","PySpark SQL"],
  "Find txn_ids present in source but missing in target. Return txn_id, account_id, amount.",
  ["transactions"],
  "Anti-join pattern between source and target subsets.",
  "CDC gap detection between systems.",
  "SELECT s.txn_id, s.account_id, s.amount FROM transactions s LEFT JOIN transactions t ON s.txn_id=t.txn_id AND t.system='target' WHERE s.system='source' AND t.txn_id IS NULL",
  "src=transactions.filter(F.col('system')=='source')\ntgt=transactions.filter(F.col('system')=='target').select('txn_id')\ndf=src.join(tgt,'txn_id','left_anti')",
  ["txn_id","account_id","amount"],1)

q(30,"Extra Records in Target","Medium",
  ["CDC","joins","PySpark SQL"],
  "Find txn_ids present in target but not in source. Return txn_id, account_id, amount.",
  ["transactions"],
  "Same as Q29 but reversed.",
  "Detecting ghost records loaded into target.",
  "SELECT t.txn_id, t.account_id, t.amount FROM transactions t LEFT JOIN transactions s ON t.txn_id=s.txn_id AND s.system='source' WHERE t.system='target' AND s.txn_id IS NULL",
  "src=transactions.filter(F.col('system')=='source').select('txn_id')\ntgt=transactions.filter(F.col('system')=='target')\ndf=tgt.join(src,'txn_id','left_anti')",
  ["txn_id","account_id","amount"],1)

# 31-40
q(31,"Customer Segment Revenue Share","Medium",
  ["aggregations","joins","PySpark SQL"],
  "Calculate each customer segment's share of total delivered revenue. Return segment, segment_revenue, total_revenue, share_pct.",
  ["orders","customers"],
  "Two-level aggregation or window SUM for total.",
  "Revenue mix analysis.",
  "WITH seg AS (SELECT c.segment, SUM(o.amount) AS segment_revenue FROM orders o JOIN customers c ON o.customer_id=c.customer_id WHERE o.status='delivered' GROUP BY c.segment) SELECT segment, segment_revenue, SUM(segment_revenue) OVER() AS total_revenue, ROUND(100.0*segment_revenue/SUM(segment_revenue) OVER(), 2) AS share_pct FROM seg ORDER BY share_pct DESC",
  "seg=orders.filter(F.col('status')=='delivered').join(customers,'customer_id').groupBy('segment').agg(F.sum('amount').alias('segment_revenue'))\ntot=seg.agg(F.sum('segment_revenue')).collect()[0][0]\ndf=seg.withColumn('total_revenue',F.lit(tot)).withColumn('share_pct',F.round(100*F.col('segment_revenue')/F.col('total_revenue'),2))",
  ["segment","segment_revenue","total_revenue","share_pct"],3,True)

q(32,"Order Status Distribution","Easy",
  ["aggregations","PySpark SQL"],
  "Count orders by status. Return status, order_count, pct of total.",
  ["orders"],
  "GROUP BY status with window for total.",
  "Status distribution analysis.",
  "SELECT status, COUNT(*) AS order_count, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(), 2) AS pct FROM orders GROUP BY status ORDER BY order_count DESC",
  "total=orders.count()\ndf=orders.groupBy('status').agg(F.count('*').alias('order_count')).withColumn('pct',F.round(100*F.col('order_count')/F.lit(total),2))",
  ["status","order_count","pct"],4,True)

q(33,"Employee Hierarchy Depth","Hard",
  ["joins","PySpark SQL"],
  "Find each employee and their manager's name. Return employee_id, employee_name, manager_name (NULL if no manager).",
  ["employees"],
  "Self-join on manager_id = employee_id.",
  "Self-join for hierarchical data.",
  "SELECT e.employee_id, e.name AS employee_name, m.name AS manager_name FROM employees e LEFT JOIN employees m ON e.manager_id=m.employee_id ORDER BY e.employee_id",
  "df=employees.alias('e').join(employees.alias('m'),F.col('e.manager_id')==F.col('m.employee_id'),'left').select(F.col('e.employee_id'),F.col('e.name').alias('employee_name'),F.col('m.name').alias('manager_name'))",
  ["employee_id","employee_name","manager_name"],15,True)

q(34,"Category Revenue Ranking","Medium",
  ["aggregations","ranking","joins","PySpark SQL"],
  "Rank product categories by total delivered revenue. Return category, category_revenue, category_rank.",
  ["orders","products"],
  "JOIN, aggregate, RANK().",
  "Category-level business analysis.",
  "SELECT p.category, SUM(o.amount) AS category_revenue, RANK() OVER(ORDER BY SUM(o.amount) DESC) AS category_rank FROM orders o JOIN products p ON o.product_id=p.product_id WHERE o.status='delivered' GROUP BY p.category ORDER BY category_rank",
  "df=orders.filter(F.col('status')=='delivered').join(products,'product_id').groupBy('category').agg(F.sum('amount').alias('category_revenue')).withColumn('category_rank',F.rank().over(Window.orderBy(F.desc('category_revenue'))))",
  ["category","category_revenue","category_rank"],4,True)

q(35,"Pipeline Average Duration","Easy",
  ["aggregations","date functions","ETL","PySpark SQL"],
  "Calculate the average run duration in minutes per pipeline (successful runs only). Return pipeline_name, avg_duration_minutes.",
  ["pipeline_run_log"],
  "Use EXTRACT(EPOCH FROM end_ts - start_ts)/60 or equivalent.",
  "Pipeline performance SLA tracking.",
  "SELECT pipeline_name, ROUND(AVG(EXTRACT(EPOCH FROM (end_ts - start_ts))/60), 2) AS avg_duration_minutes FROM pipeline_run_log WHERE status='success' GROUP BY pipeline_name ORDER BY avg_duration_minutes DESC",
  "df=pipeline_run_log.filter(F.col('status')=='success').withColumn('duration_min',(F.unix_timestamp('end_ts')-F.unix_timestamp('start_ts'))/60).groupBy('pipeline_name').agg(F.round(F.avg('duration_min'),2).alias('avg_duration_minutes'))",
  ["pipeline_name","avg_duration_minutes"],5,True)

q(36,"Customers Active in All 3 Months","Hard",
  ["aggregations","date functions","PySpark SQL"],
  "Find customers who placed at least one order in each of Jan, Feb, and Mar 2024. Return customer_id, name.",
  ["orders","customers"],
  "COUNT(DISTINCT month) = 3 after extracting month.",
  "Retention / cohort analysis.",
  "SELECT c.customer_id, c.name FROM orders o JOIN customers c ON o.customer_id=c.customer_id WHERE o.order_date >= '2024-01-01' AND o.order_date < '2024-04-01' GROUP BY c.customer_id, c.name HAVING COUNT(DISTINCT DATE_TRUNC('month', o.order_date)) = 3 ORDER BY c.customer_id",
  "df=orders.filter((F.col('order_date')>='2024-01-01')&(F.col('order_date')<'2024-04-01')).join(customers,'customer_id').withColumn('month',F.date_trunc('month','order_date')).groupBy('customer_id','name').agg(F.countDistinct('month').alias('months')).filter(F.col('months')==3)",
  ["customer_id","name"],8)

q(37,"Order Amount Percentiles","Hard",
  ["window functions","PySpark SQL"],
  "Calculate the 25th, 50th (median), and 75th percentile of order amounts. Return p25, p50, p75.",
  ["orders"],
  "Use PERCENTILE_CONT or APPROX_QUANTILE.",
  "Percentile calculations for distribution analysis.",
  "SELECT ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount), 2) AS p25, ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount), 2) AS p50, ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount), 2) AS p75 FROM orders",
  "df=orders.select(F.round(F.percentile_approx('amount',0.25),2).alias('p25'),F.round(F.percentile_approx('amount',0.5),2).alias('p50'),F.round(F.percentile_approx('amount',0.75),2).alias('p75'))",
  ["p25","p50","p75"],1)

q(38,"Department Budget Utilization","Medium",
  ["aggregations","joins","PySpark SQL"],
  "Compare total employee salaries to department budget. Return dept name, total_salaries, budget, utilization_pct.",
  ["employees","departments"],
  "JOIN and aggregate, divide salary sum by budget.",
  "Budget vs actual analysis.",
  "SELECT d.name AS dept_name, SUM(e.salary) AS total_salaries, d.budget, ROUND(100.0*SUM(e.salary)/d.budget, 2) AS utilization_pct FROM employees e JOIN departments d ON e.department_id=d.department_id WHERE e.status='active' GROUP BY d.name, d.budget ORDER BY utilization_pct DESC",
  "df=employees.filter(F.col('status')=='active').join(departments,employees['department_id']==departments['department_id']).groupBy(departments['name'].alias('dept_name'),'budget').agg(F.sum('salary').alias('total_salaries')).withColumn('utilization_pct',F.round(100*F.col('total_salaries')/F.col('budget'),2))",
  ["dept_name","total_salaries","budget","utilization_pct"],5,True)

q(39,"User Session Analysis","Hard",
  ["aggregations","date functions","PySpark SQL"],
  "Count events per session and compute session duration in minutes. Return session_id, user_id, event_count, duration_minutes.",
  ["events"],
  "GROUP BY session_id, use MIN/MAX timestamp diff.",
  "Session-level analytics — clickstream analysis.",
  "SELECT session_id, user_id, COUNT(*) AS event_count, ROUND(EXTRACT(EPOCH FROM (MAX(event_timestamp) - MIN(event_timestamp)))/60, 2) AS duration_minutes FROM events GROUP BY session_id, user_id ORDER BY duration_minutes DESC",
  "df=events.groupBy('session_id','user_id').agg(F.count('*').alias('event_count'),F.round((F.unix_timestamp(F.max('event_timestamp'))-F.unix_timestamp(F.min('event_timestamp')))/60,2).alias('duration_minutes'))",
  ["session_id","user_id","event_count","duration_minutes"],8,True)

q(40,"Products Below Reorder Point","Easy",
  ["aggregations","PySpark SQL"],
  "Using the latest inventory snapshot, find products where qty_on_hand < 100. Return product_id, warehouse_id, qty_on_hand.",
  ["inventory_snapshots"],
  "Filter for max snapshot_date then filter qty.",
  "Inventory monitoring alert.",
  "SELECT product_id, warehouse_id, qty_on_hand FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) AND qty_on_hand < 100 ORDER BY qty_on_hand",
  "max_date=inventory_snapshots.agg(F.max('snapshot_date')).collect()[0][0]\ndf=inventory_snapshots.filter((F.col('snapshot_date')==max_date)&(F.col('qty_on_hand')<100))",
  ["product_id","warehouse_id","qty_on_hand"],2,True)

# 41-53
q(41,"Order Delivery SLA","Medium",
  ["date functions","aggregations","PySpark SQL"],
  "Calculate avg delivery time in days per seller for delivered orders. Return seller_id, seller_name, avg_delivery_days.",
  ["orders","sellers"],
  "DATE_DIFF between delivery and order date.",
  "Delivery SLA monitoring.",
  "SELECT s.seller_id, s.name AS seller_name, ROUND(AVG(o.delivery_date - o.order_date), 2) AS avg_delivery_days FROM orders o JOIN sellers s ON o.seller_id=s.seller_id WHERE o.status='delivered' AND o.delivery_date IS NOT NULL GROUP BY s.seller_id, s.name ORDER BY avg_delivery_days",
  "df=orders.filter((F.col('status')=='delivered')&(F.col('delivery_date').isNotNull())).join(sellers,'seller_id').withColumn('days',F.datediff('delivery_date','order_date')).groupBy('seller_id',sellers['name'].alias('seller_name')).agg(F.round(F.avg('days'),2).alias('avg_delivery_days'))",
  ["seller_id","seller_name","avg_delivery_days"],8,True)

q(42,"Cancelled Order Rate by Seller","Medium",
  ["aggregations","joins","PySpark SQL"],
  "Calculate cancellation rate per seller. Return seller_id, name, total_orders, cancelled_orders, cancel_rate_pct.",
  ["orders","sellers"],
  "Conditional aggregation with CASE WHEN.",
  "Seller quality metric.",
  "SELECT s.seller_id, s.name, COUNT(DISTINCT o.order_id) AS total_orders, COUNT(DISTINCT CASE WHEN o.status='cancelled' THEN o.order_id END) AS cancelled_orders, ROUND(100.0*COUNT(DISTINCT CASE WHEN o.status='cancelled' THEN o.order_id END)/COUNT(DISTINCT o.order_id), 2) AS cancel_rate_pct FROM sellers s JOIN orders o ON s.seller_id=o.seller_id GROUP BY s.seller_id, s.name ORDER BY cancel_rate_pct DESC",
  "df=orders.join(sellers,'seller_id').groupBy('seller_id','name').agg(F.countDistinct('order_id').alias('total_orders'),F.countDistinct(F.when(F.col('status')=='cancelled',F.col('order_id'))).alias('cancelled_orders')).withColumn('cancel_rate_pct',F.round(100*F.col('cancelled_orders')/F.col('total_orders'),2))",
  ["seller_id","name","total_orders","cancelled_orders","cancel_rate_pct"],8,True)

q(43,"Deduplicated Orders Table","Easy",
  ["deduplication","PySpark SQL"],
  "Remove exact duplicate rows from orders. Return distinct rows sorted by order_id.",
  ["orders"],
  "SELECT DISTINCT * or ROW_NUMBER for dedup.",
  "Basic deduplication.",
  "SELECT DISTINCT * FROM orders ORDER BY order_id",
  "df=orders.dropDuplicates().orderBy('order_id')",
  ["order_id","customer_id","seller_id","product_id","quantity","amount","status","order_date","delivery_date"],60,True)

q(44,"Event Funnel Analysis","Hard",
  ["aggregations","PySpark SQL"],
  "Count unique users at each funnel stage: page_view > add_to_cart > purchase. Return event_type and user_count.",
  ["events"],
  "Filter for funnel events and COUNT DISTINCT user_id.",
  "Conversion funnel — product analytics.",
  "SELECT event_type, COUNT(DISTINCT user_id) AS user_count FROM events WHERE event_type IN ('page_view','add_to_cart','purchase') GROUP BY event_type ORDER BY CASE event_type WHEN 'page_view' THEN 1 WHEN 'add_to_cart' THEN 2 WHEN 'purchase' THEN 3 END",
  "df=events.filter(F.col('event_type').isin('page_view','add_to_cart','purchase')).groupBy('event_type').agg(F.countDistinct('user_id').alias('user_count'))",
  ["event_type","user_count"],3,True)

q(45,"Inventory vs Sold Quantity","Hard",
  ["joins","aggregations","PySpark SQL","warehousing"],
  "Compare latest inventory on hand vs total quantity sold (delivered). Return product_id, product_name, qty_on_hand, qty_sold, remaining.",
  ["inventory_snapshots","orders","products"],
  "Join latest snapshot with aggregated sales.",
  "Inventory reconciliation.",
  "WITH latest_inv AS (SELECT product_id, SUM(qty_on_hand) AS qty_on_hand FROM inventory_snapshots WHERE snapshot_date=(SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY product_id), sold AS (SELECT product_id, SUM(quantity) AS qty_sold FROM orders WHERE status='delivered' GROUP BY product_id) SELECT p.product_id, p.name AS product_name, COALESCE(i.qty_on_hand,0) AS qty_on_hand, COALESCE(s.qty_sold,0) AS qty_sold, COALESCE(i.qty_on_hand,0)-COALESCE(s.qty_sold,0) AS remaining FROM products p LEFT JOIN latest_inv i ON p.product_id=i.product_id LEFT JOIN sold s ON p.product_id=s.product_id ORDER BY p.product_id",
  "df computed with joins between latest inventory, sales aggregation, and products",
  ["product_id","product_name","qty_on_hand","qty_sold","remaining"],15)

q(46,"SCD Type 1 Simulation","Medium",
  ["SCD","PySpark SQL"],
  "From scd_customers, build a Type 1 view: only the current record per customer, dropping history columns. Return customer_id, name, region, segment.",
  ["scd_customers"],
  "Filter is_current=true, select relevant columns.",
  "SCD1 only keeps latest values, no history.",
  "SELECT customer_id, name, region, segment FROM scd_customers WHERE is_current = true ORDER BY customer_id",
  "df=scd_customers.filter(F.col('is_current')==True).select('customer_id','name','region','segment')",
  ["customer_id","name","region","segment"],12,True)

q(47,"Consecutive Pipeline Failures","Hard",
  ["window functions","ETL","PySpark SQL"],
  "Find pipelines with 2 or more consecutive failures. Return pipeline_name, run_id, status, prev_status.",
  ["pipeline_run_log"],
  "LAG() to get previous status, filter both='failed'.",
  "Alert on repeated failures — ops monitoring.",
  "WITH lagged AS (SELECT pipeline_name, run_id, status, LAG(status) OVER(PARTITION BY pipeline_name ORDER BY start_ts) AS prev_status FROM pipeline_run_log) SELECT pipeline_name, run_id, status, prev_status FROM lagged WHERE status='failed' AND prev_status='failed'",
  "w=Window.partitionBy('pipeline_name').orderBy('start_ts')\ndf=pipeline_run_log.withColumn('prev_status',F.lag('status').over(w)).filter((F.col('status')=='failed')&(F.col('prev_status')=='failed'))",
  ["pipeline_name","run_id","status","prev_status"],0)

q(48,"Revenue by Day of Week","Easy",
  ["aggregations","date functions","PySpark SQL"],
  "Calculate total delivered revenue by day of week. Return day_of_week (name) and revenue.",
  ["orders"],
  "Use DAYNAME or EXTRACT(DOW).",
  "Day-of-week analysis for patterns.",
  "SELECT DAYNAME(order_date) AS day_of_week, SUM(amount) AS revenue FROM orders WHERE status='delivered' GROUP BY DAYNAME(order_date) ORDER BY revenue DESC",
  "df=orders.filter(F.col('status')=='delivered').withColumn('day_of_week',F.date_format('order_date','EEEE')).groupBy('day_of_week').agg(F.sum('amount').alias('revenue'))",
  ["day_of_week","revenue"],7,True)

q(49,"Customer Order Gap Analysis","Hard",
  ["window functions","date functions","PySpark SQL"],
  "For each customer, calculate the days between consecutive orders. Return customer_id, order_date, prev_order_date, gap_days.",
  ["orders"],
  "LAG(order_date) OVER(PARTITION BY customer_id ORDER BY order_date).",
  "Inter-event timing — useful for churn prediction.",
  "SELECT customer_id, order_date, LAG(order_date) OVER(PARTITION BY customer_id ORDER BY order_date) AS prev_order_date, order_date - LAG(order_date) OVER(PARTITION BY customer_id ORDER BY order_date) AS gap_days FROM orders ORDER BY customer_id, order_date",
  "w=Window.partitionBy('customer_id').orderBy('order_date')\ndf=orders.withColumn('prev_order_date',F.lag('order_date').over(w)).withColumn('gap_days',F.datediff('order_date','prev_order_date'))",
  ["customer_id","order_date","prev_order_date","gap_days"],61,True)

q(50,"DENSE_RANK Products by Category Revenue","Medium",
  ["window functions","ranking","joins","PySpark SQL"],
  "Rank products within each category by delivered revenue using DENSE_RANK. Return category, product_name, product_revenue, product_rank.",
  ["orders","products"],
  "Aggregate then DENSE_RANK() OVER(PARTITION BY category).",
  "Intra-category ranking.",
  "SELECT p.category, p.name AS product_name, SUM(o.amount) AS product_revenue, DENSE_RANK() OVER(PARTITION BY p.category ORDER BY SUM(o.amount) DESC) AS product_rank FROM orders o JOIN products p ON o.product_id=p.product_id WHERE o.status='delivered' GROUP BY p.category, p.name ORDER BY p.category, product_rank",
  "w=Window.partitionBy('category').orderBy(F.desc('product_revenue'))\ndf=orders.filter(F.col('status')=='delivered').join(products,'product_id').groupBy('category',products['name'].alias('product_name')).agg(F.sum('amount').alias('product_revenue')).withColumn('product_rank',F.dense_rank().over(w))",
  ["category","product_name","product_revenue","product_rank"],14,True)

q(51,"Multi-Table Join: Full Order Details","Easy",
  ["joins","PySpark SQL"],
  "Create a full order detail view joining orders, customers, sellers, and products. Return order_id, customer_name, seller_name, product_name, amount, status. Show first 20 rows.",
  ["orders","customers","sellers","products"],
  "Four-way JOIN.",
  "Multi-table joins — common in dimensional modeling.",
  "SELECT DISTINCT o.order_id, c.name AS customer_name, s.name AS seller_name, p.name AS product_name, o.amount, o.status FROM orders o JOIN customers c ON o.customer_id=c.customer_id JOIN sellers s ON o.seller_id=s.seller_id JOIN products p ON o.product_id=p.product_id ORDER BY o.order_id LIMIT 20",
  "df=orders.join(customers,'customer_id').join(sellers,'seller_id').join(products,'product_id').select('order_id',customers['name'].alias('customer_name'),sellers['name'].alias('seller_name'),products['name'].alias('product_name'),'amount','status')",
  ["order_id","customer_name","seller_name","product_name","amount","status"],20,True)

q(52,"Year-over-Year Comparison Scaffold","Medium",
  ["date functions","aggregations","PySpark SQL"],
  "Calculate monthly revenue for Q1 2024 (Jan-Mar). Return month_num, month_name, monthly_revenue.",
  ["orders"],
  "Extract month, filter Q1, aggregate.",
  "Monthly aggregation — building block for YoY.",
  "SELECT EXTRACT(MONTH FROM order_date) AS month_num, MONTHNAME(order_date) AS month_name, SUM(amount) AS monthly_revenue FROM orders WHERE status='delivered' AND order_date >= '2024-01-01' AND order_date < '2024-04-01' GROUP BY EXTRACT(MONTH FROM order_date), MONTHNAME(order_date) ORDER BY month_num",
  "df=orders.filter((F.col('status')=='delivered')&(F.col('order_date')>='2024-01-01')&(F.col('order_date')<'2024-04-01')).withColumn('month_num',F.month('order_date')).withColumn('month_name',F.date_format('order_date','MMMM')).groupBy('month_num','month_name').agg(F.sum('amount').alias('monthly_revenue'))",
  ["month_num","month_name","monthly_revenue"],3,True)

q(53,"Cross-Seller Customer Overlap","Hard",
  ["aggregations","joins","PySpark SQL"],
  "Find customers who have purchased from more than one seller. Return customer_id, name, seller_count.",
  ["orders","customers"],
  "COUNT(DISTINCT seller_id) > 1.",
  "Customer behavior analysis across sellers.",
  "SELECT c.customer_id, c.name, COUNT(DISTINCT o.seller_id) AS seller_count FROM orders o JOIN customers c ON o.customer_id=c.customer_id GROUP BY c.customer_id, c.name HAVING COUNT(DISTINCT o.seller_id)>1 ORDER BY seller_count DESC",
  "df=orders.join(customers,'customer_id').groupBy('customer_id','name').agg(F.countDistinct('seller_id').alias('seller_count')).filter(F.col('seller_count')>1)",
  ["customer_id","name","seller_count"],20,True)

# Write final JSON
out_path = os.path.join(os.path.dirname(__file__), "questions.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(Q, f, indent=2, ensure_ascii=False)
print(f"Generated {len(Q)} questions to {out_path}")
