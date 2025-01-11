# Local components
from project_caesar.code import address, public_key, secret_key


def get_secret_key_1():
    return '00010001'

def get_secret_key_2():
    return '00020002'

def get_secret_key_3():
    return '00030003'


if __name__ == '__main__':

    sk = get_secret_key_3()
    print(sk)

    pk = public_key.secret_key_to_public_key(sk)
    print(pk)

    pk_hash = public_key.get_public_key_hash(pk)
    print(pk_hash)

    a = address.public_key_to_address(pk)
    print(a)


# Results: Secret Key 1 (Source 1)
# 00010001
# deaebef0
# f575f780
# csr_abafbc00


# Results: Secret Key 2 (Wallet 1)
# 00020002
# deafbef1
# f57df788
# csr_abefbc40


# Results: Secret Key 2 (Node 1)
# 00030003
# deb0bef2
# f585f790
# csr_ac2fbc80

