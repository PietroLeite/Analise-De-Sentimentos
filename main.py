# Imports necessários
import nltk  # Import da machine learning
import PySimpleGUI as sg  # Import da interface utilizada
import time  # Recurso técnico para que o programan não feche imediatamente
from Frases import Frases  # Importe da função Frases onde foi colocar o "banco de dados" de frases

x = 0
while x < 10:
    class Interface:
            # So pra deixar salvo : sg.Checkbox() | no imput para nao exibir : sg.Input(key='', passoword_char'*')
            # Layout
            sg.theme('DarkBrown1')
            tela = [
                [sg.Text('Digite o texto :')],
                [sg.Multiline(key='txt', size=(50, 10))],
                [sg.Button('Enviar')],
                [sg.Text('Resultado: ')],
                [sg.Output(size=(50, 10))]
                ]
            # Janela
            janela = sg.Window('Mineiração de Emoções em Textos', tela)

            # Ler eventos
            eventos, valores = janela.read()
            if eventos == sg.WINDOW_CLOSED:
                x = 10
                exit()
            if eventos == 'Enviar':
                mensagem = (valores['txt']).split()
                print(f'Processando, aguarde...')


    stopwords = Frases.stopwords

    stopwordsnltk = nltk.corpus.stopwords.words('portuguese')
    stopwordsnltk.append('vou')
    stopwordsnltk.append('tão')
    stopwordsnltk.append('vai')


    # print(stopwordsnltk)

    def removestopwords(texto):
        frase = []
        for (palavras, emocao) in texto:
            semstop = [p for p in palavras.split() if p not in stopwordsnltk]
            frase.append((semstop, emocao))
        return frase


    # print(removestopwords(base))

    def aplicastemmer(texto):  # retirar o radical das palavras
        stemmer = nltk.stem.RSLPStemmer()
        frasessstemming = []
        for (palavras, emocao) in texto:
            comstemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in stopwordsnltk]
            frasessstemming.append((comstemming, emocao))
        return frasessstemming


    frasescomstemmingTreinamento = aplicastemmer(Frases.basetreinamento)
    frasescomstemmingTeste = aplicastemmer(Frases.baseteste)


    # print(frasescomstemming)

    def buscapalavras(frase):  # buscar todas as palavras
        todaspalavras = []
        for (palavras, emocao) in frase:
            todaspalavras.extend(palavras)
        return todaspalavras


    palavrasTreinamento = buscapalavras(frasescomstemmingTreinamento)
    palavrasTeste = buscapalavras(frasescomstemmingTeste)


    # print(palavras)

    def buscafrequencia(palavras):  # frequencia das palavras
        palavras = nltk.FreqDist(palavras)
        return palavras


    frequenciaTreinamento = buscafrequencia(palavrasTreinamento)
    frequenciaTeste = buscafrequencia(palavrasTeste)


    # print(frequencia.most_common(50))

    def buscapalavrasunicas(frequencia):  # para n repetir as palavras
        freq = frequencia.keys()
        return freq


    palavrasunicasTreinamento = buscapalavrasunicas(frequenciaTreinamento)
    palavrasunicasTeste = buscapalavrasunicas(frequenciaTeste)


    # print(palavrasunicas)

    def extratorpalavras(documento):  # define se existe ou n em um documento
        doc = set(documento)
        caracteristicas = {}
        for palavras in palavrasunicasTreinamento:
            caracteristicas['%s' % palavras] = (palavras in doc)
        return caracteristicas


    # caracteristicasfrase = extratorpalavras(['am', 'nov', 'dia'])
    # print(caracteristicasfrase)

    basecompletaTreinamento = nltk.classify.apply_features(extratorpalavras,frasescomstemmingTreinamento)
    # essa função vai fazer o apply de todas as carcteristicas automaticamente(true or false)

    basecompletaTeste = nltk.classify.apply_features(extratorpalavras, frasescomstemmingTeste)
    # print(basecompleta)

    # algoritimo Naive Bayes

    classificador = nltk.NaiveBayesClassifier.train(basecompletaTreinamento)  # tabela de probrabilidade
    # print(classificador.labels())
    # print(classificador.show_most_informative_features(5))

    # rint(nltk.classify.accuracy(classificador, basecompletaTeste))

    # achando erros
    erros = []
    for (frases, classe) in basecompletaTeste:
        resultado = classificador.classify(frases)
        if resultado != classe:
            erros.append((classe, resultado, frases))

    from nltk.metrics import ConfusionMatrix  # para testar os acertos

    esperado = []
    previsto = []
    for (frase, classe) in basecompletaTeste:
        resultado = classificador.classify(frase)
        previsto.append(resultado)
        esperado.append(classe)

    # esperado = 'alegria alegria alegria alegria medo medo surpresa surpresa'.split()
    # previsto = 'alegria alegria medo surpresa medo medo medo surpresa'.split()
    matriz = ConfusionMatrix(esperado, previsto)
    # print(matriz)

    # Testes
    teste = Interface.mensagem

    testesstemming = []
    stemmer = nltk.stem.RSLPStemmer()

    for palavras in teste:
        comstem = [p for p in palavras.split()]
        testesstemming.append(str(stemmer.stem(comstem[0])))

    # print(testesstemming)

    novo = extratorpalavras(testesstemming)
    # print(novo)

    print('\n' * 9)
    print(classificador.classify(novo))
    print()
    distribuicao = classificador.prob_classify(novo)
    for classe in distribuicao.samples():
        # print('%s: %f' % (classe, distribuicao.prob(classe)))
        print(f'{classe}: {distribuicao.prob(classe) * 100:.2f}%')

