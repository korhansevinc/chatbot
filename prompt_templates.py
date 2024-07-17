''' For English Models.'''

# For chat-rag chain.
memory_prompt_template = """<s>[INST] You are an AI chatbot having a conversation with a human. Answer his questions.
   Previous conversation: {history}
   Human: {human_input}
   AI: [/INST]"""

# For summarize_chat_chain.
summarize_prompt_template = """<s>[INST] You are a helpful asistant and your task is to find a title about the given input and only write down the title. Make sure that the title contains maximum 5 word. Do not specify any informations only find a title about the theme, and write it down. Make sure use ':' but Do not use any other special characters.
   Previous conversation: {history}
   Human: {human_input}
   AI: [/INST]"""


''' For Turkish Models.'''


memory_prompt_template = """<s>[INST] Sen yardımcı bir asistansın ve sana verilen talimatlar doğrultusunda en iyi cevabı üretmeye çalışacaksın.
    Önceki Konuşmalar: {history}
    İnsan: {human_input}
    Yapay Zeka: [/INST]"""
