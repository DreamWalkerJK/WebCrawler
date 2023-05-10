import pymysql
import os
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
from CustomTool import FileOperation

db = pymysql.connect(
    host='localhost',
    user='python',
    passwd='python'
) 

cursor = db.cursor()

try:
    # 建库
    cursor.execute('drop database if exists BookDB;')
    cursor.execute('create database BookDB;')
    cursor.execute('use BookDB;')

    # 建表
    cursor.execute('drop table if exists Category;')
    cursor.execute('''
        create table Category(
            categoryNo varchar(15) not null,
            categoryName varchar(30) not null,
            categoryHref varchar(200),	
            parent varchar(15)
        )engine=innodb default charset=utf8;''')
    
    cursor.execute('drop table if exists Press;')
    cursor.execute('''
        create table Press(
            pressNo varchar(15) not null,
            pressName varchar(150) not null
        )engine=innodb default charset=utf8;''')
    
    cursor.execute('drop table if exists Book;')
    cursor.execute('''
        create table Book(
        bookNo varchar(20) not null,
        bookName varchar(150) not null,
        bookHref varchar(200),
        pictureHref varchar(200),
        bookPrice decimal(10,2),
        bookPrePrice decimal(10,2),
        author varchar(150),
        pressNo varchar(15),
        categoryNo varchar(15)
    )engine=innodb default charset=utf8;''')

    # 插入数据
    input = ','.join(['%s', ] * 4)
    categoryList = FileOperation.readCSV('./DangDang/Category.csv')
    sql = "insert into Category(categoryName,categoryNo,categoryHref,parent) values(%s)"% input
    cursor.executemany(sql, categoryList)

    input = ','.join(['%s', ] * 2)
    pressList = FileOperation.readCSV('./DangDang/Press.csv')
    sql = "insert into Press(pressNo, pressName) values(%s)"% input
    cursor.executemany(sql, pressList)

    input = ','.join(['%s', ] * 8)
    sql = "insert into Book(bookName,bookNo,bookHref,bookPrice,bookPrePrice,author,pressNo,categoryNo) values(%s)"% input
    bookDir = './DangDang/Books'
    bookFiles = os.listdir(bookDir)
    pressList = FileOperation.readCSV('./DangDang/Press.csv')
    pressDict = {}
    for press in pressList:
        pressDict[press[1]] = press[0]
    for file in bookFiles:
        bookPath = "{0}/{1}".format(bookDir, file)
        bookContentList = FileOperation.readCSV(bookPath)
        for book in bookContentList:
            if len(book[-1]) > 0:
                book[-1] = pressDict[book[-1]]
            book.append(str(file).split('.')[0]) # 新增图书分类列
        cursor.executemany(sql, bookContentList)
    db.commit()
except:
    db.rollback()

db.close()
cursor.close()