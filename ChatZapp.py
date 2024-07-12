import flet as ft

# Lista de palavras conhecidas para previsão simples
palavras_conhecidas = ['hello', 'how', 'are', 'you', 'today', 'good', 'morning', 'afternoon', 'evening']

def main(pagina):
    # Definição de estilo moderno
    pagina.style = {'background_color': '#f0f0f0', 'padding': '20px'}

    titulo = ft.Text('ChatZapp', style={'font_size': '24px', 'margin_bottom': '10px'})

    # Função para enviar mensagem ao túnel
    def enviar_mensagem_tunel(mensagem):
        chat.controls.append(ft.Text(mensagem))
        pagina.update()

    # Assinando o túnel para receber mensagens
    pagina.pubsub.subscribe(enviar_mensagem_tunel)
    pagina.pubsub.send_all()

    titulo_janela = ft.Text('Welcome to ChatZapp', style={'font_size': '18px'})
    nome_usuario = ft.TextField(label='Input your name', style={'width': '200px', 'margin_bottom': '10px'})

    # Função para enviar mensagem
    def send_message(evento):
        texto = f'{nome_usuario.value}: {texto_mensagem.value}'
        pagina.pubsub.send_all(texto)
        texto_mensagem.value = ''
        pagina.add(arquivo)
        pagina.update()

    arquivo = ft.FilePicker()
    texto_mensagem = ft.TextField(label='Write your message', on_submit=send_message, style={'width': 'calc(100% - 100px)', 'margin_right': '10px'})
    botao_enviar = ft.ElevatedButton('Send', on_click=send_message, style={'background_color': '#4CAF50', 'color': 'white', 'border_radius': '5px'})
    chat = ft.Column()

    linha_mensagem = ft.Row([texto_mensagem, botao_enviar], style={'align_items': 'center', 'margin_top': '10px'})

    # Função para iniciar um novo chat
    def start_new_chat(evento):
        pagina.remove(titulo)
        pagina.remove(botao_iniciar)
        janela.open = False
        pagina.add(chat)
        pagina.add(linha_mensagem)

        texto_entrou_chat = f'{nome_usuario.value} entered the chat'
        pagina.pubsub.send_all(texto_entrou_chat)
        pagina.update()

    botao_entrar = ft.ElevatedButton('Start a New Chat', on_click=start_new_chat, style={'background_color': '#2196F3', 'color': 'white', 'border_radius': '5px'})

    janela = ft.AlertDialog(title=titulo_janela, content=nome_usuario, actions=[botao_entrar], style={'border_radius': '10px', 'background_color': 'white'})

    # Função para abrir o popup de início do chat
    def abrir_popup(evento):
        pagina.dialog = janela
        janela.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton('Start a New Chat', on_click=abrir_popup, style={'background_color': '#2196F3', 'color': 'white', 'border_radius': '5px', 'margin_top': '20px'})
    pagina.add(titulo)
    pagina.add(botao_iniciar)

    # Função para prever a próxima palavra digitada
    def prever_proxima_palavra(texto):
        palavras_digitadas = texto.split()
        if palavras_digitadas:
            ultima_palavra = palavras_digitadas[-1]
            proxima_palavra = None
            for palavra in palavras_conhecidas:
                if palavra.startswith(ultima_palavra):
                    proxima_palavra = palavra
                    break
            return proxima_palavra

    # Adicionando a função de previsão à entrada de texto
    def on_text_change(evento):
        proxima_palavra = prever_proxima_palavra(texto_mensagem.value)
        if proxima_palavra:
            texto_mensagem.placeholder = f'Next word: {proxima_palavra}'
        else:
            texto_mensagem.placeholder = 'Write your message'

    texto_mensagem.on('input', on_text_change)

    # Iniciar a aplicação
    pagina.title = 'ChatZapp'
    ft.app(lambda: pagina, view=ft.WEB_BROWSER)

if __name__ == "__main__":
    main(ft.Page())
