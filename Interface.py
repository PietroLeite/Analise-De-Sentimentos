import PySimpleGUI as sg

class Interface:
    # So pra deixar salvo : sg.Checkbox() | no imput para nao exibir : sg.Input(key='', passoword_char'*')
    #Layout
    sg.theme('DarkBrown1')
    tela = [
        [sg.Text('Digite o texto :')],
        [sg.Multiline(key='txt', size=(90, 25))],
        [sg.Button('Enviar')]
    ]
    #Janela
    janela = sg.Window('Mineiração de Emoções em Textos', tela)

    #Ler eventos
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        exit()
    if eventos == 'Enviar':
        mensagem = valores['txt']
        print(f'Texto Digitado: {mensagem}')