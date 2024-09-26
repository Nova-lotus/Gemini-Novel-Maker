class ContextManager:
    def __init__(self):
        self.context = {
            'characters': {},
            'plot': [],
            'settings': [],
            'other_elements': []
        }

    def add_character(self, name, description):
        self.context['characters'][name] = description

    def add_plot_point(self, plot_point):
        self.context['plot'].append(plot_point)

    def add_setting(self, setting):
        self.context['settings'].append(setting)

    def add_other_element(self, element):
        self.context['other_elements'].append(element)

    def get_context(self):
        return str(self.context)

    def update_context(self, new_context):
        self.context.update(new_context)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
