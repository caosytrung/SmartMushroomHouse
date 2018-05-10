from ctypes import cdll
lib = cdll.LoadLibrary('/home/pi/Desktop/AES/libf.so')
#lib = cdll.LoadLibrary('/home/pi/Desktop/AES/adder.so')


from numpy.ctypeslib import ndpointer
import numpy
import ctypes
fun = lib.cfun
fun.restype = None
fun.argtypes = [ndpointer(ctypes.c_byte, flags="C_CONTIGUOUS"),
                ctypes.c_size_t,
                ndpointer(ctypes.c_byte, flags="C_CONTIGUOUS")]


indata = numpy.array((227,218,247,225,118,80,148,148,124,138,82,37,159,131,48,195,110,203,217,218,106,159,160,244,188,150,158,70,224,161,13,53)).astype(numpy.int8)
outdata = numpy.array((5,6,7)).astype(numpy.int8)

fun(indata, 32, outdata)

print(outdata)

 


