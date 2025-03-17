import os
import glob

def clean_faiss_cache():
    # Define os padrões de arquivos a serem removidos
    patterns = ["*.faiss", "*.pkl"]
    
    # Itera sobre os padrões e remove os arquivos correspondentes
    for pattern in patterns:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
            except Exception as e:
                print(f"Erro ao remover {file_path}: {e}")

if __name__ == "__main__":
    clean_faiss_cache()