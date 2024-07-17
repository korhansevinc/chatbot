"""
    Main Class for Chatbot Application.
    It includes architectural connections( chat_sessions, embedding_model, LLM_model, voice_handler, image_handler ... )
    and necessary functions for basic UI
"""

import streamlit as st 
from langchain.memory import StreamlitChatMessageHistory
from streamlit_mic_recorder import mic_recorder
import llm_chains as llm_chain
import yaml
import os
from utils import save_chat_history_json, get_timestamp, load_chat_history_json
from voice_handling import transcribe_audio
from image_handling import handle_image
from pdf_handling import add_documents_to_database
from llm_chains import  load_pdf_chat_chain, summarizeChatChain
import torch
import time
from html_templates import get_bot_template, get_user_template, css
from random_string_generation import random_string
from prettierListDirectories import prettierListDirChatSessions
from chat_session_utils import change_specials_with_space, slicing_response, slicing_title


# This is for your own hardware. Change the max_split_size_mb:X -> X to your GPU's vram capacity.
torch.cuda.empty_cache()
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:7168"
print(f"{os.environ['PYTORCH_CUDA_ALLOC_CONF']}")
STREAMING_DELAY = 0.01

# Load the config file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


# To load llm chain with desired chat_history so we can run over llm by run or invoke function.
# Note : If langchain will be updated , then there would be a version for run function. 
# It can be changed with invoke function. {run() ---> invoke()} Then Human - AI req - response may be differ. Check for documentation
# Do not take offense if langchain version is < 0.2.0
def load_chain(chat_history):
    if st.session_state.pdf_chat:
        return load_pdf_chat_chain(chat_history)
    return llm_chain.load_normal_chain(chat_history)


# Deletes user_question after input
def clear_input_field():
    if st.session_state.user_question == "" :
        st.session_state.user_question = st.session_state.user_input
        st.session_state.user_input = ""

# Sets send_input True so we can actually pass it to the LLM
def set_send_input():
    st.session_state.send_input = True
    clear_input_field()


#To track the current session.
def track_index():
    st.session_state.session_index_tracker = st.session_state.session_key


# Saves the current chat_history in chat_sessions directory as a json file.
def save_chat_history(chat_history,current_user_q) :
    if st.session_state.history != []:
        if st.session_state.session_key == "Yeni Konuşma Başlat":
            users_prompt = current_user_q
            print("Summarizing...")
            new_chat_history = StreamlitChatMessageHistory(key="new_history") 
            llm_sum_chain = summarizeChatChain(new_chat_history)
            response = llm_sum_chain.runsum(users_prompt)
            #response = response[response.index(":"):]
            response = slicing_response(response)
            response = change_specials_with_space(response)
            print("\n The remaining is : ", response)
            random_str = random_string(12)
            st.session_state.new_session_key = response + random_str + ".json"
            save_chat_history_json(st.session_state.history, config["chat_history_path"] + st.session_state.new_session_key )
            #st.session_state.session_key = st.session_state.new_session_key
        else:
            save_chat_history_json(st.session_state.history, config["chat_history_path"] + st.session_state.session_key )
        print("History Saved !")

# Deletes selected chat_session.
def delete_chat_session():
    file_path = config["chat_history_path"] + st.session_state.session_key
    filename = st.session_state.session_key
    isFile = os.path.isfile(file_path)
    if isFile == True :
        print("The target file has found !")
        print("Deleting...")
        os.remove(file_path)
        print("Chat Session is successfully deleted.")
        return filename
    else :
        print("File Cannot Found !")
        return "Not Found"


# Returns the length of chat_history
def count_current_sessions_length(chat_history):
    current_session_count = 0
    for i in range (len(chat_history.messages)):
        current_session_count+=1
    return current_session_count


# Activating RAG.
def toggle_rag_system():
    st.session_state.pdf_chat = True


# Main function : Includes UI functions reserved by Streamlit and session_state architecture.
def main():
    st.title(" ChatBot  ")
    st.write(css, unsafe_allow_html=True)
    chat_container = st.container()
    st.sidebar.title("  Chatbot ")
    #st.sidebar.title("Konuşma Geçmişi")

    listDir = os.listdir(config["chat_history_path"])
    chat_sessions = ["Yeni Konuşma Başlat"] + listDir
    #print("Chat sessions : ", chat_sessions)
    llm_response = None
    current_user_q = None

    if "session_delete" not in st.session_state : 
        st.session_state.session_delete = False

    if "send_input" not in st.session_state :
        st.session_state.session_key = "Yeni Konuşma Başlat"
        st.session_state.send_input = False
        st.session_state.user_question = ""
        st.session_state.new_session_key = None
        st.session_state.session_index_tracker = "Yeni Konuşma Başlat"
    if st.session_state.session_key == "Yeni Konuşma Başlat" and st.session_state.new_session_key != None:
        st.session_state.session_index_tracker = st.session_state.new_session_key
        st.session_state.new_session_key = None

    index = chat_sessions.index(st.session_state.session_index_tracker)
    print("Index is : ", index)
    st.sidebar.selectbox("Bir Sohbet Oturumu Seçiniz", chat_sessions, key="session_key", index=index, on_change=track_index, format_func= lambda s: s.split('.',1)[0])
    st.sidebar.toggle("RAG Aktifleştir 🗃️", key="pdf_chat", value=False)

    if st.session_state.session_key == "Yeni Konuşma Başlat":
        st.sidebar.toggle("Oturum Silme Modu Aktifleştir 🗑️", key="session_delete", value=False)

    st.sidebar.button("Güncel Oturumu Sil", key="current_session_delete")


    if st.session_state.session_delete or st.session_state.current_session_delete :
        print("Session Delete Toggle is True")
        print("Session Delete Mode Activated.")
        st.toast("Sohbet Oturumu Silme Modu Aktif.")
        time.sleep(.5)
        st.toast("Lütfen Silmek İstediğiniz Oturumu Seçiniz.")
        time.sleep(.5)
        name = delete_chat_session()
        if name != "Not Found":
            st.toast(f"{name} Sohbet Oturumu Başarıyla Silindi.")
            st.success(f"{name} Sohbet Oturumu Başarıyla Silindi.")
            time.sleep(.5)
            st.toast("Oturum Silme Modunu Kapatmayı Unutmayın!")
            time.sleep(.5)
        
        


    if st.session_state.session_key != "Yeni Konuşma Başlat":
        file_path = config["chat_history_path"] + st.session_state.session_key
        if os.path.isfile(file_path):
            st.session_state.history = load_chat_history_json(file_path)
            print(f"Loading the session key : { st.session_state.session_key}")
            print(f"Sessionstate_user question is :  {st.session_state.user_question}")
        else:   
            st.session_state.session_index_tracker = "Yeni Konuşma Başlat"
            st.rerun()
    else :
        st.session_state.history = []

    chat_history = StreamlitChatMessageHistory(key="history") 
    llm_chain = load_chain(chat_history)

    
    user_input = st.text_input("ChatBot_v1'e Bir Mesaj Yolla", key="user_input" , on_change=set_send_input )
    print(f"User input : {user_input} ")

    voice_recording_column, send_button_column = st.columns(2)
    with voice_recording_column :
        voice_recording=mic_recorder(
            start_prompt="Kayıt Başlat 🎙️",
            stop_prompt="Kayıt Sonlandır 🎤",
            just_once=True
        )
    with send_button_column : 
        send_button = st.button("Gönder  ", key="send_button", on_click=clear_input_field)

    uploaded_audio = st.sidebar.file_uploader("Ses dosyası yükle : 🔊", type=["wav", "mp3", "ogg"])
    uploaded_image = st.sidebar.file_uploader("Dijital resim yükle : 📸 🖼️", type=["jpg", "jpeg", "png"])
    uploaded_pdf =None    

    if st.session_state.pdf_chat == True:
        print("Pdf Chat Toggle is True")
        uploaded_pdf = st.file_uploader("(RAG) Buraya PDF Yükleyebilirsiniz : 📔 📄", accept_multiple_files=True, key="pdf_upload", type=["pdf"], on_change=toggle_rag_system)
    else:
        print("Pdf Chat Toggle is false !")

    if uploaded_pdf :
        with st.spinner("PDF'i veri tabanına yüklüyorum, lütfen bekle..."):
            add_documents_to_database(uploaded_pdf)


    if uploaded_audio :
        transcribed_audio = transcribe_audio(uploaded_audio.getvalue())
        #llm_chain = load_chain(chat_history=chat_history)
        print(transcribed_audio)
        llm_chain.run("To summarize this text: " + transcribed_audio)

    print(voice_recording)
    if voice_recording:
        transcribed_audio = transcribe_audio(voice_recording["bytes"])
        print(transcribed_audio)
        llm_chain.run(transcribed_audio)

    if send_button or st.session_state.send_input :
        if uploaded_image :
            with st.spinner("Processing image..."):
                st.image(uploaded_image, caption="User's input")
                user_message = "Describe this image in detail : " 
                if st.session_state.user_question != "" :
                    user_message = st.session_state.user_question
                    st.session_state.user_question = ""
                current_user_q = user_message
                llm_answer = handle_image(uploaded_image.getvalue(), user_message)
                chat_history.add_user_message(user_message)
                chat_history.add_ai_message(llm_answer)

        

        if st.session_state.user_question != "" :
            with st.spinner("Lütfen bekle. Senin için en uygun cevabı hazırlıyorum..."):
                llm_response = llm_chain.run(st.session_state.user_question)
                print("Here is the llm response : ", llm_response)
                current_user_q = st.session_state.user_question
                st.session_state.user_question = ""
        


    if chat_history.messages != [] :
        with chat_container:
            st.write("Konuşma Geçmişi : ")
            length_curr = count_current_sessions_length(chat_history)
            count = 0
            print(f"The type of the llm chain is : {str(type(llm_chain))}")
            for message in chat_history.messages :
                count+=1
                if message.type == "human":
                    st.write(get_user_template(message.content), unsafe_allow_html=True)
                else:
                    if count < length_curr :
                        st.write(get_bot_template(message.content), unsafe_allow_html=True)
                    else:
                        if current_user_q is not None :
                            message_placeholder = st.empty()
                            output_stream = ""
                            for i in range(len(message.content)):
                                output_stream += message.content[i]
                                message_placeholder.write(f"{get_bot_template(output_stream)}", unsafe_allow_html=True) 
                                time.sleep(STREAMING_DELAY)
                            print("Current_User_question is not None !")
                        else :
                            st.write(get_bot_template(message.content), unsafe_allow_html=True)
                            print("By the way... \n The message content is : ", message.content)
                            print("\n And the current user q is : ", current_user_q)

          
            #st.image(uploaded_image, caption="User's input")
    save_chat_history(chat_history,current_user_q)

if __name__ == "__main__" :
    main()