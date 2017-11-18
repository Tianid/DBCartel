import psycopg2
from tabels1 import type_of_equipment
from tabels1 import labs
from prettytable import PrettyTable

conn = psycopg2.connect("dbname='DB' user='LimDenson' host='localhost' password='1234'")
cur=conn.cursor()


def menu():

    choise=99
    while choise !="9":
        print("______Table: equipment______")
        print(""" 0 - Insert record \n 1 - Delete record \n 2 - Show records \n 3 - Update record \n 4 - Search record \n 5 - Cross requests \n 6 - Filtr \n 9 - Exit""")
        choise = input()
        # show_table_content()
        if choise=="0":
            labs.show_table_content()
            type_of_equipment.show_table_content()
            val=input("insert name ,type of equipment,cost,run out,lab id by using - ',' :")
            recording_in_the_end(val)
        elif choise=="1":
            show_table_content()
            val = input("select row ID to delete: ")
            delete_Record(val)
        elif choise=="2":
            show_table_content()
        elif choise=="3":
            ch1 = input("Type object of update - record of field: ")
            if ch1=="record":
                show_table_content()
                id = input("select id of record: ")
                val1 = input("type new name: ")
                type_of_equipment.show_table_content()
                val2 = input("type new type of equipment: ")
                val3 = input("type new cost: ")
                val4 = input("type new run out: ")
                labs.show_table_content()
                val5 = input("type new lab id: ")
                update_all_record(val1, val2, val3,val4,val5,id)
                update_all_record(id,val)
            elif ch1=="field":
                show_table_content()
                id = input("Select id of record: ")
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
            ch=input("Select cross request:\n 1 - equpment -> labs\n 2 - equpment -> type of equipment")
            if ch=="1":
                cross("lab_id", 1)
            if ch=="2":
                cross("name", 0)
        elif choise=="6":
            ch = input("1 - Filtr by cost \n2 - Filtr by run out")
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
    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='equipment'",)
    row=cur.fetchall()
    buff=[]
    for i in row:
        buff.append(i[0])
    return buff

def header_name_back_for_cross(value,ch):

    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='equipment'",)
    row=cur.fetchall()
    buff=[]
    for i in row:
        buff.append(i[0])
    if ch==1:
        cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='labs'", )

    else:cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='type_of_equipment'", )
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
    cur.execute("""SELECT * from cartel.equipment """)
    rows= cur.fetchall()
    print("_________\n equipment table content:")
    prt = PrettyTable()
    prt.field_names=header_name_back()
    for row in rows:
        buff=[]
        for i in range(len(row)):
            buff.append((str(row[i])).strip())
        prt.add_row(buff)
    print(prt)


def delete_Record(value):
    val = [value]
    cur.execute("DELETE FROM cartel.equipment WHERE inventory_key=%s;", (val))
    conn.commit()
    show_table_content()


def recording_in_the_end(value1):
    val = value1.split(",")
    # cur.execute("INSERT INTO cartel.equipment (name,type_of_equipment,cost,run_out,lab_id) VALUES (%s,%s,%s,%s,%s)", val)
    cur.execute("INSERT INTO cartel.equipment (name,type_of_equipment,cost,run_out,lab_id) VALUES (%s,%s,%s,%s,%s)",(val))
    conn.commit()
    show_table_content()

def update_all_record(name,type,cost,run_out,lab_id,id):
    cur.execute("UPDATE cartel.equipment SET name =%s,type_of_equipment=%s,cost=%s,run_out=%s,lab_id=%s where inventory_key=%s",(name,type,cost,run_out,lab_id,id))
    conn.commit()
def update_one_field(val,field,id):
    cur.execute(("UPDATE cartel.equipment SET {0}='{1}' WHERE inventory_key='{2}'").format(field, val,id))
    conn.commit()
def search(val, field):
    cur.execute(("SELECT * FROM cartel.equipment WHERE {0}='{1}'").format(field, val))
    row = cur.fetchone()
    prt1 = PrettyTable()
    prt1.field_names = header_name_back()
    buff = []
    for i in range(len(row)):
        buff.append((str(row[i])).strip())
    prt1.add_row(buff)
    print(prt1)
def cross(value, ch):
    if ch==1:
        cur.execute("SELECT labs.product,labs.volume_of_production,labs.lab_owner from cartel.equipment CROSS JOIN cartel.labs WHERE labs.lab_id=equipment.lab_id")
    else: cur.execute("SELECT * from cartel.equipment CROSS JOIN cartel.type_of_equipment WHERE type_of_equipment.id_of_equipment=equipment.type_of_equipment")
    rows=cur.fetchall()
    prt = PrettyTable()
    prt.field_names = header_name_back_for_cross(value,ch)
    for row in rows:
        # print(row,"!!!!!")
        buff = []
        for i in range(len(row)):
            buff.append((str(row[i])).strip())
        prt.add_row(buff)
    print(prt)
    # cur.execute("SELECT personal_position ,SUM (CASE surname WHEN )")


def filtr (ch1,ch,val):
    if ch=="1":
        if ch1=="2":
            cur.execute(("""SELECT * from cartel.equipment where  cost >= '{}' ORDER by cost""").format(val))
        elif ch1=="1":
            cur.execute(("""SELECT * from cartel.equipment where  cost <= '{}' ORDER by cost""").format(val))
    elif ch=="2":
        if ch1=="2":
            cur.execute(("""SELECT * from cartel.equipment where  run_out >= '{}' ORDER by run_out""").format(val))
        elif ch1=="1":
            cur.execute(("""SELECT * from cartel.equipment where  run_out <= '{}' ORDER by run_out""").format(val))
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
