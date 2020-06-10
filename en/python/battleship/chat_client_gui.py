from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import PySimpleGUI as sg
import sys
import random
'''
Battleship-chat-client
'''


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            #msg_list.insert(tkinter.END, msg)
            print(msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(msg, event=None):  # event is passed by binders.
    """Handles sending of messages."""
    client_socket.send(bytes(msg, "utf8"))
    if msg == "quit":
        client_socket.close()
        #top.quit()

#def on_closing(event=None):
#    """This function is to be called when the window is closed."""
#    #my_msg.set("{quit}")
#    send()

def ChatBotWithHistory():
    # -------  Make a new Window  ------- #
    # give our form a spiffy set of colors
    #sg.theme('GreenTan')

    layout = [[sg.Text("chat-window (don't write here)", size=(40, 1))],
              [sg.Output(size=(127, 30), font=('Helvetica 10'))],
              [sg.Text('Command History'),
               sg.Text('', size=(20, 3), key='history')],
              [sg.ML(size=(85, 5), enter_submits=True, key='query', do_not_clear=False),
               sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
               sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('Chat window with history', layout,
                       default_element_size=(30, 2),
                       font=('Helvetica', ' 13'),
                       default_button_element_size=(8, 2),
                       return_keyboard_events=True)

    # ---===--- Loop taking in user input and using it  --- #
    command_history = []
    history_offset = 0

    while True:
        event, value = window.read()

        if event in (sg.WIN_CLOSED, 'EXIT'):  # quit if exit event or X
            break

        elif event == 'SEND':
            query = value['query'].rstrip()
            send(query)  # send to chat server
            print('The command you entered was {}'.format(query))
            command_history.append(query)
            history_offset = len(command_history) - 1
            # manually clear input because keyboard events blocks clear
            window['query'].update('')
            window['history'].update('\n'.join(command_history[-3:]))


        elif 'Up' in event and len(command_history):
            command = command_history[history_offset]
            # decrement is not zero
            history_offset -= 1 * (history_offset > 0)
            window['query'].update(command)

        elif 'Down' in event and len(command_history):
            # increment up to end of list
            history_offset += 1 * (history_offset < len(command_history) - 1)
            command = command_history[history_offset]
            window['query'].update(command)

        elif 'Escape' in event:
            window['query'].update('')

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 4:
        HOST = args[1]
        PORT = args[2]          # is a string!
        NAME = args[3]
    else:
        HOST = "127.0.0.1"
        PORT = "33000"
        NAME = random.choice(("Alice", "Bob", "Carl", "Dave", "Emely", "Frank", "Gabriele"))
    answer = sg.PopupYesNo("Please Confirm, are those values correct? \nIP of server: {}\nPort: {}\nnickname: {}".format(HOST, PORT, NAME))
    if answer == "No":
        HOST = sg.PopupGetText(message="please enter IP of server:", default_text =HOST)
        PORT = sg.PopupGetText(message="please enter porst:", default_text=PORT)
        NAME = sg.PopupGetText(message="please enter your nickname:", default_text = NAME)

    BUFSIZ = 1024
    ADDR = (HOST, int(PORT))

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    send(NAME)
    print("sending name:", NAME)
    ChatBotWithHistory()

