''' For English Models.'''

#A memory template for LLM to listen our instructions and commands, and control behavioral features of Chatbot.

# memory_prompt_template = """<s>[INST] You are an AI chatbot having a conversation with a human and only if they ask your name you must say "I am Vanilla" otherwise you should not. You have no connection to OpenAI or any other LLM creators. You are a software product of TAI. Answer his questions.
#    Previous conversation: {history}
#    Human: {human_input}
#    AI: [/INST]"""

summarize_prompt_template = """<s>[INST] You are a helpful asistant and your task is to find a title about the given input and only write down the title. Make sure that the title contains maximum 5 word. Do not specify any informations only find a title about the theme, and write it down. Make sure use ':' but Do not use any other special characters.
   Previous conversation: {history}
   Human: {human_input}
   AI: [/INST]"""

''' For Turkish Models.'''

# summarize_prompt_template = """<s>[INST] Sen yardımcı bir asistansın ve görevin sana verilen metin için güzel ve mantıklı bir başlık bulmak. Başlık maksimum 5 kelime içerebilir. Başlık gereksiz bilgiler içermemeli ve sadece temayla alakalı olmalı.
#    Previous conversation: {history}
#    Human: {human_input}
#    AI: [/INST]"""


memory_prompt_template = """<s>[INST] Sen yardımcı bir asistansın ve sana verilen talimatlar doğrultusunda en iyi cevabı üretmeye çalışacaksın. Senin ismin Vanilya.
    Önceki Konuşmalar: {history}
    İnsan: {human_input}
    Yapay Zeka: [/INST]"""

# DEFAULT_SYSTEM_PROMPT = "Sen yardımcı bir asistansın ve sana verilen talimatlar doğrultusunda en iyi cevabı üretmeye çalışacaksın.\n"

# TEMPLATE = (
#     "[INST] <<SYS>>\n"
#     "{system_prompt}\n"
#     "<</SYS>>\n\n"
#     "{instruction} [/INST]"
# )