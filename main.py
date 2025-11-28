from sistema_hospitalar import (
    Paciente, Secretario, Enfermeiro, FilaHospital,
    BancoDeSintomas, NivelUrgencia, StatusAtendimento
)

class SistemaInterativo:
    
    def __init__(self):
        try:
            BancoDeSintomas.carregar_sintomas_csv()
        except FileNotFoundError:
            print("Aviso: Arquivo 'sintomas.csv' não encontrado. O sistema pode não funcionar corretamente.")
        except Exception as e:
            print(f"Erro ao carregar sintomas: {e}")
        
        self.secretario = Secretario("Ana Paula", "111.222.333-44")
        self.enfermeiro = Enfermeiro("Carlos Eduardo", "555.666.777-88")
        self.fila = FilaHospital()
        self.pacientes = []
    
    def obter_nome(self):
        while True:
            nome = input("Digite o nome completo do paciente: ").strip()
            if len(nome) >= 3:
                return nome
            print("Nome inválido. Deve ter pelo menos 3 caracteres.")
    
    def obter_cpf(self):
        while True:
            cpf = input("Digite o CPF do paciente (apenas números): ").strip()
            if cpf.isdigit() and len(cpf) == 11:
                cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                if any(p.cpf == cpf_formatado for p in self.pacientes):
                    print("CPF já registrado para outro paciente. Por favor, verifique.")
                    continue
                return cpf_formatado
            print("CPF inválido. Digite 11 números.")
    
    def obter_idade(self):
        while True:
            try:
                idade = int(input("Digite a idade do paciente: "))
                if 1 <= idade <= 150:
                    return idade
                print("Idade inválida. Digite um valor entre 1 e 150.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
    
    def obter_sexo(self):
        while True:
            sexo = input("Digite o sexo do paciente (M/F): ").strip().upper()
            if sexo in ['M', 'F']:
                return "Masculino" if sexo == 'M' else "Feminino"
            print("Sexo inválido. Digite 'M' para Masculino ou 'F' para Feminino.")
    
    def obter_sintoma(self):
        print("\n--- Seleção de Sintomas ---")
        sintomas_agrupados = BancoDeSintomas.agrupar_por_urgencia()
        
        opcoes_validas = {}
        indice = 1
        
        for nivel in [NivelUrgencia.CRITICO, NivelUrgencia.ALTO, NivelUrgencia.MEDIO, NivelUrgencia.BAIXO]:
            if sintomas_agrupados[nivel]:
                print(f"\n--- {nivel.name} ---")
                for sintoma, descricao in sintomas_agrupados[nivel]:
                    print(f"{indice}. {sintoma} ({descricao})")
                    opcoes_validas[str(indice)] = sintoma
                    indice += 1
        
        while True:
            escolha = input("Digite o número do sintoma ou o nome do sintoma: ").strip()
            
            if escolha.isdigit() and escolha in opcoes_validas:
                return opcoes_validas[escolha]
            
            for sintoma_nome in BancoDeSintomas.SINTOMAS.keys():
                if sintoma_nome.lower() == escolha.lower():
                    return sintoma_nome
            
            print("Opção inválida. Por favor, digite o número ou o nome exato do sintoma.")

    def processar_novo_paciente(self):
        print("\n--- REGISTRAR NOVO PACIENTE ---")
        nome = self.obter_nome()
        cpf = self.obter_cpf()
        idade = self.obter_idade()
        sexo = self.obter_sexo()
        sintoma = self.obter_sintoma()
        
        paciente = Paciente(nome, cpf, idade, sexo, sintoma)
        
        print("\n--- REGISTRO NA SECRETARIA ---")
        registro_info = self.secretario.registrar_paciente(paciente)
        print(f"Paciente {paciente.nome} registrado por {self.secretario.nome}.")
        
        print("\n--- TRIAGEM ---")
        triagem_resultado = self.enfermeiro.fazer_triagem(paciente)
        print(triagem_resultado)
        
        print("\n--- ADICIONANDO À FILA ---")
        self.fila.adicionar_paciente(paciente)
        print(f"{paciente.nome} adicionado à fila.")
        
        self.pacientes.append(paciente)
        
        print("\n--- DADOS DO PACIENTE ---")
        print(paciente)
        input("\nPressione Enter para continuar...")
    
    def listar_pacientes(self):
        print("\n--- LISTA DE PACIENTES REGISTRADOS ---")
        if not self.pacientes:
            print("Nenhum paciente registrado ainda.")
            input("\nPressione Enter para continuar...")
            return
        
        print("-" * 150)
        print(f"{'Nº':<3} {'Nome':<20} {'CPF':<15} {'Idade':<6} {'Sexo':<10} {'Pressao':<12} {'O2':<5} {'Queixa':<25} {'Urgencia':<10} {'Status':<15}")
        print("-" * 150)
        
        for i, paciente in enumerate(self.pacientes, 1):
            print(f"{i:<3} {paciente.nome:<20} {paciente.cpf:<15} {paciente.idade:<6} {paciente.sexo:<10} {paciente.pressao_arterial:<12} {paciente.saturacao_oxigenio:<5} {paciente.queixa:<25} {paciente.nivel_urgencia.name:<10} {paciente.status.value:<15}")
        
        input("\nPressione Enter para continuar...")
    
    def visualizar_fila(self):
        print("\n--- FILA DE ATENDIMENTO ---")
        total = self.fila.obter_tamanho_fila()
        
        if total == 0:
            print("Nenhum paciente na fila.")
            input("\nPressione Enter para continuar...")
            return
        
        print(f"Total: {total} pacientes | Críticos: {self.fila.obter_tamanho_fila_critica()} | Normal: {self.fila.obter_tamanho_fila_normal()}\n")
        
        if self.fila.fila_critica:
            print("FILA CRÍTICA (Atendimento Imediato):")
            for i, p in enumerate(self.fila.fila_critica, 1):
                print(f"   {i}. {p.nome:<20} | CRÍTICA | Tempo: {p.obter_tempo_espera_minutos()}min")
            print()
        
        if self.fila.fila_normal:
            print("FILA NORMAL:")
            for i, p in enumerate(self.fila.fila_normal, 1):
                urgencia_str = p.nivel_urgencia.name
                print(f"   {i}. {p.nome:<20} | {urgencia_str:<6} | Tempo: {p.obter_tempo_espera_minutos()}min")
        
        input("\nPressione Enter para continuar...")
    
    def visualizar_paciente(self):
        print("\n--- VISUALIZAR DETALHES DO PACIENTE ---")
        if not self.pacientes:
            print("Nenhum paciente registrado ainda.")
            input("\nPressione Enter para continuar...")
            return
        
        cpf_busca = input("Digite o CPF do paciente para visualizar detalhes: ").strip()
        
        paciente_encontrado = None
        for paciente in self.pacientes:
            if paciente.cpf == cpf_busca:
                paciente_encontrado = paciente
                break
        
        if paciente_encontrado:
            print("\n--- DETALHES DO PACIENTE ---")
            print(paciente_encontrado)
        else:
            print("Paciente não encontrado com o CPF informado.")
        input("\nPressione Enter para continuar...")
    
    def menu_principal(self):
        while True:
            print("\n--- SISTEMA DE HOSPITAL ---")
            print("1. Registrar novo paciente")
            print("2. Listar pacientes")
            print("3. Ver fila de atendimento")
            print("4. Ver detalhes de paciente")
            print("5. Sair")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.processar_novo_paciente()
            elif opcao == "2":
                self.listar_pacientes()
            elif opcao == "3":
                self.visualizar_fila()
            elif opcao == "4":
                self.visualizar_paciente()
            elif opcao == "5":
                print("Saindo do sistema. Obrigado!")
                break
            else:
                print("Opção inválida. Tente novamente.")
                input("\nPressione Enter para continuar...")

def main():
    try:
        sistema = SistemaInterativo()
        sistema.menu_principal()
    except Exception as e:
        print(f"Erro ao executar o sistema: {str(e)}")

if __name__ == "__main__":
    main()