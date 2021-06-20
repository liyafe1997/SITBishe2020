#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import cgi
import socket
import urllib.parse as urlparse
# if you run in Python 2 just replace http.server with BaseHTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import base64
import jwt
import hashlib
from http.cookies import SimpleCookie

nodes_permission_level = {}
nodes_permission_level[0] = [
    "/checklogin", "/get_all_users", "/get_all_import_item", "/get_all_store_item", "/get_all_sale_item", "/get_all_store_places", "/get_all_sale_customs", "/get_all_import_finished_item", "/new_import_item",
    "/new_store_item", "/new_sale_item", "/delete_sale_item_by_id", "/delete_import_item_by_id", "/delete_store_item_by_id", "/update_import_item_by_id", "/update_store_item_by_id", "/update_sale_item_by_id",
    "/mark_sale_item_finished", "/mark_import_item_finished", "/newuser", "/deleteuser", "/modifyuser", "/editpassword", "/get_dashboard_count", "/get_sorted_import_data", "/get_sorted_store_data",
    "/get_sorted_sale_data", "/store_from_import", "/sale_from_store", "/get_login_history", "/get_all_username", "/logout"
]
nodes_permission_level[1] = [
    "/checklogin", "/get_all_store_item", "/get_all_store_places", "/get_all_import_finished_item", "/new_store_item", "/delete_store_item_by_id", "/update_store_item_by_id", "/store_from_import",
    "/editpassword_with_old_password", "/logout"
]

nodes_permission_level[2] = [
    "/checklogin", "/get_all_import_item", "/new_import_item", "/delete_import_item_by_id", "/update_import_item_by_id", "/editpassword_with_old_password", "/mark_import_item_finished", "/logout"
]

nodes_permission_level[3] = [
    "/checklogin", "/get_all_store_item", "/get_all_sale_item", "/get_all_sale_customs", "/new_sale_item", "/delete_sale_item_by_id", "/update_sale_item_by_id", "/sale_from_store", "/mark_sale_item_finished",
    "/editpassword_with_old_password", "/logout"
]
nodes_permission_level[4] = ["/checklogin", "/get_all_store_item", "/get_all_store_places", "/get_all_import_finished_item", "/store_from_import", "/editpassword_with_old_password", "/logout"]
nodes_permission_level[5] = ["/checklogin", "/get_all_store_item", "/get_all_sale_item", "/get_all_sale_customs", "/mark_sale_item_finished", "/sale_from_store", "/editpassword_with_old_password", "/logout"]


def ReadFile(filename):
    file_object = open(filename, "rb")
    try:
        fileContent = file_object.read()
    finally:
        file_object.close()
    return fileContent


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        requests = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        node = self.path.split('?')
        node = node[0]
        print("Request node = " + str(node))
        #Prevent access .. to filesystem
        if (".." in node):
            self.send_response(403)
            self.end_headers()
            self.wfile.write("HTTP 403 Error. illegal operation.".encode())
            return
        #--Prevent access .. to filesystem
        #Process Authorization
        receivedtoken = "0"
        login_user_role = None
        try:
            cookies = SimpleCookie(self.headers.get('Cookie'))
            receivedtoken = cookies["token"].value
            tokendecodedjson = jwt.decode(receivedtoken, 'yo58q8oBYIYI35v2yb010U9RW84YOsdf832T7IUEJGS', algorithms=['HS256'])
            login_user_role = int(tokendecodedjson['role'])
        except:
            pass
        node_needs_login = False
        for i in nodes_permission_level:
            node_needs_login = node_needs_login or (node in nodes_permission_level[i])
        if (node_needs_login):
            if ((login_user_role == None) or (node not in nodes_permission_level[login_user_role])):
                self.send_response(403)
                self.end_headers()
                self.wfile.write("HTTP 403 Error. Not Authorized.".encode())
                return
        #--Process Authorization

        # Process header
        self.send_response(200)
        try:
            if node.split('.')[-1] == "html" or node.split('.')[-1] == "htm":
                print("Html files, set header Content-Type=text/html")
                self.send_header('Content-type', 'text/html')
        except:
            pass
        self.end_headers()
        # --Process header
        # ------------------Web Services Start-----------------
        # A example of hello world, request URL is http://your.server/requestnode?hello=World:
        if node == "/requestnode":
            self.wfile.write(("Hello, " + str(requests["hello"][0])).encode())
        #-------------------Get Items-------------------
        elif node == "/get_all_users":
            QueryString = ("select * from users")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString)))
        elif node == "/get_all_import_item":
            QueryString = ("select * from import_items")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString)))
        elif node == "/get_all_store_item":
            QueryString = ("select * from store_items")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString)))
        elif node == "/get_all_sale_item":
            QueryString = ("select * from sale_items")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString)))
        elif node == "/get_all_store_places":
            QueryString = ("select place from store_items")
            result = SQLike_Query(QueryString)
            self.wfile.write(SingleColumnDataToJson(result))
        elif node == "/get_all_sale_customs":
            QueryString = ("select custom from sale_items")
            result = SQLike_Query(QueryString)
            self.wfile.write(SingleColumnDataToJson(result))
        elif node == "/get_all_import_finished_item":
            QueryString = ("select * from import_items where finished=1")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString)))
        #-------------------Get Items-------------------

        #-------------------Insert Items-------------------
        elif node == "/new_import_item":
            insertlist = []
            insertlist.append(str(requests["name"][0]))
            insertlist.append(str(requests["number"][0]))
            insertlist.append(str(requests["factory"][0]))
            insertlist.append(str(requests["finished"][0]))
            if (GeneralInsert(insertlist, "import_items")):
                self.wfile.write(("ok").encode())
            else:
                self.wfile.write(("failed").encode())
        elif node == "/new_store_item":
            insertlist = []
            insertlist.append(str(requests["name"][0]))
            insertlist.append(str(requests["number"][0]))
            insertlist.append(str(requests["place"][0]))
            if (GeneralInsert(insertlist, "store_items")):
                self.wfile.write(("ok").encode())
            else:
                self.wfile.write(("failed").encode())
        elif node == "/new_sale_item":
            insertlist = []
            insertlist.append(str(requests["name"][0]))
            insertlist.append(str(requests["number"][0]))
            insertlist.append(str(requests["custom"][0]))
            insertlist.append(str(requests["finished"][0]))
            if (GeneralInsert(insertlist, "sale_items")):
                self.wfile.write(("ok").encode())
            else:
                self.wfile.write(("failed").encode())
        #-------------------Insert Items-------------------

        #-------------------Delete Items-------------------
        elif node == "/delete_sale_item_by_id":
            try:
                print(("delete_sale_item_by_id: " + SQLike_Query("DELETE FROM sale_items WHERE id=" + str(requests["id"][0]))))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/delete_import_item_by_id":
            try:
                print(("delete_import_item_by_id: " + SQLike_Query("DELETE FROM import_items WHERE id=" + str(requests["id"][0]))))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/delete_store_item_by_id":
            try:
                print(("delete_store_item_by_id: " + SQLike_Query("DELETE FROM store_items WHERE id=" + str(requests["id"][0]))))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())

        #-------------------Delete Items-------------------

        #-------------------Update Items-------------------
        elif node == "/update_import_item_by_id":
            try:
                id = str(requests["id"][0])
                name = str(requests["name"][0])
                number = str(requests["number"][0])
                factory = str(requests["factory"][0])
                finished = str(requests["finished"][0])
                print("update_import_item_by_id NAME: " + SQLike_Query("UPDATE import_items SET name=" + name + " WHERE id=" + id))
                print("update_import_item_by_id NUMBER: " + SQLike_Query("UPDATE import_items SET number=" + number + " WHERE id=" + id))
                print("update_import_item_by_id FACTORY: " + SQLike_Query("UPDATE import_items SET factory=" + factory + " WHERE id=" + id))
                print("update_import_item_by_id FINISHED: " + SQLike_Query("UPDATE import_items SET finished=" + finished + " WHERE id=" + id))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/update_store_item_by_id":
            try:
                id = str(requests["id"][0])
                name = str(requests["name"][0])
                number = str(requests["number"][0])
                place = str(requests["place"][0])
                print("update_store_item_by_id NAME: " + SQLike_Query("UPDATE store_items SET name=" + name + " WHERE id=" + id))
                print("update_store_item_by_id NUMBER: " + SQLike_Query("UPDATE store_items SET number=" + number + " WHERE id=" + id))
                print("update_store_item_by_id PLACE: " + SQLike_Query("UPDATE store_items SET place=" + place + " WHERE id=" + id))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/update_sale_item_by_id":
            try:
                id = str(requests["id"][0])
                name = str(requests["name"][0])
                number = str(requests["number"][0])
                custom = str(requests["custom"][0])
                finished = str(requests["finished"][0])
                print("update_sale_item_by_id NAME: " + SQLike_Query("UPDATE sale_items SET name=" + name + " WHERE id=" + id))
                print("update_sale_item_by_id NUMBER: " + SQLike_Query("UPDATE sale_items SET number=" + number + " WHERE id=" + id))
                print("update_sale_item_by_id CUSTOM: " + SQLike_Query("UPDATE sale_items SET custom=" + custom + " WHERE id=" + id))
                print("update_sale_item_by_id FINISHED: " + SQLike_Query("UPDATE sale_items SET finished=" + finished + " WHERE id=" + id))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/mark_sale_item_finished":
            try:
                id = str(requests["id"][0])
                print("mark_sale_item_finished: " + SQLike_Query("UPDATE sale_items SET finished=1 WHERE id=" + id))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/mark_import_item_finished":
            try:
                id = str(requests["id"][0])
                print("mark_import_item_finished: " + SQLike_Query("UPDATE import_items SET finished=1 WHERE id=" + id))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        #-------------------Update Items-------------------

        #-------------------Users Manager-------------------
        elif node == "/newuser":
            #/newuser?username=xxx&password=123&role=xxx
            insertlist = []
            insertlist.append(str(requests["username"][0]))
            insertlist.append(hashlib.sha256((str(requests["password"][0]) + "u98jojIOGA1240U3HF43T53R1I100kass").encode()).hexdigest())
            insertlist.append(str(requests["role"][0]))
            if (GeneralInsert(insertlist, "users")):
                self.wfile.write(("ok").encode())
            else:
                self.wfile.write(("failed").encode())
        elif node == "/deleteuser":
            if (str(requests["id"][0]) == 1):
                self.wfile.write(("failed").encode())
            else:
                try:
                    print(("delete_user_by_id: " + SQLike_Query("DELETE FROM users WHERE id=" + str(requests["id"][0]))))
                    self.wfile.write(("ok").encode())
                except:
                    self.wfile.write(("failed").encode())
        elif node == "/modifyuser":
            try:
                id = str(requests["id"][0])
                username = str(requests["username"][0])
                role = str(requests["role"][0])
                print("update username: " + SQLike_Query("UPDATE users SET username=" + username + " WHERE id=" + id))
                print("update role: " + SQLike_Query("UPDATE users SET role=" + role + " WHERE id=" + id))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/editpassword":
            try:
                id = str(requests["id"][0])
                password = str(requests["password"][0])
                hashresult = hashlib.sha256((password + "u98jojIOGA1240U3HF43T53R1I100kass").encode()).hexdigest()
                print("update password: " + SQLike_Query("UPDATE users SET password=" + hashresult + " WHERE id=" + id))
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/editpassword_with_old_password":
            try:
                id = str(requests["id"][0])
                oldpassword = str(requests["oldpassword"][0])
                newpassword = str(requests["newpassword"][0])
                sql = "SELECT password FROM users WHERE id=" + id
                result = SQLike_Query(sql).split("\n")
                result = RemoveEmptyLinesInList(result)[1].split("\t")
                oldpassword = hashlib.sha256((oldpassword + "u98jojIOGA1240U3HF43T53R1I100kass").encode()).hexdigest()
                if (oldpassword == result[0]):
                    hashresult = hashlib.sha256((newpassword + "u98jojIOGA1240U3HF43T53R1I100kass").encode()).hexdigest()
                    print("update password: " + SQLike_Query("UPDATE users SET password=" + hashresult + " WHERE id=" + id))
                    self.wfile.write(("ok").encode())
                else:
                    self.wfile.write(("-1").encode())
            except:
                self.wfile.write(("failed").encode())
        elif node == "/get_all_username":
            try:
                QueryString = ("select id,username from users")
                Result = SQLike_Query(QueryString)
                self.wfile.write(GeneralResultToJson(Result))
            except:
                self.wfile.write(("failed").encode())
        elif node == "/login":
            username = str(requests["username"][0])
            password = str(requests["password"][0])
            self.wfile.write(Login(username, password).encode())
            '''
        elif node == "/logout":
            try:
                cookies = SimpleCookie(self.headers.get('Cookie'))
                receivedtoken = cookies["token"].value
                login_token.remove(receivedtoken)
                if (receivedtoken not in login_token):
                    self.wfile.write("ok".encode())
                else:
                    self.wfile.write("failed".encode())
            except:
                self.wfile.write("failed".encode())
            '''
        elif node == "/checklogin":
            pass
        #-------------------Users Manager-------------------
        #-------------------Dashboard-------------------
        elif node == "/get_dashboard_count":
            #User Count
            QueryString = ("select id from users")
            Result = SQLike_Query(QueryString).split("\n")[1:]
            Result = [line for line in Result if line.strip()]  # remove empty line
            UserCount = len(Result)

            QueryString = ("select number from sale_items")
            Result = SQLike_Query(QueryString).split("\n")[1:]
            Result = [line for line in Result if line.strip()]  # remove empty line
            AllSaleCount = 0
            for i in (Result):
                AllSaleCount += int(i)
            SaleCount = len(Result)

            QueryString = ("select number from import_items")
            Result = SQLike_Query(QueryString).split("\n")[1:]
            Result = [line for line in Result if line.strip()]  # remove empty line
            AllImportCount = 0
            for i in (Result):
                AllImportCount += int(i)
            ImportCount = len(Result)

            QueryString = ("select number from store_items")
            Result = SQLike_Query(QueryString).split("\n")[1:]
            Result = [line for line in Result if line.strip()]  # remove empty line
            AllStoreCount = 0
            for i in (Result):
                AllStoreCount += int(i)
            StoreCount = len(Result)

            QueryString = ("select id from login_history")
            Result = SQLike_Query(QueryString).split("\n")[1:]
            Result = [line for line in Result if line.strip()]  # remove empty line
            AllStoreCount = 0
            for i in (Result):
                AllStoreCount += int(i)
            LoginCount = len(Result)

            ResultDict = {}
            ResultDict["UserCount"] = UserCount
            ResultDict["SaleCount"] = SaleCount
            ResultDict["ImportCount"] = ImportCount
            ResultDict["StoreCount"] = StoreCount
            ResultDict["AllSaleCount"] = AllSaleCount
            ResultDict["AllImportCount"] = AllImportCount
            ResultDict["AllStoreCount"] = AllStoreCount
            ResultDict["LoginCount"] = LoginCount
            self.wfile.write(json.dumps(ResultDict).encode() + "\n".encode())
        elif node == "/get_sorted_import_data":
            QueryString = ("select * from import_items order by number DESC")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString), 5))
        elif node == "/get_sorted_store_data":
            QueryString = ("select * from store_items order by number DESC")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString), 5))
        elif node == "/get_sorted_sale_data":
            QueryString = ("select * from sale_items order by number DESC")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString), 5))
        elif node == "/get_login_history":
            QueryString = ("select * from login_history order by time DESC")
            self.wfile.write(GeneralResultToJson(SQLike_Query(QueryString), 5))
        #-------------------Dashboard-------------------

        #-------------------Dataflow-------------------
        elif node == "/store_from_import":
            id = int(str(requests["id"][0]))
            number = int(str(requests["number"][0]))
            storeplace = str(requests["storeplace"][0])

            result = SQLike_Query("select name,number from import_items where id=" + str(id))
            result = RemoveEmptyLinesInList(result.split("\n"))
            if (len(result) <= 1):
                self.wfile.write("-3".encode())  #Error Code -3: 进货库中无此商品
                return
            oldnumber = int((result[1]).split("\t")[1])

            name = (result[1]).split("\t")[0]

            newnumber = oldnumber - number
            if (newnumber < 0):
                self.wfile.write("-2".encode())  #Error Code -2: 进货单中的数量小于入库数量
                return

            result = SQLike_Query("UPDATE import_items SET number=" + str(newnumber) + " WHERE id=" + str(id))
            if ("Updated" not in result):
                self.wfile.write("-1".encode())  #Error Code -1: 数据库错误：更新进货单商品数量失败
                return
            result = SQLike_Query("select number,place from store_items where name=" + name + " and place=" + storeplace)
            result = RemoveEmptyLinesInList(result.split("\n"))
            oldplace = None
            try:
                oldplace = (result[1]).split("\t")[1]
            except:
                pass
            if (len(result) > 1 and oldplace == storeplace):
                oldstorenumber = int((result[1]).split("\t")[0])
                result = SQLike_Query("UPDATE store_items SET number=" + str(oldstorenumber + number) + " WHERE name=" + name + " and place=" + storeplace)
                if ("Updated" not in result):
                    self.wfile.write("-4".encode())  #Error Code -4: 数据库错误：更新库存商品失败
                    return
                else:
                    self.wfile.write("1".encode())  #Error Code 1: 入库成功（已有商品增加库存数量）
                    return
            elif (len(result) == 1):
                insertlist = []
                insertlist.append(name)
                insertlist.append(str(number))
                insertlist.append(storeplace)
                if (GeneralInsert(insertlist, "store_items")):
                    self.wfile.write("0".encode())  #Error Code 0: 入库成功（新商品）
                    return
                else:
                    self.wfile.write("-5".encode())  #Error Code -5: 数据库错误：新增库存商品失败
                    return

            else:
                self.wfile.write("-5".encode())  #Error Code -5: 未知错误（库存数据库错误）
                return
        elif node == "/sale_from_store":
            id = int(str(requests["id"][0]))
            number = int(str(requests["number"][0]))
            custom = str(requests["custom"][0])

            result = SQLike_Query("select name,number from store_items where id=" + str(id))
            result = RemoveEmptyLinesInList(result.split("\n"))
            if (len(result) <= 1):
                self.wfile.write("-3".encode())  #Error Code -3: 库存中无此商品
                return
            oldnumber = int((result[1]).split("\t")[1])

            name = (result[1]).split("\t")[0]

            newnumber = oldnumber - number
            if (newnumber < 0):
                self.wfile.write("-2".encode())  #Error Code -2: 库存不足
                return

            result = SQLike_Query("UPDATE store_items SET number=" + str(newnumber) + " WHERE id=" + str(id))
            if ("Updated" not in result):
                self.wfile.write("-1".encode())  #Error Code -1: 数据库错误：更新库存商品数量失败
                return
            result = SQLike_Query("select number,custom from sale_items where name=" + name + " and custom=" + custom + " and finished=0")
            result = RemoveEmptyLinesInList(result.split("\n"))
            existcustom = None
            try:
                existcustom = (result[1]).split("\t")[1]
            except:
                pass
            if (len(result) > 1 and existcustom == custom):
                oldstorenumber = int((result[1]).split("\t")[0])
                result = SQLike_Query("UPDATE sale_items SET number=" + str(oldstorenumber + number) + " WHERE name=" + name + " and custom=" + custom + " and finished=0")
                if ("Updated" not in result):
                    self.wfile.write("-4".encode())  #Error Code -4: 数据库错误：更新销售商品失败
                    return
                else:
                    self.wfile.write("1".encode())  #Error Code 1: 更新销售单成功（已有销往相同客户商品增加数量）
                    return
            elif (len(result) == 1):
                insertlist = []
                insertlist.append(name)
                insertlist.append(str(number))
                insertlist.append(custom)
                insertlist.append("0")
                if (GeneralInsert(insertlist, "sale_items")):
                    self.wfile.write("0".encode())  #Error Code 0: 新建销售单成功（新客户）
                    return
                else:
                    self.wfile.write("-5".encode())  #Error Code -5: 数据库错误：新增新建销售单失败
                    return

            else:
                self.wfile.write("-5".encode())  #Error Code -5: 未知错误（销售数据库错误）
                return

# ------------------Web Services End-----------------

# ------------------Web Server Load File From File System Start-----------------
        elif node == "/":
            try:
                filecontent = ReadFile(os.path.split(os.path.abspath(__file__))[0] + "/WEBCONTENT/index.html")
                self.wfile.write(filecontent)
                print("Return file: " + node)
            except:
                print("File not found: " + node)
                self.wfile.write(("<html><title>404 Not Found</title>404 Error<br>File /index.html Not Found.</html>\n").encode())
        else:
            try:
                filecontent = ReadFile(os.path.split(os.path.abspath(__file__))[0] + "/WEBCONTENT" + node)
                self.wfile.write(filecontent)
                print("Return file: " + node)
            except:
                print("File not found: " + node)
                self.wfile.write(("<html><title>404 Not Found</title>404 Error<br>File " + node + " Not Found.</html>\n").encode())


# ------------------Web Server Load File From File System End-----------------

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

        value = form.getvalue("key")

        # self._set_headers()
        self.wfile.write("Post key" + value)


def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Fucking http server is started.")
    print("http://127.0.0.1:" + str(port))
    httpd.serve_forever()


# ————————SQLike Connector————————
def SQLike_Query(cmdstring):
    global sqlikesock
    sqlikesock.send(cmdstring.encode('utf-8'))
    data = sqlikesock.recv(40960)
    return str(data, encoding="utf-8")


# ————————SQLike Connector————————


#-------------------------Logic part-------------------------
def GeneralResultToJson(resultstr, slicedata=0):
    contain = resultstr.split('\n')
    contain = [line for line in contain if line.strip()]  # remove empty line
    if (slicedata != 0):
        contain = contain[:slicedata]
    a_key = contain[0].split('\t')
    contain = contain[1:]
    jsonarray = []
    for j in range(0, len(contain)):
        a_value = contain[j].split('\t')
        dic = {}  #store contain from db save as json format
        for i in range(0, len(a_value)):
            if (a_key[i] != ""):
                dic[a_key[i]] = a_value[i]
        jsonarray.append(dic)
    return (json.dumps(jsonarray).encode() + "\n".encode())


def RemoveEmptyLinesInList(lineslist):
    return [line for line in lineslist if line.strip()]


def SingleColumnDataToJson(SelectResult):
    SelectResult = RemoveEmptyLinesInList(SelectResult.split("\n"))[1:]
    datalist = []
    for i in SelectResult:
        datalist.append(i.strip("\t"))
    finalresult = json.dumps(datalist).encode()
    return finalresult


def GeneralInsert(colunmlist, table):
    #get last user id
    queryString = "SELECT id FROM " + table
    print(queryString)
    result = SQLike_Query(queryString)
    lines = result.split('\n')
    lines = [line for line in lines if line.strip()]  # remove empty line
    lines = lines[1:]
    lines.sort()
    print(lines)
    newid = 1
    if (len(lines) != 0):
        newid = int(lines[-1].strip('\t')) + 1
    print("New " + table + " ID = " + str(newid))
    #--get last user id

    try:
        newid = str(newid)
        queryString = "INSERT INTO " + table + " VALUES (" + newid + ","
        for i in colunmlist:
            queryString = queryString + i + ","
        queryString = queryString[:-1]  #remove last,
        queryString += ")"
        print(queryString)
        result = SQLike_Query(queryString)
        print("New " + table + "Insert Result=")
        print(result)
        return True
    except:
        return False


def Login(username, password):
    hashresult = hashlib.sha256((password + "u98jojIOGA1240U3HF43T53R1I100kass").encode()).hexdigest()

    sql = "SELECT id,password,role FROM users WHERE username=" + username
    result = SQLike_Query(sql).split("\n")
    result = RemoveEmptyLinesInList(result)
    try:
        result = result[1]
        result2 = RemoveEmptyLinesInList(result.split("\t"))
        if (result2[1] == hashresult):
            encoded_jwt = jwt.encode({username: username, "timestamp": str(int(time.time())), "role": result2[2]}, 'yo58q8oBYIYI35v2yb010U9RW84YOsdf832T7IUEJGS', algorithm='HS256')
            generatedtoken = ""
            try:
                generatedtoken = encoded_jwt.decode()
            except:
                generatedtoken = encoded_jwt
            dic = {}
            dic['id'] = result2[0]
            dic['result'] = "1"
            dic['role'] = result2[2]
            dic['token'] = generatedtoken
            insertlist = []
            insertlist.append(result2[0])
            insertlist.append(str(int(time.time())))
            GeneralInsert(insertlist, "login_history")
            return json.dumps(dic)
        else:
            dic = {}
            dic['result'] = "0"
            return json.dumps(dic)
    except:
        dic = {}
        dic['result'] = "0"
        return json.dumps(dic)


#-------------------------Logic part-------------------------

if __name__ == "__main__":
    # ————————SQLike, if you don't nood you can remove it————————
    global sqlikesock
    sqlikesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sqlikesock.connect(('127.0.0.1', 1234))
        print("SQLike Server Connected!")
    except:
        print("Failed to Connect SQLike DB Server")
    # ————————SQLike, if you don't nood you can remove it————————
run(HTTPServer, S, 8081)
