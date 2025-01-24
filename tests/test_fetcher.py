from fetcher.fetcher import fetch_python_dependencies

def test_fetch_python_dependencies(mocker):
    # Mock subprocess.run to prevent actual installation
    mock_run = mocker.patch('subprocess.run')
    dependencies = ['flask==2.1.0']
    fetch_python_dependencies(dependencies)
    mock_run.assert_called_with(['pip', 'install', 'flask==2.1.0'])
