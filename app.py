import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Biblioteca para redimensionamento de imagem

class App(ctk.CTk):
    def __init__(self): #função que inicia as coisas
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()

    #configurando a janela principal
    def configuracoes_da_janela_inicial(self): #o self utilizado é o mesmo self do init
        self.geometry("800x600") # tamanho da tela
        self.title("Sistema de Login") # titulo da tela
        self.resizable(False, False) # falso para altura, falso para largura 

    def redimensionar_imagem(self, caminho, largura, altura):
        imagem = Image.open(caminho)
        imagem = imagem.resize((largura, altura), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagem)

    def tela_de_login(self):
        #Remover widgets anteriores
        for widget in self.winfo_children():
            widget.destroy()

        #trabalhando com as imagens
        self.img = self.redimensionar_imagem("logi-img.png", 400, 600)
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img) #self representa a aplicação principal
        self.lb_img.place(x=0, y=0)
        
        #Criar a moldura (frame) do formulario de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=580)
        self.frame_login.place(x=420, y=10)

        #Colocando widgets dentro do frame - formulario de login
        ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("Century Gothic bold", 24)).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(self.frame_login, width=330, placeholder_text="Seu nome de usuário..", font=("Century Gothic", 16), corner_radius=15).grid(row=1, column=0, pady=10, padx=10)
        ctk.CTkEntry(self.frame_login, width=330, placeholder_text="Sua senha..", font=("Century Gothic", 16), corner_radius=15, show="°").grid(row=2, column=0, pady=10, padx=10)
        ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha", font=("Century Gothic", 12), corner_radius=20).grid(row=3, column=0, pady=10, padx=10)
        ctk.CTkButton(self.frame_login, width=330, text="FAZER LOGIN", font=("Century Gothic", 16), corner_radius=15).grid(row=4, column=0, pady=10, padx=10)
        ctk.CTkButton(self.frame_login, width=330, fg_color="green", hover_color="#050", text="FAZER CADASTRO", font=("Century Gothic", 16), corner_radius=15, command=self.tela_de_cadastro).grid(row=6, column=0, pady=10, padx=10)

    def tela_de_cadastro(self):
        #Remover widgets anteriores
        for widget in self.winfo_children():
            widget.destroy()

        #Frame(moldura) do formulário de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=580)
        self.frame_cadastro.place(x=420, y=10)

        #Criando o nosso titulo
        ctk.CTkLabel(self.frame_cadastro, text="Crie sua conta", font=("Century Gothic bold", 24)).grid(row=0, column=0, padx=10, pady=10)
        
        #Criar os widgets da tela de cadastro
        ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Seu nome de usuário..", font=("Century Gothic", 16), corner_radius=15).grid(row=1, column=0, pady=5, padx=10)
        ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Email..", font=("Century Gothic", 16), corner_radius=15).grid(row=2, column=0, pady=5, padx=10)
        ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Senha..", font=("Century Gothic", 16), corner_radius=15, show="°").grid(row=3, column=0, pady=5, padx=10)
        ctk.CTkEntry(self.frame_cadastro, width=330, placeholder_text="Confirme sua senha..", font=("Century Gothic", 16), corner_radius=15, show="°").grid(row=4, column=0, pady=5, padx=10)
        ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", font=("Century Gothic", 12), corner_radius=20).grid(row=5, column=0, pady=10, padx=5)
        ctk.CTkButton(self.frame_cadastro, width=330, fg_color="green", hover_color="#050", text="CADASTRAR", font=("Century Gothic", 16), corner_radius=15).grid(row=6, column=0, pady=5, padx=10)
        ctk.CTkButton(self.frame_cadastro, width=330, text="VOLTAR PARA LOGIN", font=("Century Gothic", 16), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login).grid(row=7, column=0, pady=5, padx=10)

if __name__ == "__main__":
    app = App() #app recebe a classe App
    app.mainloop()
