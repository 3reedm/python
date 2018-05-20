from random import randrange
from struct import pack
from binascii import b2a_hex

class MD4:
    def __init__(self):
        self.saMode = 1
    
    # Функция вызова для получения хеша
    def get_hash(self, text):
        result = self.md4_main(text)
        return result
    
    # Главная функция
    def md4_main(self, strIn):

        x = self.str_to_blks(strIn)
        
        a = 1732584193
        b = -271733879
        c = -1732584194
        d = 271733878

        for i in range(0, len(x), 16):
            olda = a
            oldb = b
            oldc = c
            oldd = d

            # Раунд 1
            a = self.md4_ff(a, b, c, d, x[i+0], 3)
            d = self.md4_ff(d, a, b, c, x[i+1], 7)
            c = self.md4_ff(c, d, a, b, x[i+2], 11)
            b = self.md4_ff(b, c, d, a, x[i+3], 19)
            a = self.md4_ff(a, b, c, d, x[i+4], 3)
            d = self.md4_ff(d, a, b, c, x[i+5], 7)
            c = self.md4_ff(c, d, a, b, x[i+6], 11)
            b = self.md4_ff(b, c, d, a, x[i+7], 19)
            a = self.md4_ff(a, b, c, d, x[i+8], 3)
            d = self.md4_ff(d, a, b, c, x[i+9], 7)
            c = self.md4_ff(c, d, a, b, x[i+10], 11)
            b = self.md4_ff(b, c, d, a, x[i+11], 19)
            a = self.md4_ff(a, b, c, d, x[i+12], 3)
            d = self.md4_ff(d, a, b, c, x[i+13], 7)
            c = self.md4_ff(c, d, a, b, x[i+14], 11)
            b = self.md4_ff(b, c, d, a, x[i+15], 19)

            # Раунд 2
            a = self.md4_gg(a, b, c, d, x[i+0], 3)
            d = self.md4_gg(d, a, b, c, x[i+4], 5)
            c = self.md4_gg(c, d, a, b, x[i+8], 9)
            b = self.md4_gg(b, c, d, a, x[i+12], 13)
            a = self.md4_gg(a, b, c, d, x[i+1], 3)
            d = self.md4_gg(d, a, b, c, x[i+5], 5)
            c = self.md4_gg(c, d, a, b, x[i+9], 9)
            b = self.md4_gg(b, c, d, a, x[i+13], 13)
            a = self.md4_gg(a, b, c, d, x[i+2], 3)
            d = self.md4_gg(d, a, b, c, x[i+6], 5)
            c = self.md4_gg(c, d, a, b, x[i+10], 9)
            b = self.md4_gg(b, c, d, a, x[i+14], 13)
            a = self.md4_gg(a, b, c, d, x[i+3], 3)
            d = self.md4_gg(d, a, b, c, x[i+7], 5)
            c = self.md4_gg(c, d, a, b, x[i+11], 9)
            b = self.md4_gg(b, c, d, a, x[i+15], 13)

            # Раунд 3
            a = self.md4_hh(a, b, c, d, x[i+0], 3)
            d = self.md4_hh(d, a, b, c, x[i+8], 9)
            c = self.md4_hh(c, d, a, b, x[i+4], 11)
            b = self.md4_hh(b, c, d, a, x[i+12], 15)
            a = self.md4_hh(a, b, c, d, x[i+2], 3)
            d = self.md4_hh(d, a, b, c, x[i+10], 9)
            c = self.md4_hh(c, d, a, b, x[i+6], 11)
            b = self.md4_hh(b, c, d, a, x[i+14], 15)
            a = self.md4_hh(a, b, c, d, x[i+1], 3)
            d = self.md4_hh(d, a, b, c, x[i+9], 9)
            c = self.md4_hh(c, d, a, b, x[i+5], 11)
            b = self.md4_hh(b, c, d, a, x[i+13], 15)
            a = self.md4_hh(a, b, c, d, x[i+3], 3)
            d = self.md4_hh(d, a, b, c, x[i+11], 9)
            c = self.md4_hh(c, d, a, b, x[i+7], 11)
            b = self.md4_hh(b, c, d, a, x[i+15], 15)

            a = self.safe_add(a, olda)
            b = self.safe_add(b, oldb)
            c = self.safe_add(c, oldc)
            d = self.safe_add(d, oldd)
        
        x = pack('<4L', a, b, c, d)
        return b2a_hex(x)
    
    # Вспомогательные функции для раундов
    def md4_cmn(self, q, a, b, x, s, t):
        return self.safe_add(self.shift(self.safe_add(self.safe_add(a, q), self.safe_add(x, t)), s), b)

    def md4_ff(self, a, b, c, d, x, s):
        return self.md4_cmn((b & c) | ((~b) & d), a, 0, x, s, 0)

    def md4_gg(self, a, b, c, d, x, s):
        return self.md4_cmn((b & c) | (b & d) | (c & d), a, 0, x, s, 1518500249)

    def md4_hh(self, a, b, c, d, x, s):
        return self.md4_cmn(b ^ c ^ d, a, 0, x, s, 1859775393)
    
    # Общие вспомогательные функции
    
    # Деление сообщения на блоки
    def str_to_blks(self, strIn):
        lenstr = len(strIn)
        nblk = ((lenstr + 8) >> 6) + 1
        blks = [0 for s in range(nblk*16)]
        i = 0
        for i in range(lenstr):
            blks[i >> 2] |= (ord(strIn[i])) << ((i%4) * 8)
        i = lenstr
        blks[i >> 2] |= 0x80 << ((i%4) * 8)
        blks[nblk*16 - 2] = lenstr * 8
        return blks
    
    # Сложение слов (a, b, c, d) с их начальным значением после прохода трёх циклов (безопасный и небезопасный режим)
    def safe_add(self, x, y):
        if (self.saMode == 0):
            return (x + y) & 0xFFFFFFFF

        lsw = (x & 0xFFFF) + (y & 0xFFFF)
        msw = (x >> 16) + (y >> 16) + (lsw >> 16)
        return ((msw & 0xFFFF) << 16) | (lsw & 0xFFFF) 
       
    # Смещение
    def shift(self, num, cnt):
        return (num << cnt) | num >> (32 - cnt)    

class DSA:
    def __init__(self):
        self.hasher = MD4()
        self.q = 23
        self.p = 47
        self.g = 2**((self.p-1)//self.q)
        self.x = randrange(1, self.q)
        self.y = self.g**self.x % self.p
        
    def get_sign(self, message):
        r = 0
        s = 0
        while (r==0 or s==0):
            # Шаг 1
            k = randrange(1, self.q)
        
            # Шаг 2
            r = (self.g**k % self.p) % self.q
            if (r == 0):
                continue
        
            # Шаг 3
            hash = self.hasher.get_hash(message).decode()
            s = int(hash, 16) + self.x*r
        
            for i in range(1, self.q):
                kRev = i*k % self.q
                if (kRev == 1):
                    kRev = i
                    break
        
            s = kRev*s % self.q
        
        # Шаг 4
        sign = '0x' + hex(r)[2:].zfill(32) + hex(s)[2:].zfill(32)
        
        return sign
    
    def valid_sign(self, message, sign):
        r = int(sign[2:34], 16)
        s = int(sign[34:], 16)
               
        # Шаг 1
        for i in range(1, self.q):
            sRev = i*s % self.q
            if (sRev == 1):
                sRev = i
                break 
        w = sRev
       
        # Шаг 2
        hash = self.hasher.get_hash(message).decode()
        u1 = int(hash, 16)*w  % self.q
        
        # Шаг 3
        u2 = r*w % self.q
        
        # Шаг 4
        v = ((self.g**u1 * self.y**u2) % self.p) % self.q
        
        # Шаг 5
        if (v == r):
            return "Подпись верна"
        else:
            return "Подпись не верна"
        
def __main__():  
    # Входные данные  
    crypt = DSA() 
    
    # Действия
    print('\n' + str('Digital Signature Algorithm (use MD4)').center(80) + '\n')  
    print('Для простоты взяты следующие данные (в реальных случаях числа должны быть гораздо больше)')
    print('p: ' + str(crypt.p))
    print('q: ' + str(crypt.q))
    print('g: ' + str(crypt.g))
    
    message = ""
    sign = crypt.get_sign(message)
    validation = crypt.valid_sign(message, sign)
    print('\n' + str('EXAMPLE 1').center(80) + '\n')
    print('message: ' + message)
    print('x: ' + str(crypt.x))
    print('y: ' + str(crypt.y))
    print('signature: ' + sign)
    print('signature status: ' + validation)
    
    sign = "0x" + '4' + sign[3:]
    validation = crypt.valid_sign(message, sign)
    print('\n message: ' + message)
    print('x: ' + str(crypt.x))
    print('y: ' + str(crypt.y))
    print('signature: ' + sign)
    print('signature status: ' + validation)
    
    message = "abc"
    crypt.x = randrange(1, crypt.q)
    crypt.y = crypt.g**crypt.x % crypt.p
    sign = crypt.get_sign(message)
    validation = crypt.valid_sign(message, sign)
    print('\n' + str('EXAMPLE 2').center(80) + '\n')
    print('message: ' + message)
    print('x: ' + str(crypt.x))
    print('y: ' + str(crypt.y))
    print('signature: ' + sign)
    print('signature status: ' + validation)
    
    crypt.y = crypt.y + 1
    validation = crypt.valid_sign(message, sign)
    print('\n message: ' + message)
    print('x: ' + str(crypt.x))
    print('y: ' + str(crypt.y))
    print('signature: ' + sign)
    print('signature status: ' + validation)
    
if __name__ == '__main__':
    __main__()