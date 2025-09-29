#Module: basic Python
#Assignment #1 (September 30, 2019)


#Download a book (not covered by copyright) in plain-text format, e.g., from
#https://www.gutenberg.org/

#(If you have a hard time picking one, we suggest this English translation
#of "The Republic" by Plato: http://www.gutenberg.org/cache/epub/1497/pg1497.txt)


#--- Goal
#Write a Python program that prints the relative frequence of each letter
#of the alphabet (without distinguishing between lower and upper case) in the
#book.

#--- Specifications
#- the program should have a --help option summarizing the usage
#- the program should accept the path to the input file from the command line
#- the program should print out the total elapsed time
#- the program should have an option to display a histogram of the frequences
#- [optional] the program should have an option to skip the parts of the text
#  that do not pertain to the book (e.g., preamble and license)
#- [optional] the program should have an option to print out the basic book
#  stats (e.g., number of characters, number of words, number of lines, etc.)



#Importiamo i comandi che ottimizzano il conteggio
import string
from collections import Counter
import time
import argparse
import logging
import matplotlib.pyplot as plt

#definiamo una funzione che permette di associare le lettere di un testo alla loro frequenza relativa
def frequenze_relative(testo: str) -> dict[str, float]:
    #serve un comando che permette di filtrare il testo e che porti tutte le lettere in minuscolo e ci siano solo quelle in ascii. c è la variabile temporanea che rappresenta i caratteri del testo
    lettere= (c for c in testo.lower() if c in string.ascii_lowercase)
    #utilizziamo la funzione counter che fornisce un modo semplice per associare un contatore (un intero) a ogni chiave, in questo caso al numero di volte che appare una lettera nel testo considerato
    conteggio=Counter(lettere)
    #permette di conoscere il numero totale di lettere nel testo, sommando tutti i valori del dizionario creato da counter
    totale = sum(conteggio.values())
    #logghiamo le info che ci interessano, quelle che non sono le freq relative sono debuggate
    logging.debug(f"totale lettere considerate:{totale}")
    frequenze= {l: conteggio[l] / totale for l in conteggio}
    logging.info(f"frequenze relative:{frequenze}")
    return frequenze


#definiamo una funzione che mostri l'istogramma
def mostra_istogramma(frequenze):
    #Visualizza un istogramma delle frequenze relative, sortando prima le lettere in ordine alfabetico, mentre keys poichè per noi frequenze è un dizionario e ci servono le chiavi
    lettere = sorted(frequenze.keys())
    #restituiamo il valore associato ad una certa chiave
    valori = [frequenze[l] for l in lettere]

    plt.figure(figsize=(10,6))
    plt.bar(lettere, valori, color='skyblue')
    plt.xlabel("Lettere")
    plt.ylabel("Frequenza relativa")
    plt.title("Istogramma delle frequenze delle lettere")
    plt.show()

#definiamo una funzione che permette di saltare le parti del testo non relative al libro
def estrai_testo_libro(testo: str) -> str:
    #marker utilizzato sia per l'inizio che per la fine
    marker = "APPENDIX"
    
    #prima occorrenza → inizio
    start_idx = testo.find(marker)
    #ultima occorrenza → fine
    end_idx = testo.rfind(marker)

    if start_idx != -1 and end_idx != -1 and start_idx != end_idx:
        #restituisce solo la parte compresa tra i due marker
        return testo[start_idx + len(marker):end_idx]
    else:
        #se non trova il marker o c'è solo una occorrenza, restituisce tutto
        return testo

#definiamo una funzione che calcoli le statistiche di base del libro
def book_stats(testo: str):
    #numero totale di caratteri nel testo
    num_chars = len(testo)
    #numero totale di parole, ottenuto splittando sullo spazio
    num_words = len(testo.split())
    #numero totale di righe, ottenuto splittando per newline
    num_lines = len(testo.splitlines())

    #le statistiche sono informazioni rilevanti, quindi le logghiamo a livello INFO
    logging.info(f"Numero di caratteri: {num_chars}")
    logging.info(f"Numero di parole: {num_words}")
    logging.info(f"Numero di righe: {num_lines}")

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
#Questo comando permette di dare una descrizione del programma che si andrà ad utilizzare e permette di gestire tutti gli argomenti da riga di comando, la descrizione viene mostrata attraverso il comando -h. Questo oggetto definisce gli argomenti che il programma accetta
parser = argparse.ArgumentParser(description="Questo programmino permette di calcolare le frequenze relative delle lettere in un testo. ")
parser.add_argument("--histogram", action="store_true", help="Mostra un istogramma delle frequenze")
#Questo invece permette di aggiungere un argomento al parser (posizionale e obbligatorio): file= nome dell'arg, help=descrizione dell'argomento per -h, quella precedente era per il programma in generale, questa h solo per l'argomento
parser.add_argument("file", help="Percorso del file di testo di input")
#aggiunta dell'argomento opzionale per saltare le parti non del libro
parser.add_argument("--skip-nonbook", action="store_true", help="Ignora le parti del file non appartenenti al libro")
#aggiunta dell'argomento opzionale per stampare le statistiche di base del libro
parser.add_argument("--stats", action="store_true", help="Mostra statistiche di base sul libro (caratteri, parole, righe)")
#Questo legge la riga di comando, interpreta gli argomenti secondo le regole definite da add_argument e restituisce un oggetto args. Args.file=percorso da eseguire
args = parser.parse_args()
file_path=args.file

#per leggere il file usiamo la funzione open(built in), con open(file_path, "r", encoding="utf-8")
#file_path → il percorso del file da aprire (ricevuto da riga di comando con argparse).
#"r" → modalità di apertura del file: read (lettura).
with open(file_path, "r", encoding="utf-8") as f:
    testo = f.read()


#with è un context manager: apre il file e lo chiude automaticamente alla fine del blocco.
#Non serve fare f.close(), Python gestisce tutto da solo.
#Questo previene problemi come file rimasti aperti in caso di errori.
#f.read()

#Legge tutto il contenuto del file in una singola stringa.

#Nel nostro caso, testo sarà quindi una stringa lunga quanto tutto il file.

#Se il file fosse molto grande, si potrebbe leggere a blocchi per risparmiare memoria, ma per file di testo normali va benissimo così.

#Se l’utente vuole saltare le parti non del libro
if args.skip_nonbook:
    testo = estrai_testo_libro(testo)

#Se l’utente vuole stampare le statistiche di base del libro
if args.stats:
    book_stats(testo)

#iniziare il cronometro
start = time.perf_counter()
frequenze=frequenze_relative(testo)
#stoppa il cronometro e fa la differenza tra i due istanti
end = time.perf_counter()
elapsed = end - start
logging.debug(f"tempo totale:{elapsed:.6f} secondi")

#mostra l'istogramma se richiesto attraverso il terminale
if args.histogram:
    mostra_istogramma(frequenze)
 