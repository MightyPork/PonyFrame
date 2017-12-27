import struct

class PayloadParser:
    """
    Utility for parsing a binary payload
    """

    def __init__(self, buf, endian:str='little'):
        """ buf - buffer to parse (bytearray or binary string) """
        self.buf = buf
        self.ptr = 0
        self.endian = endian

    def _slice(self, n:int) -> bytearray:
        """ Extract a slice and advance the read pointer for the next slice """
        if self.ptr + n > len(self.buf):
            raise Exception("Out of bounds")

        slice = self.buf[self.ptr:self.ptr + n]
        self.ptr += n
        return slice

    def rewind(self):
        """ Reset the slice pointer to the beginning """
        self.ptr = 0

    def tail(self) -> bytearray:
        """ Get all remaining bytes """
        return self._slice(len(self.buf) - self.ptr)

    def u8(self) -> int:
        """ Read a uint8_t """
        slice = self._slice(1)
        return int.from_bytes(slice, byteorder=self.endian, signed=False)

    def u16(self) -> int:
        """ Read a uint16_t """
        slice = self._slice(2)
        return int.from_bytes(slice, byteorder=self.endian, signed=False)

    def u32(self) -> int:
        """ Read a uint32_t """
        slice = self._slice(4)
        return int.from_bytes(slice, byteorder=self.endian, signed=False)

    def i8(self) -> int:
        """ Read a int8_t """
        slice = self._slice(1)
        return int.from_bytes(slice, byteorder=self.endian, signed=True)

    def i16(self) -> int:
        """ Read a int16_t """
        slice = self._slice(2)
        return int.from_bytes(slice, byteorder=self.endian, signed=True)

    def i32(self) -> int:
        """ Read a int32_t """
        slice = self._slice(4)
        return int.from_bytes(slice, byteorder=self.endian, signed=True)

    def float(self) -> float:
        """ Read a float (4 bytes) """
        slice = self._slice(4)
        fmt = '<f' if self.endian == 'little' else '>f'
        return struct.unpack(fmt, slice)[0]

    def double(self) -> float:
        """ Read a double (8 bytes) """
        slice = self._slice(8)
        fmt = '<d' if self.endian == 'little' else '>d'
        return struct.unpack(fmt, slice)[0]

    def bool(self) -> bool:
        """ Read a bool (1 byte, True if != 0) """
        return 0 != self._slice(1)[0]

    def str(self) -> str:
        """ Read a zero-terminated string """
        p = self.ptr
        while p < len(self.buf) and self.buf[p] != 0:
            p += 1

        bs = self._slice(p - self.ptr)
        self.ptr += 1
        return bs.decode('utf-8')

    def blob(self, length) -> bytearray:
        """ Read a blob of given length """
        return self._slice(length)
