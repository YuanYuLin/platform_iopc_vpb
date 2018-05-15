#!/bin/python2.7

import struct
import pprint
import sys
import ConfigParser

'''
[Boot disk layout]
'''

def create_buffer(record_count, record_size):
    buff=[]
    for idx in range(0, record_count):
        buff.append(bytearray('\0' * record_size))

    return buff

def dao_to_buffer(dao, buff, record_format, data_size):
    g_index=0
    for key in dao.keys():
        pad = bytearray(str.encode('\0' *  data_size))

        idx=0
        for ch in bytearray(key):
            pad[idx]=ch
            idx+=1

        for ch in bytearray(dao[key]):
            pad[idx]=ch
            idx+=1

        data = struct.pack(record_format, 0, 1, len(key), len(dao[key]), 0, str(pad))

        idx=0
        for ch in bytearray(data):
            buff[g_index][idx] = ch
            idx+=1
        g_index+=1

    return buff

def out_to_binary(buff):
    #create_buffer(1, (64 * 1024))
    #struct.pack("12sH50s", "$[IOPC_DATA]", record_count, bytearray('\0' * 50))
    fd=open('db_init.bin', 'wb')
    for rec in buff:
        fd.write(rec)
    fd.close()

def out_to_c(buff, record_count, record_format):
    ft=open('db_init.inc', 'w')
    ft.write('#define DAO_KV_MAX ' + str(record_count) + '\n')
    ft.write('static struct dao_kv_512_t dao_kv_list[DAO_KV_MAX]={')
    idx=0
    for rec in buff:
        csum, tp, kl, vl, rsv, data = struct.unpack(record_format, rec)
        ft.write('\n' + '{')
        ft.write(str(int(csum)))
        ft.write(',')
        ft.write(str(int(tp)))
        ft.write(',')
        ft.write(str(int(kl)))
        ft.write(',')
        ft.write(str(int(vl)))
        ft.write(',')
        ft.write(str(int(rsv)))
        ft.write(',{')
        for ch in bytearray(data):
            ft.write(str(int(ch)))
            ft.write(',')
        ft.write('},')
        ft.write('},')
    ft.write('};')
    ft.close()

def help():
    print "usage: dao.py <dao.ini>"
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
    dao={}
    cfg_ini = sys.argv[1]
    config = ConfigParser.RawConfigParser()
    config.read(cfg_ini)
    single_section = config.items("CFG_IMAGE")
    for item in single_section:
        print "key = %s, valule = %s" % (item[0], item[1])
        key = item[0]
        val = item[1]
        dao[key] = val
    sys.exit(1)

    header_size = 12
    data_size = 500
    record_count=128
    record_format="IBBHI" + str(data_size) + "s"
    record_size= header_size + data_size

    buf=create_buffer(record_count, record_size)
    buf=dao_to_buffer(dao, buf, record_format, data_size)
    out_to_binary(buf)
    out_to_c(buf, record_count, record_format)
