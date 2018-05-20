from random import randrange

class Point:	
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def add(self, point2, a, p):
        point3 = Point()
        point1 = self

        if (point1.x != point2.x):
            lamb = ((point1.y-point2.y) / (point1.x-point2.x)) % p
            point3.x = int(lamb**2 - point1.x - point2.x) % p
            point3.y = int(lamb*(point1.x-point3.x) - point1.y) % p
        else:
            if (point1.y == point2.y and point1.y != 0):
                lamb = ((3*point1.x**2+a) / (2*point1.y)) % p
                point3.x = int(lamb**2 - 2*point1.x) % p
                point3.y = int(lamb*(point1.x-point3.x) - point1.y) % p
        return point3

class Hash:
    def __init__(self):
        # Таблица замены (определённая комитетом по стандартизации ТК 26 
        #                 Росстандарта)
        self.__sblocks = \
                    [[12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
                     [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
                     [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
                     [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
                     [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
                     [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
                     [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
                     [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]]
        

        # self.__sblocks = \
                    # [[4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
                     # [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
                     # [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
                     # [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
                     # [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
                     # [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
                     # [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
                     # [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]]
    
    def E_f(self, A, K): 
        # Складываем по модулю 2^32. c - перенос  в следующий разряд
        c = 0
        R = [0x00 for i in range(4)]
        for i in range(4):
            c += A[i] + K[i]
            R[i] = c & 0xFF
            c >>= 8
        
        # Заменяем 4х-битные кусочки согласно S-блокам
        for i in range(8):                      
            x = R[i >> 1] & (0xF0 if (i & 1) else 0x0F)  # x - 4x-битный кусок
            R[i >> 1] ^= x                     # Обнуляем соответствующие биты
            x >>= 4 if (i & 1) else 0       # Сдвигаем x на 0 или 4 бита влево
            x = self.__sblocks[i][x]               # Заменяем согласно S-блоку 
            R[i >> 1] |= x << (4 if (i & 1) else 0)

        tmp = R[3]                          # Сдвигаем на 8 бит (1 байт) влево
        R[3] = R[2]
        R[2] = R[1]
        R[1] = R[0]
        R[0] = tmp 

        tmp = R[0] >> 5                         # Сдвигаем еще на 3 бита влево
        for i in range(1, 4):
            nTmp = R[i] >> 5
            R[i] = ((R[i] << 3) | tmp) & 0xFF
            tmp = nTmp
        R[0] = ((R[0] << 3) | tmp) & 0xFF
        
        return R
    
    def E(self, D, K):
        R = [0x00 for i in range(8)]
        
        # Инициализация блоков A и B
        A = [0x00 for i in range(4)]
        B = [0x00 for i in range(4)]
        for i in range(4): 
            A[i] = D[i]
            B[i] = D[i + 4]

        tmp = [0x00 for i in range(4)]
        for step in range(3):                  # K1..K24 идут в прямом порядке  
            for i in range(0, 32, 4):
                tmp = self.E_f(A, K[i:i+4])             
                for j in range(4):
                    tmp[j] ^= B[j];
                B = A[:]
                A = tmp[:]
                
        for i in range(28, -1, -4):       # А K25..K32 идут в обратном порядке
            tmp = self.E_f(A, K[i:i+4])
            for j in range(4):
                tmp[j] ^= B[j]
            B = A[:]
            A = tmp[:]

        for i in range(4): 
            R[i] = B[i]                                 # Возвращаем результат
            R[i + 4] = A[i]
        
        return R

    def A(self, Y):
        R = [0x00 for i in range(32)]
        for i in range(24):
            R[i] = Y[i + 8]
        for i in range(8):
            R[i + 24] = Y[i] ^ Y[i + 8]
        
        return R

    def fi(self, arg):
        i = arg & 0x03
        k = arg >> 2 
        k = k + 1
        
        return (i << 3) + k - 1
    
    def P(self, Y):
        R = [0x00 for i in range(32)]
        for i in range(32):
            R[i] = Y[self.fi(i)]
        
        return R

    def psi(self, arr, p):
        y16 = [0x00 for i in range(2)]
        
        while (p != 0):    
            y16[0] ^= arr[0] 
            y16[0] ^= arr[2] 
            y16[0] ^= arr[4] 
            y16[0] ^= arr[6] 
            y16[0] ^= arr[24]
            y16[0] ^= arr[30] 
            y16[1] ^= arr[1]
            y16[1] ^= arr[3]
            y16[1] ^= arr[5]
            y16[1] ^= arr[7]
            y16[1] ^= arr[25]
            y16[1] ^= arr[31]
            for i in range(30):
                arr[i] = arr[i + 2]
            arr[30] = y16[0] 
            arr[31] = y16[1]
            y16[0] = 0x00
            y16[1] = 0x00
            p = p - 1
        
        return arr

    # Функция f
    def f(self, H, M): 
        C = [[0x00 for i in range(32)], 
             [0x00 for i in range(32)], 
             [0x00 for i in range(32)], 
             [0x00 for i in range(32)]]

        C[2][0] = 0x00
        C[2][1] = 0xFF
        C[2][2] = 0x00
        C[2][3] = 0xFF
        C[2][4] = 0x00
        C[2][5] = 0xFF
        C[2][6] = 0x00
        C[2][7] = 0xFF
        C[2][8] = 0xFF
        C[2][9] = 0x00
        C[2][10] = 0xFF
        C[2][11] = 0x00
        C[2][12] = 0xFF
        C[2][13] = 0x00
        C[2][14] = 0xFF
        C[2][15] = 0x00
        C[2][16] = 0x00
        C[2][17] = 0xFF
        C[2][18] = 0xFF
        C[2][19] = 0x00
        C[2][20] = 0xFF
        C[2][21] = 0x00
        C[2][22] = 0x00
        C[2][23] = 0xFF
        C[2][24] = 0xFF
        C[2][25] = 0x00
        C[2][26] = 0x00
        C[2][27] = 0x00
        C[2][28] = 0xFF
        C[2][29] = 0xFF
        C[2][30] = 0x00
        C[2][31] = 0xFF

        U = [0x00 for i in range(32)]
        V = [0x00 for i in range(32)]
        W = [0x00 for i in range(32)]
        K = [[0x00 for i in range(32)], 
             [0x00 for i in range(32)], 
             [0x00 for i in range(32)], 
             [0x00 for i in range(32)]]
        tmp = [0x00 for i in range(32)]
        newH = [0x00 for i in range(32)]
        U = H[:]
        V = M[:]
        for i in range(32):
            W[i] = U[i] ^ V[i]
        K[0] = self.P(W)

        for step in range(1,4):
            tmp = self.A(U)
            for i in range(32):
                U[i] = tmp[i] ^ C[step][i]
            tmp = self.A(V)
            V = self.A(tmp)
            for i in range(32): 
                W[i] = U[i] ^ V[i]
            K[step] = self.P(W)

        S = [0x00 for i in range(32)]
        for i in range(0, 32, 8):
            S[i:i+8] = self.E(H[i:i+8], K[i >> 3])
        
        S = self.psi(S, 12) 
        for i in range(32):
            S[i] ^= M[i]
        S = self.psi(S, 1)
        for i in range(32): 
            S[i] ^= H[i]
        S = self.psi(S, 61)
        
        newH = S[:]
        
        return newH

    def hash(self, buf):
        length = len(buf)
        block = [0x00 for i in range(32)]
        Sum = [0x00 for i in range(32)]
        L = [0x00 for i in range(32)] 
        H = [0x00 for i in range(32)]
        newH = [0x00 for i in range(32)]
        result = [0x00 for i in range(32)]
        pos = 0
        posIB = 0

        while ((posIB < length) or pos != 0):
            if (posIB < length): 
                block[pos] = buf[posIB]
                pos = pos + 1
                posIB = posIB + 1
            else:
                block[pos] = 0
                pos = pos + 1
            if (pos == 32): 
                pos = 0

                c = 0
                for i in range(32):
                    c += block[i] + Sum[i]
                    Sum[i] = c & 0xFF
                    c >>= 8

                newH = self.f(H, block)
                H = newH[:]
        
        c = length << 3
        for i in range(32):
            L[i] = c & 0xFF
            c >>= 8
        newH = self.f(H, L)
        H = newH[:]
        newH = self.f(H, Sum)
        result = newH[:]
        
        return result
        
class Goste:
    def __init__(self):
        self.__hasher = Hash()
        
        # В десятичной системе 
        # self.p = int("57896044618658097711785492504" \
                     # "34395392663499233282028201972" \
                     # "8792003956564821041")
        self.p = 5
        self.a = 3
        # self.b = int("4330887654676727690576590" \
                     # "45956509319959421117944510395" \
                     # "83252968842033849580414")
        # self.m = int("57896044618658097711785492504" \
                     # "343953927082934583725450622380973" \
                     # "592137631069619")
        # self.q = int("57896044618658097711785492504" \
                     # "343953927082934583725450622380973" \
                     # "592137631069619")
        self.q = 11
        # self.P = Point() 
        # self.P.x = 2
        # self.P.y = int("40189740565390375033354494229" \
                       # "370597756357393899055450806909793" \
                       # "65213431566280")
        # self.d = int("5544119606536324612635562413032" \
                     # "418319657670922234001657210809775000" \
                     # "6097525544")
        self.P = Point(1, 0)
        
        self.d = 7
        # self.Q = Point()
        # self.Q.x = int("5752021612617680844363140502333" \
                       # "80711766301049063136321828967413422" \
                       # "06604859403")
        # self.Q.y = int("1761494441921378154380939194965" \
                       # "40800319426620453636392607098478594" \
                       # "38286763994")
        self.Q = Point(4, 0)
        
    # Шифрование (получение цифровой подписи)
    def encryption(self, message):
        # Входные данные (сообщение)
        symbolList = [hex(ord(el.encode('cp1251')))[2:].upper() 
                      for el in message]
        buf = [int(el, 16) for el in symbolList]
        
        # Вычисление хеш-кода (Шаг 1)
        hash = ""
        result = self.__hasher.hash(buf)
        for el in result:
            hash = hash + hex(el)[2:].zfill(2).upper() 
        
        # Вычисление e (Шаг 2)
        alfa = int(hash, 16)
        e = alfa % self.q
        if (e == 0):
            e = 1

        r = 0
        s = 0
        while (r==0 or s==0): 
            # Генерация k (Шаг 3)
            k = randrange(1, self.q) 
        
            # Вычисление точки C=kP (Шаг 4)
            C = self.P.add(self.P, self.a, self.p)
            k = k - 1
            while (k != 0):
                C = C.add(self.P, self.a, self.p) 
                k = k - 1

            r = C.x % self.q
            if (r == 0):
                continue
            
            # Вычисление s (Шаг 5)
            s = (r*self.d + k*e) % self.q
        
        # Вычисление хешей от r и s, 
        # определение цифровой подписи (sign) (Шаг 6)
        rhash = ""
        r = str(r)
        buf = [int(el) for el in r]
        result = self.__hasher.hash(buf)
        for el in result:
            rhash = rhash + hex(el)[2:].zfill(2).upper()
            
        shash = ""
        s = str(s)
        buf = [int(el) for el in s]
        result = self.__hasher.hash(buf)
        for el in result:
            shash = shash + hex(el)[2:].zfill(2).upper()
        
        sign = rhash + shash
        
        return sign
        
    # Проверка цифровой подписи
    def validation(self, message, sign):
        if ((len(sign) != 128) or not(0<=self.Q.x<self.p and 0<=self.Q.y<self.p)):
            return False
        
        # Вычисление r и s (Шаг 1)
        rhash = sign[:64]
        shash = sign[64:]
        flagR = False
        flagS = False
        
        for i in range(self.q):
            rhashv = ""
            tmp = str(i)
            buf = [int(el) for el in tmp]
            result = self.__hasher.hash(buf)
            for el in result:
                rhashv = rhashv + hex(el)[2:].zfill(2).upper()
            if (rhashv == rhash):
                r = i
                flagR = True
                
            shashv = ""
            tmp = str(i)
            buf = [int(el) for el in tmp]
            result = self.__hasher.hash(buf)
            for el in result:
                shashv = shashv + hex(el)[2:].zfill(2).upper()    
            if (shashv == shash):
                s = i
                flagS = True
        
        if (not(flagR and flagS)):
            return False
        
        # Вычисление хеша сообщения (Шаг 2)
        symbolList = [hex(ord(el.encode('cp1251')))[2:].upper() 
                      for el in message]
        buf = [int(el, 16) for el in symbolList]
        
        hash = ""
        result = self.__hasher.hash(buf)
        for el in result:
            hash = hash + hex(el)[2:].zfill(2).upper()
        
        # Вычисление e (Шаг 3)
        alfa = int(hash, 16)
        e = alfa % self.q
        if (e == 0):
            e = 1
        
        # Вычисление v (Шаг 4)
        for i in range(1, self.q): 
            backe = (e*i) % self.q
            if (backe == 1):
                backe = i
                break
        
        v = backe % self.q

        # Вычисление z1 и z2 (Шаг 5)
        z1 = s*v % self.q
        z2 = -r*v % self.q
        
        # Вычисление R (Шаг 6)
        C1 = self.P.add(self.P, self.a, self.p)
        z1 = z1 - 1
        while (z1 != 0):
            C1 = C1.add(self.P, self.a, self.p) 
            z1 = z1 - 1
        
        C2 = self.Q.add(self.Q, self.a, self.p)
        z2 = z2 - 1
        while (z2 != 0):
            C2 = C2.add(self.Q, self.a, self.p) 
            z2 = z2 - 1
        
        C = C1.add(C2, self.a, self.p)
        R = C.x % self.q
        
        # Сравнение данных (Шаг 7)
        if (R == r):
            return True
        else:
            return False
        
def __main__():  
    # Входные данные  
    data = []
    for line in open('data.txt', 'rt'):
        tmp = line.strip()
        data.append(tmp)
    
    signs = []
    crypt = Goste() 
    
    length = len(data)
    if (length == 10):
        crypt.d = data[0]
        crypt.Q.x = data[1]
        crypt.Q.y = data[2]
        crypt.p = data[3]
        crypt.a = data[4]
        crypt.b = data[5]
        crypt.m = data[6]
        crypt.q = data[7]
        crypt.P.x = data[8]
        crypt.P.y = data[9]
    elif (length == 3):
        crypt.d = data[0]
        crypt.Q.x = data[1]
        crypt.Q.y = data[2]

    # Действия 
    print('\n' + str('-Gost Digital Signature-').center(80) + '\n')  
    print('Для простоты взяты следующие данные (в реальных случаях числа должны быть гораздо больше)')
    print('p: ' + str(crypt.p))
    print('q: ' + str(crypt.q))
    print('a: ' + str(crypt.a))
    print('P: ' + '(' + str(crypt.P.x) + ';' + str(crypt.P.y) + ')')
    
    crypt.d = 7 
    crypt.Q.x = 4
    crypt.Q.y = 0
    signs.append(crypt.encryption(data[0]))
    print('\n' + str('EXAMPLE 1').center(80) + '\n')
    print('message: ' + data[0])
    print('d: ' + str(crypt.d))
    print('Q: ' + '(' + str(crypt.Q.x) + ';' + str(crypt.Q.y) + ')')
    print('signature: ' + signs[0])
    print('signature status: ' + ("valid" if crypt.validation(data[0], signs[0]) else "invalid"))
    
    crypt.d = 3 
    crypt.Q.x = 4
    crypt.Q.y = 4
    signs.append(crypt.encryption(data[1]))
    print('\n' + str('EXAMPLE 2').center(80) + '\n')
    print('message: ' + data[1])
    print('d: ' + str(crypt.d))
    print('Q: ' + '(' + str(crypt.Q.x) + ';' + str(crypt.Q.y) + ')')
    print('signature: ' + signs[1])
    print('signature status: ' + ("valid" if crypt.validation(data[1], signs[1]) else "invalid"))
    
    crypt.d = 3 
    crypt.Q.x = 0
    crypt.Q.y = 4
    signs.append(crypt.encryption(data[1]))
    print('\n' + str('EXAMPLE 3').center(80) + '\n')
    print('message: ' + data[1])
    print('d: ' + str(crypt.d))
    print('Q: ' + '(' + str(crypt.Q.x) + ';' + str(crypt.Q.y) + ')')
    print('signature: ' + signs[1])
    print('signature status: ' + ("valid" if crypt.validation(data[1], signs[1]) else "invalid"))
    
if __name__ == '__main__':
    __main__()