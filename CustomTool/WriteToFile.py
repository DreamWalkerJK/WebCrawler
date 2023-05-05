# 写入csv保存
import csv 

def writeToCSV(path, header, bookList):
    f = open(path, 'w', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    csv_writer.writerows(bookList)
    f.close()