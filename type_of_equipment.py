import psycopg2
from prettytable import PrettyTable

conn = psycopg2.connect("dbname='DB' user='LimDenson' host='localhost' password='1234'")
cur=conn.cursor()

def menu():

    choise=99
    while choise !="9":
        print("______Table: type of equipment______")
        print(""" 0 - Insert record \n 1 - Delete record \n 2 - Show records \n 3 - Update record \n 4 - Search record \n 9 - Exit""")
        choise = input()
        # show_table_content()
        if choise=="0":
            val=input("insert name :")
            recording_in_the_end(val)
        elif choise=="1":
            val = input("select row to delete: ")
            delete_Record(val)
        elif choise=="2":
            show_table_content()
        elif choise=="3":
            ch1 = input("Type object of update - record of field: ")
            if ch1=="record":
                show_table_content()
                id = input("select id of record: ")
                val = input("type name: ")
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
        elif choise == "4":
            headers = header_name_back();
            count = 0
            for i in headers:
                print("     ", count, "-", i, "\n")
                count = count + 1
            field = input("select field of search: ")
            val = input("type what are you searching: ")
            search(val, headers[int(field)])
        elif choise=="90":
            pass


def header_name_back():
    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='type_of_equipment'",)
    row=cur.fetchall()
    buff=[]
    for i in row:
        buff.append(i[0])
    return buff


def show_table_content():
    cur.execute("""SELECT * from cartel.type_of_equipment """)
    rows= cur.fetchall()
    print("_________\n type of equipment table content:")
    prt = PrettyTable()
    prt.field_names=header_name_back()
    for row in rows:
        buff=[]
        for i in range(len(row)):
            buff.append((str(row[i])).strip())
        prt.add_row(buff)
    print(prt)




# def Show_table_content1():
#     val=('cartel.equipment',)
#     v="SELECT * FROM cartel.equipment"
#     cur.execute(v,val)
#     rows= cur.fetchall()
#     for row in rows:
#         print(" ",row)
#     print("__________")

def delete_Record(value):
    val=[value]
    cur.execute("DELETE FROM cartel.type_of_equipment WHERE id_of_equipment=%s;",(val))
    conn.commit()
    show_table_content()

def recording_in_the_end(value1):
    val = [value1]
    # cur.execute("INSERT into cartel.type_of_equipment (Null,'kek1')")
    cur.execute("INSERT INTO cartel.type_of_equipment (name) VALUES (%s)",val )
    conn.commit()
    show_table_content()

def update_all_record(id,value):
    cur.execute("UPDATE cartel.type_of_equipment SET name =%s where id_of_equipment=%s",(value,id))
    conn.commit()
def update_one_field(val,field,id):
    cur.execute(("UPDATE cartel.type_of_equipment SET {0}='{1}' WHERE id_of_equipment='{2}'").format(field, val,id))
    conn.commit()
def search(val,field):
    cur.execute(("SELECT * FROM cartel.type_of_equipment WHERE {0}='{1}'").format(field,val))
    row = cur.fetchone()
    prt1 = PrettyTable()
    prt1.field_names = header_name_back()
    buff = []
    for i in range(len(row)):
        buff.append((str(row[i])).strip())
    prt1.add_row(buff)
    print(prt1)
#
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
