# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 15:42:48 2023

@author: 1012985
"""

from lxml import etree

RefDates = ["20241217", "20250109", "20250121" #,"20240927"
            ]



'''
with open( r'D:\working\Reuters EIKON Messenger\dir.text', 'rt') as dirtext:
    for s in dirtext :
        RefDates.append( s.split()[0])
'''


dest_users = [ # FX Platform 
"ralph.son", "jw.sim", "mkyoo", "wychun" , 
"jungeun.choi",  "dlwlgh416", "jang_kj" , 
"lil" ,
"shinjaemin",  "special_weon","jinwk_lee",
  "wlstla2014", "sunmi.jeon", "youngkunoh", "pjstar80", 
"seokjinlee"  
#]

#dest_users = [  # sales
,"younghwajo", "parkjongwoo", "joara0809", 
              "aramchoi", "kdhwan9568", "gitaepark", "jaehwipark",  "junhyuk1109", "woojae0416",
              "hyangleem.lee2", "soojeongjang", "mj_lim", "jeehoonchoi" , "gusgh12299" ]

dest_chk = [ False for i in range(len(dest_users))  ]
dest_cnt = [ 0 for i in range(len(dest_users))  ]


class User:
    def __init__(self, user_name, RefDate):
        self.user_name = user_name
        self.RefDate = RefDate
        self.dest_cnt = 0
        self.text_arr = ""
        self.write_cnt = 0
        self.bChk = False
        
    def addCount(self) :
        self.dest_cnt += 1
        
    def setChk(self, bChk) :
        self.bChk = bChk
        
    def setText(self, strText, Type = "Event"  ) :
        if self.bChk == False : return
        
        self.text_arr += strText
        
        if Type == "Start" :            
            self.text_arr += str(self.dest_cnt) + ']\n채팅 시작 ---------------\n'
    
        if len(self.text_arr) > 100000 :
            self.Print()
        
        
    def Print(self) :
        if self.text_arr == "" :
            return
        print( "write - name :" + self.user_name + " Date :" + self.RefDate + " Cnt: " + str(self.write_cnt) )
        
        self.write_cnt += 1
        write_op = "at"
        
        if self.write_cnt == 1 :
            write_op = "wt"
        
        with open(r'D:\working\rm\\' +  self.RefDate +"_" + self.user_name +'.txt', write_op , encoding='utf-8' ) as f2:
            f2.write(self.text_arr)
            self.text_arr = ""
        


#%%

import zipfile

for RefDate in RefDates :
    
    #cmdd = 'powershell.exe Expand-Archive "D:\\working\\rm\\' + RefDate + '\\messages.zip" ' + ' "D:\\working\\rm\\' + RefDate + '\\" \n'

    #os.system(cmdd)
    try :
        zipfile.ZipFile('D:\\working\\rm\\' + RefDate + '\\messages.zip').extractall('D:\\working\\rm\\' + RefDate )
        
        tree = etree.parse(r'D:\working\rm\\'+ RefDate+ r'\messages.xml' )
    except FileNotFoundError as e:
        print(e)
        continue
    
    root = tree.getroot()
    
    chat_cnt = 0
    
    dest_cnt = [ 0 for i in range(len(dest_users))  ]
    
    users_array = []
    
    for user in dest_users :
        users_array.append( User(user, RefDate ) ) 
        
    SuperUser = User("", RefDate )
    SuperUser.setChk(False)
        
    
    datas = root.getchildren()
    
    for d in datas :
        if d.tag == "Headers" :
            datas2 = d.getchildren()
            
            for d2 in datas2 :
                if d2.tag == "DataPeriod" :
                    datas3 = d2.getchildren()
                    
                    for d3 in datas3 :
                        if d3.tag == "From" :
                            print("From : " + d3.text)
                            SuperUser.setText("From : " + d3.text + "\n")
                        elif d3.tag == "To" :
                            print("To : " + d3.text)
                            SuperUser.setText("To : " + d3.text + "\n")
        elif d.tag == "Users" :
            datas2 = d.getchildren()
    
            for d2 in datas2 :
                if d2.tag == "UserInfo" :
                    datas3 = d2.getchildren()
    
                    SuperUser.setText(d2.tag + "\n")
                    for d3 in datas3 :
                        if d3.tag == "Email" :                            
                            try :
                                SuperUser.setText(d3.text+"\n")
                                if "@hanafn.com" in d3.text :                                    
                                    pass
                            except :                                
                                pass
        elif d.tag == "Chats" :
            
            chats = d.getchildren()
            
            SuperUser.setText("\nChat Start" + "\n")
            
            for chat in chats :
                if chat.tag == "Chat" :
                    chat_cnt += 1
                    bChk = False
                    dest_chk = [ False for i in range(len(dest_users))  ]                                        
                    
                    chat_childs = chat.getchildren() 
                    
                    for chat_child in chat_childs :
                        if chat_child.tag == "Participants" :
                            users = chat_child.getchildren() 
                            
                            SuperUser.setText(chat_child.tag + "\n")
                            
                            for user in users :
                                if user.tag == "User" :
                                    SuperUser.setText(user.text)
                                    for i in range(len(dest_users)) :
                                        if user.text == dest_users[i] + "@hanafn.com" :
                                            dest_chk[i] = True                                            
                                            users_array[i].setChk(True)
                            
                        elif chat_child.tag == "Events" :
                            SuperUser.setText("\n[Chat "+ str(chat_cnt)+"채팅시작----\n" )
                            
                            
                            for i in range(len(dest_users)) :
                                if dest_chk[i] :
                                    dest_cnt[i] += 1
                                    
                                    users_array[i].addCount()
                                    
                                    #text_arr[i] += "\n[Chat " + str(dest_cnt[i]) + ']\n채팅 시작 ---------------\n'
                                    users_array[i].setText( "[Chat " , "Start" )
                                    
                            events = chat_child.getchildren()
                            
                                
                            for event_child in events :
                                
                                event_list = event_child.getchildren()
                                
                                for event in event_list:
                                    
                                    SuperUser.setText( event.tag + ": " )
                                    if event.text :
                                        SuperUser.setText( event.text + "\n" )
                                
                                    if event.tag == "Type" :
                                        for i in range(len(dest_users)) :                                            
                                            if dest_chk[i] :
                                                users_array[i].setText("[" + event.text + "] \n")
                                    elif event.tag == "User" :
                                        for i in range(len(dest_users)) :
                                            if dest_chk[i] :
                                                users_array[i].setText("User " + event.text + " \n" )
                                    elif event.tag == "UTCTime" :
                                        for i in range(len(dest_users)) :
                                            if dest_chk[i] :
                                                users_array[i].setText("UTCTime " + event.text + "\n" )
                                    elif event.tag == "Message" :
                                        messages = event.getchildren()                                            
                                        
                                        for message in messages :                                                                                       
                                            if message.tag == "Content" :                                                
                                                SuperUser.setText( message.text + "\n" )                                    

                                                for i in range(len(dest_users)) :
                                                    if dest_chk[i] :
                                                        users_array[i].setText(message.text + "\n") 
                                
                            
                            SuperUser.setText("채팅 끝 --------------\n" )    
                            for i in range(len(dest_users)) :
                                if dest_chk[i] :
                                    users_array[i].setText("채팅 끝 --------------\n"  ) 
                                            
                
                        
                        
    for i in range(len(dest_users)) :
        #if text_arr[i] != "" :
            #with open(r'D:\working\rm\\' +  RefDate+ dest_users[i] +'.txt', "wt", encoding='utf-8' ) as f2:
                #f2.write(text_arr[i])
                #pass
        users_array[i].Print()

    SuperUser.Print()                
    print(chat_cnt)
                        

#%%
print("end")    
    
    
