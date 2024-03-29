from http.server import BaseHTTPRequestHandler,HTTPServer
import os
from os import curdir, sep, path
import cgi
import __main__
import _thread
from datetime import datetime
import hashlib
from bin.both.log import LogginSystem as logsys
import platform
from bin.both.dbcon import dbmanager
import http.cookies
from bin.both.config import config_var
from pathlib import Path
import hashlib

LISTENON = config_var('LOCAL', 'LISTEN')
PORT_NUMBER = config_var('API', 'PORT')
WEB_PORT_NUMBER = config_var('WEB', 'PORT')

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        log = logsys('api')
        log.write(str(self.client_address[0]) + ' - "' + str(self.requestline) + '"')

        xmlheader = '<?xml version="1.0" encoding="UTF-8"?>'

        if self.get_session('userid') != False:
            ############################################
            # GET INFORMATIONS (Pool, Backup, Task)    #
            ############################################
            #GET POOL
            if self.path=="/get/pools":
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_pool' WHERE ownerid = '" + self.get_session('userid') + "';")
                count_pools = qry.fetchone()
                response = "<response>"
                response = response + "<info>"
                response = response + "<status>OK</status>"
                response = response + "</info>"
                response = response + "<data>"
                response = response + "<amount>" + str(count_pools[0]) + "</amount>"
                response = response + "<pools>"
                qry = db.query("SELECT id,name,system,host,port,username,password,path,ownerid FROM '143_pool' WHERE ownerid='"+ self.get_session('userid') +"';")
                for row in qry:
                    response = response + "<pool>"
                    response = response + "<id>"+str(row[0])+"</id>"
                    response = response + "<name>"+str(row[1])+"</name>"
                    response = response + "<system>"+str(row[2])+"</system>"
                    response = response + "<host>"+str(row[3])+"</host>"
                    response = response + "<port>"+str(row[4])+"</port>"
                    response = response + "<username>"+str(row[5])+"</username>"
                    response = response + "<password>"+str(row[6])+"</password>"
                    response = response + "<path>"+str(row[7])+"</path>"
                    response = response + "<ownerid>"+str(row[8])+"</ownerid>"
                    response = response + "</pool>"
                response = response + "</pools>"
                response = response + "</data>"
                response = response + "</response>"
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Successful: Sending pools!"))
            #GET POOLLIST
            elif self.path=="/get/poollist":
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_pool' WHERE ownerid = '" + self.get_session('userid') + "';")
                count_pools = qry.fetchone()
                response = "<response>"
                response = response + "<info>"
                response = response + "<status>OK</status>"
                response = response + "</info>"
                response = response + "<data>"
                response = response + "<amount>" + str(count_pools[0]) + "</amount>"
                response = response + "<pools>"
                qry = db.query("SELECT id,name FROM '143_pool' WHERE ownerid='"+ self.get_session('userid') +"';")
                for row in qry:
                    response = response + "<pool>"
                    response = response + "<id>"+str(row[0])+"</id>"
                    response = response + "<name>"+str(row[1])+"</name>"
                    response = response + "</pool>"
                response = response + "</pools>"
                response = response + "</data>"
                response = response + "</response>"
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Successful: Sending poollist!"))
            #GET BACKUP
            elif self.path=="/get/backups":
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_backups' b INNER JOIN '143_pool' p on b.pool_src = p.id WHERE p.ownerid = '" + self.get_session('userid') + "';")
                count_backups = qry.fetchone()
                response = "<response>"
                response = response + "<info>"
                response = response + "<status>OK</status>"
                response = response + "</info>"
                response = response + "<data>"
                response = response + "<amount>" + str(count_backups[0]) + "</amount>"
                response = response + "<backups>"
                qry = db.query("SELECT b.id, b.pool_src, b.pool_dst, b.compare, b.encrypt, b.compression FROM '143_backups' b INNER JOIN '143_pool' p on b.pool_src = p.id WHERE p.ownerid = '" + self.get_session('userid') + "';")
                for row in qry:
                    response = response + "<backup>"
                    response = response + "<id>"+str(row[0])+"</id>"
                    response = response + "<pool_src>"+str(row[1])+"</pool_src>"
                    response = response + "<pool_dst>"+str(row[2])+"</pool_dst>"
                    response = response + "<compare>"+str(row[3])+"</compare>"
                    response = response + "<encrypt>"+str(row[4])+"</encrypt>"
                    response = response + "<compression>"+str(row[5])+"</compression>"
                    response = response + "</backup>"
                response = response + "</backups>"
                response = response + "</data>"
                response = response + "</response>"
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Successful: Sending backups!"))
            # GET TASKS
            elif self.path=="/get/tasks":
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + self.get_session('userid') + "' AND t.state = 'running';")
                count_running = qry.fetchone()
                qry = db.query("SELECT COUNT(*) FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + self.get_session('userid') + "' AND t.state = 'waiting';")
                count_waiting = qry.fetchone()
                qry = db.query("SELECT COUNT(*) FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + self.get_session('userid') + "' AND t.state = 'failed';")
                count_failed = qry.fetchone()
                response = "<response>"
                response = response + "<info>"
                response = response + "<status>OK</status>"
                response = response + "</info>"
                response = response + "<data>"
                response = response + "<running>" + str(count_running[0]) + "</running>"
                response = response + "<waiting>" + str(count_waiting[0]) + "</waiting>"
                response = response + "<failed>" + str(count_failed[0]) + "</failed>"
                response = response + "<tasks>"
                qry = db.query("SELECT t.id,t.name,t.action,t.schedule,t.last_run,t.state,t.backupid,t.backuptyp,t.backupfilesid FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + self.get_session('userid') + "';")
                for row in qry:
                    response = response + "<task>"
                    response = response + "<id>"+str(row[0])+"</id>"
                    response = response + "<name>"+str(row[1])+"</name>"
                    response = response + "<action>"+str(row[2])+"</action>"
                    response = response + "<schedule>"+str(row[3])+"</schedule>"
                    response = response + "<last_run>"+str(row[4])+"</last_run>"
                    response = response + "<state>"+str(row[5])+"</state>"
                    response = response + "<backupid>"+str(row[6])+"</backupid>"
                    response = response + "<backuptyp>"+str(row[7])+"</backuptyp>"
                    response = response + "<backupfilesid>"+str(row[8])+"</backupfilesid>"
                    response = response + "</task>"
                response = response + "</tasks>"
                response = response + "</data>"
                response = response + "</response>"
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Successful: Sending tasks!"))
            # GET RESTORES
            elif self.path=="/get/restores":
                db = dbmanager()
                response = "<response>"
                response = response + "<info>"
                response = response + "<status>OK</status>"
                response = response + "</info>"
                response = response + "<data>"
                response = response + "<restores>"
                qry = db.query("SELECT t.id,t.name,t.state,t.backupid,t.backuptyp,t.backupfilesid FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + self.get_session('userid') + "' AND t.action='restore';")
                for row in qry:
                    response = response + "<restore>"
                    response = response + "<id>"+str(row[0])+"</id>"
                    response = response + "<name>"+str(row[1])+"</name>"
                    response = response + "<state>"+str(row[2])+"</state>"
                    response = response + "<backupid>"+str(row[3])+"</backupid>"
                    response = response + "<backuptyp>"+str(row[4])+"</backuptyp>"
                    response = response + "<backupfilesid>"+str(row[5])+"</backupfilesid>"
                    response = response + "</restore>"
                response = response + "</restores>"
                response = response + "</data>"
                response = response + "</response>"
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Successful: Sending Restores!"))
            else:
                response = "<response>"
                response = response + "<status>ERROR</status>"
                response = response + "<message>Unknown Parameter</message>"
                response = response + "</response>"
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Unknown Request parameter!"))
        else:
            response = "<response>"
            response = response + "<status>ERROR</status>"
            response = response + "<message>Unauthorized</message>"
            response = response + "</response>"
            self.send_response(401)
            self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
            self.send_header('Access-Control-Allow-Credentials','true')
            self.send_header('Content-type','text/xml')
            self.end_headers()
            self.wfile.write(bytes(xmlheader + response, 'utf8'))
            log = logsys('api')
            log.write(str("Unauthorized Access!"))
            print("Unauthorized Access!")
            

    def do_POST(self):

        log = logsys('http')
        log.write(str(self.client_address[0]) + ' - "' + str(self.requestline) + '"')
		
        xmlheader = '<?xml version="1.0" encoding="UTF-8"?>'
		
        if self.get_session('userid') != False:
            ############################################################
            # GET INFORMATIONS FOR SPECIFIC ID (Pool, Backup, Task)    #
            ############################################################
            # USER CHANGE PASSWORD
            if self.path=="/post/changepw":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
                    
                userid = self.get_session('userid')
                passwordhash = hashlib.sha512(str(form['password'].value).encode('utf8')).hexdigest()
                
                db = dbmanager()
                qry = db.query("UPDATE '143_users' SET password = '"+passwordhash+"' WHERE id = '"+userid+"';")
                
                response = "<response>"
                response = response + "<info>"
                response = response + "<status>OK</status>"
                response = response + "</info>"
                response = response + "<data>"
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Successful: Changing Password!"))
            
            # USER CHANGE EMAIL
            elif self.path=="/post/changemail":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
                    
                userid = self.get_session('userid')
                email = str(form['email'].value)
                
                db = dbmanager()
                qry = db.query("UPDATE '143_users' SET email = '"+email+"' WHERE id = '"+userid+"';")
                
                response = "<response>"
                response = response + "<info>"
                response = response + "<status>OK</status>"
                response = response + "</info>"
                response = response + "<data>"
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Successful: Changing Password!"))
            # GET TASKLOG FOR TASK
            elif self.path=="/post/tasklog":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                taskid = form['id'].value
                userid = self.get_session('userid')
                
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + userid + "' AND t.id = '" + taskid + "';")
                usercheck = qry.fetchone()
                
                if(usercheck[0] == 1):
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "<data>"
                    response = response + "<messages>"
                    qry = db.query("SELECT date,taskid,value FROM '143_tasklog' WHERE taskid='"+taskid+"' ORDER BY date DESC LIMIT 80;")
                    for row in qry:
                        response = response + "<message>"
                        response = response + "<datetime>"+str(row[0])+"</datetime>"
                        response = response + "<taskid>"+str(row[1])+"</taskid>"
                        response = response + "<value>"+str(row[2])+"</value>"
                        response = response + "</message>"
                    response = response + "</messages>"
                    response = response + "</data>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Sending tasklog!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>This Task doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Tasklog not found for user!"))
            # GET BACKUPFILESLIST BY TASKID
            elif self.path == "/post/backupfileslistbytask":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                taskid = form['taskid'].value
                userid = self.get_session('userid')
                
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + userid + "' AND t.id = '" + taskid + "';")
                usercheck = qry.fetchone()
                
                if(usercheck[0] == 1):
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "<data>"
                    response = response + "<backupfiles>"
                    qry = db.query("SELECT id,date,taskid,state,path FROM '143_backupfiles' WHERE taskid='"+taskid+"' ORDER BY date DESC LIMIT 80;")
                    for row in qry:
                        response = response + "<backupfile>"
                        response = response + "<id>"+str(row[0])+"</id>"
                        response = response + "<date>"+str(row[1])+"</date>"
                        response = response + "<taskid>"+str(row[2])+"</taskid>"
                        response = response + "<state>"+str(row[3])+"</state>"
                        response = response + "<path>"+str(row[4])+"</path>"
                        response = response + "</backupfile>"
                    response = response + "</backupfiles>"
                    response = response + "</data>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Sending Backupfilelist!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>This Task doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Backupfilelist not found for user!"))
            # GET TASKS BY BACKUP ID
            elif self.path=="/post/backuptasks":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                backupid = form['id'].value
                userid = self.get_session('userid')
                
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_backups' b INNER JOIN '143_pool' p ON b.pool_src = p.id WHERE b.id = '" + backupid + "' AND p.ownerid = '" + userid + "';")
                usercheck = qry.fetchone()
                
                if(usercheck[0] == 1):
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "<data>"
                    response = response + "<backupid>"+backupid+"</backupid>"
                    response = response + "<tasks>"
                    qry = db.query("SELECT id,name,action,schedule,last_run,state,backupid,backuptyp,backupfilesid FROM '143_tasks' WHERE backupid='"+backupid+"' AND action='backup' ORDER BY 'id' DESC LIMIT 80;")
                    for row in qry:
                        response = response + "<task>"
                        response = response + "<id>"+str(row[0])+"</id>"
                        response = response + "<name>"+str(row[1])+"</name>"
                        response = response + "<action>"+str(row[2])+"</action>"
                        response = response + "<schedule>"+str(row[3])+"</schedule>"
                        response = response + "<last_run>"+str(row[4])+"</last_run>"
                        response = response + "<state>"+str(row[5])+"</state>"
                        response = response + "<backupid>"+str(row[6])+"</backupid>"
                        response = response + "<backuptyp>"+str(row[7])+"</backuptyp>"
                        response = response + "<backupfilesid>"+str(row[8])+"</backupfilesid>"
                        response = response + "</task>"
                    response = response + "</tasks>"
                    response = response + "</data>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Sending backuptasks!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>This Backup doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Backuptasks not found for user!"))
            ###########################################
            # CREATE COMMANDS (Pool, Backup, Task)    #
            ###########################################
            # CREATE POOL
            elif self.path=="/post/createpool":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                name = form['name'].value
                system = form['system'].value
                    
                try:
                    host = form['host'].value
                except KeyError:
                    host = ""
                    
                try:
                    port = form['port'].value
                except KeyError:
                    port = ""
                    
                try:
                    username = form['username'].value
                except KeyError:
                    username = ""
                    
                try:
                    password = form['password'].value
                except KeyError:
                    password = ""

                path = form['path'].value
                userid = self.get_session('userid')

                db = dbmanager()
                qry = db.query("INSERT INTO '143_pool' (name,system,host,port,username,password,path,ownerid) VALUES ('"+name+"','"+system+"','"+host+"','"+port+"','"+username+"','"+password+"','"+path+"','"+userid+"');")
				
                response = "<response>"
                response = response + "<info>"
                response = response + "<status>OK</status>"
                response = response + "</info>"
                response = response + "</response>"
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Successful: Created Pool!"))
            # CREATE BACKUP
            elif self.path=="/post/createbackup":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                pool_src = form['pool_src'].value
                pool_dst = form['pool_dst'].value
                compare = form['compare'].value
                encrypt = form['encrypt'].value
                compression = form['compression'].value
                userid = self.get_session('userid')
                
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_pool' WHERE ownerid='"+userid+"' AND id='"+pool_src+"';")
                checkdependency_src = qry.fetchone()
                qry = db.query("SELECT COUNT(*) FROM '143_pool' WHERE ownerid='"+userid+"' AND id='"+pool_dst+"';")
                checkdependency_dst = qry.fetchone()
                
                if checkdependency_src[0] == 1 and checkdependency_dst[0] == 1:
                    qry = db.query("INSERT INTO '143_backups' (pool_src,pool_dst,compare,encrypt,compression) VALUES ('"+pool_src+"','"+pool_dst+"','"+compare+"','"+encrypt+"','"+compression+"');")
                    
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Created Backup!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>The Pool you selected doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Pool not found for user!"))
            # CREATE BACKUP TASK
            elif self.path=="/post/createbackuptask":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                name = form['name'].value
                backupid = form['backupid'].value
                backuptyp = form['backuptyp'].value
                time = form['time'].value
                days = form['days'].value
                userid = self.get_session('userid')
                    
                time = time.split(":")

                cron = time[1] + " " + time[0] + " * * " + days
				
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_backups' b INNER JOIN '143_pool' p ON b.pool_src = p.id WHERE p.ownerid='"+userid+"' AND b.id='"+backupid+"';")
                checkdependency = qry.fetchone()
                
                if checkdependency[0] == 1:
                    qry = db.query("INSERT INTO '143_tasks' (name,action,schedule,state,backupid,backuptyp) VALUES ('"+name+"','backup','"+cron+"','waiting','"+backupid+"', '"+backuptyp+"');")
                    
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Created Backup Task!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>The Backup you selected doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Backup not found for user!"))
            # CREATE RESTORE TASK
            elif self.path=="/post/createrestoretask":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                taskid = form['taskid'].value
                backupfile = form['backupfile'].value
                userid = self.get_session('userid')
				
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_tasks' t INNER JOIN '143_backups' b ON t.backupid = b.id INNER JOIN '143_pool' p ON b.pool_src = p.id WHERE p.ownerid='"+userid+"' AND t.id='"+taskid+"';")
                checkdependency_task = qry.fetchone()
                qry = db.query("SELECT COUNT(*) FROM '143_backupfiles' bf INNER JOIN '143_tasks' t ON bf.taskid = t.id INNER JOIN '143_backups' b ON t.backupid = b.id INNER JOIN '143_pool' p ON b.pool_src = p.id WHERE p.ownerid='"+userid+"' AND bf.id='"+backupfile+"';")
                checkdependency_backupfile = qry.fetchone()
                
                if checkdependency_task[0] == 1 and checkdependency_backupfile[0] == 1:
                    qry = db.query("SELECT name,backupid FROM '143_tasks' WHERE id = '" + taskid + "';")
                    taskinfo = qry.fetchone()
                    qry = db.query("SELECT date FROM '143_backupfiles' WHERE id = '" + backupfile + "';")
                    backupfileinfo = qry.fetchone()
                    name = "Restore backup "+str(taskinfo[0])+" from "+str(backupfileinfo[0])
                    qry = db.query("INSERT INTO '143_tasks' (name,action,state,backupid,backupfilesid) VALUES ('"+str(name)+"','restore','waiting','"+str(taskinfo[1])+"', '"+str(backupfile)+"');")
                    
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Created Restore Task!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>The Backup you selected doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Backup not found for user!"))
            ##########################################
            # UPDATE COMMAND (Pool, Backup, Task)    #
            ##########################################
            # UPDATE POOL
            elif self.path=="/post/updatepool":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                id = form['id'].value
                name = form['name'].value
                system = form['system'].value
                path = form['path'].value
                try:
                    host = form['host'].value
                except KeyError:
                    host = ""
                    
                try:
                    port = form['port'].value
                except KeyError:
                    port = ""
                    
                try:
                    username = form['username'].value
                except KeyError:
                    username = ""
                    
                try:
                    password = form['password'].value
                except KeyError:
                    password = ""
                
                userid = self.get_session('userid')
				
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_pool' WHERE ownerid = '" + userid + "' AND id = '" + id +"';")
                usercheck = qry.fetchone()
                
                if(usercheck[0] == 1):
                    qry = db.query("UPDATE '143_pool' SET name='"+name+"', system='"+system+"', host='"+host+"', port='"+port+"', username='"+username+"', password='"+password+"', path='"+path+"' WHERE id='"+id+"' AND ownerid='"+userid+"';")
                    
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "<data>"
                    response = response + "<id>"+id+"</id>"
                    response = response + "</data>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Updated Pool!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>This Pool doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Pool not found for user!"))
            # UPDATE BACKUP
            elif self.path=="/post/updatebackup":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                id = form['id'].value
                pool_src = form['pool_src'].value
                pool_dst = form['pool_dst'].value
                compare = form['compare'].value
                encrypt = form['encrypt'].value
                compression = form['compression'].value
                userid = self.get_session('userid')
				
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_backups' b INNER JOIN '143_pool' p ON b.pool_src = p.id WHERE b.id = '" + id + "' AND p.ownerid = '" + userid + "';")
                usercheck = qry.fetchone()
                
                if(usercheck[0] == 1):
                    qry = db.query("SELECT COUNT(*) FROM '143_pool' WHERE ownerid='"+userid+"' AND id='"+pool_src+"';")
                    checkdependency_src = qry.fetchone()
                    qry = db.query("SELECT COUNT(*) FROM '143_pool' WHERE ownerid='"+userid+"' AND id='"+pool_dst+"';")
                    checkdependency_dst = qry.fetchone()
                    
                    if checkdependency_src[0] == 1 and checkdependency_dst[0] == 1:
                        qry = db.query("UPDATE '143_backups' SET pool_src='"+pool_src+"',pool_dst='"+pool_dst+"',compare='"+compare+"',encrypt='"+encrypt+"',compression='"+compression+"' WHERE id='"+id+"';")
                        
                        response = "<response>"
                        response = response + "<info>"
                        response = response + "<status>OK</status>"
                        response = response + "</info>"
                        response = response + "<data>"
                        response = response + "<id>"+id+"</id>"
                        response = response + "</data>"
                        response = response + "</response>"
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                        self.send_header('Access-Control-Allow-Credentials','true')
                        self.send_header('Content-type','text/xml')
                        self.end_headers()
                        self.wfile.write(bytes(xmlheader + response, 'utf8'))
                        log = logsys('api')
                        log.write(str("Successful: Updated Backup!"))
                    else:
                        response = "<response>"
                        response = response + "<info>"
                        response = response + "<status>ERROR</status>"
                        response = response + "<message>The Pool you selected doesn't exist or doesn't belong to you!</message>"
                        response = response + "</info>"
                        response = response + "</response>"
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                        self.send_header('Access-Control-Allow-Credentials','true')
                        self.send_header('Content-type','text/xml')
                        self.end_headers()
                        self.wfile.write(bytes(xmlheader + response, 'utf8'))
                        log = logsys('api')
                        log.write(str("ERROR: Pool not found for user!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>This Backup doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Backup not found for user!"))
            # UPDATE TASK
            elif self.path=="/post/updatetask":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
					
                id = form['id'].value
                name = form['name'].value
                backuptyp = form['backuptyp'].value
                time = form['time'].value
                days = form['days'].value
                userid = self.get_session('userid')
				
                time = time.split(":")

                cron = time[1] + " " + time[0] + " * * " + days
                
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + userid + "' AND t.id = '" + id + "';")
                usercheck = qry.fetchone()
                
                if(usercheck[0] == 1):
                    qry = db.query("UPDATE '143_tasks' SET name='"+name+"',schedule='"+cron+"',backuptyp='"+backuptyp+"' WHERE id='"+id+"';")
                    
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "<data>"
                    response = response + "<id>"+id+"</id>"
                    response = response + "</data>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Updated Task!"))
                else:
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>This Task doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Task not found for user!"))
            ###########################################
            # DELETE COMMANDS (Pool, Backup, Task)    #
            ###########################################
            # DELETE POOL
            elif self.path=="/post/deletepool":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                id = form['id'].value
                userid = self.get_session('userid')
				
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_pool' WHERE ownerid = '" + userid + "' AND id = '" + id +"';")
                usercheck = qry.fetchone()
				
                if(usercheck[0] == 1):
				
                    qry = db.query("SELECT COUNT(*) FROM '143_backups' WHERE pool_src = '" + id + "' OR pool_dst = '" + id + "';")
                    usedbycount = qry.fetchone()
                
                    if usedbycount[0] == 0:
				
                        qry = db.query("DELETE FROM '143_pool' WHERE id='"+id+"';")
				
                        response = "<response>"
                        response = response + "<info>"
                        response = response + "<status>OK</status>"
                        response = response + "</info>"
                        response = response + "<data>"
                        response = response + "<id>"+id+"</id>"
                        response = response + "</data>"
                        response = response + "</response>"
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                        self.send_header('Access-Control-Allow-Credentials','true')
                        self.send_header('Content-type','text/xml')
                        self.end_headers()
                        self.wfile.write(bytes(xmlheader + response, 'utf8'))
                        log = logsys('api')
                        log.write(str("Successful: Deleted Pool!"))
					
                    else:
				
                        response = "<response>"
                        response = response + "<info>"
                        response = response + "<status>ERROR</status>"
                        response = response + "<message>This Pool is currently used by a Backup. Please delete Backup first!</message>"
                        response = response + "</info>"
                        response = response + "</response>"
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                        self.send_header('Access-Control-Allow-Credentials','true')
                        self.send_header('Content-type','text/xml')
                        self.end_headers()
                        self.wfile.write(bytes(xmlheader + response, 'utf8'))
                        log = logsys('api')
                        log.write(str("ERROR: Pool is currently used by Backup!"))

                else:

                        response = "<response>"
                        response = response + "<info>"
                        response = response + "<status>ERROR</status>"
                        response = response + "<message>This Pool doesn't exist or doesn't belong to you!</message>"
                        response = response + "</info>"
                        response = response + "</response>"
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                        self.send_header('Access-Control-Allow-Credentials','true')
                        self.send_header('Content-type','text/xml')
                        self.end_headers()
                        self.wfile.write(bytes(xmlheader + response, 'utf8'))
                        log = logsys('api')
                        log.write(str("ERROR: Pool not found for user!"))
            # DELETE BACKUP
            elif self.path=="/post/deletebackup":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                id = form['id'].value
                userid = self.get_session('userid')
				
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_backups' b INNER JOIN '143_pool' p ON b.pool_src = p.id WHERE b.id = '" + id + "' AND p.ownerid = '" + userid + "';")
                usercheck = qry.fetchone()
				
                if(usercheck[0] == 1):

                    qry = db.query("DELETE FROM '143_backups' WHERE id='"+id+"';")
                    qry = db.query("DELETE FROM '143_tasks' WHERE backupid='"+id+"';")
                    
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "<data>"
                    response = response + "<id>"+id+"</id>"
                    response = response + "</data>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Deleted Backup!"))
                    
                else:
                
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>This Backup doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Backup not found for user!"))
            # DELETE TASK
            elif self.path=="/post/deletetask":
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

                id = form['id'].value
                userid = self.get_session('userid')
				
                db = dbmanager()
                qry = db.query("SELECT COUNT(*) FROM '143_tasks' t INNER JOIN '143_backups' bu on t.backupid = bu.id INNER JOIN '143_pool' p on bu.pool_src = p.id WHERE p.ownerid = '" + userid + "' AND t.id = '" + id + "';")
                usercheck = qry.fetchone()
				
                if(usercheck[0] == 1):
                
                    qry = db.query("DELETE FROM '143_tasks' WHERE id='"+id+"';")
                    
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>OK</status>"
                    response = response + "</info>"
                    response = response + "<data>"
                    response = response + "<id>"+id+"</id>"
                    response = response + "</data>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("Successful: Deleted Task!"))
                    
                else:
                
                    response = "<response>"
                    response = response + "<info>"
                    response = response + "<status>ERROR</status>"
                    response = response + "<message>This Task doesn't exist or doesn't belong to you!</message>"
                    response = response + "</info>"
                    response = response + "</response>"
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                    self.send_header('Access-Control-Allow-Credentials','true')
                    self.send_header('Content-type','text/xml')
                    self.end_headers()
                    self.wfile.write(bytes(xmlheader + response, 'utf8'))
                    log = logsys('api')
                    log.write(str("ERROR: Task not found for user!"))
                
            else:
                response = "<response>"
                response = response + "<status>ERROR</status>"
                response = response + "<message>Unknown Parameter</message>"
                response = response + "</response>"
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
                self.send_header('Access-Control-Allow-Credentials','true')
                self.send_header('Content-type','text/xml')
                self.end_headers()
                self.wfile.write(bytes(xmlheader + response, 'utf8'))
                log = logsys('api')
                log.write(str("Unknown Request parameter!"))
        else:
            response = "<response>"
            response = response + "<status>ERROR</status>"
            response = response + "<message>Unauthorized</message>"
            response = response + "</response>"
            self.send_response(401)
            self.send_header('Access-Control-Allow-Origin', LISTENON + ':' + WEB_PORT_NUMBER)
            self.send_header('Access-Control-Allow-Credentials','true')
            self.send_header('Content-type','text/xml')
            self.end_headers()
            self.wfile.write(bytes(xmlheader + response, 'utf8'))
            log = logsys('api')
            log.write(str("Unauthorized Access!"))
            print("Unauthorized Access!")
			
			
			
			
			
			
			
			

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
        
file_dir = os.path.dirname(__file__)
rel_path = "../../tmp/"
tmp_folder_path = Path(os.path.join(file_dir, rel_path))
if tmp_folder_path.is_dir() == False:
    os.makedirs(tmp_folder_path)

server = HTTPServer(('', int(PORT_NUMBER)), myHandler)
log = logsys('http')
log.write('Started Webserver on Port: ' + str(PORT_NUMBER))
_thread.start_new_thread(server.serve_forever, ())