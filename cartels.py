import psycopg2
conn = psycopg2.connect("dbname='DB' user='LimDenson' host='localhost' password='1234'")
cur=conn.cursor()
from prettytable import PrettyTable
# prt = PrettyTable()

def menu():

    choise=99
    while choise !="9":
        print("______Table: cartels______")
        print(""" 0 - Insert record \n 1 - Delete record \n 2 - Show records \n 3 - Update record \n 4 - Search record \n 5 - Filtr \n 9 - Exit""")
        choise = input()
        # show_table_content()
        if choise=="0":
            val=input("insert cartel name,baron name ,level of danger,income by using - ','  :")
            recording_in_the_end(val)
        elif choise=="1":
            show_table_content()
            val = input("select row to delete: ")
            delete_Record(val)
        elif choise=="2":
            show_table_content()
        elif choise=="3":
            ch1 = input("Type object of update - record of field: ")
            if ch1=="record":
                show_table_content()
                id = input("select name of cartel: ")
                val0 = input("type new name: ")
                val1 = input("type new baron name: ")
                val2 = input("type new level of danger: ")
                val3 = input("type new income: ")
                update_all_record(val0,val1,val2,val3,id)
            elif ch1=="field":
                show_table_content()
                id = input("Select name of cartel: ")
                headers = header_name_back()
                count = 0
                for i in headers:
                    print("     ", count, "-", i, "\n")
                    count = count + 1
                field = input("select field of update: ")
                val = input("type new content of field: ")
                update_one_field(val, headers[int(field)], id)
        elif choise=="4":
            headers=header_name_back();
            count=0
            for i in headers:
                print("     ",count,"-",i,"\n")
                count=count+1
            field=input("select field of search: ")
            val=input("type what are you searching: ")
            search(val,headers[int(field)])
        elif choise=="5":
            ch = input("1 - Filtr by level of danger \n2 - Filtr by income")
            if ch == "1":
                ch1 = input(" 1 - <= \n 2 - >=")
                val = input("Input value ")
                if ch1 == "1":
                    filtr(ch1, ch, val)
                elif ch1 == "2":
                    filtr(ch1, ch, val)
            elif ch == "2":
                ch1 = input(" 1 - <= \n 2 - >=")
                val = input("Input value ")
                if ch1 == "1":
                    filtr(ch1, ch, val)
                elif ch1 == "2":
                    filtr(ch1, ch, val)



def header_name_back():
    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='cartels'",)
    row=cur.fetchall()
    buff=[]
    for i in row:
        buff.append(i[0])
    return buff


def show_table_content():
    cur.execute("""SELECT * from cartel.cartels """)
    rows= cur.fetchall()
    print("_________\n cartel table content:")
    prt = PrettyTable()
    prt.field_names=header_name_back()
    for row in rows:
        buff=[]
        for i in range(len(row)):
            buff.append((str(row[i])).strip())
        prt.add_row(buff)
    print(prt)


def delete_Record(value):
    val=[value]
    cur.execute("DELETE FROM cartel.cartels WHERE name=%s;",(val))
    conn.commit()
    show_table_content()

def recording_in_the_end(value1):
    val = value1.split(",")
    cur.execute("INSERT INTO cartel.cartels (name,drug_barons_name,level_of_danger,income) VALUES (%s,%s,%s,%s)",val )
    conn.commit()
    show_table_content()

def update_all_record(name,baron,level,income,id):
    cur.execute("UPDATE cartel.cartels SET name =%s,drug_barons_name=%s,level_of_danger=%s,income=%s where name=%s",(name,baron,level,income,id))
    conn.commit()
def update_one_field(val,field,id):
    cur.execute(("UPDATE cartel.cartels SET {0}='{1}' WHERE name='{2}'").format(field, val,id))
    conn.commit()



# def search_record_by_name(val):
#     value=[val]
#     cur.execute("SELECT * FROM cartel.cartels WHERE name =%s;",(value))
#     row=cur.fetchone()
#     prt1 = PrettyTable()
#     prt1.field_names = header_name_back()
#     buff = []
#     for i in range(len(row)):
#         buff.append((str(row[i])).strip())
#     prt1.add_row(buff)
#     print(prt1)
#
# def search_record_by_baron_name(val):
#     value = [val]
#     cur.execute(("SELECT * FROM cartel.cartels WHERE name ={0};").format (value))
#     row = cur.fetchone()
#     prt1 = PrettyTable()
#     prt1.field_names = header_name_back()
#     buff = []
#     for i in range(len(row)):
#         buff.append((str(row[i])).strip())
#     prt1.add_row(buff)
#     print(prt1)

def search(val,field):
    cur.execute(("SELECT * FROM cartel.cartels WHERE {0}='{1}'").format(field,val))
    row = cur.fetchone()
    prt1 = PrettyTable()
    prt1.field_names = header_name_back()
    buff = []
    for i in range(len(row)):
        buff.append((str(row[i])).strip())
    prt1.add_row(buff)
    print(prt1)


def filtr (ch1,ch,val):
    if ch=="1":
        if ch1=="2":
            cur.execute(("""SELECT * from cartel.cartels where  level_of_danger >= '{}' ORDER by level_of_danger""").format(val))
        elif ch1=="1":
            cur.execute(("""SELECT * from cartel.cartels where  level_of_danger <= '{}' ORDER by level_of_danger""").format(val))
    elif ch=="2":
        if ch1=="2":
            cur.execute(("""SELECT * from cartel.cartels where  income >= '{}' ORDER by income""").format(val))
        elif ch1=="1":
            cur.execute(("""SELECT * from cartel.cartels where  income <= '{}' ORDER by income""").format(val))
    rows = cur.fetchall()
    print("_________\n position table content:")
    prt = PrettyTable()
    prt.field_names = header_name_back()
    for row in rows:
        buff = []
        for i in range(len(row)):
            buff.append((str(row[i])).strip())
        prt.add_row(buff)
    print(prt)
# cur.execute("""SELECT COLUMN_NAME from information_schema.columns where table_name='type_of_equipment'""")
# rows = cur.fetchall()
# for row in rows:
#     print("     ", row)



# menu()
# show_table_content1()
# show_table_content()
# recording_in_the_end(input())
# show_table_content()
# update_all_record(2,333333)
# show_table_content()
# menu()
# cur.execute("""SELECT COLUMN_NAME from information_schema.columns where table_name='type_of_equipment'""")
# rows= cur.fetchall()
# for row in rows:
#     print(" ",row)
# show_table_content()
# print()
# delete_Record(4)
# delete_Record(2)

# print()
# recording_in_the_end("kekekekk")
