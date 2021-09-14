import logging
from captcha_validation.config.Config import Config
from captcha_validation.utils.Validators import StringValidator


class ConfigBusiness:

    def __init__(self):
        self.config = Config()
        self.ttf_file = self.config.get_font_type()
        logLevel = self.config.get_log_level()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(getattr(logging, logLevel))
        self.width = int(self.config.get_image_width())
        self.height = int(self.config.get_image_height())
        self.min_char_len = int(self.config.get_image_min_char_len())
        self.max_char_len = int(self.config.get_image_max_char_len())
        self.min_num_lines = int(self.config.get_image_min_num_lines())
        self.max_num_lines = int(self.config.get_image_max_num_lines())
        self.min_num_points = int(self.config.get_image_min_num_points())
        self.max_num_points = int(self.config.get_image_max_num_points())
        self.font_size = int(self.config.get_image_font_size())
        self.min_shift_len = float(self.config.get_image_min_shift_len())
        self.max_shift_len = float(self.config.get_image_max_shift_len())
        self.stringValidator = StringValidator()
