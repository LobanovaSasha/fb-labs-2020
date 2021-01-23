import requests
import random


def power(num, pow, mod):
    result = 1
    binn= bin(pow)[2:]
    for i in range(len(binn)):
        if binn[i] != '0':
            result = (num * result) % mod
        if i == len(binn) - 1:
            break
        result = (result * result) % mod
    return result


def gcd(x,y):
    while (y):
        x, y = y, x % y
    return x


def inverse_of_el(el, mod):  # Знаходження оберненого та нсд  gcd = el * v + u * mod
    if el == 0:
        return 0
    if mod == 0:
        return el, 1, 0
    gcd, u, v = inverse_of_el(mod, el % mod)
    return gcd, v, u - (el // mod) * v


def prime_check(number_to_check):  # Імовірністний тест Ферма
    accuracy = 100  # Обираєм точніть
    for i in range(accuracy):  # крок 0 і 1 починаєм ітеруватись до вказаної ймовіносі
        x = random.randint(2, number_to_check)  # Обираєм незалежне випадкове число
        gcd = inverse_of_el(x, number_to_check)[0]  # Знаходим НСД за алгоритмом Евкліда
        if gcd > 1:  # Якщо більше 1 то не просте
            return False
        else:  # Інакше крок 2
            value = power(x, number_to_check - 1, number_to_check)  # Рахуєм х^(p-1) mod p
            if value == 1:  # Якщо одиниця то р - псевдопросте за х і переходим до наступної ітерації
                continue
            else:  # шнакше не псевдо просте, а отже складне
                return False
    return True  # Якщо пройшли всі провірки то число просте


def generate_prime(num_len_in_bit):  # Генерація простих чисел вказаної довжини в бітах
    minimum = pow(2, num_len_in_bit)
    maximum = pow(2, num_len_in_bit + 1) - 1
    prime = random.randint(minimum, maximum)
    if prime % 2 != 1:
        prime += 1
    while not prime_check(prime):
        prime += 2
    return prime


def generate_keys(key_length):  # Генерація ключів вказаної довжини в бітах
    minimum =2**key_length
    maximum = 2 ** (key_length + 1) - 1
    p = generate_prime(key_length // 2)
    q = generate_prime(key_length // 2)
    n = p * q
    while not minimum <= n <= maximum:
        p = generate_prime(key_length // 2)
        q = generate_prime(key_length // 2)
        n = p * q
    fi_n = (p - 1) * (q - 1)
    pub_exp = pow(2, 16) + 1
    d = inverse_of_el(pub_exp ,fi_n)[1]% fi_n
    return p, q, pub_exp, d, n


def send_message(text, d, n, e1,n1):
    Signature = power(text, d, n)
    Cipher_text = power(text, e1, n1)
    S1ignature= power(Signature, e1, n1)
    return Cipher_text, S1ignature

def recieve_msg(ctext,s1, e, n, d1, n1):
    msg = power(ctext,d1, n1)
    sign = power(s1, d1,n1)
    chck = power(sign, e, n)
    if msg == chck:
        print("=======Verified=======")
    else:
        print("=======Opps, something went wrong=======")
    print("Decryped message: ", msg)
Alice = dict()
alice = generate_keys(256)
Alice['p']= alice[0]
Alice['q']= alice[1]
Alice['exp']= alice[2]
Alice['d']= alice[3]
Alice['n']=alice[4]
Bob = dict()
bob = generate_keys(257)
Bob['p']= bob[0]
Bob['q']= bob[1]
Bob['exp']= bob[2]
Bob['d']= bob[3]
Bob['n']=bob[4]

print("Keys:  ")
print("=====================Alice=====================")
print("p: ", hex(Alice['p']))
print("q: ", hex(Alice['q']))
print("exp: ", hex(Alice['exp']))
print("d: ", hex(Alice['d']))
print("n: ", hex(Alice['n']))
print("=====================Bob=====================")
print("p: ", hex(Bob['p']))
print("q: ", hex(Bob['q']))
print("exp: ", hex(Bob['exp']))
print("d: ", hex(Bob['d']))
print("n: ", hex(Bob['n']))
text = random.randint(1000,9999)
print("========Generated open message: ", text, " =========")
ciphertxt,S1= send_message(text, Alice['d'], Alice['n'], Bob['exp'], Bob['n'])
recieve_msg(ciphertxt, S1, Alice['exp'], Alice['n'],Bob['d'], Bob['n'])

print("\n\n=========Server=========\n\n")

public_key_request = f"http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize=300"
server_public_key = requests.get(public_key_request)
print("\n\n\nServer public key:" + str(server_public_key.json()))
serv_public_mod = int(server_public_key.json()["modulus"], 16)
serv_public_exp = int(server_public_key.json()["publicExponent"], 16)
text = random.randint(1000,9999)
ciphertxt,S1= send_message(text, Alice['d'], Alice['n'], serv_public_exp, serv_public_mod)
print("========Generated open message: ", text, " =========")

send_public_key = f"http://asymcryptwebservice.appspot.com/rsa/receiveKey?key={hex(ciphertxt)[2:]}" \
                  f"&signature={hex(S1)[2:]}&modulus={hex(Alice['n'])[2:]}&publicExponent={hex(Alice['exp'])[2:]}"
verify_signature_request = requests.get(send_public_key, cookies=server_public_key.cookies)
verified_text = int(verify_signature_request.json()["key"], 16)
verification_result = verify_signature_request.json()["verified"]
print("msg server got after verification: " + str(verified_text) + "\nverification result: " + str(verification_result))
