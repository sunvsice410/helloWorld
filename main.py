# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from MainWindow import Ui_Form
from LogoutMsg  import  LogoutRespMsg
import CommonMsg
import SVTCmdMsg,SVTCmdCancelMsg
import RemoteControlHornOrFlashCmdMsg as RCHornFlash
import RmtCtlACCmdMsg as RCAC
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject,pyqtSignal
import binascii
import operator
from ctypes import *
import time
import struct
import paho.mqtt.client as mqtt
from threading import Thread

VIN = "UCIT123456789ABCD"

# /*===================MQTT publish TOPIC ===========================*/
MQTT_TOPIC_IOT_RESP_LOGIN = "/iot/login/resp/" + VIN
MQTT_TOPIC_IOT_RESP_LOGOUT = "/iot/logout/resp/" + VIN
MQTT_TOPIC_IOT_RESP_OFFLINE = "/iot/offline/resp/" + VIN
MQTT_TOPIC_IOT_REQ_CONTROL = "/iot/control/" + VIN
MQTT_TOPIC_IOT_REQ_PARAMETER = "/iot/parameters/" + VIN

# /*===================global MQTT subcriber TOPIC ===========================*/
MQTT_TOPIC_IOT_REQ_LOGIN = "/iot/login/req/" + VIN
MQTT_TOPIC_IOT_REQ_LOGOUT = "/iot/logout/req/" + VIN
MQTT_TOPIC_IOT_REQ_SHADOW_STATE = "/iot/shadow/state/" + VIN
MQTT_TOPIC_IOT_REQ_SHADOW_REISSUE = "/iot/shadow/reissue/" + VIN
MQTT_TOPIC_IOT_REQ_SHADOW_DATA = "/iot/shadow/data" + VIN
MQTT_TOPIC_IOT_REQ_BUSINESS_DATA = "/iot/business/data/" + VIN
MQTT_TOPIC_IOT_REQ_OFFLINE = "/iot/offline/req/" + VIN
MQTT_TOPIC_IOT_RESP_CONTROL = "/iot/controlResp/" + VIN
MQTT_TOPIC_IOT_RESP_PARAMETER = "/iot/parametersResp/" + VIN


class MainWindowInst(QtWidgets.QWidget, Ui_Form):
    show_infoes_signal = pyqtSignal(str)
    def __init__(self):
        super(MainWindowInst, self).__init__()
        self.setupUi(self)
        self.show_infoes_signal.connect(self.show_infoes)

    def connect_log(self, info):
        self.show_infoes_signal.emit(info)

    def Connect_click(self):
        t = Thread(target=MqttTask)
        t.start()

    def Disconnect_click(self):
        client.disconnect()

    def LogoutSend_click(self):
        self.textEdit.append(">>>>>>>>>>>>Send Msg>>>>>>>>>>>>>>>>>>>>>>")
        self.textEdit.append("publish topic is "+MQTT_TOPIC_IOT_RESP_LOGOUT)
        logoutMsg = LogoutRespMsg(VIN)
        payload = logoutMsg.pack()
        self.textEdit.append("Logout Msg Send: " + str(binascii.hexlify(payload)) + "Success ")
        client.publish(MQTT_TOPIC_IOT_RESP_LOGOUT, payload, qos=2, retain=False)

    def LoginSend_click(self):
        self.textEdit.append(">>>>>>>>>>>>Send Msg>>>>>>>>>>>>>>>>>>>>>>")
        self.textEdit.append("publish topic is "+MQTT_TOPIC_IOT_RESP_LOGIN)
        sendMsg = LoginRespMsg()
        payload = sendMsg.pack()
        self.textEdit.append("Login resp payload is "+str(binascii.hexlify(payload)))
        client.publish(MQTT_TOPIC_IOT_RESP_LOGIN, payload, qos=2, retain=False)

    def SVTCmdSend_click(self):
        self.textEdit.append(">>>>>>>>>>>>Send Msg>>>>>>>>>>>>>>>>>>>>>>")
        self.textEdit.append("publish topic is "+MQTT_TOPIC_IOT_REQ_CONTROL)
        svtReqMsg = SVTCmdMsg.SVTCmdReqMsg(VIN)
        payload = svtReqMsg.pack()
        self.textEdit.append("SVT CMD REQ payload is "+str(binascii.hexlify(payload)))
        client.publish(MQTT_TOPIC_IOT_REQ_CONTROL, payload, qos=2, retain=False)

    def SvtCmdCancel_click(self):
        self.textEdit.append(">>>>>>>>>>>>Send Msg>>>>>>>>>>>>>>>>>>>>>>")
        self.textEdit.append("publish topic is "+MQTT_TOPIC_IOT_REQ_CONTROL)
        svtReqMsg = SVTCmdCancelMsg.SVTCmdReqMsg(VIN)
        payload = svtReqMsg.pack()
        self.textEdit.append("SVT CMD REQ payload is "+str(binascii.hexlify(payload)))
        client.publish(MQTT_TOPIC_IOT_REQ_CONTROL, payload, qos=2, retain=False)

    def RCHornFlashCmd_click(self):
        self.textEdit.append(">>>>>>>>>>>>Send Msg>>>>>>>>>>>>>>>>>>>>>>")
        self.textEdit.append("publish topic is "+MQTT_TOPIC_IOT_REQ_CONTROL)
        SendReqMsg = RCHornFlash.RCHornFlashReqMsg(VIN)
        payload = SendReqMsg.pack()
        self.textEdit.append("RC HornFlash CMD REQ payload is "+str(binascii.hexlify(payload)))
        client.publish(MQTT_TOPIC_IOT_REQ_CONTROL, payload, qos=2, retain=False)

    def RCACCmd_click(self):
        self.textEdit.append(">>>>>>>>>>>>Send Msg>>>>>>>>>>>>>>>>>>>>>>")
        self.textEdit.append("publish topic is "+MQTT_TOPIC_IOT_REQ_CONTROL)
        SendReqMsg = RCAC.RCACReqMsg(VIN)
        payload = SendReqMsg.pack()
        self.textEdit.append("RC AC CMD REQ payload is "+str(binascii.hexlify(payload)))
        client.publish(MQTT_TOPIC_IOT_REQ_CONTROL, payload, qos=2, retain=False)

    # 展示信息槽函数
    def show_infoes(self, info):
    #    print(info)
        #pre_text = self.show_label.text()
        #self.textEdit.setText(info + '\n\n')
        self.textEdit.append(info + '')


class LoginRespMsg(BigEndianStructure):
    _fields_ = [("businessType", c_ushort),
                ("protocolVerNum", c_byte),
                ("flag", c_ubyte),
                ("serialNum", c_ushort),
                ("vinLen", c_ushort),
                ("vin", c_byte * 17),
                ("time", c_byte * 6),
                ("rspBusinessID", c_ushort),
                ("rspResult", c_byte),
                ("businessEndFlag", c_byte),
                ("errorCodeNum", c_byte),
                ("tokenLen", c_ushort),
                ("token", c_byte * 16),
                ("isGBFlag", c_byte)]

    def __init__(self):
        self.businessType = 0x0001
        self.protocolVerNum = 0x04
        self.flag = 0xC1
        self.serialNum = LoginReqSerialNum
        self.vinLen = 0x0011
        for i in range(len(VIN)):
            self.vin[i] = ord(VIN[i])
        curTime = int(time.time())
        # print("curTime=", curTime)
        self.time[0] = (curTime & 0xFF0000000000) >> 40
        self.time[1] = (curTime & 0x00FF00000000) >> 32
        self.time[2] = (curTime & 0x0000FF000000) >> 24
        self.time[3] = (curTime & 0x000000FF0000) >> 16
        self.time[4] = (curTime & 0x00000000FF00) >> 8
        self.time[5] = (curTime & 0x0000000000FF)
        self.rspBusinessID = 0x5001
        self.rspResult = 0x00
        self.businessEndFlag = 0x00
        self.errorCodeNum = 0x00
        self.tokenLen = 0x0010
        self.token[0] = ord('s')
        self.token[1] = ord('u')
        self.token[2] = ord('n')
        self.token[3] = ord('s')
        self.token[4] = ord('h')
        self.token[5] = ord('i')
        self.token[6] = ord('g')
        self.token[7] = ord('u')
        self.token[8] = ord('o')
        self.token[9] = ord('#')
        self.token[10] = ord('#')
        self.token[11] = ord('t')
        self.token[12] = ord('o')
        self.token[13] = ord('k')
        self.token[14] = ord('e')
        self.token[15] = ord('n')
        self.isGBFlag = 0x01


    def get_crc(self, payload):
        polynomial = 0x1021
        crc = 0xFFFF
        crcResult = [0x00, 0x00]
        for index in range(0, len(payload), 2):
            b = int(payload[index:index + 2], 16)
            for i in range(8):
                if ((b >> (7 - i) & 1) == 1):
                    bit = 1
                else:
                    bit = 0
                # bit = (((b >> (7 - i) & 1) == 1)? 1 : 0)
                if ((crc >> 15 & 1) == 1):
                    c15 = 1
                else:
                    c15 = 0
                # c15 = (((crc >> 15 & 1) == 1) ? 1 : 0)
                crc <<= 1
                if 0 != c15 ^ bit:
                    crc ^= polynomial
        crc &= 0xFFFF
        crcResult[0] = crc >> 8
        crcResult[1] = crc & 0xFF
        return crcResult

    def pack(self):
        curTime = int(time.time())
        timeTmp = [0x00,0x00,0x00,0x00,0x00,0x00]
        timeTmp[0] = (curTime&0xFF0000000000)>>40
        timeTmp[1] = (curTime&0x00FF00000000)>>32
        timeTmp[2] = (curTime&0x0000FF000000)>>24
        timeTmp[3] = (curTime&0x000000FF0000)>>16
        timeTmp[4] = (curTime&0x00000000FF00)>>8
        timeTmp[5] = curTime&0x0000000000FF
        timeStr = ''
        for i in range(6):
            timeStr += '{:02x}'.format(timeTmp[i])
        print("timeStr=",timeStr)

        vinStr=''
        for i in range(17):
            vinStr += '{:02x}'.format(self.vin[i])
        print("vinStr=",vinStr)
        #print("vinBytes=", bytes(vinStr, encoding = "utf8"))
        #print("vinAsciiBytes=", binascii.hexlify(bytes(vinStr, encoding = "utf8")))

        #00B4
        payloadStr = '00B4'
        payloadStr += '{:04x}'.format(self.tokenLen)
        for i in range(16):
            payloadStr += '{:02x}'.format(self.token[i])
        #0090
        payloadStr += '0090'
        payloadStr += '{:02x}'.format(self.isGBFlag)
        print("payloadStr=",payloadStr)

        '''
        buffer = struct.pack("!HBbHHBBBBBBBBBBBBBBBBBbbbbbbHBBBBbBBBBBBBBBBBBBBBBBB", self.businessType, self.protocolVerNum, self.flag, self.serialNum, self.vinLen,
                             self.vin[0], self.vin[1], self.vin[2], self.vin[3],self.vin[4], self.vin[5],self.vin[6], self.vin[7], self.vin[8], self.vin[9],self.vin[10], self.vin[11]
                            ,self.vin[12], self.vin[13], self.vin[14], self.vin[15],self.vin[16], self.time[0], self.time[1], self.time[2], self.time[3],self.time[4], self.time[5]
                             , self.rspBusinessID, self.rspResult, self.businessEndFlag, self.errorCodeNum, self.payload[0], self.payload[1], self.payload[2], self.payload[3],self.payload[4], self.payload[5]
                              ,self.payload[6], self.payload[7], self.payload[8], self.payload[9],self.payload[10], self.payload[11],self.payload[12]
                              , self.payload[13], self.payload[14], self.payload[15],self.payload[16],self.payload[17],self.payload[18],self.payload[19])
        '''
        bufferTmp = '{:04x}{:02x}{:02x}{:04x}{:04x}'.format(self.businessType, self.protocolVerNum, self.flag, self.serialNum, self.vinLen)
        buffer  = bufferTmp + vinStr + timeStr + '{:04x}{:02x}{:02x}{:02x}'.format(self.rspBusinessID, self.rspResult, self.businessEndFlag, self.errorCodeNum) + payloadStr
        #print("buffer type is", type(buffer), buffer)
        bufferBytes=bytes(buffer, encoding="utf-8")
        #bufferBytes=binascii.hexlify(buffer)
        crcRet = self.get_crc(bufferBytes)
        #crc0Hex = hex(crcRet[0])
        crc0Str = '{:02x}'.format(crcRet[0])
        #print("crc0Str is",crc0Str)
        btmp=bytes(crc0Str, "utf-8")
        #print("btmp= type is",btmp, type(btmp))
        bufferTmp=bufferBytes+btmp
        #crc1Hex = hex(crcRet[1])
        crc1Str = '{:02x}'.format(crcRet[1])
        #print("crc1Str is",crc1Str)
        btmp=bytes(crc1Str, "utf-8")
        bufferTmp +=btmp
        print("buffer+crc=",bufferTmp)

        return binascii.unhexlify(bufferTmp)

    def unpack(self, data):
        (self.businessType, self.protocolVerNum, self.flag, self.serialNum, self.vinLen, self.vin, self.time[0:6] \
             , self.rspBusinessID, self.rspResult, self.businessEndFlag, self.errorCodeNum \
             , self.payload) = struct.unpack("!HBBHH17s6sHBBB1024s", data)


# deconde LoginReqMsg
LoginReqSerialNum = 0x0000
class LoginMsg(object):
    def decode_Header(self, payload, myUI):
        sPayload = str(payload, encoding="utf-8")
        myUI.connect_log("=========Login Msg header begin===========")
        myUI.connect_log("businessType = 0x"+sPayload[0:4])
        myUI.connect_log("protocolVerNum = 0x"+sPayload[4:6])
        myUI.connect_log("flag = 0x"+sPayload[6:8])
        LoginReqSerialNum = int(sPayload[8:12], 16)
        myUI.connect_log("serialNum = 0x"+sPayload[8:12])
        myUI.connect_log("vinLen = 0x"+sPayload[12:16])
        myUI.connect_log("vin ="+sPayload[16:50])
        '''myUI.connect_log("vin = %c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c" % (
        int(sPayload[16:18], 16), int(sPayload[18:20], 16), int(sPayload[20:22], 16) \
            , int(sPayload[22:24], 16), int(sPayload[24:26], 16), int(sPayload[26:28], 16) \
            , int(sPayload[28:30], 16), int(sPayload[30:32], 16), int(sPayload[32:34], 16) \
            , int(sPayload[34:36], 16), int(sPayload[36:38], 16), int(sPayload[38:40], 16) \
            , int(sPayload[40:42], 16), int(sPayload[42:44], 16), int(sPayload[44:46], 16) \
            , int(sPayload[46:48], 16), int(sPayload[48:50], 16)))
        '''
        myUI.connect_log("timestamp ="+sPayload[50:62])
        if 0xc1 == int(sPayload[6:8], 16):
            myUI.connect_log("=========Login Msg Result begin  ===========")
            myUI.connect_log("rspBusinessID = 0x"+sPayload[62:66])
            myUI.connect_log("rspResult = 0x"+sPayload[66:68])
            myUI.connect_log("businessEndFlag = 0x"+sPayload[68:70])
            myUI.connect_log("errorCodeNum = 0x"+sPayload[70:72])
            myUI.connect_log("=========Login Msg Result end   ===========")

        else:
            myUI.connect_log("=========Login Msg header end  ===========")

    def decode_MsgBody(self, payload, myUI):
        sPayload = str(payload, encoding="utf-8")
        if 0xc1 == int(sPayload[6:8], 16):
            myUI.connect_log("=========Login Msg Body begin===========")
            myUI.connect_log("msgBody ="+sPayload[72:])
            myUI.connect_log("=========Login Msg Body end  ===========")
        else:
            myUI.connect_log("=========Login Msg Body begin===========")
            myUI.connect_log("msgBody ="+sPayload[62:])
            myUI.connect_log("=========Login Msg Body end  ===========")

    def check_crc(self, payload):
        polynomial = 0x1021
        crc = 0xFFFF
        crcResult = [0x00, 0x00]
        for index in range(0, len(payload) - 4, 2):
            b = int(payload[index:index + 2], 16)
            for i in range(8):
                if ((b >> (7 - i) & 1) == 1):
                    bit = 1
                else:
                    bit = 0
                # bit = (((b >> (7 - i) & 1) == 1)? 1 : 0)
                if ((crc >> 15 & 1) == 1):
                    c15 = 1
                else:
                    c15 = 0
                # c15 = (((crc >> 15 & 1) == 1) ? 1 : 0)
                crc <<= 1
                if c15 ^ bit:
                    crc ^= polynomial
        crc &= 0xFFFF
        crcResult[0] = crc >> 8
        crcResult[1] = crc & 0xFF
        # print("crcResult[0]=0x%x,crcResult[1]=0x%x"%(crcResult[0],crcResult[1]))
        if (crcResult[0] == int(payload[len(payload) - 4:len(payload) - 2], 16)) and (
                crcResult[1] == int(payload[len(payload) - 2:len(payload)], 16)):
            return True
        else:
            return False

def on_disconnect(client, userdata, rc):
    myUI = userdata
    if rc != 0:
        myUI.connect_log("Unexpected disconnection.")
    else:
        myUI.connect_log("Disconnection success.")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    myUI = userdata
    myUI.connect_log("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/iot/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if True == operator.eq(msg.topic, MQTT_TOPIC_IOT_RESP_LOGIN) \
        or True == operator.eq(msg.topic, MQTT_TOPIC_IOT_RESP_LOGOUT) \
        or True == operator.eq(msg.topic, MQTT_TOPIC_IOT_RESP_OFFLINE) \
        or True == operator.eq(msg.topic, MQTT_TOPIC_IOT_REQ_CONTROL) \
        or True == operator.eq(msg.topic, MQTT_TOPIC_IOT_REQ_PARAMETER):
        return

    myUI = userdata
    #myUI.connect_log(msg.topic+" "+str(msg.payload))
    myUI.connect_log("<<<<<<<<<<<<<Rec Msg<<<<<<<<<<<<<<<<<<<<<<<<")
    myUI.connect_log("Rec topic is"+msg.topic)
    msgPayload = binascii.hexlify(msg.payload)
    myUI.connect_log("payload:"+str(msgPayload))
    DecodeMsg = CommonMsg.DecodeMsg()
    if (True == DecodeMsg.check_crc(msgPayload)):
        myUI.connect_log("CRC Check is OK")
    else:
        myUI.connect_log("CRC Check is not OK")
        #return
    busnisstype = DecodeMsg.decode_Header(msgPayload, myUI)
    if True == operator.eq(msg.topic,MQTT_TOPIC_IOT_REQ_LOGIN):
        recMsg = LoginMsg()
        recMsg.decode_MsgBody(msgPayload, myUI)
    elif True == operator.eq(msg.topic,  MQTT_TOPIC_IOT_RESP_CONTROL):
        if 0x1501 == busnisstype:
            recMsg = SVTCmdMsg.SVTRepMsg()
            recMsg.decode_MsgBody(msgPayload, myUI)
        elif 0x1102 == busnisstype:
            recMsg = RCHornFlash.RCHornFlashRespMsg()
            recMsg.decode_MsgBody(msgPayload, myUI)
        elif 0x1107 == busnisstype:
            recMsg = RCAC.RCACRespMsg()
            recMsg.decode_MsgBody(msgPayload, myUI)

def MqttTask():
    print("MqttSubThread is running....")
    global  client
    #client = mqtt.Client(client_id="ssg_python", clean_session=True, userdata=None, protocol=4, transport="tcp")
    client = mqtt.Client(client_id="ssg_python", clean_session=True, userdata=myUI, protocol=4, transport="tcp")
    myUI.connect_log("client_id=ssg_python, clean_session=True, userdata=myUI, protocol=MQTTv311, transport=tcp")

    #Register Callback function
    client.on_disconnect = on_disconnect
    client.on_connect = on_connect
    client.on_message = on_message

    #client.connect("tcp://localhost:1883", 1883, 30)
    client.connect("10.203.204.214", 1883, 30)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.

    client.loop_forever()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    myapp = QtWidgets.QApplication(sys.argv)
    #myDlg = QtWidgets.QDialog()
    myUI = MainWindowInst()
    myUI.show()

    sys.exit(myapp.exec_())
