from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import random
import csv
from typing import Dict, Any, List

class NivelUrgencia(Enum):
    BAIXO = 4
    MEDIO = 3
    ALTO = 2
    CRITICO = 1

class StatusAtendimento(Enum):
    AGUARDANDO = "Aguardando"
    TRIAGEM = "Triagem"
    ATENDIMENTO = "Atendimento"
    OBSERVACAO = "Observação"
    FINALIZADO = "Finalizado"

class BancoDeSintomas:
    
    SINTOMAS = {}
    
    @classmethod
    def carregar_sintomas_csv(cls, caminho_arquivo: str = "sintomas.csv") -> None:
        cls.SINTOMAS = {}
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                
                for linha in leitor:
                    sintoma = linha['sintoma'].strip()
                    urgencia_str = linha['urgencia'].strip()
                    descricao = linha['descricao'].strip()
                    
                    try:
                        urgencia = NivelUrgencia[urgencia_str]
                    except KeyError:
                        raise ValueError(f"Urgência inválida: {urgencia_str}")
                    
                    cls.SINTOMAS[sintoma] = {
                        "urgencia": urgencia,
                        "descricao": descricao
                    }
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo {caminho_arquivo} não encontrado!")
        except Exception as e:
            raise Exception(f"Erro ao carregar sintomas do CSV: {str(e)}")
    
    @classmethod
    def obter_urgencia(cls, sintoma: str) -> NivelUrgencia:
        if not cls.SINTOMAS:
            cls.carregar_sintomas_csv()
        
        if sintoma in cls.SINTOMAS:
            return cls.SINTOMAS[sintoma]["urgencia"]
        return NivelUrgencia.MEDIO
    
    @classmethod
    def obter_descricao(cls, sintoma: str) -> str:
        if not cls.SINTOMAS:
            cls.carregar_sintomas_csv()
        
        if sintoma in cls.SINTOMAS:
            return cls.SINTOMAS[sintoma]["descricao"]
        return ""
    
    @classmethod
    def agrupar_por_urgencia(cls) -> Dict[NivelUrgencia, List[tuple]]:
        if not cls.SINTOMAS:
            cls.carregar_sintomas_csv()
        
        agrupados = {
            NivelUrgencia.BAIXO: [],
            NivelUrgencia.MEDIO: [],
            NivelUrgencia.ALTO: [],
            NivelUrgencia.CRITICO: []
        }
        
        for sintoma, dados in cls.SINTOMAS.items():
            urgencia = dados["urgencia"]
            agrupados[urgencia].append((sintoma, dados["descricao"]))
        
        return agrupados
    
    @classmethod
    def obter_todos_sintomas(cls) -> List[str]:
        if not cls.SINTOMAS:
            cls.carregar_sintomas_csv()
        
        return list(cls.SINTOMAS.keys())

class Funcionario(ABC):
    
    @abstractmethod
    def trabalhar(self) -> str:
        pass

class Pessoa(ABC):
    
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf = cpf
    
    @abstractmethod
    def __str__(self) -> str:
        pass

class Paciente(Pessoa):
    
    def __init__(self, nome: str, cpf: str, idade: int, sexo: str, sintoma: str):
        super().__init__(nome, cpf)
        self.idade = idade
        self.sexo = sexo
        self.sintoma = sintoma
        self.nivel_urgencia = BancoDeSintomas.obter_urgencia(sintoma)
        self.queixa = BancoDeSintomas.obter_descricao(sintoma)
        self.status = StatusAtendimento.AGUARDANDO
        self.timestamp_entrada = datetime.now()
        self.pressao_arterial = f"{random.randint(110, 160)}/{random.randint(70, 100)}"
        self.saturacao_oxigenio = random.randint(95, 100)
        self.prescricoes = []
    
    def obter_tempo_espera_minutos(self) -> int:
        tempo_decorrido = datetime.now() - self.timestamp_entrada
        return int(tempo_decorrido.total_seconds() / 60)
    
    def __str__(self) -> str:
        return f"Nome: {self.nome} | CPF: {self.cpf} | Idade: {self.idade} | Sexo: {self.sexo} | Pressao: {self.pressao_arterial} | O2: {self.saturacao_oxigenio}% | Queixa: {self.queixa} | Urgencia: {self.nivel_urgencia.name} | Status: {self.status.value}"

class Secretario(Pessoa, Funcionario):
    
    def __init__(self, nome: str, cpf: str):
        super().__init__(nome, cpf)
    
    def trabalhar(self) -> str:
        return f"{self.nome} na secretaria"
    
    def registrar_paciente(self, paciente: Paciente) -> str:
        paciente.status = StatusAtendimento.AGUARDANDO
        return f"Registrado por {self.nome}"
    
    def __str__(self) -> str:
        return f"Secretario: {self.nome}"

class Enfermeiro(Pessoa, Funcionario):
    
    def __init__(self, nome: str, cpf: str):
        super().__init__(nome, cpf)
    
    def trabalhar(self) -> str:
        return f"{self.nome} na triagem"
    
    def fazer_triagem(self, paciente: Paciente) -> str:
        paciente.status = StatusAtendimento.TRIAGEM
        
        if paciente.nivel_urgencia == NivelUrgencia.CRITICO:
            paciente.status = StatusAtendimento.OBSERVACAO
            return f"Triagem por {self.nome}: CRITICA - Observacao"
        elif paciente.nivel_urgencia == NivelUrgencia.ALTO:
            return f"Triagem por {self.nome}: ALTA"
        elif paciente.nivel_urgencia == NivelUrgencia.MEDIO:
            return f"Triagem por {self.nome}: MEDIA"
        else:
            return f"Triagem por {self.nome}: BAIXA"
    
    def __str__(self) -> str:
        return f"Enfermeiro: {self.nome}"

class FilaHospital:
    
    def __init__(self):
        self.fila_normal: List[Paciente] = []
        self.fila_critica: List[Paciente] = []
    
    def adicionar_paciente(self, paciente: Paciente) -> None:
        if paciente.nivel_urgencia == NivelUrgencia.CRITICO:
            self.fila_critica.append(paciente)
        else:
            self.fila_normal.append(paciente)
            self.ordenar_fila_normal()
    
    def ordenar_fila_normal(self) -> None:
        def calcular_prioridade(p: Paciente) -> float:
            peso_urgencia = (5 - p.nivel_urgencia.value) * 10
            tempo_bonus = min(p.obter_tempo_espera_minutos() / 10, 5)
            return peso_urgencia + tempo_bonus
        
        self.fila_normal.sort(key=calcular_prioridade, reverse=True)
    
    def proximo_paciente(self) -> Paciente:
        if self.fila_critica:
            return self.fila_critica.pop(0)
        
        if self.fila_normal:
            return self.fila_normal.pop(0)
        
        return None
    
    def obter_tamanho_fila(self) -> int:
        return len(self.fila_critica) + len(self.fila_normal)
    
    def obter_tamanho_fila_critica(self) -> int:
        return len(self.fila_critica)
    
    def obter_tamanho_fila_normal(self) -> int:
        return len(self.fila_normal)

class SistemaHospital:
    
    def __init__(self):
        try:
            BancoDeSintomas.carregar_sintomas_csv()
        except Exception as e:
            print(f"Aviso: {str(e)}")
        
        self.secretario = Secretario("Joao Silva", "123.456.789-00")
        self.enfermeiro = Enfermeiro("Maria Santos", "987.654.321-00")
        self.fila = FilaHospital()
        self.pacientes = []
    
    def criar_pacientes_demo(self) -> None:
        dados_pacientes = [
            ("Carlos Alberto", "111.111.111-11", 45, "Masculino", "Dor de Cabeça"),
            ("Ana Silva", "222.222.222-22", 34, "Feminino", "Febre Alta"),
            ("Pedro Santos", "333.333.333-33", 67, "Masculino", "Dor Intensa no Peito"),
            ("Lucia Costa", "444.444.444-44", 28, "Feminino", "Infarto"),
            ("Roberto Oliveira", "555.555.555-55", 52, "Masculino", "Tosse com Febre"),
            ("Fernanda Lima", "666.666.666-66", 41, "Feminino", "Sangramento")
        ]
        
        for nome, cpf, idade, sexo, sintoma in dados_pacientes:
            paciente = Paciente(nome, cpf, idade, sexo, sintoma)
            self.pacientes.append(paciente)
    
    def processar_pacientes(self) -> None:
        for paciente in self.pacientes:
            self.secretario.registrar_paciente(paciente)
            self.enfermeiro.fazer_triagem(paciente)
            self.fila.adicionar_paciente(paciente)
    
    def exibir_relatorio_final(self) -> None:
        print("PACIENTES REGISTRADOS")
        print("-" * 150)
        print(f"{'Nº':<3} {'Nome':<20} {'CPF':<15} {'Idade':<6} {'Sexo':<10} {'Pressao':<12} {'O2':<5} {'Queixa':<25} {'Urgencia':<10} {'Status':<15}")
        print("-" * 150)
        
        for i, paciente in enumerate(self.pacientes, 1):
            print(f"{i:<3} {paciente.nome:<20} {paciente.cpf:<15} {paciente.idade:<6} {paciente.sexo:<10} {paciente.pressao_arterial:<12} {paciente.saturacao_oxigenio:<5} {paciente.queixa:<25} {paciente.nivel_urgencia.name:<10} {paciente.status.value:<15}")
    
    def executar(self) -> None:
        self.criar_pacientes_demo()
        self.processar_pacientes()
        self.exibir_relatorio_final()

if __name__ == "__main__":
    sistema = SistemaHospital()
    sistema.executar()