import os

# APP FUNCTIONS
# ///////////////////////////////////////////////////////////////
class Functions:

    # SET SVG ICON
    # ///////////////////////////////////////////////////////////////
    def set_svg_icon(icon_name):
        # 获取当前工作目录（Current Working Directory）相对路径
        app_path = os.path.abspath(os.getcwd())
        folder = "gui/images/svg_icons/"
        path = os.path.join(app_path, folder)
        # normpath 规范化路径 清除多余的 "/"等符号
        icon = os.path.normpath(os.path.join(path, icon_name))
        return icon  
    
    # SET SVG IMAGE
    # ///////////////////////////////////////////////////////////////
    def set_svg_image(icon_name):
        app_path = os.path.abspath(os.getcwd())
        folder = "gui/images/svg_images/"
        path = os.path.join(app_path, folder)
        icon = os.path.normpath(os.path.join(path, icon_name))
        return icon