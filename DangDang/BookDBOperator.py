import pymysql
import os
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
from CustomTool import FileOperation
import traceback

def createDataBaseAndTable():
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
                categoryNo varchar(50) not null,
                categoryName varchar(50) not null,
                categoryHref varchar(200),	
                parent varchar(50)
            )engine=innodb default charset=utf8;''')
        
        cursor.execute('drop table if exists Book;')
        cursor.execute('''
            create table Book(
            bookNo varchar(50) not null,
            bookName varchar(150) not null,
            bookHref varchar(200),
            pictureHref varchar(200),
            bookPrice decimal(10,2),
            bookPrePrice decimal(10,2),
            author varchar(150),
            press varchar(150),
            bookStore varchar(50),
            categoryNo varchar(50)
        )engine=innodb default charset=utf8;''')
        db.commit()
    except Exception:
        print(traceback.format_exc())
        db.rollback()

    db.close()
    cursor.close()

# 插入分类至数据库
def insertDataListToDB(tableName, dataList):
    db = pymysql.connect(
        host='localhost',
        user='python',
        passwd='python',
        database='bookDB'
    ) 

    try:
        cursor = db.cursor()
        match tableName.lower():
            case 'category':
                input = ','.join(['%s', ] * 4)
                sql = "insert into Category(categoryNo,categoryName,categoryHref,parent) values(%s)"% input
            case 'book':
                input = ','.join(['%s', ] * 9)
                sql = "insert into Book(bookNo,bookName,bookHref,bookPrice,bookPrePrice,author,press,bookStore,categoryNo) values(%s)"% input   
        cursor.executemany(sql, dataList)
        db.commit()
    except Exception:
        print(traceback.format_exc())
        db.rollback()

    db.close()
    cursor.close()

# 获取数据列表
def getDataList(tableName):
    if len(tableName) == 0:
        return
    db = pymysql.connect(
        host='localhost',
        user='python',
        passwd='python',
        database='bookDB'
    ) 
    cursor = db.cursor()
    sql = "select * from {0};".format(tableName)
    match tableName.lower():
        case 'category':
            sql = "select categoryNo, categoryName, categoryHref, parent from {0};".format(tableName)
    cursor.execute(sql)
    dataList = cursor.fetchall()
    db.close()
    cursor.close()
    return list(dataList)