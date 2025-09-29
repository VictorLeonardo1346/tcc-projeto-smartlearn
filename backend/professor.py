class ProfessorManager:
    professores_fixos = {
        "professor01@sp.gov.br": {"senha": "123456", "nome": "Junior"},
        "professor02@sp.gov.br": {"senha": "654321", "nome": "Maria"}
    }

    def verifica_login(self, email, senha):
        if email in self.professores_fixos and self.professores_fixos[email]["senha"] == senha:
            return self.professores_fixos[email]["nome"]
        return None
