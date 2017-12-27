import struct

class PayloadBuilder:
    """
    Utility for building binary payloads
    """

    def __init__(self, endian='little'):
        self.buf = bytearray()
        self.endian = endian

    def close(self):
        """ Get the byte buffer """
        return self.buf

    def u8(self, num):
        """ Add a uint8_t """
        self.buf.extend(num.to_bytes(length=1, byteorder=self.endian, signed=False))

    def u16(self, num):
        """ Add a uint16_t """
        self.buf.extend(num.to_bytes(length=2, byteorder=self.endian, signed=False))

    def u32(self, num):
        """ Add a uint32_t """
        self.buf.extend(num.to_bytes(length=4, byteorder=self.endian, signed=False))

    def i8(self, num):
        """ Add a int8_t """
        self.buf.extend(num.to_bytes(length=1, byteorder=self.endian, signed=True))

    def i16(self, num):
        """ Add a int16_t """
        self.buf.extend(num.to_bytes(length=2, byteorder=self.endian, signed=True))

    def i32(self, num):
        """ Add a int32_t """
        self.buf.extend(num.to_bytes(length=4, byteorder=self.endian, signed=True))

    def float(self, num):
        """ Add a float (4 bytes) """
        fmt = '<f' if self.endian == 'little' else '>f'
        self.buf.extend(struct.pack(fmt, num))

    def double(self, num):
        """ Add a double (8 bytes) """
        fmt = '<d' if self.endian == 'little' else '>d'
        self.buf.extend(struct.pack(fmt, num))

    def bool(self, num):
        """ Add a bool (0 or 1) """
        self.buf.append(1 if num != False else 0)

    def str(self, string):
        """ Add a 0-terminated string """
        self.buf.extend(string.encode('utf-8'))
        self.buf.append(0)

    def blob(self, blob):
        """ Ad an arbitrary blob (bytearray or binary string) """
        self.buf.extend(blob)
