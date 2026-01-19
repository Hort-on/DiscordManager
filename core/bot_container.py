class AppContainer:
    _instance = None

    @classmethod
    def set(cls, container):
        cls._instance = container

    @classmethod
    def get(cls):
        if cls._instance is None:
            raise RuntimeError('Container not initialized')
        return cls._instance
