import psycopg2
from tabels1 import cartels
from tabels1 import position
from prettytable import PrettyTable
conn = psycopg2.connect("dbname='DB' user='LimDenson' host='localhost' password='1234'")
cur=conn.cursor()


def menu():

    choise=99
    while choise !="9":
        print("______Table: persone______")
        print(""" 0 - Insert record \n 1 - Delete record \n 2 - Show records \n 3 - Update record \n 4 - Search record \n 5 - Cross requests \n 6 - Filtr by persentage of trust \n 9 - Exit""")
        choise = input()
        # show_table_content()
        if choise=="0":
            cartels.show_table_content()
            position.show_table_content()
            val=input("insert surname,name,second name,persentage of trust,personal position,workplace by using - ',' :")
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
                val1 = input("type new surname: ")
                val2 = input("type new name: ")
                val3 = input("type new second name: ")
                val4 = input("type new persentage of trust: ")
                position.show_table_content()
                val5 = input("type new personal position ")
                cartels.show_table_content()
                val6 = input("type new workplace: ")
                update_all_record(val1, val2, val3,val4,val5,val6,id)
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
            ch = input("Select cross request:\n 1 - persone -> position\n 2 - persone -> cartels")
            if ch == "1":
                cross("name", 1)
            if ch == "2":
                cross("name", 0)
        elif choise == "6":

            ch1 = input(" 1 - <= \n 2 - >=")
            val = input("Input value ")
            if ch1 == "1":
                filtr(ch1, val)
            elif ch1 == "2":
                filtr(ch1, val)


def header_name_back():
    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='persone'",)
    row=cur.fetchall()
    buff=[]
    for i in row:
        buff.append(i[0])
    return buff

def header_name_back_for_cross(value,ch):

    cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='persone'",)
    row=cur.fetchall()
    buff=[]
    for i in row:
        buff.append(i[0])
    if ch==1:
        cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='position'", )

    else:cur.execute(" SELECT column_name FROM information_schema.columns WHERE table_name ='cartels'", )
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
    cur.execute("""SELECT * from cartel.persone""")
    rows= cur.fetchall()
    print("_________\n persone table content:")
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
    cur.execute("DELETE FROM cartel.persone WHERE id=%s;", (val))
    conn.commit()
    show_table_content()


def recording_in_the_end(value1):
    val = value1.split(",")
    # cur.execute("INSERT INTO cartel.equipment (name,type_of_equipment,cost,run_out,lab_id) VALUES (%s,%s,%s,%s,%s)", val)
    cur.execute("INSERT INTO cartel.persone (surname,name,second_name,percentage_of_trust,personal_position,workplace) VALUES (%s,%s,%s,%s,%s,%s)",(val))
    conn.commit()
    show_table_content()

def update_all_record(surname,name,sname,trust,position,workplace,id):
    cur.execute("UPDATE cartel.persone SET surname=%s,name=%s,second_name=%s,percentage_of_trust=%s,personal_position=%s,workplace=%s where id=%s",(surname,name,sname,trust,position,workplace,id))
    conn.commit()
def update_one_field(val,field,id):
    cur.execute(("UPDATE cartel.persone SET {0}='{1}' WHERE id='{2}'").format(field, val,id))
    conn.commit()


def search(val,field):
    cur.execute(("SELECT * FROM cartel.persone WHERE {0}='{1}'").format(field,val))
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
        cur.execute("SELECT * from cartel.persone CROSS JOIN cartel.position WHERE position.name=persone.personal_position")
    else: cur.execute("SELECT * from cartel.persone CROSS JOIN cartel.cartels WHERE cartels.name=persone.workplace")
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

def filtr (ch1,val):

    if ch1=="2":
        cur.execute(("""SELECT * from cartel.persone where  percentage_of_trust >= '{}' ORDER by percentage_of_trust""").format(val))
    elif ch1=="1":
        cur.execute(("""SELECT * from cartel.persone where  percentage_of_trust <= '{}' ORDER by percentage_of_trust""").format(val))
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
