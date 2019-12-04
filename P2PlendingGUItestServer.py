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
        sm = ScreenManager()
        p2pwhispertest = P2PWhisperTestScreen(name = "p2pwhispertest")
        p2pcontracttest = P2PContractTestScreen(name ="p2pcontracttest")
        p2pchattest = P2PChatTestScreen(name = "p2pchattest")
        kadefindnodetest = KadeFindNodeTestScreen(name = "kadefindnodetest")
        kadefiletest = KadeFileTestScreen(name = "kadefiletest")
        mode_selecter = modeselecterScreen(name="mode_selecter")
        self.bulletinboard = bulletinboardScreen(name="Bulletin_Board")
        sm.add_widget(mode_selecter)
        sm.add_widget(self.bulletinboard)
        sm.add_widget(p2pwhispertest)
        sm.add_widget(p2pcontracttest)
        sm.add_widget(p2pchattest)
        sm.add_widget(kadefindnodetest)
        sm.add_widget(kadefiletest)
        #variables
        self.nodeID = P2Plending_node_ID
        self.node = P2PNode(ID = P2Plending_node_ID)
        self.node.save()
        mode_selecter.ids.title.text = 'Welcome :' + self.nodeID
        kadefindnodetest.ids.node_ID.text = 'Your ID : ' + self.nodeID
        p2pchattest.ids.node_ID.text = 'Your ID : ' + self.nodeID
        p2pcontracttest.ids.node_ID.text = 'Your ID : ' + self.nodeID
        return sm

    def get_Node_ID(self):
        return self.nodeID

    def P2P_final_test(self,instruction):
        from P2PFinalTest import FinalTest
        FinalTest(instruction)
    
    def P2P_whisper_test(self):
        from P2PWhisperTest import WhisperTest
        WhisperTest()
    
    def P2P_find_node(self,target_ID):
        print(target_ID)
        self.node.LookUp(target_ID) 
    
    def P2P_chat(self,target_ID,message):
        self.P2P_find_node(target_ID)
        self.node.chat(target_ID,message)

    def P2P_chat_getmessage(self,target_ID):
        self.P2P_find_node(target_ID)
        content = self.node.GetChat(target_ID)
        print(content)
        for item in content:
            print("msg:" + item['msg'])
        return content[-1]['msg']

    def P2P_contract_test(self,transaction_ID,interest,name,period,amount):
        if self.node.GetTmpContract(transaction_ID) == None:
            self.node.WriteContract(lender = True, transation = None,interest = interest,name =  name, period = period,amount = amount )
        else:
            contract = self.node.SendContract(lender = False, ID = transaction_ID , transation = self.node.GetTmpContract(transaction_ID)[0]['msg'] ,interest = interest,name =  name, period = period,amount = amount)
            self.node.UpLoadFile(str(contract))

    def P2P_receive_contract(self,search_ID):
        self.node.GetTmpContract(self, search_ID)

    def refresh_bulletinboard(self):
        self.bulletinboard.ids.display_01.text = 'Your ID : ' + self.nodeID
        self.bulletinboard.ids.display_02.text = 'Your ID : ' + self.nodeID
        self.bulletinboard.ids.display_03.text = 'Your ID : ' + self.nodeID
        self.bulletinboard.ids.display_04.text = 'Your ID : ' + self.nodeID
        self.bulletinboard.ids.display_05.text = 'Your ID : ' + self.nodeID

        self.node.GetPost(ID = '00000000')
        time.sleep(1)
        post_save = self.node.GetPost()
        print('start refresh')

        print('finish refresh')


    def post(self,interest,period):
        message = 'interest' + str(interest) + 'period' + str(period)
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
    Setup()
    P2PlendingApp().run()