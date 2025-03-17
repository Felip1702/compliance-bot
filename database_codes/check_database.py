import sqlite3
import sys
import csv
import os

class SQLiteInspector:
    def __init__(self, database_path):
        """
        Inicializa o objeto SQLiteInspector com o caminho do banco de dados.

        Args:
            database_path (str): O caminho para o arquivo do banco de dados SQLite.
        """
        self.database_path = database_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Conecta ao banco de dados SQLite."""
        try:
            self.conn = sqlite3.connect(self.database_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            sys.exit(1)

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()

    def get_tables(self):
        """
        Obtém a lista de tabelas no banco de dados.

        Returns:
            list: Uma lista com os nomes das tabelas.
        """
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in self.cursor.fetchall()]
            return tables
        except sqlite3.Error as e:
            print(f"Erro ao obter tabelas: {e}")
            return []

    def get_table_schema(self, table_name):
        """
        Obtém o schema (formato dos campos) de uma tabela.

        Args:
            table_name (str): O nome da tabela.

        Returns:
            list: Uma lista com tuplas (nome, tipo, notnull, default, pk) para cada campo.
        """
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            schema = self.cursor.fetchall()
            return schema
        except sqlite3.Error as e:
            print(f"Erro ao obter schema da tabela {table_name}: {e}")
            return []

    def get_first_record(self, table_name):
        """
        Obtém o primeiro registro de uma tabela.

        Args:
            table_name (str): O nome da tabela.

        Returns:
            tuple: O primeiro registro da tabela, ou None se a tabela estiver vazia.
        """
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
            first_record = self.cursor.fetchone()
            return first_record
        except sqlite3.Error as e:
            print(f"Erro ao obter o primeiro registro da tabela {table_name}: {e}")
            return None

    def save_to_csv(self, table_name, schema, first_record):
        """Salva os dados da tabela em um arquivo CSV."""
        # Create results directory if it doesn't exist
        results_dir = os.path.join(os.path.dirname(self.database_path), "database_results")
        os.makedirs(results_dir, exist_ok=True)
        
        # Create CSV file path
        csv_path = os.path.join(results_dir, f"{table_name}_info.csv")
        
        # Write schema and first record to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write schema header
            writer.writerow(["Table Name", table_name])
            writer.writerow([])
            writer.writerow(["Schema Information"])
            writer.writerow(["Column Name", "Type", "Not Null", "Default Value", "Primary Key"])
            
            # Write schema rows
            for col in schema:
                writer.writerow([col[1], col[2], "YES" if col[3] else "NO", col[4], "YES" if col[5] else "NO"])
            
            # Write first record header
            writer.writerow([])
            writer.writerow(["First Record"])
            
            # Write column names
            if schema:
                writer.writerow([col[1] for col in schema])
                
                # Write first record if exists
                if first_record:
                    writer.writerow(first_record)
                else:
                    writer.writerow(["Table is Empty"])

    def format_output(self, table_name, schema, first_record):
        """
        Formata a saída para uma tabela especifica sem usar lib tabulate.

        Args:
            table_name (str): O nome da tabela.
            schema (list): O schema da tabela (lista de tuplas).
            first_record (tuple): O primeiro registro da tabela.

        Returns:
            str: Uma string formatada com os dados da tabela.
        """
        output = f"Tabela: {table_name}\n\n"
        if schema:
            headers = ["Column Name", "Type", "Not Null", "Default Value", "Primary Key"]
            rows = [(col[1], col[2], "YES" if col[3] else "NO", col[4], "YES" if col[5] else "NO") for col in schema]

            column_widths = [max(len(str(header)), max(len(str(item)) for item in col)) for header, col in zip(headers, zip(*rows))]

            output += self.format_row(headers, column_widths) + "\n"
            output += "-" * sum(column_widths) + "-" * len(column_widths) + "\n"
            for row in rows:
                output += self.format_row(row, column_widths) + "\n"
            output += "\n"

        if first_record:
            headers = [col[1] for col in schema]
            column_widths = [max(len(str(header)), max(len(str(item)) for item in first_record)) for header, item in zip(headers, first_record)]
            output += "First Record:\n"
            output += self.format_row(headers, column_widths) + "\n"
            output += "-" * sum(column_widths) + "-" * len(column_widths) + "\n"
            output += self.format_row(first_record, column_widths)
        else:
            output += "First Record: (Table is Empty)\n\n"
        return output

    def format_row(self, row, column_widths):
        """Formata uma linha de dados para output."""
        formatted_row = ""
        for item, width in zip(row, column_widths):
            formatted_row += f"{str(item):<{width}} | "
        return formatted_row.strip()

    def inspect_database(self):
        """
        Inspeciona o banco de dados e salva os resultados em arquivos CSV.
        """
        self.connect()
        tables = self.get_tables()

        if not tables:
            print("Nenhuma tabela encontrada no banco de dados.")
            self.close()
            return

        for table in tables:
            schema = self.get_table_schema(table)
            first_record = self.get_first_record(table)
            
            # Save to CSV
            self.save_to_csv(table, schema, first_record)
            
            # Print formatted output
            formatted_output = self.format_output(table, schema, first_record)
            print(formatted_output)

        self.close()
        print("\nResultados salvos na pasta 'database_results'")

if __name__ == "__main__":
    # Set the database path
    db_path = "C:/Projetos/compliance_bot_TEST/compliance_bot.db"
    
    # Create inspector instance
    inspector = SQLiteInspector(db_path)
    
    # Run inspection
    inspector.inspect_database()