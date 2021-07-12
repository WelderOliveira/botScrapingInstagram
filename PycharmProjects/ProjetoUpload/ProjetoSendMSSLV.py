import pandas as pd
import pyodbc


class analiseDados:

    def __init__(self):
        try:
            self.conexao = pyodbc.connect('Driver={SQL Server};'
                                          'Server=localhost\\SQLEXPRESS;'
                                          'Database=funpresp;'
                                          'Trusted_Connection=True;')

            self.cursor = self.conexao.cursor()
            self.conectado = 1
        except Exception:
            exit("Erro ao instanciar a base de dados")

    def inserirDados(self):
        if self.conectado == 1:
            self.cursor.execute('INSERT INTO funpresp.dbo.dadosExcel '
                                'VALUES(?,?,?,?,?,?,?,?,?,?)',
                                (self.mesPagamento, self.competencia, self.cpf, self.nome,
                                 self.baseContrib, self.remuneracao, self.percentual, self.contrib,
                                 self.contribServidor, self.contribPatrocinador))
            self.conexao.commit()
        else:
            return ({'mensagem': 'Not conect'})

    def capturarDados(self, arquivo):

        self.lista = []

        diretorio = r"C:\Users\Will\Desktop\TesteArquivos\{}".format(arquivo)
        dataset = pd.read_excel(diretorio, sheet_name="Analitico", header=None, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                names=["Mês de pagamento (A)", "Competência (inclusive 13º) (B)",
                                       "CPF ( C )", "Nome (D)", "Base de Contribuição (E)",
                                       "Remuneração de Participação (F)", "Percentual (G)", "Contribuição (H)",
                                       "Contrib. Servidor (I)", "Contrib. Patrocinador (J)"], skiprows=4)

        contador = int(len(dataset.index))
        for linha in range(contador):  # Pega cada linha e insere um a um na Base
            self.mesPagamento = str(dataset.iloc[linha].loc["Mês de pagamento (A)"])
            self.competencia = str(dataset.iloc[linha].loc["Competência (inclusive 13º) (B)"])
            self.cpf = str(dataset.iloc[linha].loc["CPF ( C )"])
            self.nome = str(dataset.iloc[linha].loc["Nome (D)"])
            self.baseContrib = str(dataset.iloc[linha].loc["Base de Contribuição (E)"])
            self.remuneracao = str(dataset.iloc[linha].loc["Remuneração de Participação (F)"])
            self.percentual = str(dataset.iloc[linha].loc["Percentual (G)"])
            self.contrib = str(dataset.iloc[linha].loc["Contribuição (H)"])
            self.contribServidor = str(dataset.iloc[linha].loc["Contrib. Servidor (I)"])
            self.contribPatrocinador = str(dataset.iloc[linha].loc["Contrib. Patrocinador (J)"])

            self.inserirDados()
        if (linha + 1) == contador:
            return print("FINISH DEU BOM")
        else:
            return print("DEU RUIM")
