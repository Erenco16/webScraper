import hafeleScraping as hafeleScraping
import xlsxwriter
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    credentials = {
        "username": os.getenv('HAFELE_USERNAME'),
        "password": os.getenv('HAFELE_PASSWORD')
    }

    #asking for user to enter the data they would like the info of.
    print("Choose the data types you would like the scrape: ")
    print("1-) Price\n2-) Stock\n3-) Description\n4-) Photos\nEnter values [1-5]. Enter 0 to end the data list.")
    data_list = list()

    #making sure the user enters the proper values.
    while True:
        data = int(input("Enter data: "))
        if data < 1 or data > 5:
            if data == 0:
                break
            data = int(input("Data should be between [1-5]. Enter again: "))
            continue
        data_list.append(data)

    #asking for user to enter the filename which contains the stock code of the products.
    excel_filename = input("Enter the excel file name that you would like to scrape the data for: ")
    code_list = hafeleScraping.excel_read(excel_filename)

    #asking and checking for username and password.
    while True:
        credentials['username'] = input("Enter username: ")
        credentials['password'] = input("Enter password: ")
        if hafeleScraping.login(credentials) == 0:
            print('Username or password is wrong. Enter credentials again: ')
        else:
            driver = hafeleScraping.login(credentials)
            break


    #creating the excel file
    Workbook = xlsxwriter.Workbook("excel-output-file.xlsx")
    Outsheet = Workbook.add_worksheet()

    #adding a bold format to use to  highlight cells
    bold = Workbook.add_format({'bold': True})

    #creating the headers of the excel file
    Outsheet.write(0,0,"stockCode",bold)
    i=1
    for data in data_list:
        if data==1:
            Outsheet.write(0,i,"price",bold)
            i=i+1
        elif data==2:
            Outsheet.write(0, i, "stock",bold)
            i = i + 1
        elif data==3:
            Outsheet.write(0, i, "description",bold)
            i = i + 1
        elif data==4:
            Outsheet.write(0, i, "photos",bold)
            i = i + 1

    #scraping and extracting the data to an excel file
    k=1
    j=0
    for code in code_list:
        try:
            #creating the soup object of the product page
            soup = hafeleScraping.product_soup_extractor(driver,code)
            Outsheet.write(k,j,code)
            j=j+1
            for data in data_list:
                if data==1:
                    #scraping and writing the price info of the product
                    Outsheet.write(k,j,hafeleScraping.product_price(soup))
                    j=j+1
                elif data==2:
                    # scraping and writing the stock info of the product
                    Outsheet.write(k, j, hafeleScraping.stock_finder(soup))
                    j=j+1
                elif data==3:
                    # scraping and writing the product description info of the product
                    Outsheet.write(k, j,hafeleScraping.table_extractor(soup))
                    j=j+1
                elif data==4:
                    # extracting all the photos of the product and writing it to an excel file one by one.
                    photo_list = hafeleScraping.product_photo_extractor(soup)
                    for photo in photo_list:
                        Outsheet.write(k, j, photo)
                        j=j+1
            print(code,"product done")
        except:
            print(code,"product not done.")
            k=k-1
        j=0
        k=k+1
    Workbook.close()

if __name__ == "__main__":
    main()
