import re
import string


def slicing_title(s, word):
    index = s.find(word)
    if index != -1 :
        return s[index+len(word) :]
    return s


def turkish_char_replacement(text):
    turkish_chars = {'ü': 'u', 'Ü': 'U', 'ç': 'c', 'Ç': 'C', 'ğ': 'g', 'Ğ': 'G', 'ö': 'o', 'Ö': 'O', 'ı' :'i', 'ş' : 's', 'Ş' : 'S', 'İ':'I'}
    for turkce, latin in turkish_chars.items():
        text = text.replace(turkce, latin)
    return text


def slicing_response(s):
    index = s.find(":")
    if index != -1 :
        return s[index+1 :]
    return s


def change_specials_with_space(string):
    string = turkish_char_replacement(string)
    return re.sub(r'[^a-zA-Z0-9]', ' ', string).strip()


def main():
    str = " Some awkard T'it'le ^?+ "
    print(f"Old version of str : {str}")
    # TEST - 1 
    str =change_specials_with_space(str)
    print(f"New version of str : {str}")
    # TEST - 2
    s= "Some"
    str = slicing_title(str,s)
    print(f"Second new version of str : {str}")
    # TEST - 3
    str = str + ": some text : " + " continued txt."
    print("str : ", str)
    str = slicing_response(str)
    print(f"Third New version of str : {str}")
    str = slicing_response(str)
    print(f"Fourth version of str : {str}")
    print("Succesfully done.")
    print("Last test : for Turkish to Latin : ")
    metin = "Bu örnek metin içerisinde özel Türkçe karakterler ü, ç, ğ bulunmaktadır."
    sonuc = turkish_char_replacement(metin)
    print(sonuc)


if __name__ == "__main__":
    main()