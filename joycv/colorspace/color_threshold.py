# General color mask
import cv2

color_threshold = \
    {
        'general': {'general': {
            cv2.COLOR_RGB2HSV: [(0.381 * 180, 0.235 * 255, 0.235), (0.572 * 180, 1 * 255, 1.000 * 255)],
            cv2.COLOR_RGB2Lab: [(27.395 * 255 / 100, -50.539 + 128, -56.825 + 128),
                                (98.827 * 255 / 100, -4.534 + 128, 5.829 + 128)],
            cv2.COLOR_RGB2YCrCb: [(0.000, 0.000, 117.000), (255.000, 114.000, 255.000)]
        }

        },
        'apricot': {'apricot': {
            cv2.COLOR_RGB2HSV: [(0.381 * 180, 0.235 * 255, 0.235), (0.572 * 180, 1 * 255, 1.000 * 255)],
            cv2.COLOR_RGB2Lab: [(59.702 * 255 / 100, -14.294 + 128, 12.372 + 128),
                                (99.274 * 255 / 100, 29.078 + 128, 79.385 + 128)],
            cv2.COLOR_RGB2YCrCb: [(126.000, 0.000, 121.000), (255.000, 123.000, 255.000)]
        }

        },
        'chustnut': {'chustnut': {
            cv2.COLOR_RGB2HSV: [(0.381 * 180, 0.235 * 255, 0.235), (0.572 * 180, 1 * 255, 1.000 * 255)],
            cv2.COLOR_RGB2Lab: [(27.395 * 255 / 100, -50.539 + 128, -56.825 + 128),
                                (98.827 * 255 / 100, -4.534 + 128, 5.829 + 128)],
            cv2.COLOR_RGB2YCrCb: [(0.000, 0.000, 117.000), (255.000, 114.000, 255.000)]
        }}
    }


# PamlDate/Ajwa color mask


def get_lower_color(color_cvt_code, genre, category):
    return color_threshold[genre][category][color_cvt_code][0]


def get_upper_color(color_cvt_code, genre, category):
    return color_threshold[genre][category][color_cvt_code][1]
