from http.server import BaseHTTPRequestHandler,HTTPServer
import os
from os import curdir, sep, path
import cgi
import __main__
import _thread
from datetime import datetime
import hashlib
from bin.both.log import LogginSystem as logsys
from bin.both.dbcon import dbmanager
import http.cookies
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from bin.both.config import config_var
from pathlib import Path
import random
from bin.both.sendmail import mail
from bin.both.dbconfig import dbconf

PORT_NUMBER = config_var('WEB', 'PORT')
API_PORT_NUMBER = config_var('API', 'PORT')

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
	
        log = logsys('http')
        log.write(str(self.client_address[0]) + ' - "' + str(self.requestline) + '"')

        if self.path=="/":
            self.path="/index.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            haederfooter = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if "/panel" in self.path and self.path.endswith(".html") == True:
                if self.get_session('userid') == False:
                    self.send_response(301)
                    self.send_header('Location','../../index.html')
                    self.end_headers()
                    return
                haederfooter = True
            elif "/panel" not in self.path and self.path.endswith(".html") == True:
                if self.get_session('userid') != False:
                    self.send_response(301)
                    self.send_header('Location','/panel/index.html')
                    self.end_headers()
                    return
				
            if self.path == "/logout":
                self.send_response(301)
                self.remove_session('userid')
                self.remove_session('username')
                self.send_header('Location','index.html')
                self.end_headers()
                return
				
            if sendReply == True:
                script_dir = os.path.dirname(__file__)
                rel_path = "../../web"
                web_folder_path = os.path.join(script_dir, rel_path)
                if haederfooter == True:
                    html = open(web_folder_path + "/panel/includes/header.html", "rb").read()
                    html = html + open(web_folder_path + self.path, "rb").read()
                    html = html + open(web_folder_path + "/panel/includes/footer.html", "rb").read()
                else:
                    html = open(web_folder_path + self.path, "rb").read()
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.send_header('X-APIPORT',API_PORT_NUMBER)
                self.end_headers()
                self.wfile.write(html)
            return

        except IOError:
            script_dir = os.path.dirname(__file__)
            rel_path = "../../web/error_docs/404.html"
            abs_file_path = os.path.join(script_dir, rel_path)
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(open(abs_file_path, "rb").read())

    #Handler for the POST requests
    def do_POST(self):

        log = logsys('http')
        log.write(str(self.client_address[0]) + ' - "' + str(self.requestline) + '"')

        if self.path=="/login":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
				
            passwordhash = hashlib.sha512(str(form['password'].value).encode('utf8')).hexdigest()
				
            db = dbmanager()
            qry = db.query("SELECT id, username, password FROM '143_users' WHERE username='" + str(form['username'].value) + "' AND password='" + passwordhash + "';")
            result = qry.fetchone()
            if result != None:
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db = dbmanager()
                qry = db.query("UPDATE '143_users' SET last_login='"+ str(date) +"' WHERE id='" + str(result[0]) + "';")
                self.send_response(301)
                self.create_session('userid', result[0], 86400)
                self.create_session('username', result[1], 86400)
                self.send_header('Location','/panel/index.html')
                self.end_headers()
            else:
                self.send_response(301)
                self.send_header('Location','index.html')
                self.end_headers()
            return
        elif self.path=="/forgotten":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

            username = form['username'].value
            
            code = random.randint(100000, 1000000)
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db = dbmanager()
            qry = db.query("SELECT COUNT(*) FROM '143_users' WHERE username='" + str(username) + "' OR email = '" + str(username) + "';")
            result = qry.fetchone()
            if result[0] > 0:
                qry = db.query("SELECT id,email FROM '143_users' WHERE username='" + str(username) + "' OR email = '" + str(username) + "';")
                result = qry.fetchone()
                db.query("INSERT INTO '143_pwreset' (userid, authcode, req_date) VALUES ('" + str(result[0]) + "','" + str(code) + "','" + str(date) + "');")
                mail(str(result[1]), "Password Reset", "Your Reset Code is: "+ str(code))
                self.send_response(301)
                self.send_header('Location','forgot_password_auth.html')
                self.create_session('reset_userid', str(result[0]), 1200)
                self.end_headers()
                return  
            else:
                self.send_response(301)
                db.query("DELETE FROM '143_pwreset' WHERE userid='" + self.get_session('reset_userid') + "';")
                self.remove_session('reset_userid')
                self.remove_session('reset_auth')
                self.send_header('Location','index.html')
                self.end_headers()
        elif self.path=="/forgottenauth":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

            if self.get_session('reset_userid') != False:
                code = form['code'].value
                
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_pwreset' WHERE userid = '" + self.get_session('reset_userid') + "' AND authcode = '" + str(code) + "';")
                result = qry.fetchone()
                if result[0] > 0:
                    qry = db.query("SELECT req_date FROM '143_pwreset' WHERE userid = '" + self.get_session('reset_userid') + "' AND authcode = '" + str(code) + "';")
                    result = qry.fetchone()
                    crdatetime = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
                    timebetween = datetime.now() - crdatetime
                    if timebetween.seconds < 1200:
                        self.send_response(301)
                        self.send_header('Location','forgot_password_set.html')
                        self.create_session('reset_auth', "True", 1200)
                        self.end_headers()
                        return 
                    else:
                        print("REQUEST TOO OLD!")
                        self.send_response(301)
                        db.query("DELETE FROM '143_pwreset' WHERE userid='" + self.get_session('reset_userid') + "';")
                        self.remove_session('reset_userid')
                        self.remove_session('reset_auth')
                        self.send_header('Location','index.html')
                        self.end_headers()
                else:
                    self.send_response(301)
                    db.query("DELETE FROM '143_pwreset' WHERE userid='" + self.get_session('reset_userid') + "';")
                    self.remove_session('reset_userid')
                    self.remove_session('reset_auth')
                    self.send_header('Location','index.html')
                    self.end_headers()
            else:
                self.send_response(301)
                db.query("DELETE FROM '143_pwreset' WHERE userid='" + self.get_session('reset_userid') + "';")
                self.remove_session('reset_userid')
                self.remove_session('reset_auth')
                self.send_header('Location','index.html')
                self.end_headers()
        elif self.path=="/forgottenset":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

            if self.get_session('reset_userid') != False:
                if self.get_session('reset_auth') != False:
                    db = dbmanager()
                    qry = db.query("SELECT req_date FROM '143_pwreset' WHERE userid = '" + self.get_session('reset_userid') + "';")
                    result = qry.fetchone()
                    crdatetime = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
                    timebetween = datetime.now() - crdatetime
                    if timebetween.seconds < 1200:
                        password = form['password'].value
                        passwordhash = hashlib.sha512(str(password).encode('utf8')).hexdigest()
                        db = dbmanager()
                        db.query("UPDATE '143_users' SET password = '" + passwordhash + "' WHERE id = '" + self.get_session('reset_userid') + "';")
                        db.query("DELETE FROM '143_pwreset' WHERE userid='" + self.get_session('reset_userid') + "';")
                        self.send_response(301)
                        self.remove_session('reset_userid')
                        self.remove_session('reset_auth')
                        self.send_header('Location','index.html')
                        self.end_headers()
                    else:
                        print("REQUEST TOO OLD!")
                        self.send_response(301)
                        db.query("DELETE FROM '143_pwreset' WHERE userid='" + self.get_session('reset_userid') + "';")
                        self.remove_session('reset_userid')
                        self.remove_session('reset_auth')
                        self.send_header('Location','index.html')
                        self.end_headers()
                else:
                    self.send_response(301)
                    db.query("DELETE FROM '143_pwreset' WHERE userid='" + self.get_session('reset_userid') + "';")
                    self.remove_session('reset_userid')
                    self.remove_session('reset_auth')
                    self.send_header('Location','index.html')
                    self.end_headers()
            else:
                self.send_response(301)
                db.query("DELETE FROM '143_pwreset' WHERE userid='" + self.get_session('reset_userid') + "';")
                self.remove_session('reset_userid')
                self.remove_session('reset_auth')
                self.send_header('Location','index.html')
                self.end_headers()
        else:
            script_dir = os.path.dirname(__file__)
            rel_path = "../../web/error_docs/404.html"
            abs_file_path = os.path.join(script_dir, rel_path)
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(open(abs_file_path, "rb").read())
			
    def create_cookie(self, name, value, expire):
        try:
            cookie = http.cookies.SimpleCookie()
            cookie[name] = str(value)
            cookie[name]['max-age'] = expire
            self.send_header('Set-Cookie', cookie.output(header=''))
            return True
        except:
            return False

    def get_cookie(self, name):
        try:
            cookie = http.cookies.SimpleCookie(self.headers["Cookie"])
            value = cookie[name].value
            return value
        except:
            return False
		
    def remove_cookie(self, name):
        try:
            cookie = http.cookies.SimpleCookie()
            cookie[name] = ''
            cookie[name]['max-age'] = 1
            self.send_header('Set-Cookie', cookie.output(header=''))
            return True
        except:
            return False

    def create_session(self, name, value, expire):
        try:
            dt = datetime.now()
            hash = str(hashlib.md5(str(dt.microsecond).encode('utf8')).hexdigest())
            cookie = http.cookies.SimpleCookie()
            cookie['session_'+name] = hash
            self.send_header('Set-Cookie', cookie.output(header=''))
            script_dir = os.path.dirname(__file__)
            rel_path = "../../tmp/session_"+hash
            session_file_path = os.path.join(script_dir, rel_path)
            f = open(session_file_path, 'w+')
            f.write(name+'\n'+str(value))
            f.close()
            return True
        except:
            return False

    def get_session(self, name):
        try:
            cookie = http.cookies.SimpleCookie(self.headers["Cookie"])
            hash = cookie['session_'+name].value
            script_dir = os.path.dirname(__file__)
            rel_path = "../../tmp/session_"+str(hash)
            session_file_path = os.path.join(script_dir, rel_path)
            f = open(session_file_path, 'r')
            content = f.read()
            f.close()
            value = content.split('\n')[1]
            return value
        except:
            return False
		
    def remove_session(self, name):
        try:
            cookie = http.cookies.SimpleCookie(self.headers["Cookie"])
            hash = cookie['session_'+name].value
            script_dir = os.path.dirname(__file__)
            rel_path = "../../tmp/session_"+str(hash)
            session_file_path = os.path.join(script_dir, rel_path)
            os.remove(session_file_path)
            cookie = http.cookies.SimpleCookie()
            cookie['session_'+name] = ''
            cookie['session_'+name]['max-age'] = 1
            self.send_header('Set-Cookie', cookie.output(header=''))
            return True
        except:
            return False
        
file_dir = os.path.dirname(__file__)
rel_path = "../../tmp/"
tmp_folder_path = Path(os.path.join(file_dir, rel_path))
if tmp_folder_path.is_dir() == False:
    os.makedirs(tmp_folder_path)

server = HTTPServer(('', int(PORT_NUMBER)), myHandler)
log = logsys('http')
log.write('Started Webserver on Port: ' + str(PORT_NUMBER))
_thread.start_new_thread(server.serve_forever, ())