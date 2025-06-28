import pandas as pd
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import random
import re  # For sanitizing file names

def wrap_text(c, text, width, font_name="Helvetica", font_size=10):
    """Wrap text to fit within the specified width (in points)."""
    c.setFont(font_name, font_size)
    lines = []
    line = ""
    for word in text.split():
        if c.stringWidth(line + word, font_name, font_size) < width:
            line += " " + word
        else:
            lines.append(line)
            line = word
    lines.append(line)  # Add the last line
    return lines


def initialize_bill_number_file():
    bill_file = "bill_number.csv"
    if not os.path.exists(bill_file):
        df = pd.DataFrame({'BillID': [1]})
        df.to_csv(bill_file, index=False)
        print(f"Bill Number file '{bill_file}' created with initial Bill ID 1.")
    else:
        print(f"Bill Number file '{bill_file}' already exists.")


def inventory():
    inventory_file = "D:\\IKEA\\Furniture.csv"
    if os.path.exists(inventory_file):
        inventory_df = pd.read_csv(inventory_file)
        print("\n" + "=" * 70 + " Inventory of products in stock " + "=" * 70 + "\n")
        print(inventory_df.to_string(index=False))
    else:
        print(f"Error: {inventory_file} not found!")


def add_data(file_path, new_data):
    try:
        df = pd.read_csv(file_path)
        df2 = pd.DataFrame([new_data])
        df = pd.concat([df, df2], ignore_index=True)
        df.to_csv(file_path, index=False)
        print("Data added successfully.")
    except Exception as e:
        print(f"Error while adding data: {e}")


def update_inventory(file_path, product_id, new_quantity):
    try:
        df = pd.read_csv(file_path)
        if product_id in df['Product_id'].values:
            df.loc[df['Product_id'] == product_id, 'Quantity'] = new_quantity
            df.to_csv(file_path, index=False)
            print("Quantity updated successfully.")
        else:
            print(f"Error: Product ID {product_id} not found!")
    except Exception as e:
        print(f"Error in updating quantity: {e}")


def bill_making():
    inventory_file = "D:\\IKEA\\Furniture.csv"
    bill_file = "bill_number.csv"
    all_bills_file = "all_bills.csv"
    gst_rate = 4.8

    try:
        df3 = pd.read_csv(inventory_file)
        df4 = pd.read_csv(bill_file)
    except FileNotFoundError:
        print("File not found. Make sure all required files exist.")
        return

    final_bill = pd.DataFrame(
        columns=['Bill ID', 'Buyer name', 'Buyer contact', 'ProductID', 'ProductName', 'GST', 'Price', 'Quantity', 'Total'])
    bill_number = df4.loc[0, 'BillID']

    buyer_name = input("Enter buyer name: ")
    buyer_contact = int(input("Enter Buyer contact number: "))

    while True:
        print("\nAvailable Products in inventory:")
        print(df3.to_string(index=False))
        sell_id = int(input("Enter the Product_id to sell: "))
        quantity_sold = int(input("Enter the quantity sold: "))

        if sell_id in df3['Product_id'].values:
            stock = df3.loc[df3['Product_id'] == sell_id, 'Quantity'].values[0]
            if quantity_sold <= stock:
                product_details = df3.loc[df3['Product_id'] == sell_id].iloc[0]
                product_price = product_details['Total Price']
                gst_amount = (product_price * gst_rate) / 100
                total_cost = quantity_sold * (product_price + gst_amount)

                df3.loc[df3['Product_id'] == sell_id, 'Quantity'] -= quantity_sold

                new_sale = {
                    'Bill ID': bill_number,
                    'Buyer name': buyer_name,
                    'Buyer contact': buyer_contact,
                    'ProductID': sell_id,
                    'ProductName': product_details['Furniture Entities'],
                    'GST': gst_amount,
                    'Price': product_price,
                    'Quantity': quantity_sold,
                    'Total': total_cost
                }
                final_bill = pd.concat([final_bill, pd.DataFrame([new_sale])], ignore_index=True)

                print('\n----Current purchase----')
                print(f"Product_id: {sell_id}")
                print(f"Furniture Entities: {product_details['Furniture Entities']}")
                print(f"Quantity: {quantity_sold}")
                print(f"Price per unit: INR {product_price}")
                print(f"GST per unit: INR {gst_amount}")
                print(f"Total cost (including GST): INR {total_cost}")

                purchase = input("Do you want to buy another product? (yes/no): ").lower()
                if purchase != 'yes':
                    break
            else:
                print("Not enough quantity in stock.")
        else:
            print("Product_id not found in inventory.")

    df4.loc[0, 'BillID'] = bill_number + 1
    df4.to_csv(bill_file, index=False)

    total = final_bill['Total'].sum()
    print("\n" + "=" * 29 + " HHJR FURNITURE SHOP " + "=" * 29)
    print("\n" + "=" * 34 + " Final Bill " + "=" * 34)
    print(f"\nBill ID of Final Bill is: {bill_number}")
    print(f"Buyer name: {buyer_name}")
    print(f"Buyer Contact Number: {buyer_contact}")
    print("\n", final_bill.to_string(index=False))
    print(f"\nFinal Total: INR {total}")

    if os.path.exists(all_bills_file):
        all_bills = pd.read_csv(all_bills_file)
        all_bills = pd.concat([all_bills, final_bill], ignore_index=True)
    else:
        all_bills = final_bill

    all_bills.to_csv(all_bills_file, index=False)
    print(f"Bill data appended to '{all_bills_file}' successfully.")

    output_folder = "Bill files"
    safe_buyer_name = re.sub(r'[\\/*?:"<>|]', "_", buyer_name)  # sanitize name
    bill_folder = os.path.join(output_folder, f'Bill_{bill_number}_{safe_buyer_name}')
    os.makedirs(bill_folder, exist_ok=True)
    final_bill.to_csv(os.path.join(bill_folder, f"bill_{bill_number}.csv"), index=False)
    print(f"Final bill saved to '{bill_folder}' successfully.")

    # Define PDF file path here
    pdf_file = os.path.join(bill_folder, f"bill_{bill_number}.pdf")

    # Generate PDF
    custom_width = 900
    custom_height = random.randint(600, 900)
    c = canvas.Canvas(pdf_file, pagesize=(custom_width, custom_height))

    def print_header(c, width, height, bill_number, buyer_name, buyer_contact):
        header_text = "HHJR FURNITURE SHOP"
        c.setFont("Helvetica-Bold", 16)
        header_width = c.stringWidth(header_text, "Helvetica-Bold", 16)
        c.drawString((width - header_width) / 2, height - 50, header_text)

        c.setFont("Helvetica", 12)
        address = "Address: XYZ Street, Some City"
        c.drawString((width - c.stringWidth(address, "Helvetica", 12)) / 2, height - 70, address)
        c.drawString((width - 200) / 2, height - 90, "Phone: +91 123 456 7890")
        c.drawString((width - 250) / 2, height - 110, "Email: contact@hhjrfurniture.com")

        title = f"RECEIPT - Bill ID: {bill_number}"
        c.setFont("Helvetica-Bold", 14)
        c.drawString((width - c.stringWidth(title, "Helvetica-Bold", 14)) / 2, height - 130, title)

        date_text = f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        c.setFont("Helvetica", 12)
        c.drawString(width - 10 - c.stringWidth(date_text, "Helvetica", 12), height - 130, date_text)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, height - 180, f"Buyer: {buyer_name}")
        c.setFont("Helvetica", 12)
        c.drawString(30, height - 200, f"Contact: {buyer_contact}")

    row_height = 20
    y = custom_height - 250
    max_rows = 10

    print_header(c, custom_width, custom_height, bill_number, buyer_name, buyer_contact)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y, "Product ID")
    c.drawString(100, y, "Product Name")
    c.drawString(300, y, "Price")
    c.drawString(400, y, "Quantity")
    c.drawString(500, y, "GST")
    c.drawString(700, y, "Total")
    c.line(30, y - 5, 800, y - 5)
    y -= row_height

    for idx, row in final_bill.iterrows():
        if (idx + 1) % max_rows == 0:
            c.showPage()
            print_header(c, custom_width, custom_height, bill_number, buyer_name, buyer_contact)
            y = custom_height - 250
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y, "Product ID")
            c.drawString(100, y, "Product Name")
            c.drawString(300, y, "Price")
            c.drawString(400, y, "Quantity")
            c.drawString(500, y, "GST")
            c.drawString(700, y, "Total")
            c.line(30, y - 5, 800, y - 5)
            y -= row_height

        c.setFont("Helvetica", 10)
        c.drawString(30, y, str(row['ProductID']))

        wrapped = wrap_text(c, row['ProductName'], 180)
        for line in wrapped:
            c.drawString(100, y, line)
            y -= row_height

        c.drawString(300, y, f"INR {row['Price']}")
        c.drawString(400, y, str(row['Quantity']))
        c.drawString(500, y, f"INR {row['GST']}")
        c.drawString(700, y, f"INR {row['Total']}")
        y -= row_height

    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y - 20, f"Total: INR {total}")

    c.setFont("Helvetica", 10)
    c.drawString(30, y - 40, "Thank you for shopping with us!")
    c.drawString(30, y - 60, "Visit again!")

    c.save()
    print(f"Receipt saved as PDF: {pdf_file}")


# Main function
if __name__ == "__main__":
    initialize_bill_number_file()

    while True:
        print("\nMenu:")
        print("1. View Inventory")
        print("2. Add Product to Inventory")
        print("3. Update Inventory Quantity")
        print("4. Make Bill")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            inventory()
        elif choice == '2':
            new_product = {
                'Product_id': int(input("Enter Product ID: ")),
                'Furniture Entities': input("Enter Product Name: "),
                'Total Price': float(input("Enter Product Price: ")),
                'Quantity': int(input("Enter Product Quantity: "))
            }
            add_data("D:\\IKEA\\Furniture.csv", new_product)
        elif choice == '3':
            product_id = int(input("Enter Product ID to update quantity: "))
            new_quantity = int(input("Enter new quantity: "))
            update_inventory("D:\\IKEA\\Furniture.csv", product_id, new_quantity)
        elif choice == '4':
            bill_making()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")