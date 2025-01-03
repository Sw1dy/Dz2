import unittest
import os
import tempfile
import shutil
import subprocess
from unittest.mock import patch, mock_open, MagicMock
from graph import generate_plantuml_code, visualize_graph, main
from datetime import datetime, timedelta

class TestGraphFunctions(unittest.TestCase):

    def setUp(self):
        # Создаем временную директорию для репозитория
        self.temp_dir = tempfile.mkdtemp()
        self.temp_repo_path = os.path.join(self.temp_dir, 'temp_repo')
        os.makedirs(self.temp_repo_path, exist_ok=True)

        # Инициализируем Git репозиторий
        subprocess.run(['git', 'init'], cwd=self.temp_repo_path)

        # Создаем коммиты для тестирования
        with open(os.path.join(self.temp_repo_path, 'testfile.txt'), 'w') as f:
            f.write('Test content')
        subprocess.run(['git', 'add', 'testfile.txt'], cwd=self.temp_repo_path)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=self.temp_repo_path)

    def tearDown(self):
        # Удаляем временную директорию
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_temp_repo(self):
        # Проверяем, что временный репозиторий создается и удаляется корректно
        self.assertTrue(os.path.exists(self.temp_repo_path))
        self.assertTrue(os.path.isdir(self.temp_repo_path))

    def test_add_commits(self):
        # Проверяем, что коммиты добавляются в репозиторий корректно
        result = subprocess.run(['git', 'log', '--oneline'], cwd=self.temp_repo_path, capture_output=True, text=True)
        self.assertEqual(len(result.stdout.strip().split('\n')), 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.run')
    def test_generate_plantuml_code(self, mock_subprocess_run, mock_file):
        # Путь к файлу-результату в виде кода
        output_file_path = os.path.join(self.temp_dir, "graph.puml")

        # Дата коммитов в репозитории (например, за последние 30 дней)
        date_threshold = datetime.now() - timedelta(days=30)

        # Создаем мок-объект для вывода команды git log
        mock_subprocess_run.return_value = MagicMock(stdout='abc123 1672531199\n', returncode=0)

        # Генерация PlantUML кода
        generate_plantuml_code(self.temp_repo_path, output_file_path, date_threshold)

        mock_file.assert_called()
        self.assertIn('@startuml', mock_file().write.call_args_list[0][0][0])
        self.assertIn('@enduml', mock_file().write.call_args_list[-1][0][0])

    @patch('subprocess.run')
    def test_visualize_graph(self, mock_subprocess_run):
        # Путь к программе для визуализации графов (PlantUML)
        plantuml_path = "C:/Users/Sw1dy/Dz2/PlantUML/plantuml-1.2024.8.jar"

        # Путь к файлу-результату в виде кода
        output_file_path = os.path.join(self.temp_dir, "graph.puml")

        # Визуализация графа
        visualize_graph(plantuml_path, output_file_path)

        mock_subprocess_run.assert_called_once_with(
            ['java', '-jar', plantuml_path, '-tpng', output_file_path, '-o', os.path.dirname(output_file_path)],
            capture_output=True,
            text=True
        )

if __name__ == '__main__':
    unittest.main()
