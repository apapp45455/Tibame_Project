import csv

def CreateCSV(data_list: list, file_path: str) -> csv:
    """將list轉換成csv檔，欄位分別為日期與數量"""
    sales_dates = []
    for date in data_list:
        sales_dates.append((date[0].strftime("%Y/%m/%d")))

    sales_quantity = []
    for quantity in data_list:
        sales_quantity.append((int(quantity[1])))

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for date, quantity in zip(sales_dates, sales_quantity):
            writer.writerow([date, quantity])
    
    return f"File has been saved to {file_path}"