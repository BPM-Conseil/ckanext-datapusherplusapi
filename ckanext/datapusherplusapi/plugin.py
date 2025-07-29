from ckan.plugins import SingletonPlugin, implements, IRoutes

class DatapusherPlusAPIPlugin(SingletonPlugin):
    implements(IRoutes, inherit=True)

    def before_map(self, map):
        from ckanext.datapusherplusapi import controller
        controller_instance = controller.DatapusherPlusAPIController()

        map.connect(
            '/api/3/action/datapusher_relaunch',
            controller='ckanext.datapusherplusapi.controller:DatapusherPlusAPIController',
            action='relaunch'
        )

        return map
