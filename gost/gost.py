from math import sqrt

class Gost:
    def __init__(self):
        self.__dictionary = {}
        for i in range(1040, 1104): 
            self.__dictionary[bin(ord(chr(i).encode('cp1251')))[2:]] = chr(i)
        self.__dictionary[bin(ord(chr(1025).encode('cp1251')))[2:]] = chr(1025)
        self.__dictionary[bin(ord(chr(1105).encode('cp1251')))[2:]] = chr(1105)
        
        # Таблица замены (определённая комитетом по стандартизации ТК 26 Росстандарта)
        self.__sblocks = [[12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
                          [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
                          [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
                          [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
                          [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
                          [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
                          [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
                          [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]]
    
    # Шифрование
    def encryption(self, textDecrypted, K):
        textPart = ''
        textEncrypted = ''
        
        keyPart = []
        for i in range(8):
            keyPart.append(K[i*4:(i+1)*4]);
        
        for i in range(2):
            for j in range(8):
                keyPart.append(keyPart[j])
        
        for i in range(7, -1, -1):
                keyPart.append(keyPart[i])
        
        for i in range(32):
            kIList = []   
            kIList = [bin(ord(s.encode('cp1251')))[2:].zfill(8) for s in keyPart[i]] 
            keyPart[i] = ''
            for j in range(len(kIList)):
                keyPart[i] = keyPart[i] + kIList[j]
        
        for i in range(0,len(textDecrypted),8):
            
            textPart = textDecrypted[i:i+8]
            textPartL = textPart[0:4]
            textPartR = textPart[4:8]
            
            aIList = []           
            aIList = [bin(ord(s.encode('cp1251')))[2:].zfill(8) for s in textPartL] 
            textPartL = ''
            for j in range(len(aIList)):
                textPartL = textPartL + aIList[j] 
      
            rIList = []           
            rIList = [bin(ord(s.encode('cp1251')))[2:].zfill(8) for s in textPartR] 
            textPartR = ''
            for j in range(len(rIList)):
                textPartR = textPartR + rIList[j] 
            
            for j in range(32):
                textPartTmp = textPartL
                
                f = self.f(textPartL, keyPart[j]);

                textPartL = bin(int(textPartR, 2)^int(f, 2))[2:].zfill(32)
                
                textPartR = textPartTmp
            
            textPartLE = ''
            textTmp = ''
            for i in range(0, len(textPartL), 4):
                textTmp = textPartL[i:i+4] 
                textPartLE = textPartLE + hex(int(textTmp, 2))[2:].upper()
            
            textPartRE = ''
            textTmp = ''
            for i in range(0, len(textPartR), 4):
                textTmp = textPartR[i:i+4] 
                textPartRE = textPartRE + hex(int(textTmp, 2))[2:].upper()
            
            textEncrypted = textEncrypted + textPartRE + textPartLE
        
        return textEncrypted
            
    # Дешифрование
    def decryption(self, textEncrypted, K):
        textPart = ''
        textDecrypted = ''
        
        keyPart = []
        for i in range(8):
            keyPart.append(K[i*4:(i+1)*4]);
        
        for i in range(3):
            for j in range(7, -1, -1):
                keyPart.append(keyPart[j])
        
        for i in range(32):
            kIList = []   
            kIList = [bin(ord(s.encode('cp1251')))[2:].zfill(8) for s in keyPart[i]] 
            keyPart[i] = ''
            for j in range(len(kIList)):
                keyPart[i] = keyPart[i] + kIList[j]
        
        for i in range(0,len(textEncrypted),16):            
            aIList = [] 
            for k in range(i,i+8,2):
                aIList.append(bin(int(textEncrypted[k], 16))[2:].zfill(4)+bin(int(textEncrypted[k+1], 16))[2:].zfill(4))
            textPartL = ''
            for j in range(len(aIList)):
                textPartL = textPartL + aIList[j] 
            
            rIList = []           
            for k in range(i+8,i+16,2):
                rIList.append(bin(int(textEncrypted[k], 16))[2:].zfill(4)+bin(int(textEncrypted[k+1], 16))[2:].zfill(4))
            textPartR = ''
            for j in range(len(rIList)):
                textPartR = textPartR + rIList[j] 
            
            for j in range(32):
                textPartTmp = textPartL
                
                f = self.f(textPartL, keyPart[j]);

                textPartL = bin(int(textPartR, 2)^int(f, 2))[2:].zfill(32)
                
                textPartR = textPartTmp
            
            textPartLE = ''
            textTmp = ''
            for i in range(0, len(textPartL), 8):
                textTmp = textPartL[i:i+8] 
                if (textTmp in self.__dictionary):
                    textPartLE = textPartLE + self.__dictionary[textTmp]
                else: 
                    textPartLE = textPartLE + chr(int(textTmp, 2))
            
            textPartRE = ''
            textTmp = ''
            for i in range(0, len(textPartR), 8):
                textTmp = textPartR[i:i+8] 
                if (textTmp in self.__dictionary):
                    textPartRE = textPartRE + self.__dictionary[textTmp]
                else: 
                    textPartRE = textPartRE + chr(int(textTmp, 2))
                
            textDecrypted = textDecrypted + textPartRE + textPartLE
        
        return textDecrypted
    
    # Функция замены
    def f(self, Ai, Ki):
        resSum = bin((int(Ai, 2)+int(Ki, 2)) % 2**32)[2:].zfill(32)
        res = []
        for i in range(8):
            res.append(resSum[i*4:(i+1)*4])
        
        resLine = ''
        for i in range(8): 
            resLine = resLine + bin(self.__sblocks[i][int(res[i], 2)])[2:].zfill(4)
        
        resShift = int(resLine, 2)
        
        resLine = resShift<<11 | resShift>>21
        resLine = bin(resLine)[13:]
        
        return resLine
    
def __main__():  
    # Входные данные  
    text = []
    tmp = ''
    for line in open('text.txt', 'rt'):
        tmp = line.strip()
        if ((len(tmp) % 8) != 0 or len(tmp) == 0):
            print('Ошибка! Длина текста не кратна длине блока (64 бит = 8 байт)')
            return False
        text.append(tmp)

    key = []
    for line in open('key.txt', 'rt'):
        tmp = line.strip()
        if (len(tmp) != 32):
            print('Ошибка! Задан ключ неверной длины (256 бит = 32 байт)')
            return False
        key.append(tmp)
    
    crypt = Gost()   
    cypher = []
    
    # Действия 
    print('\n' + str('-Gost Cipher-').center(80) + '\n')
    
    # Пример 1
    cypher.append(crypt.encryption(text[0], key[0]))
    print('\n' + str('EXAMPLE 1').center(80) + '\n')
    print('input message: ' + text[0])
    print('input key: ' + key[0])
    print('encrypted message: ' + cypher[0])
    text[0] = crypt.decryption(cypher[0], key[0])
    print('decrypted message: ' + text[0])    
    
    # Пример 2
    cypher.append(crypt.encryption(text[0], key[1]))
    print('\n' + str('EXAMPLE 2').center(80) + '\n')
    print('input message: ' + text[0])
    print('input key: ' + key[1])
    print('encrypted message: ' + cypher[1])
    text[0] = crypt.decryption(cypher[1], key[1])
    print('decrypted message: ' + text[0]) 

    # Пример 3
    cypher.append(crypt.encryption(text[1], key[1]))
    print('\n' + str('EXAMPLE 3').center(80) + '\n')
    print('input message: ' + text[1])
    print('input key: ' + key[1])
    print('encrypted message: ' + cypher[2])
    text[1] = crypt.decryption(cypher[2], key[1])
    print('decrypted message: ' + text[1])     
    
if __name__ == '__main__':
    __main__()