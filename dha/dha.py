from random import randrange
class User:	
    def __init__(self, name):
        self.__name = name
        self.__key = 0
        
    def send(self, addressee):
        addressee.gmessage = self.smessage**self.__number % self.mod
        
    def calculate(self):
        self.__key = self.gmessage**self.__number % self.mod
 
    def get_data(self): 
        return self.__name, str(self.__number), str(self.__key)
    
    def set_data(self, n, g):
        self.smessage = g
        self.mod = n
        self.__number = randrange(1, n)
    
class Diffie_Hellman:
    def __init__(self, users, n, g):
        self.users = users
        self.n = n
        self.g = g
        
    def encryption(self):
        
        # Регистрация общих параметров (n и g) и вычисление секретных ключей пользователей
        for user in self.users:
            user.set_data(self.n, self.g)
        
        # Циклическая перессылка
        nUsers = len(self.users)
        rounds = nUsers - 1
        for i in range(rounds):
            for j in range(nUsers-1):
                self.users[j].send(self.users[j+1])
            self.users[nUsers-1].send(self.users[0])
            for user in self.users:
                user.smessage = user.gmessage
        
        # Вычисление ключей
        for i in range(nUsers):
            self.users[i].calculate()
        
def __main__():  
    user1 = User("Alice")
    user2 = User("Bob")
    user3 = User("Carol")
    
    users = [user1, user2, user3]
    crypt = Diffie_Hellman(users, 23, 5)
    
    # Действия 
    print('\n' + str('-Diffie-Hellman Algorithm-').center(80) + '\n')  
    
    print(str('EXAMPLE 1').center(80) + '\n')
    print('n: ' + str(crypt.n))
    print('g: ' + str(crypt.g))
    
    crypt.encryption()
    print()
    for user in users:
        data = user.get_data()
        print("Имя пользователя: " + data[0] + "\n" +  "Секретный ключ пользователя: " + data[1] + "\n" + "Общий секретный ключ: " + data[2] + "\n")
   
    crypt.n = 29
    crypt.g = 7
    print(str('EXAMPLE 2').center(80) + '\n')
    print('n: ' + str(crypt.n))
    print('g: ' + str(crypt.g))
    
    crypt.users.append(User("David")) 
    crypt.encryption()
    print()
    for user in users:
        data = user.get_data()
        print("Имя пользователя: " + data[0] + "\n" +  "Секретный ключ пользователя: " + data[1] + "\n" + "Общий секретный ключ: " + data[2] + "\n")
    
if (__name__ == '__main__'):
    __main__()