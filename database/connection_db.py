import mysql.connector
import traceback
def ConnectionToDB():
    
    return mysql.connector.connect(host="localhost", user="root",  passwd="", database="budget_template")
    try:
        
        print("Connexion Etablished with cursor!")
    except Exception:
        print("problem when try to connect")
        print(traceback.format_exc())
        
def ConnectionToDBControleur():
    
    return mysql.connector.connect(host="localhost", user="root",  passwd="", database="controleur_gestion")
    try:
        
        print("Connexion Etablished with cursor!")
    except Exception:
        print("problem when try to connect")
        print(traceback.format_exc())
        
def list_known_names():
    mydb = ConnectionToDB()
    print("db connected")
    mycursor = mydb.cursor()
    sql = "SELECT  project_name FROM template "
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    print(myresult)
    list=["'","(",")",","] 
    #res="".join(i for i in myresult if i not in list) 
    res="".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    print(res)
    return res

def list_known_projects_Id():
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  project_id FROM template "
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    #print(myresult)
    list=["'","(",")",","] 
    #res="".join(i for i in myresult if i not in list) 
    res=",".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    #print(res)
    list = res
    #print(list)
    return list


def get_template(num):
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  project_name,budget,homme,days,delivery,budget_monthly FROM template WHERE project_id = {}".format(num)
    mycursor.execute(sql)   
    myresult = mycursor.fetchone()
    mydb.close()
    mydb1 = ConnectionToDB()
    mycursor1 = mydb1.cursor()
    sql1 = "SELECT developer, quality, devops, support FROM list_ressource WHERE project_id = {}".format(num)
    mycursor1.execute(sql1)
    myresult1 = mycursor1.fetchone()
    print(myresult1)
    mydb2 = ConnectionToDBControleur()
    mycursor2 = mydb2.cursor()
    sql2 ="SELECT sum_salary FROM sum_salary_in_project WHERE project_id = {}".format(num)
    mycursor2.execute(sql2)
    myresult2 = mycursor2.fetchone()
    print(myresult2)
    #print(myresult[0],myresult[1],myresult[2],myresult[3],myresult[4],myresult[5])
    list=[myresult[0],myresult[1],myresult[2],myresult[3],myresult[4],myresult[5],myresult1[0],myresult1[1],myresult1[2],myresult1[3],myresult2[0]] 
    #res=",".join(str(i) for i in myresult if i not in list) 
    #print(res[0])
    #res=",".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    #list = res
    return list

def get_ressource_details(num):
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  project_name,budget,homme,days,delivery,budget_monthly FROM template WHERE project_id = {}".format(num)
    mycursor.execute(sql)   
    myresult = mycursor.fetchone()
    list=["'","(",")",","] 
    res="".join(str(i) for i in myresult if i not in list) 
    #res=",".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    #list = res
    return res