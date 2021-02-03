#!/usr/bin/env python3
# -*- coding: utf-8 -*-#

###########################################################################
#                   Copyright by UCIT                                     #
#         Create by sunshiguo for simulating RC Horn/Flash Cmd Msg        #
#                                                                         #
#                         2021.01.15                                      #
#                                                                         #
#                                                                         #
###########################################################################


from ctypes import *
import time
import struct
import binascii
from sys import byteorder
import CommonMsg

class RCHornFlashReqMsg(BigEndianStructure):
    _fields_ = [("businessType",c_ushort),
                ("protocolVerNum",c_byte),
                ("flag",c_ubyte),
                ("serialNum",c_ushort),
                ("vinLen",c_ushort),
                ("vin",c_byte * 17),
                ("time",c_ubyte * 6),
                ("tokenLen", c_ushort),
                ("token", c_ubyte*16),
                ("u8RCvalitionTime", c_ubyte),
                ("u16DurationOfHonk", c_ushort),
                ("u16DurationOfFlash", c_ushort),
                ("requestIdLen", c_ushort),
                ("requestId", c_ubyte*10)]

    def __init__(self, VIN):
        self.businessType = 0x1102
        self.protocolVerNum = 0x04
        self.flag   = 0xC0
        self.serialNum = 0x0111
        #0x0011
        self.vinLen = 0x0011
        for i in range(len(VIN)):
            self.vin[i] = ord(VIN[i])
        curTime = int(time.time())
        timeTmp = [0x00,0x00,0x00,0x00,0x00,0x00]
        timeTmp[0] = (curTime&0xFF0000000000)>>40
        timeTmp[1] = (curTime&0x00FF00000000)>>32
        timeTmp[2] = (curTime&0x0000FF000000)>>24
        timeTmp[3] = (curTime&0x000000FF0000)>>16
        timeTmp[4] = (curTime&0x00000000FF00)>>8
        timeTmp[5] = curTime&0x0000000000FF
        for i in range(6):
            self.time[i] = timeTmp[i]
        #0x0010
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

        # 0x205	下发有效时间
        self.u8RCvalitionTime= 0x50
        #0x90A 鸣笛持续时间
        self.u16DurationOfHonk = 0x0010
        #0x90B	闪灯持续时间
        self.u16DurationOfFlash = 0x0020
        #0x000A
        self.requestIdLen = 0x000A
        self.requestId[0] = ord('r')
        self.requestId[1] = ord('e')
        self.requestId[2] = ord('q')
        self.requestId[3] = ord('u')
        self.requestId[4] = ord('e')
        self.requestId[5] = ord('s')
        self.requestId[6] = ord('t')
        self.requestId[7] = ord('I')
        self.requestId[8] = ord('d')
        self.requestId[9] = ord('1')

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
        #print("timeStr=",timeStr)

        vinStr=''
        for i in range(17):
            vinStr += '{:02x}'.format(self.vin[i])
        #print("vinStr=",vinStr)

        #encode Token
        payloadStr = '00B4'
        payloadStr += '{:04x}'.format(self.tokenLen)
        for i in range(16):
            payloadStr += '{:02x}'.format(self.token[i])
        #print("payloadStr=",payloadStr)

        #encode validationTime
        payloadStr += '2050'
        payloadStr += '{:02x}'.format(self.u8RCvalitionTime)
        #print("payloadStr=",payloadStr)

        #encode Duration Honk
        payloadStr += '90A1'
        payloadStr += '{:04x}'.format(self.u16DurationOfHonk)
        #print("payloadStr=",payloadStr)

        #encode Duration Flash
        payloadStr += '90B1'
        payloadStr += '{:04x}'.format(self.u16DurationOfFlash)
        #print("payloadStr=",payloadStr)

        #encode requestID
        payloadStr += '00D4'
        payloadStr += '{:04x}'.format(self.requestIdLen)
        for i in range(10):
            payloadStr += '{:02x}'.format(self.requestId[i])
        #print("payloadStr=",payloadStr)

        bufferTmp = '{:04x}{:02x}{:02x}{:04x}{:04x}'.format(self.businessType, self.protocolVerNum, self.flag, self.serialNum, self.vinLen)
        buffer  = bufferTmp + vinStr + timeStr + payloadStr
        bufferBytes = bytes(buffer, encoding="utf-8")

        EncodeMsg = CommonMsg.EncodeMsg()
        crcRet = EncodeMsg.get_crc(bufferBytes)
        crc0Str = '{:02x}'.format(crcRet[0])
        btmp = bytes(crc0Str, "utf-8")
        bufferTmp = bufferBytes + btmp
        crc1Str = '{:02x}'.format(crcRet[1])
        btmp = bytes(crc1Str, "utf-8")
        bufferTmp += btmp
        print("buffer+crc=",bufferTmp)

        return binascii.unhexlify(bufferTmp)

    def unpack(self, data):
        print("Only for reserved")

class RCHornFlashRespMsg(object):
    def decode_MsgBody(self, payload, UIDisp):
        sPayload = str(payload, encoding = "utf-8")
        if 0xc1 == int(sPayload[6:8], 16):
            UIDisp.connect_log("=========RC HornFlash Resp Msg Body begin===========")
            strlen = len(sPayload[72:])
            # 4 indicate no msgbody only have CRC
            if 4 == len(sPayload[72:]):
                UIDisp.connect_log("msgBody is NULLLLLLLL")
            else:
                UIDisp.connect_log("msgBody ="+sPayload[72:72+strlen-4])
            UIDisp.connect_log("=========RC HornFlash Resp Msg Body end  ===========")
        else:
            UIDisp.connect_log("=========RC HornFlash Resp Msg Body begin===========")
            strlen = len(sPayload[62:])
            #remove CRC part
            UIDisp.connect_log("msgBody ="+sPayload[62:62+strlen-4])
            length =  0
            DecodeMsg = CommonMsg.DecodeMsg()
            for i in range(3):
                UIDisp.connect_log("key=0x"+ '{:03x}'.format(DecodeMsg.decode_key(int(sPayload[62+length : 62+length +4], 16))))
                type = DecodeMsg.decode_type(int(sPayload[62+length : 62+length +4], 16))
                UIDisp.connect_log("type=0x"+'{:02x}'.format(type))
                #based on type to set len
                lenvalue =  DecodeMsg.decode_len(type)*2
                if 0 == lenvalue:
                    lenvalue = int(sPayload[62 + length + 4: 62 + length + 8], 16)
                    UIDisp.connect_log("len=0x" + '{:04x}'.format(lenvalue))
                    UIDisp.connect_log("data=" + sPayload[62 + length + 8: 62 + length + lenvalue])
                    length += (8 + lenvalue)
                else:
                    UIDisp.connect_log("len=0x" + '{:02x}'.format(lenvalue))
                    UIDisp.connect_log("data=" + sPayload[62 + length + 4: 62 + length + lenvalue])
                    length += (4 + lenvalue)
            UIDisp.connect_log("=========RC HornFlash Resp Msg Body end  ===========")

if __name__ == '__main__':
    #VIN="UCIT123456789ABCD"
    #SVTCmdReqMsg = SVTCmdReqMsg(VIN)
    #SVTCmdReqMsg.pack()
    RCHornFlashReqMsg = RCHornFlashReqMsg()
    DecodeMsg = CommonMsg.DecodeMsg()
    print("is big endian = ", DecodeMsg.is_big_endian())
