from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

    def is_going_to_houseplant(self, event):
        text = event.message.text
        return text == "盆栽推薦"
    
    def on_enter_houseplant(self, event):
        send_text_message(event.reply_token, '請問你有養過植物嗎？輸入"是"或"否"')

    def is_going_to_hpReccomend(self, event):
        text = event.message.text
        return text == "否" or text == "是" 

    def on_enter_hpReccomend(self, event):
        text = event.message.text
        if text == "是":
            send_text_message(event.reply_token, '推薦給你 虎尾蘭 \n有著「空氣清淨機」的稱號 而且很好照顧大約兩三周澆一次水即可 新手也能上手呦~')
        else:
            send_text_message(event.reply_token, '推薦給你 虎尾蘭 \n有著「空氣清淨機」的稱號 而且很好照顧大約兩三周澆一次水即可 新手也能上手呦~\n輸入"圖片"可查看它的圖片')
            #send_image_message(event.reply_token, "https://images.unsplash.com/photo-1599009944997-3544a939813c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8c25ha2UlMjBwbGFudHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60")
        self.go_back()
    
    def is_going_to_hpImage(self, event):
        text = event.message.text
        return text == "圖片" 

    def on_enter_hpImage(self, event):
        send_image_message(event.reply_token, "https://images.unsplash.com/photo-1599009944997-3544a939813c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8c25ha2UlMjBwbGFudHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60")
        self.go_back()
