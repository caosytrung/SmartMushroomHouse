from ctypes import cdll
lib = cdll.LoadLibrary('/home/pi/Desktop/AES/libf.so')
from numpy.ctypeslib import ndpointer
import numpy
import ctypes
from app.config.app_config import KEY_SIE

class AesDecryptData:
    def __init__(self):
        self.setup()

    def setup(self):
        self.funnSetup = lib.decryptDatas
        self.funnSetup.restype = None
        self.funnSetup.argtypes = [ndpointer(ctypes.c_byte, flags="C_CONTIGUOUS"),
                        ctypes.c_size_t,
                        ndpointer(ctypes.c_byte, flags="C_CONTIGUOUS")]
    def setCipherData(self,cipherArray):
        self.cipherData = numpy.asarray(cipherArray).astype(numpy.int8)
        self.plainData = numpy.asarray(cipherArray).astype(numpy.int8)
    def decryptData(self):
        self.funnSetup(self.cipherData,KEY_SIE,self.plainData);
        return self.plainData
    def getPlainData(self):
        return self.plainData
    def getCipher(self):
        return self.cipherData