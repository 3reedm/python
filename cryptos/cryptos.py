from math import sqrt

class Cryptographer :

    # Шифрование
    def encryption(self, textDecrypted, key, keySystem = 16) :
            
        systemType = ''
        if (keySystem == 2) :
            systemType = 'bin'
        elif (keySystem == 8) :
            systemType = 'oct'
        else : 
            systemType = 'hex'
        
        decryptedLine = []
        keyLine = []        
        decryptedLine = [bin(ord(s.encode('cp1251')))[2:].zfill(int(sqrt(keySystem) * 2)) for s in textDecrypted] 
        keyLine = [e for e in key.split()]
            
        for i in range(len(keyLine)) :
            key = ''
            for p in keyLine[i] :
                key = key + bin(int(p, keySystem))[2:].zfill(int(sqrt(keySystem)))
            keyLine[i] = key
        
        encryptedLine = []
        for dLi, kLi in zip(decryptedLine, keyLine) :
            eLi = ''
            for dLii, kLii in zip(dLi, kLi) : 
                eLi = eLi + bin((int(dLii, 2) + int(kLii, 2)) % 2)[2:]
            encryptedLine.append(eLi)
        
        textLine = ''
        for e in encryptedLine :
            textLine = textLine + eval(systemType)(int(e, 2))[2:].upper().zfill(2) + ' '
            
        return textLine[:-1]
    
    # Дешифрование
    def decryption(self, textEncrypted, key, encryptedSystem = 16) :
                    
        systemType = ''
        if (encryptedSystem == 2) :
            systemType = 'bin'
        elif (encryptedSystem == 8) :
            systemType = 'oct'
        else : 
            systemType = 'hex'
        
        dictionary = {}
        for i in range(1040, 1104) : 
            dictionary[eval(systemType)(ord(chr(i).encode('cp1251')))[2:].upper()] = chr(i)
        dictionary[eval(systemType)(ord(chr(1025).encode('cp1251')))[2:].upper()] = chr(1025)
        dictionary[eval(systemType)(ord(chr(1105).encode('cp1251')))[2:].upper()] = chr(1105)
        
        encryptedLine = []
        keyLine = []
        encryptedLine = [e for e in textEncrypted.split()] 
        keyLine = [e for e in key.split()]
        
        for i in range(len(encryptedLine)) :
            encrypt = ''
            for p in encryptedLine[i] :
                encrypt = encrypt + bin(int(p, encryptedSystem))[2:].zfill(int(sqrt(encryptedSystem)))
            encryptedLine[i] = encrypt
            
        for i in range(len(keyLine)) :
            key = ''
            for p in keyLine[i] :
                key = key + bin(int(p, encryptedSystem))[2:].zfill(int(sqrt(encryptedSystem)))
            keyLine[i] = key
        
        decryptedLine = []
        for eLi, kLi in zip(encryptedLine, keyLine) :
            dLi = ''
            for eLii, kLii in zip(eLi, kLi) : 
                dLi = dLi + bin((int(eLii, 2) + int(kLii, 2)) % 2)[2:] 
            decryptedLine.append(eval(systemType)(int(dLi, 2))[2:].upper())
        
        textLine = ''
        for e in decryptedLine :
            if (e in dictionary) :
                textLine = textLine + dictionary[e]
            else : 
                textLine = textLine + chr(int(e, encryptedSystem))
            
        return textLine
        
    def unKeyDecryption(self, textEncrypted1, textEncrypted2, textDecrypted, encryptedSystem = 16) : 
        
        systemType = ''
        if (encryptedSystem == 2) :
            systemType = 'bin'
        elif (encryptedSystem == 8) :
            systemType = 'oct'
        else : 
            systemType = 'hex'
        
        encryptedLine1 = []
        encryptedLine2 = []
        encryptedLine1 = [e for e in textEncrypted1.split()] 
        encryptedLine2 = [e for e in textEncrypted2.split()]
            
        for i in range(len(encryptedLine1)) :
            encrypt = ''
            for p in encryptedLine1[i] :
                encrypt = encrypt + bin(int(p, encryptedSystem))[2:].zfill(int(sqrt(encryptedSystem)))
            encryptedLine1[i] = encrypt
            
        for i in range(len(encryptedLine2)) :
            encrypt = ''
            for p in encryptedLine2[i] :
                encrypt = encrypt + bin(int(p, encryptedSystem))[2:].zfill(int(sqrt(encryptedSystem)))
            encryptedLine2[i] = encrypt
         
        encryptedLine = []
        for eL1i, eL2i in zip(encryptedLine1, encryptedLine2) :
            eLi = ''
            for eL1ii, eL2ii in zip(eL1i, eL2i) : 
                eLi = eLi + bin((int(eL1ii, 2) + int(eL2ii, 2)) % 2)[2:]
            encryptedLine.append(eLi)
        
        textLine = ''
        for e in encryptedLine :
            textLine = textLine + eval(systemType)(int(e, 2))[2:].upper().zfill(2) + ' '
          
        textDecryptedTmp = ''
        for s in textDecrypted :
            textDecryptedTmp = textDecryptedTmp + eval(systemType)(ord(s.encode('cp1251')))[2:].upper() + ' '
        
        textDecryptedOther = self.decryption(textDecryptedTmp[:-1], textLine, encryptedSystem)
  
        return textDecryptedOther
        
def __main__() :
    
    # Входные данные  
    text = []
    for line in open('text.txt', 'rt') :
        text.append(line.strip())

    key = []
    for line in open('key.txt', 'rt') :
        key.append(line.strip())
    
    crypt = Cryptographer()   
    cypher = []
    
    # Действия 
    # Задание 1
    print('\n' + str('-Exercise 1-').center(80) + '\n')
    
    cypher.append(crypt.encryption(text[0], key[0]))
    print('input message : ' + text[0])
    print('input key : ' + key[0])
    print('encrypted message: ' + cypher[0])
    
    text[0] = crypt.decryption(cypher[0], key[0])
    print('decrypted message: ' + text[0])
    
    key.append(crypt.encryption(text[1], cypher[0]))
    print('\n' + 'input message : ' + text[1])
    print('encrypted message : ' + cypher[0])
    print('decrypted key : ' + key[1])
    
    text[1] = crypt.decryption(cypher[0], key[1])
    print('decrypted message : ' + text[1])
    print('\n' + str().center(80, '<') + '\n')
    
    # Задание 2
    print(str('-Exercise 2-').center(80))
    
    print('\ninput key : ' + key[0])
    for i in range(2, 4) : 
        cypher.append(crypt.encryption(text[i], key[0]))
        print(str(i - 1) + ' input message : ' + text[i])
        print(str(i - 1) + ' encrypted message : ' + cypher[i - 1])
    
    text[3] = crypt.unKeyDecryption(cypher[1], cypher[2], text[2])
    print('\n' + 'first encrypted message : ' + cypher[1])
    print('second encrypted message : ' + cypher[2])
    print('one known message : ' + text[2])
    print('decrypted message (without key) : ' + text[3])

if __name__ == '__main__' :
    __main__()
