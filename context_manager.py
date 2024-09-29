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
        context_str = ""
        for key, value in self.context.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    context_str += f"{key}: {sub_key}: {sub_value}\n"
            elif isinstance(value, list):
                for item in value:
                    context_str += f"{key}: {item}\n"
        return context_str

    def update_context(self, new_context):
        self.context.update(new_context)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
