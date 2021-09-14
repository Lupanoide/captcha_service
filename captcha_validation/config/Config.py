import logging
import configparser
import os

class Config(object):
    '''
    Classe di utils per il file config
    '''
    def __init__(self):
        name = os.path.abspath( os.path.join( __file__ , r"../../config/properties.ini"))
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        self.config.read(name)

        FORMAT = "%(asctime)s %(levelname)s %(name)s.%(funcName)s() - %(message)s"
        logging.basicConfig(format=FORMAT, filename=self.config.get("default", "log_file"), level=logging.DEBUG)

    def get_log_level(self):
        return self.config.get("default", "log_level")

    def get_font_type(self):
        return self.config.get("default", "font_type")

    def get_sqlite_file(self):
        return self.config.get("sqlite_server", "sqlite_path")

    def get_table_name(self):
        return self.config.get("sqlite_server", "table_name")

    def get_image_width(self):
        return self.config.get("captcha_image", "width")

    def get_image_height(self):
        return self.config.get("captcha_image", "height")

    def get_image_min_char_len(self):
        return self.config.get("captcha_image","min_char_len")

    def get_image_max_char_len(self):
        return self.config.get("captcha_image","max_char_len")

    def get_image_min_num_lines(self):
        return self.config.get("captcha_image", "min_num_lines")

    def get_image_max_num_lines(self):
        return self.config.get("captcha_image", "max_num_lines")

    def get_image_min_num_points(self):
        return self.config.get("captcha_image", "min_num_points")

    def get_image_max_num_points(self):
        return self.config.get("captcha_image", "max_num_points")

    def get_image_font_size(self):
        return self.config.get("captcha_image", "font_size")

    def get_image_min_shift_len(self):
        return self.config.get("captcha_image", "min_shift_len")

    def get_image_max_shift_len(self):
        return self.config.get("captcha_image", "max_shift_len")