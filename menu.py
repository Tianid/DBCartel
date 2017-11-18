import psycopg2

import tabels1

conn = psycopg2.connect("dbname='DB' user='LimDenson' host='localhost' password='1234'")
cur=conn.cursor()



def show_BD_tables():
    # cur.execute("""SELECT TABLE_NAME  from information_schema.tables where table_schema='cartel'""")
    # rows = cur.fetchall()
    rows=["type of equipment","labs","equipment","sell point","position","persone","cartel"]
    counter=0
    for row in rows:
        print(" ",counter,"-",row)
        counter=counter+1
    print(" ","9 - exit")


def menu():
    choise=99
    while choise !="9":
        show_BD_tables()
        choise=input("coise the tabel,for exit press - 9\n")
        if choise=="0":
            tabels1.type_of_equipment.menu()
            pass
        elif choise=="1":
            tabels1.labs.menu()
        elif choise=="2":
            tabels1.equipment.menu()
        elif choise=="3":
            tabels1.sale_point.menu()
        elif choise=="4":
            tabels1.position.menu()
        elif choise=="5":
            tabels1.persone.menu()
        elif choise=="6":
            tabels1.cartels.menu()



menu()