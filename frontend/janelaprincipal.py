import customtkinter as ctk
from backend.aluno import UserManager
from backend.professor import ProfessorManager
from frontend.paginas import LoginPage, CadastroPage, AlunoPage, ProfessorPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Sistema de Login")
        self.resizable(False, False)
        self.configure(fg_color="#2E2E2E")
        self.username_login = ""

        # Backend
        self.user_manager = UserManager()
        self.professores_fixos = {
            "professor01@sp.gov.br": {"senha": "123456", "nome": "Junior"},
            "professor02@sp.gov.br": {"senha": "654321", "nome": "Maria"}
        }

        # Páginas
        self.login_page = LoginPage(self, self.user_manager, self.professores_fixos)
        self.cadastro_page = CadastroPage(self, self.user_manager)
        self.aluno_page = AlunoPage(self)
        self.professor_page = ProfessorPage(self)

        # Mostra tela inicial
        self.mostrar_login()

    # Métodos de utilidade
    def redimensionar_imagem(self, caminho, largura, altura):
        from PIL import Image, ImageTk
        imagem = Image.open(caminho)
        imagem = imagem.resize((largura, altura), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagem)

    def centralizar_frame(self, frame, largura, altura):
        self.update_idletasks()
        x = (self.winfo_width() - largura) // 2
        y = (self.winfo_height() - altura) // 2
        frame.place(x=x, y=y)

    # Métodos para trocar de página
    def mostrar_login(self):
        self.login_page.mostrar()

    def mostrar_cadastro(self):
        self.cadastro_page.mostrar()

    def mostrar_aluno(self):
        self.aluno_page.mostrar()

    def mostrar_professor(self):
        self.professor_page.mostrar()
