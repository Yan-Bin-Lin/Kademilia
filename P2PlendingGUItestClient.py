#all kivy funcitons
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen

import threading
import pickle
import json
import time
import ast

from src.util.hash import GetHash
from src.util import setup
from src.util.error import CheckError
from configparser import ConfigParser

lock = threading.Lock()

def Setup():
    # read config setup
    path_ = 'Config.ini'
    cfg = ConfigParser()
    cfg.read(path_)
    setup.init(
        cfg.get('log', 'wait'),
        cfg.get('hash', 'OutSize'),
        lock
    )
    
class MainScreen(Screen):
    pass 

class modeselecterScreen(Screen):
    pass

class bulletinboardScreen(Screen):
    pass

class P2PWhisperTestScreen(Screen):
    pass

class P2PContractTestScreen(Screen):
    pass

class P2PChatTestScreen(Screen):
    pass

class KadeFindNodeTestScreen(Screen):
    pass

class KadeFileTestScreen(Screen):
    pass

class P2PlendingApp(App):
    
    def build(self):
        from src.P2PLending.P2PNode import P2PNode
        global P2Plending_node_ID
        self.sm = ScreenManager()
        p2pwhispertest = P2PWhisperTestScreen(name = "p2pwhispertest")
        self.p2pcontracttest = P2PContractTestScreen(name ="p2pcontracttest")
        self.p2pchattest = P2PChatTestScreen(name = "p2pchattest")
        kadefindnodetest = KadeFindNodeTestScreen(name = "kadefindnodetest")
        self.kadefiletest = KadeFileTestScreen(name = "kadefiletest")
        mode_selecter = modeselecterScreen(name="mode_selecter")
        self.bulletinboard = bulletinboardScreen(name="Bulletin_Board")
        self.sm.add_widget(mode_selecter)
        self.sm.add_widget(self.bulletinboard)
        self.sm.add_widget(p2pwhispertest)
        self.sm.add_widget(self.p2pcontracttest)
        self.sm.add_widget(self.p2pchattest)
        self.sm.add_widget(kadefindnodetest)
        self.sm.add_widget(self.kadefiletest)
        #variables
        self.nodeID = P2Plending_node_ID
        self.bulletinboard_handler = 0
        self.transaction_target = None
        self.file_handler = 0
        self.post_lenth = []
        with open('Save/00000000/00000000.txt', 'rb') as file:
            self.node = P2PNode(ID = P2Plending_node_ID)
            self.node.update(pickle.load(file),True)
        mode_selecter.ids.title.text = 'Welcome :' + self.nodeID
        kadefindnodetest.ids.node_ID.text = 'Your ID : ' + self.nodeID
        self.p2pchattest.ids.node_ID.text = 'Your ID : ' + self.nodeID
        self.p2pcontracttest.ids.node_ID.text = 'Your ID : ' + self.nodeID
        self.kadefiletest.ids.node_ID.text = 'Your ID : ' + self.nodeID
        self.bulletinboard.ids.title.text = 'Your ID : ' + self.nodeID
        self.refresh_bulletinboard()
        return self.sm
    
    def submit_ID(self,text):
        
        print(self.nodeID)

    def get_Node_ID(self):
        return self.node.ID

    def P2P_final_test(self,instruction):
        from P2PFinalTest import FinalTest
        FinalTest(instruction)
    
    def P2P_whisper_test(self):
        from P2PWhisperTest import WhisperTest
        WhisperTest()
    
    def P2P_find_node(self,target_ID):
        if target_ID == '':
            target_ID = str(self.transaction_target)
        print(target_ID + '\n\n\n')
        self.node.LookUp(target_ID) 

    def P2P_chat(self,target_ID,message):
        if target_ID == '':
            target_ID = str(self.transaction_target)
            self.p2pchattest.ids['target_ID'].text = self.transaction_target
        self.P2P_find_node(target_ID)
        self.node.chat(target_ID,message)

    def P2P_contract_test(self,transaction_ID,interest,name,period,amount,return_money = False):
        if transaction_ID == '':
            transaction_ID = str(self.transaction_target)
        self.P2P_find_node(transaction_ID)
        if return_money == True:
            amount = float(amount) + (float(amount) * float(interest) / 100)
            period = (float(period) - 1)
            amount = amount - (amount/period)
            period = str(period)
            amount = str(amount)
            print('\n\n|interest:' + interest + amount + period + '|end\n\n')
        if self.node.GetTmpContract(transaction_ID) == None or return_money ==True:
            print('start send')
            contract = self.node.SendContract(lender = False, ID = transaction_ID,transation = None,interest = interest,name =  name, period = period,amount = amount )
            print('\n\n\n')
            print(contract)
            self.node.SecreteInit(transaction_ID)
            while self.node.secrete.get(transaction_ID,None) == None:
                print('\nget Key\n')
                continue
            self.node.SaveKey()
        else:
            #while self.node.secrete.get(transaction_ID,None) == None:
                #continue
            contract = self.node.SendContract(lender = True, ID = transaction_ID , transation = self.node.GetTmpContract(transaction_ID)[-1]['msg']['Transation'],other = self.node.GetTmpContract(transaction_ID)[0]['msg']['Trader']['brower'])
            contract = self.node.EncryptMsg(transaction_ID , str(contract))['msg']
            print(contract)
            if int(transaction_ID,2) > int(self.nodeID,2):
                self.node.UpLoadFile(contract,GetHash((str(transaction_ID)+str(self.nodeID)),OutSize = 8))
                self.node.SaveKey()
            else:
                self.node.UpLoadFile(contract,GetHash((str(self.nodeID))+(str(transaction_ID)),OutSize = 8))
                self.node.SaveKey()
        self.p2pcontracttest.ids.transaction_ID.disabled = False
        self.p2pcontracttest.ids.period.disabled = False
        self.p2pcontracttest.ids.amount.disabled = False
        self.p2pcontracttest.ids.interest.disabled = False

    def P2P_receive_contract(self,search_ID,number = '',transaction_finished = False):
        if search_ID == '':
            search_ID = str(self.transaction_target)
        if transaction_finished == False :
            print(self.node.GetTmpContract(search_ID))
            received_contract = self.node.GetTmpContract(search_ID)
            print(received_contract)
            self.p2pcontracttest.ids.transaction_ID.text = received_contract[-1]['msg']['Trader']['brower']['node']['ID']
            self.p2pcontracttest.ids.amount.text = received_contract[-1]['msg']['Transation']['amount']
            self.p2pcontracttest.ids.interest.text = received_contract[-1]['msg']['Transation']['interest']
            self.p2pcontracttest.ids.period.text = received_contract[-1]['msg']['Transation']['period']
            self.p2pcontracttest.ids.transaction_ID.disabled = True
            self.p2pcontracttest.ids.period.disabled = True
            self.p2pcontracttest.ids.amount.disabled = True
            self.p2pcontracttest.ids.interest.disabled = True
        else:
            if number == '':
                self.file_handler = self.file_handler - 1
            else:
                self.file_handler = self.file_handler - int(number)
            self.node.LoadKey()
            if int(search_ID,2) > int(self.nodeID,2):
                received_contract = self.node.GetFile(GetHash((str(search_ID)+str(self.nodeID)),OutSize = 8))
                if self.file_handler < -(len(received_contract)):
                    if number == '':
                        self.file_handler = -1
                    else :
                        self.kadefiletest.ids.range.text = 'out of range'
                        return
                received_contract = self.node.DecryptMsg(search_ID, received_contract[self.file_handler]['file'])
                print(received_contract)
            else:
                received_contract = self.node.GetFile(GetHash((str(self.nodeID)+str(search_ID)),OutSize = 8))
                received_contract = self.node.DecryptMsg(search_ID, received_contract[self.file_handler]['file'])
                print(received_contract)
            received_contract = ast.literal_eval(received_contract)
            print('\n\n\n')
            print(received_contract)
            print('\n\n')
            if received_contract['Trader']['brower']['node']['ID'] == self.nodeID:
                self.kadefiletest.ids.transaction_ID.text = received_contract['Trader']['lender']['node']['ID']
            else:
                self.kadefiletest.ids.transaction_ID.text = received_contract['Trader']['brower']['node']['ID']
            self.kadefiletest.ids.amount.text = received_contract['Transation']['amount']
            self.kadefiletest.ids.interest.text = received_contract['Transation']['interest']
            self.kadefiletest.ids.period.text = received_contract['Transation']['period']
            self.kadefiletest.ids.name.text = received_contract['Transation']['name']
            self.kadefiletest.ids.transaction_ID.disabled = True
            self.kadefiletest.ids.period.disabled = True
            self.kadefiletest.ids.amount.disabled = True
            self.kadefiletest.ids.interest.disabled = True
            self.kadefiletest.ids.name.disabled = True

    async def check_return_key(self,transaction_ID):
        while self.node.secrete.get(transaction_ID,None) == None:
            continue
        return True
    async def await_controller(self,transaction_ID):
        result = await self.check_return_key(transaction_ID)
        return result
    
    def P2P_chat_getmessage(self,target_ID):
        if target_ID == '':
            target_ID = str(self.transaction_target)
        self.P2P_find_node(target_ID)
        content = self.node.GetChat(target_ID)
        for item in content:
            print("msg:" + item['msg'])
        return content[-1]['msg']
    
    def refresh_bulletinboard(self):
        column = 0
        post_data_amount = 0
        bulletinboard_column = self.bulletinboard_handler
        post = self.node.GetPost(ID = '00000000')
        print(post)
        self.post_lenth = []
        for x in range(0,(len(post))):
            self.post_lenth.append(len(post[x]))
        for x in range(0,(len(self.post_lenth))):
            post_data_amount = post_data_amount + 1
        if post_data_amount <= bulletinboard_column:
            bulletinboard_column = 0
            self.bulletinboard_handler = 0
        print(len(self.post_lenth))
        time.sleep(2)
        post_save = self.node.GetPost()
        print('start refresh')
        for y in range(0,len(self.post_lenth)):
            print(self.post_lenth[y])
            print('\n\n')
            for x in range(0,(self.post_lenth[y])):
                print(post_save[y][(-1-x)]['msg'])
        print('\n\n\n\n')
        for node in range(0,len(self.post_lenth)):
            for x in range(0,self.post_lenth[node]):
                if bulletinboard_column > 0:
                    bulletinboard_column = bulletinboard_column - 1
                else: 
                    self.bulletinboard_handler = self.bulletinboard_handler + 1
                    temp = post_save[node][(-1-x)]['msg'].split("|")
                    print(temp[0]+'  '+temp[1]+'  '+temp[2]+'\n\n')
                    self.bulletinboard.ids["display_0"+str(column+1)].text = 'amount : '+ self.split_string(temp[2],6) +' period : '+self.split_string(temp[1],6)+' interest : ' + self.split_string(temp[0],8)
                    column = column + 1
        print('\n\n\n\n')
        
        print('finish refresh')

    def split_string(self,post,size):
        return post[size:]

    def select_target(self,column):
        print(column)
        post_file = self.node.GetPost()
        for node in range(0,len(self.post_lenth)):
            for x in range(0,self.post_lenth[node]):
                if column > 0:
                    column = column - 1
                else:
                    print('write contract')
                    temp = post_file[node][(-1-x)]['msg'].split("|")
                    self.transaction_target = post_file[node][-1-x]['from']['ID']
                    self.p2pcontracttest.ids.transaction_ID.text =  post_file[node][-1-x]['from']['ID']
                    self.p2pcontracttest.ids.transaction_ID.disabled = True
                    self.p2pcontracttest.ids.interest.text =  self.split_string(temp[0],8)
                    self.p2pcontracttest.ids.interest.disabled = True
                    self.p2pcontracttest.ids.amount.text = self.split_string(temp[2],6)
                    self.p2pcontracttest.ids.amount.disabled = True
                    self.p2pcontracttest.ids.period.text = self.split_string(temp[1],6)
                    self.p2pcontracttest.ids.period.disabled = True
                    print(self.transaction_target)
                    self.P2P_find_node(self.transaction_target)
                    if self.transaction_target == None:
                        return 
                    else:
                        self.change_screen('p2pchattest')
                    return
            
        
    def change_screen(self,change_screen_name):
        self.sm.current = change_screen_name

    def post(self,interest,period,amount):
        message = 'interest' + str(interest) + '|period' + str(period) + '|amount' + str(amount)
        self.node.post(ID = '00000000',msg = message)
        print('finish post')





    def P2P_whisper(self,user_ID,target_ID,message):
        from P2PWhisperTest import WhisperTest
        self.nodeID = user_ID
        if message == '':
            thread = threading.Thread(target = WhisperTest,args = ( user_ID,target_ID,message,'s'))
            thread.start()
        else:
            thread = threading.Thread(target = WhisperTest,args = ( user_ID,target_ID,message,'n'))
            thread.start()

    def file_test(self):
        from KadeFileTest import FileTest
        thread = threading.Thread(target = FileTest, args = (instruction))
        thread.start()        



class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        scm = MainScreen(name="main")
        sm.add_widget(scm)
        return sm
    
    def change_ID(self,name):
        global P2Plending_node_ID
        P2Plending_node_ID = name
        return 


def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


if __name__ == "__main__":
    P2Plending_node_ID = ''
    LoginApp().run()
    reset()
    print(P2Plending_node_ID + '\n\n\n\n')
    Setup()
    P2PlendingApp().run()