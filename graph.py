import os
import subprocess
import argparse
from git import Repo
from datetime import datetime, timedelta

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

def main():
    parser = argparse.ArgumentParser(description="Generate and visualize commit graph using PlantUML.")
    parser.add_argument("plantuml_path", help="Path to the PlantUML JAR file.")
    parser.add_argument("repo_url", help="URL of the repository.")
    parser.add_argument("output_dir", help="Path to the output directory.")
    parser.add_argument("--days", type=int, default=30, help="Number of days for commit threshold.")

    args = parser.parse_args()

    plantuml_path = args.plantuml_path
    repo_url = args.repo_url
    output_dir = args.output_dir
    days = args.days

    # Путь к файлу-результату в виде кода
    output_file_path = os.path.join(output_dir, "graph.puml")

    # Создание директории, если она не существует
    os.makedirs(output_dir, exist_ok=True)

    # Путь к клонированному репозиторию
    repo_path = os.path.join(output_dir, "cloned_repo")

    # Проверка существования директории
    if not os.path.exists(repo_path):
        # Клонирование репозитория
        Repo.clone_from(repo_url, repo_path)

    # Дата коммитов в репозитории (например, за последние 30 дней)
    date_threshold = datetime.now() - timedelta(days=days)

    # Генерация PlantUML кода
    generate_plantuml_code(repo_path, output_file_path, date_threshold)

    # Визуализация графа
    visualize_graph(plantuml_path, output_file_path)

if __name__ == "__main__":
    main()
