class DatabaseRouter(object):
    _maps = {
        'wordpress': {
            'settings': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'wpauth',
                'USER': 'wpauth',
                'PASSWORD': 'wpauth',
                'HOST': 'localhost',
            },
            'apps': ['djpress', ],
        },
    }

    def get_database(self, model, **hints):
        for db, apps in self._maps.items():
            if model._meta.app_label in apps:
                return db
        return 'default'

    def db_for_read(self, model, **hints):
        return self.get_database(model, **hints)

    def db_for_write(self, model, **hints):
        return self.get_database(model, **hints)

    def allow_migrate(self, db, model):
        return self.get_database(model)

    def allow_relation(self, obj1, obj2, **hints):
        db1, db2 = [self._get(o) for o in [obj1, obj2]]

        if db1 == db2 and db1:
            return db1

        return None

    @classmethod
    def router(cls):
        return "{0}.{1}".format(cls.__module__, cls.__name__)

    @classmethod
    def confs(cls):
        return dict([(db, conf['settings'])
                     for db, conf in DatabaseRouter._maps.items()])
