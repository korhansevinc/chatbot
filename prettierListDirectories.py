import os
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# . --> % 'ye çevrilecek. Güncel olarak nokta çünkü eski chat session'lara erişim sağlanmasını istiyoruz.
def prettierListDirChatSessions(listdir):
    #listdir = os.listdir(config["chat_history_path"])
    #print(f"Type of listdir is : {type(listdir)}")
    listdirPrettier = []
    for dir in listdir :
       # prettyNameForDir = dir[:dir.index("%")]
        if "." in dir :
            prettyNameForDir = dir[:dir.index(".")]
            listdirPrettier.append(prettyNameForDir)
        else:
            listdirPrettier.append(dir)
    
    return listdirPrettier

def main():
    listdir = ["Selam.rand.json", "AAAA.rand342.json"]
    listdir = prettierListDirChatSessions(listdir)
    print(f"Listdir :  {listdir}")
    print(f"Type of listdir2 is : {type(listdir)}")
    print("Successfully prettier.")

if __name__ == "__main__" :
    main()