import os
import subprocess
from git import Repo
from datetime import datetime, timedelta

# Путь к программе для визуализации графов (PlantUML)
plantuml_path = "F:/Projects/DzConf_2/PlantUML/plantuml-1.2024.8.jar"

# Путь к анализируемому репозиторию
repo_path = "F:/Projects/DzConf_2/Dz_local"

# Путь к файлу-результату в виде кода
output_dir = "F:/Projects/DzConf_2/output"
output_file_path = os.path.join(output_dir, "graph.puml")

# Создание директории, если она не существует
os.makedirs(output_dir, exist_ok=True)

# Дата коммитов в репозитории (например, за последние 30 дней)
date_threshold = datetime.now() - timedelta(days=30)

def generate_plantuml_code(repo_path, output_file_path, date_threshold):
    repo = Repo(repo_path)
    commits = list(repo.iter_commits())

    with open(output_file_path, 'w') as f:
        f.write("@startuml\n")
        for commit in commits:
            commit_date = datetime.fromtimestamp(commit.committed_date)
            if commit_date > date_threshold:
                f.write(f"[{commit.hexsha}] -> [{commit.hexsha}]\n")
        f.write("@enduml\n")

def visualize_graph(plantuml_path, output_file_path):
    output_image_path = output_file_path.replace(".puml", ".png")
    subprocess.run(["java", "-jar", plantuml_path, output_file_path])

# Генерация PlantUML кода
generate_plantuml_code(repo_path, output_file_path, date_threshold)

# Визуализация графа
visualize_graph(plantuml_path, output_file_path)
