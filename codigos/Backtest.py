import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class backtest:
    def __init__(self,dias, preco, sinal):
        self.aux = pd.DataFrame({'dias':dias, 'preco':preco, 'sinal':sinal})
        self.trades_long = pd.DataFrame(columns = ['Entrada', 'Saida', 'N dia', 'Perfomance'])
        self.trades_short = pd.DataFrame(columns = ['Entrada', 'Saida', 'N dia', 'Perfomance']) 
        
        #definicoes para criar patrimonio
        self.nL = len(dias)
        preco = pd.Series(preco)
        retorno = preco/preco.shift(1)-1
        CDI = np.full(self.nL,0.0004)
        CDI[0] = None
        
        df = {'dias': dias,
              'preco': preco,
              'Retorno': retorno,
              'CDI':CDI,
              'Sinal':sinal}
        
        #Criando dataframe
        self.df = pd.DataFrame(df)
        
    def trade_long(self):
        aux_1 = self.aux[self.aux.sinal == 1]
        entrada = []
        saida = []
        ndias = []
        perfomance = []

        index = aux_1.index.values

        n = len(aux_1)
        i = 0
        while(i < n-2):
            linha_entrada = index[i]
            entrada.append(self.aux.dias.iloc[linha_entrada])
            
            while(index[i+1] - index[i] == 1 and (i < n-2)):# a segunda condicao nao parece necessaria mas verifique
                i += 1
                
            #registramos o i+1 como saida, veja a tabela
            linha_saida = index[i] + 1
            saida.append(self.aux.dias.iloc[linha_saida])
            perfomance.append(self.aux.preco.iloc[linha_saida]/self.aux.preco.iloc[linha_entrada] - 1)
            i += 1
        
            
        trade = ['Trade {}'.format(x+1) for x in range(len(entrada))]
        
        self.trades_long = pd.DataFrame({'trade':trade, 'entrada':entrada, 'saida':saida, 'ndias':pd.Series(saida)-pd.Series(entrada), 'perfomance':perfomance})
        return self.trades_long
    
    def trade_short(self):
        aux_1 = self.aux[self.aux.sinal == -1]
        entrada = []
        saida = []
        ndias = []
        perfomance = []

        index = aux_1.index.values

        n = len(aux_1)
        i = 0
        while(i < n-2):
            linha_entrada = index[i]
            entrada.append(self.aux.dias.iloc[linha_entrada])
            
            while(index[i+1] - index[i] == 1 and (i < n-2)):# a segunda condicao nao parece necessaria mas verifique
                i += 1
                
            #registramos o i+1 como saida, veja a tabela
            linha_saida = index[i] + 1
            saida.append(self.aux.dias.iloc[linha_saida])
            perfomance.append(self.aux.preco.iloc[linha_saida]/self.aux.preco.iloc[linha_entrada] - 1)
            i += 1
        
            
        trade = ['Trade {}'.format(x+1) for x in range(len(entrada))]
        
        self.trades_short = pd.DataFrame({'trade':trade, 'entrada':entrada, 'saida':saida, 'ndias':pd.Series(saida)-pd.Series(entrada), 'performance':perfomance})
        return self.trades_short
    
    def long_info(self):
        n_trades = len(self.trades_long)
        win = len(self.trades_long[self.trades_long.perfomance > 0])
        acerto = round(100*win/n_trades,2)
        avg_win = round(100*np.mean(self.trades_long[self.trades_long.perfomance > 0].perfomance),2)
        erro = 1 - win
        avg_loss = round(100*np.mean(self.trades_long[self.trades_long.perfomance < 0].perfomance),2)
        avg_total = round(100*np.mean(self.trades_long.perfomance),2)
        avg_holding = np.mean(self.trades_long.ndias)
        avg_holding_win = np.mean(self.trades_long[self.trades_long.perfomance > 0].ndias)
        avg_holding_loss = np.mean(self.trades_long[self.trades_long.perfomance < 0].ndias)
        
        print('\nPerf Long\n')
        #(n_trades, win, acerto, avg_win, erro, avg_loss, avg_total, avg_holding, avg_holding_win, avg_holding_loss)
        print('N Trades:{} \nWin:{} \nAcerto:{}% \nAvg Win:{}% \nErro:{}% \nAvg Loss:{}%  \nAvg Total:{}%  \nAvg Holding:{}  \nAvg Holding Win:{}  \nAvg Holding Loss:{}'.format(n_trades, win, acerto, avg_win, erro, avg_loss, avg_total, avg_holding, avg_holding_win, avg_holding_loss))

    def short_info(self):
        n_trades = len(self.trades_short)
        win = len(self.trades_short[self.trades_short.performance > 0])
        acerto = round(100*win/n_trades,2)
        avg_win = round(100*np.mean(self.trades_short[self.trades_short.performance > 0].performance),2)
        erro = 1 - win
        avg_loss = round(100*np.mean(self.trades_short[self.trades_short.performance < 0].performance),2)
        avg_total = round(100*np.mean(self.trades_short.performance),2)
        avg_holding = np.mean(self.trades_short.ndias)
        avg_holding_win = np.mean(self.trades_short[self.trades_short.performance > 0].ndias)
        avg_holding_loss = np.mean(self.trades_short[self.trades_short.performance < 0].ndias)
        
        print('\nPerf Short\n')
        #(n_trades, win, acerto, avg_win, erro, avg_loss, avg_total, avg_holding, avg_holding_win, avg_holding_loss)
        print('N Trades:{} \nWin:{} \nAcerto:{}% \nAvg Win:{}% \nErro:{}% \nAvg Loss:{}%  \nAvg Total:{}%  \nAvg Holding:{}  \nAvg Holding Win:{}  \nAvg Holding Loss:{}'.format(n_trades, win, acerto, avg_win, erro, avg_loss, avg_total, avg_holding, avg_holding_win, avg_holding_loss))
        
    
    def patrimonio(self, cash):
        #criando arrays que serao as colunas
        patrimonio = np.full(self.nL, 0)
        PL = np.full(self.nL, 0)
        PL_caixa = np.full(self.nL, 0)
        qtd = np.full(self.nL, 0)
        caixa = np.full(self.nL, 0)
        trade = np.full(self.nL, 0)

        #Primeira atualizacao
        patrimonio[0] = cash
        PL[0] = 0
        PL_caixa[0] = 0

        qtd[0] = self.df.Sinal[0]*patrimonio[0]/self.df.preco[0]
        trade[0] = qtd[0]
        caixa[0] = cash-(trade[0]*self.df.preco[0])

        #n outras atualizacoes
        for i in range(1,self.nL):
          PL[i] = qtd[i-1]*(self.df.preco[i] - self.df.preco[i-1])
          PL_caixa[i] = caixa[i-1] * self.df.CDI[i]
          patrimonio[i] = patrimonio[i-1] + PL[i] + PL_caixa[i]
          qtd[i] = self.df.Sinal[i]*patrimonio[i]/self.df.preco[i]
          trade[i] = qtd[i] - qtd[i-1]
          caixa[i] = caixa[i-1] - trade[i]*self.df.preco[i] + PL_caixa[i]

        self.df['Patrimonio'] = patrimonio
        self.df['P&L'] = PL
        self.df['PL_caixa'] = PL_caixa
        self.df['Qtd'] = qtd
        self.df['trade'] = trade
        self.df['caixa'] = caixa
        
        print('Patrimonio final:{}'.format(self.df.Patrimonio.iloc[-1]))
        #Tabela com os sinais
        sinal_1 = self.df[self.df.Sinal == 1]
        sinal_0 = self.df[self.df.Sinal == 0]

        #Plotar grafico
        plt.rcParams["figure.figsize"] = (20,12)
               
        plt.plot(self.df.dias, self.df.Patrimonio , label ='Close', color = 'Blue', lw=2)

        #plt.scatter(x = sinal_1.dias, y=sinal_1.Patrimonio,s=300,color='blue', marker="^")
        #plt.scatter(x = sinal_0.dias, y=sinal_0.Patrimonio,s=300,color='red', marker="v")

        plt.title(f'Patrimonio')
        plt.xlabel('Tempo')
        plt.ylabel('Patrimonio')


        plt.show()
        #return self.df