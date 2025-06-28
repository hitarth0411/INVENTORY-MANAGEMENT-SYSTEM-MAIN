# INVENTORY-MANAGEMENT-SYSTEM-MAIN
 Furniture Inventory Management 
System with Billing Feature with PDF 
1. Introduction 
The Inventory Management System is a Python application designed to manage products in 
a store or warehouse efficiently. The system reads inventory data from a CSV dataset 
(sourced from Kaggle), allows searching and updating of inventory, and supports billing 
functionality for purchases. 

2. Tools and Technologies Used
- Programming Language: Python 3.x
- Libraries:
- pandas (for handling datasets)
- canvas (for styling PDF)
- datetime (for timestamps in billing)
- tabulate (for neat display of bills, optional)
- Dataset Source: Kaggle (Sample Furniture Inventory Dataset)
- IDE: VS Code / Jupyter Notebook / PyCharm 

4. Dataset Description 
The dataset used is a CSV file containing inventory records with the following columns:
- Product ID
- Product Name
- Category
- Quantity Available
- Price Per Unit 

5. Key Functionalities
- Load inventory from CSV 
- Display inventory
- Search product by name or ID
- Update inventory after sale
- Generate customer bill in pdf (with product details, total price, timestamp)

6.Conclusion 
This Python-based Inventory Management System is a simple but powerful tool for 
managing stock and automating billing. It can be extended with features like GUI (using 
Tkinter), database integration (SQLite/MySQL), and user authentication.
