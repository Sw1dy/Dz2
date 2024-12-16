import os
import subprocess
import argparse
from git import Repo, GitCommandError
from datetime import datetime, timedelta

def generate_plantuml_code(repo_path, output_file_path, date_threshold):
    print(f"Generating PlantUML code for repository at {repo_path}")
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())

        with open(output_file_path, 'w') as f:
            f.write("@startuml\n")
            for commit in commits:
                commit_date = datetime.fromtimestamp(commit.committed_date)
                if commit_date > date_threshold:
                    f.write(f"[{commit.hexsha}] -> [{commit.hexsha}]\n")
            f.write("@enduml\n")
        print(f"PlantUML code generated at {output_file_path}")
    except Exception as e:
        print(f"Error generating PlantUML code: {e}")

def visualize_graph(plantuml_path, output_file_path):
    print(f"Visualizing graph using PlantUML at {plantuml_path}")
    try:
        output_image_path = output_file_path.replace(".puml", ".png")
        result = subprocess.run(["java", "-jar", plantuml_path, "-tpng", output_file_path, "-o", os.path.dirname(output_file_path)], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        else:
            print(f"Graph visualized and saved as {output_image_path}")
    except Exception as e:
        print(f"Error visualizing graph: {e}")

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
        try:
            # Клонирование репозитория
            print(f"Cloning repository from {repo_url} to {repo_path}")
            Repo.clone_from(repo_url, repo_path)
        except GitCommandError as e:
            print(f"Error cloning repository: {e}")
            return

    # Проверка, что директория является Git-репозиторием
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"The directory {repo_path} is not a Git repository.")
        return

    # Дата коммитов в репозитории (например, за последние 30 дней)
    date_threshold = datetime.now() - timedelta(days=days)

    # Генерация PlantUML кода
    generate_plantuml_code(repo_path, output_file_path, date_threshold)

    # Визуализация графа
    visualize_graph(plantuml_path, output_file_path)

if __name__ == "__main__":
    main()
