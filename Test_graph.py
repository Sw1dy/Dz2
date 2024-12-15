import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open, MagicMock
from graph import generate_plantuml_code, visualize_graph, main
from git import Repo
from datetime import datetime, timedelta

class TestGraphFunctions(unittest.TestCase):

    def setUp(self):
        # Создаем временную директорию для репозитория
        self.temp_dir = tempfile.mkdtemp()
        self.temp_repo_path = os.path.join(self.temp_dir, 'temp_repo')
        os.makedirs(self.temp_repo_path, exist_ok=True)
        self.repo = Repo.init(self.temp_repo_path)

        # Создаем коммиты для тестирования
        with open(os.path.join(self.temp_repo_path, 'testfile.txt'), 'w') as f:
            f.write('Test content')
        self.repo.index.add(['testfile.txt'])
        self.repo.index.commit('Initial commit')

    def tearDown(self):
        # Удаляем временную директорию
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_temp_repo(self):
        # Проверяем, что временный репозиторий создается и удаляется корректно
        self.assertTrue(os.path.exists(self.temp_repo_path))
        self.assertTrue(os.path.isdir(self.temp_repo_path))

    def test_add_commits(self):
        # Проверяем, что коммиты добавляются в репозиторий корректно
        self.assertEqual(len(list(self.repo.iter_commits())), 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('graph.Repo.iter_commits')
    def test_generate_plantuml_code(self, mock_iter_commits, mock_file):
        # Путь к файлу-результату в виде кода
        output_file_path = os.path.join(self.temp_dir, "graph.puml")

        # Дата коммитов в репозитории (например, за последние 30 дней)
        date_threshold = datetime.now() - timedelta(days=30)

        # Создаем мок-объект для коммитов
        mock_commit = MagicMock()
        mock_commit.committed_date = datetime.now().timestamp()
        mock_commit.hexsha = 'abc123'
        mock_iter_commits.return_value = [mock_commit]

        # Генерация PlantUML кода
        generate_plantuml_code(self.temp_repo_path, output_file_path, date_threshold)

        mock_file.assert_called()
        self.assertIn('@startuml', mock_file().write.call_args_list[0][0][0])
        self.assertIn('@enduml', mock_file().write.call_args_list[-1][0][0])

    @patch('subprocess.run')
    def test_visualize_graph(self, mock_subprocess_run):
        # Путь к программе для визуализации графов (PlantUML)
        plantuml_path = "F:/Projects/DzConf_2/PlantUML/plantuml-1.2024.8.jar"

        # Путь к файлу-результату в виде кода
        output_file_path = os.path.join(self.temp_dir, "graph.puml")

        # Визуализация графа
        visualize_graph(plantuml_path, output_file_path)

        mock_subprocess_run.assert_called_once_with(
            ['java', '-jar', plantuml_path, output_file_path]
        )

    @patch('graph.Repo.clone_from')
    @patch('graph.generate_plantuml_code')
    @patch('graph.visualize_graph')
    @patch('shutil.rmtree')
    def test_main(self, mock_rmtree, mock_visualize_graph, mock_generate_plantuml_code, mock_clone_from):
        # Путь к программе для визуализации графов (PlantUML)
        plantuml_path = "F:/Projects/DzConf_2/PlantUML/plantuml-1.2024.8.jar"

        # URL репозитория
        repo_url = "https://github.com/example/repo.git"

        # Путь к выходной директории
        output_dir = self.temp_dir

        # Аргументы командной строки
        args = [
            "graph.py",
            plantuml_path,
            repo_url,
            output_dir,
            "--days", "30"
        ]

        with patch('sys.argv', args):
            main()

        mock_clone_from.assert_called_once_with(repo_url, os.path.join(output_dir, "cloned_repo"))
        mock_generate_plantuml_code.assert_called_once()
        mock_visualize_graph.assert_called_once()

if __name__ == '__main__':
    unittest.main()
