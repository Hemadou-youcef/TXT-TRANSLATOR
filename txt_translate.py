import sys
import os
import time
import requests
import json
import re
from bs4 import BeautifulSoup
# from parsel import Selector

# googleTranslateTKK = "448487.932609646"
googleTrans = "https://translate.googleapis.com/translate_a/t?anno=3&client=te&v=1.0&format=html&sl={}&tl={}&tk={}"
headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
class txt_translate:
    def initialisation (self):
        try:
            self.single_file = "n"
            
            while True:
                try:
                    self.novel_name = input("WRITE NOVEL NAME: ").upper()
                    if not self.novel_name :
                        self.novel_name="NOVEL"
                    for key in ['\\','/',':','?','*','<','>','|','"']:
                        self.novel_name = self.novel_name.replace(key,'')
                    self.suffix  = ""

                    os.chdir("txt_files/" + self.novel_name)
                    self.complete_name=["".join(f.split('.')[:-1]) for f in os.listdir() if f.endswith(".txt")]
                    self.complete_name.sort(key=self.natural_keys)
                    os.chdir("../..")
                    if len(self.complete_name) != 0:
                        break
                    print("there is no file here")
                except Exception as e:
                    print(e)
                

            # self.start = input("START NUMBER: ")
            # if not self.start :
            #     self.start = 1
            # else:
            #     self.start = int(self.start)
             
            # self.end = input("END NUMBER: ")
            # if not self.end :
            #     self.end = 1
            # else:
            #     self.end = int(self.end)

            self.src = input("SOURCE LANGUAGE : ").lower()
            if not self.src :
                self.src = 'auto'


            self.dest = input("DESTINATION LANGUAGE : ").lower()
            if not self.dest :
                self.dest = 'en'

            self.type = input("TXT OR HTML (DEFAULT = HTML): ").lower()
            if not self.type :
                self.type="html"
            if self.type == "txt" and len(self.complete_name) != 1:
                self.single_file = input("SINGLE FILE??: (Y/N)(DEFAULT=N): ").lower()
                if not self.type :
                    self.type="n"
            
            

            header = open("required/header.txt", "r")
            self.header = header.read()
            header.close()

            footer = open("required/footer.txt", "r")
            self.footer = footer.read()
            footer.close()

            style = open("required/style.css", "r")
            self.style = style.read()
            style.close()

            self.document_creating()
            self.translate_loop()
            if self.single_file == "y":
                os.chdir("../../translated_novel/" + self.novel_name + self.suffix )
                new_file = open(self.novel_name + ".txt", "w",encoding="utf-8")
                new_file.write(self.single_txt)
                new_file.close()
                os.chdir("../../txt_files/" + self.novel_name)
            os.chdir("../")
            os.rmdir(self.novel_name) 
            print("")
            print("DONE!!")
            print("THANK FOR USING OUR PRODUCT")
        except Exception as e:
            print("ERROR ENTRING LIGHT NOVEL")
            print(e)

    def document_creating(self):
        print("CREATING DOCUMENT...")
        try:
            if not os.path.exists('translated_novel'):
                os.mkdir('translated_novel')
            os.chdir('translated_novel')
            i = 2
            while True:
                if os.path.exists(self.novel_name + self.suffix ):
                    self.suffix  = "-" + str(i)
                    i += 1
                else:
                    os.mkdir(self.novel_name + self.suffix )
                    os.chdir(self.novel_name + self.suffix )
                    break
            if self.type == "html":
                style = open("style.css", "w",encoding="utf-8")
                style.write(self.style)
                style.close()

            print("CREATING SUCCESSFULLY")
            os.chdir("../../txt_files/" + self.novel_name)
        except Exception as e:
            print("ERROR CREATING DOCUMENT")
            print("CLOSING...")
            print(e)
            sys.exit()

    def translate_loop(self):
        range_bar = 0
        range_text = 3000
        self.single_txt= ""

        range_bar_unit = 50 / len(self.complete_name)

        current_message = "0/" + str(len(self.complete_name))
        self.progress_bar_header(current_message)
        self.session_requests = requests.session()
        for i in range(len(self.complete_name)):
            range_bar += range_bar_unit
                
            self.txt = ""
            self.temp_txt = ""
            self.txt_formdata = "q"

            try_counter = 0
            while True and try_counter <= 3: 
                if self.translate(i,range_text):
                    break
                try_counter += 1
            if try_counter == 4:
                print("error while translating")
                break
            current_message = str(i + 1) + "/" + str(len(self.complete_name))
            sys.stdout.write(" " * (self.progress - 1) + "|" + current_message + " ")
            sys.stdout.write("\b" * (self.progress + len(current_message) + 1))
                
            sys.stdout.flush()

            for j in range(int(range_bar)):
                self.progress_bar_animated()
                range_bar-= 1
        
        for i in range(len(self.complete_name)):
            os.remove(self.complete_name[i] + ".txt") 
            
        sys.stdout.write("|\n")
    def translate(self,i,range_text):
        try:
            txt = open(self.complete_name[i] + ".txt", "r",encoding="utf-8")
            txt_read = txt.read()
            txt_read_lenght = len(txt_read)
            txt.seek(0)
            if txt_read_lenght > range_text:
                for line in txt:
                    if line == '\n':
                        self.temp_txt += ""
                        self.txt_formdata += "&q"
                    else:
                        self.temp_txt += "<pre>" + line[:-1] + "</pre>"
                        self.txt_formdata += "&q=%3Cpre%3E%" + "%".join(re.findall('..',line[:-1].encode("utf-8").hex())) + "%3C%2Fpre%3E"

                    if len(self.temp_txt) > range_text:
                        self.Hash = requests.post("http://localhost:14756/",data ={'text':self.temp_txt} , timeout=10).text
                        translated_txt = self.session_requests.post(googleTrans.format(self.src,self.dest,self.Hash),data=self.txt_formdata[2:],headers=headers, timeout=50).text
                        translated_txt = json.loads(translated_txt)
                        self.txt += "\n".join(translated_txt)
                        self.temp_txt = ""
                        self.txt_formdata = 'q'
            else:
                for line in txt:
                    if line == '\n':
                        self.temp_txt += ""
                        self.txt_formdata += "&q"
                    else:
                        self.temp_txt += "<pre>" + line[:-1] + "</pre>"
                        self.txt_formdata += "&q=%3Cpre%3E%" + "%".join(re.findall('..',line[:-1].encode("utf-8").hex())) + "%3C%2Fpre%3E"
                                    
            self.Hash = requests.post("http://localhost:14756/",data ={'text':self.temp_txt}, timeout=10).text
            translated_txt = self.session_requests.post(googleTrans.format(self.src,self.dest,self.Hash),data=self.txt_formdata[2:],headers=headers, timeout=50).text
            translated_txt = json.loads(translated_txt)
            self.txt += "\n".join(translated_txt)

            txt.close()
        except:
            return False
        
        if self.single_file == "y":
            self.single_txt += "----------------------------------\n"
            self.single_txt += self.complete_name[i] + "\n\n"
            
            soup = BeautifulSoup(self.txt, 'html5lib')
            for s in soup.select('i'):
                s.extract()

            results = soup.select('pre')
            for k in range(len(results)):
                self.single_txt +=  results[k].get_text(strip=True).strip() + "\n"
            self.single_txt += "\n\n"
        else:
            os.chdir("../../translated_novel/" + self.novel_name + self.suffix )
            if self.type == "html":
                if i == 0:
                    if i == (len(self.complete_name) - 1):
                        navigation = ''
                    else:
                        navigation = '<div id="navigation"><a href="#"><button>PREV</button></a><a href="' + self.complete_name[i + 1] + '.html"><button>NEXT</button></a></div>'
                elif i == (len(self.complete_name) - 1):
                    navigation = '<div id="navigation"><a href="' + self.complete_name[i - 1] + '.html"><button>PREV</button></a><a href="#"><button>NEXT</button></a></div>'
                else:
                    navigation = '<div id="navigation"><a href="' + self.complete_name[i - 1] + '.html"><button>PREV</button></a><a href="' + self.complete_name[i + 1] + '.html"><button>NEXT</button></a></div>'
                
                new_file = open(self.complete_name[i] + ".html", "w",encoding="utf-8")
                new_file.write(self.header)
                new_file.write(navigation)
            else:
                new_file = open(self.complete_name[i] + ".txt", "w",encoding="utf-8")

            soup = BeautifulSoup(self.txt, 'html5lib')
            for s in soup.select('i'):
                s.extract()

            results = soup.select('pre')
            
            
            
            if self.type == "html":
                for k in range(len(results)):
                    new_file.write("<p>" + results[k].get_text(strip=True).strip() + '</p>')
                
                new_file.write(navigation)
                new_file.write(self.footer)
            else:
                for k in range(len(results)):
                    new_file.write(results[k].get_text(strip=True).strip() + '\n')
                
            
            new_file.close()
            os.chdir("../../txt_files/" + self.novel_name)
        
        return True
    def progress_bar_header(self,message):
        toolbar_width = 50
        self.progress = 51
        print("")
        print("PROGRESS...")
        sys.stdout.write("│%s│" % (" " * toolbar_width) + message + " ")
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width + len(message) + 2))

    def progress_bar_animated(self):
        sys.stdout.write("█")
        sys.stdout.flush()
        self.progress -= 1
    
    def atoi(self,text):
        return int(text) if text.isdigit() else text
    def natural_keys(self,text):
        return [ self.atoi(c) for c in re.split(r'(\d+)', text) ]

Acc = txt_translate()
Acc.initialisation ()
time.sleep(10)