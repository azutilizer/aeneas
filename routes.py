from main_prog import MyService


def add_routes_to_resource(_api):
    _api.add_resource(MyService, '/get_aeneas_result', strict_slashes=False)
