from module.base.decorator import del_cached_property
from module.config import language


class Resource:
    # Class property, record all button and templates
    instances = {}
    # Instance property, record cached properties of instance
    cached = []

    def resource_add(self, key):
        Resource.instances[key] = self

    def resource_release(self):
        for cache in self.cached:
            del_cached_property(self, cache)

    @staticmethod
    def parse_property(data, l=None):
        """
        Parse properties of Button or Template object input.
        Such as `area`, `color` and `button`.

        Args:
            data: Dict or str
            l (str): Load from given a language or load from global attribute `language.language`
        """
        if l is None:
            l = language.language
        if isinstance(data, dict):
            return data.get(l)
        else:
            return data


def release_resources(next_task=''):
    # Release assets cache
    # module.ui has about 80 assets and takes about 3MB
    # Alas has about 800 assets, but they are not all loaded.
    # Template images take more, about 6MB each
    for key, obj in Resource.instances.items():
        # Preserve assets for ui switching
        # if next_task and str(obj) in _preserved_assets.ui:
        #     continue
        # if Resource.is_loaded(obj):
        #     logger.info(f'Release {obj}')
        obj.resource_release()
