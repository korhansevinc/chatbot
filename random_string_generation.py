import random
import string

def random_string(length):
    """
    Belirtilen uzunlukta rastgele karakterlerden oluşan bir string oluşturur. Başina özel karakter yerleştirir. (%)
    Güncel olarak . yerleştiriyor, bu % ye çevrilecek, eski chat'lere erişim için . olarak birakildi.
    
    Args:
    length (int): Oluşturulacak string'in uzunluğu.
    
    Returns:
    str: Oluşturulan rastgele karakterlerden oluşan string.
    """
    characters = string.ascii_letters + string.digits
    
    random_string = ''.join(random.choice(characters) for _ in range(length))
    random_string = ".rand" + random_string
    return random_string

def main():
    random_str = random_string(12)
    print(f"Random String is : {random_str}")

if __name__ == "__main__":
    main()
