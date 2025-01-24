from resolver.resolver_engine import resolve_dependencies

def test_resolve_dependencies():
    dependencies = ['flask==2.1.0', 'flask==2.0.0', 'requests==2.26.0']
    resolved = resolve_dependencies(dependencies)
    assert resolved == {'flask': '2.1.0', 'requests': '2.26.0'}
