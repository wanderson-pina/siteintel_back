from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

class Avaliador:

    def avaliar(self, modelo, X_test, Y_test):
        """ Faz uma predição e avalia o modelo. Poderia parametrizar o tipo de
        avaliação, entre outros.
        """
        predicoes = modelo.predict(X_test)
        
        # Caso o seu problema tenha mais do que duas classes, altere o parâmetro average
        return (accuracy_score(Y_test, predicoes),
                recall_score(Y_test, predicoes, average='binary'),
                precision_score(Y_test, predicoes, average='binary'),
                f1_score(Y_test, predicoes, average='binary'))

