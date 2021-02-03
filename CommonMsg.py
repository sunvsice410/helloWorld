#!/usr/bin/env python3
# -*- coding: utf-8 -*-#

###########################################################################
#                   Copyright by UCIT                                     #
#         Create by sunshiguo for simulating Logout Msg                   #
#                                                                         #
#                         2020.12.02                                      #
#                                                                         #
#                                                                         #
###########################################################################


from ctypes import *
import binascii
from sys import byteorder

class EncodeMsg(BigEndianStructure):
    def get_crc(self, payload):
        polynomial = 0x1021
        crc = 0xFFFF
        crcResult = [0x00, 0x00]
        for index in range(0,len(payload),2):
            b = int(payload[index:index+2], 16)
            for i in range(8):
                if ((b >> (7 - i) & 1) == 1):
                    bit = 1
                else:
                    bit = 0
                #bit = (((b >> (7 - i) & 1) == 1)? 1 : 0)
                if ((crc >> 15 & 1) == 1):
                    c15 = 1
                else:
                    c15 = 0
                #c15 = (((crc >> 15 & 1) == 1) ? 1 : 0)
                crc <<= 1
                if 0 != c15^bit :
                    crc ^= polynomial
        crc &= 0xFFFF
        crcResult[0] = crc >> 8
        crcResult[1] = crc & 0xFF
        return crcResult
                

class DecodeMsg(object):
    def is_big_endian(self):
        if byteorder == 'little':
            return False
        else:
            return True

    def decode_Header(self, payload, UIDisp):
        sPayload = str(payload, encoding = "utf-8")
        UIDisp.connect_log("=========Msg header begin===========")
        UIDisp.connect_log("businessType = 0x"+sPayload[0:4])
        UIDisp.connect_log("protocolVerNum = 0x"+sPayload[4:6])
        UIDisp.connect_log("flag = 0x"+sPayload[6:8])
        UIDisp.connect_log("serialNum = 0x"+sPayload[8:12])
        UIDisp.connect_log("vinLen = 0x"+sPayload[12:16])
        UIDisp.connect_log("vin ="+sPayload[16:50])
        vin = '{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}{:c}'.format(int(sPayload[16:18], 16), int(sPayload[18:20], 16), int(sPayload[20:22], 16) \
                                                                  , int(sPayload[22:24], 16), int(sPayload[24:26], 16), int(sPayload[26:28], 16) \
                                                                  , int(sPayload[28:30], 16), int(sPayload[30:32], 16), int(sPayload[32:34], 16) \
                                                                  , int(sPayload[34:36], 16), int(sPayload[36:38], 16), int(sPayload[38:40], 16) \
                                                                  , int(sPayload[40:42], 16), int(sPayload[42:44], 16), int(sPayload[44:46], 16) \
                                                                  , int(sPayload[46:48], 16), int(sPayload[48:50], 16))
        UIDisp.connect_log(vin)
        UIDisp.connect_log("timestamp ="+sPayload[50:62])
        if 0xc1 == int(sPayload[6:8],16):
            UIDisp.connect_log("=========Msg Result begin  ===========")
            UIDisp.connect_log("rspBusinessID = 0x"+sPayload[62:66])
            busnisstype = int(sPayload[62:66], 16)
            UIDisp.connect_log("rspResult = 0x"+sPayload[66:68])
            UIDisp.connect_log("businessEndFlag = 0x"+sPayload[68:70])
            UIDisp.connect_log("errorCodeNum = 0x"+sPayload[70:72])
            errorCodeNum = int(sPayload[70:72], 16)
            if 0 != errorCodeNum:
                for i in range(errorCodeNum):
                    UIDisp.connect_log("errorCode = 0x" + sPayload[72+i*4:76+i*4])

            UIDisp.connect_log("=========Msg Result end   ===========")

        else:
            busnisstype = 0x0000
            UIDisp.connect_log("=========Msg header end  ===========")
        return busnisstype

    def decode_key(self, keyType):
        return (keyType & 0xFFFFFF00) >> 4

    def decode_type(self, keyType):
        return (keyType & 0x000000FF)

    def decode_len(self, value):
        length = {'0': '1', '1': '2', '2': '4', '3': '6', '4': '0', '5': '0', '6': '0', '7': '0', '8': '8'}
        return int(length.get(str(value)))

    def decode_MsgBody(self, payload, UIDisp):
        sPayload = str(payload, encoding = "utf-8")
        if 0xc1 == int(sPayload[6:8], 16):
            UIDisp.connect_log("=========Msg Body begin===========")
            # 4 indicate no msgbody only have CRC
            if 4 == len(sPayload[72:]):
                UIDisp.connect_log("msgBody is NULLLLLL")
            else:
                len = len(sPayload[72:])
                UIDisp.connect_log("msgBody ="+sPayload[72:72+len-4])
            UIDisp.connect_log("=========Msg Body end  ===========")
        else:
            UIDisp.connect_log("=========Msg Body begin===========")
            if 4 == len(sPayload[62:]):
                UIDisp.connect_log("msgBody is NULLLLLL")
            else:
                len = len(sPayload[62:])
                UIDisp.connect_log("msgBody ="+sPayload[62:62+len-4])
            UIDisp.connect_log("=========Msg Body end  ===========")

    def check_crc(self, payload):
        polynomial = 0x1021
        crc = 0xFFFF
        crcResult = [0x00, 0x00]
        for index in range(0,len(payload) - 4,2):
            b = int(payload[index:index+2], 16)
            for i in range(8):
                if ((b >> (7 - i) & 1) == 1):
                    bit = 1
                else:
                    bit = 0
                #bit = (((b >> (7 - i) & 1) == 1)? 1 : 0)
                if ((crc >> 15 & 1) == 1):
                    c15 = 1
                else:
                    c15 = 0
                #c15 = (((crc >> 15 & 1) == 1) ? 1 : 0)
                crc <<= 1
                if c15^bit :
                    crc ^= polynomial
        crc &= 0xFFFF
        crcResult[0] = crc >> 8
        crcResult[1] = crc & 0xFF
        #print("crcResult[0]=0x%x,crcResult[1]=0x%x"%(crcResult[0],crcResult[1]))
        if (crcResult[0] == int(payload[len(payload) -4:len(payload) - 2], 16)) and (crcResult[1] == int(payload[len(payload) -2:len(payload)], 16)):
            return True
        else:
            return False

if __name__ == '__main__':
    #VIN="UCIT123456789ABCD"
    #SVTCmdReqMsg = SVTCmdReqMsg(VIN)
    #SVTCmdReqMsg.pack()
    DecodeMsg = DecodeMsg()
    print("is big endian = ", DecodeMsg.is_big_endian())
