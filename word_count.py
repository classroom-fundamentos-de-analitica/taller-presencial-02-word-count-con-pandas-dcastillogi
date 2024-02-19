"""Taller evaluable"""

import glob

import pandas as pd

import fileinput


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #

    filenames = glob.glob(f"{input_directory}/*.*") # Lista los archivos en el directorio

    with fileinput.input(files=filenames) as f:
        df = pd.DataFrame(f, columns=["word"])

    """
    Método 2: Profesor
    filenames = glob.glob(f"{input_directory}/*.*")
    dataframes = [
        pd.read_csv(filename, sep=';', names=['text']) for filename in filenames
    ]
    dataframe = pd.concat(dataframes).reset_index(drop=True)
    """

    return df

def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #

    # Nota: Desde la libreria string se podria obtener la lista de puntuaciones
    dataframe["word"] = dataframe["word"].str.lower().str.replace(',', '').str.replace('.', '').str.replace(',', '')
    # Si no estuviera usando funciones, sería recomendable hacer una copia del dataframe cuando lo modifico
    return dataframe



def count_words(dataframe):
    """Word count"""
    # TRUCO: Convertir el texto en una lista de palabras en cada fila
    dataframe["word"] = dataframe["word"].str.split()
    
    dataframe["word"] = dataframe.explode("word").reset_index(drop=True)

    dataframe["count"] = 1

    dataframe = dataframe.groupby(["word"]).agg({"count": "sum"})

    return dataframe


def save_output(dataframe, output_filename):
    """Save output to a file."""

    dataframe.to_csv(output_filename)


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""
    df = load_input(input_directory)
    df = clean_text(df)
    df = count_words(df)
    save_output(df, output_filename)



if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
