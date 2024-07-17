import os
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #ff7f7f
}
.chat-message.bot {
    background-color: #add8e6
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 100%;
  padding: 0 1.5rem;
  color: #000;
}
'''
def get_bot_template(MSG):
    bot_template = f'''
    <div class="chat-message bot">
        <div class="message">{MSG}</div>
    </div>
    '''
    return bot_template

def get_user_template(MSG):
    # if os.path.exists("image.txt"):
    #     with open("image.txt", "r") as f:
    #         img_src = f.read()
    # else:
    #     img_src = "https://i.ibb.co/rdZC7LZ/Photo-logo-1.png"
        
    user_template = f'''
    <div class="chat-message user">
        <div class="message">{MSG}</div>
    </div>
    '''
    return user_template