class Duration:

    def __init__(self, duration_name, duration_value, is_tie=False):
        self.duration_value = duration_value
        self.duration_name = duration_name
        self.is_tie = is_tie

        if duration_value == 0.0 or duration_value is None:
            if duration_name == 'quarter':
                self.duration_value = 0.25
            elif duration_name == 'eighth':
                self.duration_value = 0.125
            elif duration_name == 'whole':
                self.duration_value = 1.0
            elif duration_name == 'half':
                self.duration_value = 0.5
            elif duration_name == '16th':
                self.duration_value = 0.0625
            elif duration_name == '32nd':
                self.duration_value = 0.03125
            elif duration_name == '64th':
                self.duration_value = 0.015625
            else:
                self.duration_value = 0.015625
        elif duration_name == '' or duration_name is None:
            if duration_value == 0.25:
                self.duration_name = 'quarter'
            elif duration_value == 0.5:
                self.duration_name = 'half'
            elif duration_value == 0.125:
                self.duration_name = 'eighth'
            elif duration_value == 0.0625:
                self.duration_name = '16th'
            elif duration_value == 0.03125:
                self.duration_name = '32nd'
            elif duration_value == 0.015625:
                self.duration_name = '64th'
            else:
                print(f"duration not found {duration_value}")
                self.duration_name = '64th'

    def __str__(self):
        return f"{self.duration_name}"

    __repr__ = __str__
