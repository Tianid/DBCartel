import psycopg2
from prettytable import PrettyTable
from tabels1 import cartels


# prt.add_row(["kk","ss","dcscasdsfd"])


conn = psycopg2.connect("dbname='DB' user='LimDenson' host='localhost' password='1234'")
cur=conn.cursor()


def menu():

    choise=99
    while choise !="9":
        print("______Table: sele point______")
        print(""" 0 - Insert record \n 1 - Delete record \n 2 - Show records \n 3 - Update record \n 4 - Search record \n 5 - Cross request \n 6 - Filtr \n 9 - Exit""")
        choise = input()
        # show_table_content()
        if choise=="0":
            cartels.show_table_content()
            val=input("insert city ,address,point owner,possibility of detection,income by using - ',' :")
            recording_in_the_end(val)
        elif choise=="1":
            show_table_content()
            val = input("select row ID to delete: ")
            delete_Record(val)
        elif choise=="2":
            header_name_back()
            show_table_content()
        elif choise=="3":
            ch1=input("Type object of update - record of field: ")
            if ch1=="record":
                show_table_content()
                id = input("select id of record: ")
                val1 = input("type new city: ")
                val2 = input("type new address: ")
                cartels.show_table_content()
                val3 = input("type new point owner: ")
                val4 = input("type new possibility of detection: ")
                val5 = input("type new income: ")
                update_all_record(val1,val2,val3,val4,val5,id)
            elif ch1=="field":
                show_table_content()
                id=input("Select id of record: ")
                headers=header_name_back()
                count = 0
                for i in headers:
                    print("     ", count, "-", i, "\n")
                    count = count + 1
                field = input("select field of update: ")
                val = input("type new content of field: ")
                update_one_field(val, headers[int(field)],id)
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
            cross("income")
        elif choise == "6":
            ch = input("1 - Filtr by possibility of detection \n2 - Filtr by income")
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
    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='sale_point'",)
    row=cur.fetchall()
    buff=[]
    for i in row:
        buff.append(i[0])
    return buff


def header_name_back_for_cross(value):

    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='sale_point'",)
    row=cur.fetchall()
    buff=[]
    for i in row:
        buff.append(i[0])
    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='cartels'", )
    row = cur.fetchall()
    for i in row:
        buff.append(i[0])
    val=value
    count=0
    for i in range(len(buff)):
        if val==buff[i] and count>0:
            buff[i]=buff[i]+" "
        elif val==buff[i] and count<=0:
            count=count+1


    # print(buff)
    return buff

def show_table_content():
    cur.execute("""SELECT * from cartel.sale_point """)
    rows= cur.fetchall()
    print("_________\n sale point table content:")
    prt = PrettyTable()
    # prt.field_names = ["1", "2", "3", "4", "5", "6"]
    prt.field_names=header_name_back()
    for row in rows:
        buff=[]
        for i in range(len(row)):

            buff.append((str(row[i])).strip())

            # print(" ",row[0],"|",row[1],"|",str(row[2]).strip(),"|",str(row[3]).strip(),"|",str(row[4]).strip(),"|")
        prt.add_row(buff)
    print(prt)
        # print(" ",str(row[0]).strip(),"|",str(row[1]).strip(),"|",str(row[2]).strip(),"|",str(row[3]).strip(),"|",str(row[4]).strip(),"|")
    # print("__________\n")



def delete_Record(value):
    val=[value]
    cur.execute("DELETE FROM cartel.sale_point WHERE sale_point_id=%s;",(val))
    conn.commit()
    show_table_content()

def recording_in_the_end(value1):
    # val=(value1,)
    val = value1.split(",")
    cur.execute("INSERT INTO cartel.sale_point (city,address,point_owner,possibility_of_detection,income) VALUES (%s,%s,%s,%s,%s)",val)
    conn.commit()
    show_table_content()

def update_all_record(city,addr,point,possib,income,id):
    cur.execute("UPDATE cartel.sale_point SET city = %s,address = %s,point_owner = %s, possibility_of_detection=%s,income=%s where sale_point_id = %s",(city,addr,point,possib,income,id,))
    conn.commit()
def update_one_field(val,field,id):
    cur.execute(("UPDATE cartel.sale_point SET {0}='{1}' WHERE sale_point_id='{2}'").format(field, val,id))
    conn.commit()
def search(val, field):
    cur.execute(("SELECT * FROM cartel.sale_point WHERE {0}='{1}'").format(field, val))
    row = cur.fetchone()
    prt1 = PrettyTable()
    prt1.field_names = header_name_back()
    buff = []
    for i in range(len(row)):
        buff.append((str(row[i])).strip())
    prt1.add_row(buff)
    print(prt1)


def cross(value):
    cur.execute("SELECT * from cartel.sale_point CROSS JOIN cartel.cartels WHERE cartels.name=sale_point.point_owner")
    rows=cur.fetchall()
    prt = PrettyTable()
    prt.field_names = header_name_back_for_cross(value)
    for row in rows:
        # print(row,"!!!!!")
        buff = []
        for i in range(len(row)):
            buff.append((str(row[i])).strip())
        prt.add_row(buff)
    print(prt)


def filtr (ch1,ch,val):
    if ch=="1":
        if ch1=="2":
            cur.execute(("""SELECT * from cartel.sale_point where  possibility_of_detection >= '{}' ORDER by possibility_of_detection""").format(val))
        elif ch1=="1":
            cur.execute(("""SELECT * from cartel.sale_point where  possibility_of_detection <= '{}' ORDER by possibility_of_detection""").format(val))
    elif ch=="2":
        if ch1=="2":
            cur.execute(("""SELECT * from cartel.sale_point where  income >= '{}' ORDER by income""").format(val))
        elif ch1=="1":
            cur.execute(("""SELECT * from cartel.sale_point where  income <= '{}' ORDER by income""").format(val))
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




# show_table_content1()
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
