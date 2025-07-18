import sys
import json
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class ConnectionPoint(QWidget):
    """连接点类 - 箭头形状"""
    def __init__(self, parent, is_input=True, point_id=""):
        super().__init__(parent)
        self.is_input = is_input
        self.point_id = point_id
        self.connections = []
        self.setFixedSize(16, 16)
        self.setToolTip(f"{'输入' if is_input else '输出'}端口: {point_id}")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.is_input:
            # 绘制输入箭头（向右的三角形）
            painter.setBrush(QBrush(QColor(76, 175, 80)))  # 绿色
            painter.setPen(QPen(QColor(46, 125, 50), 2))
            points = [QPoint(2, 8), QPoint(14, 4), QPoint(14, 12)]
        else:
            # 绘制输出箭头（向左的三角形）
            painter.setBrush(QBrush(QColor(255, 87, 34)))  # 橙红色
            painter.setPen(QPen(QColor(216, 67, 21), 2))
            points = [QPoint(14, 8), QPoint(2, 4), QPoint(2, 12)]
        
        painter.drawPolygon(points)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.is_input:
            # 只有输出端口才能开始拖拽连接
            canvas = self.get_canvas()
            if canvas:
                canvas.start_connection(self)
                # 记录拖拽起点位置
                self.drag_start_pos = self.mapToParent(event.pos())
                event.accept()  # 确保事件被处理
    
    def mouseMoveEvent(self, event):
        # 如果画布正在拖拽连接，将鼠标事件传递给画布
        canvas = self.get_canvas()
        if canvas and canvas.is_dragging_connection:
            # 将连接点坐标转换为画布坐标
            canvas_pos = self.mapTo(canvas, event.pos())
            canvas_event = QMouseEvent(event.type(), canvas_pos, event.button(), event.buttons(), event.modifiers())
            canvas.mouseMoveEvent(canvas_event)
            return
            
        super().mouseMoveEvent(event)
    
    def get_canvas(self):
        """获取画布对象"""
        parent = self.parent()
        while parent:
            if isinstance(parent, Canvas):
                return parent
            parent = parent.parent()
        return None

class ModuleWidget(QWidget):
    """模块组件类"""
    def __init__(self, module_type, module_id, canvas):
        super().__init__(canvas)
        self.module_type = module_type
        self.module_id = module_id
        self.canvas = canvas
        self.input_points = []
        self.output_points = []
        
        self.setFixedSize(120, 80)
        self.setup_ui()
        self.setStyleSheet("""
            ModuleWidget {
                background-color: #E3F2FD;
                border: 2px solid #1976D2;
                border-radius: 8px;
            }
            ModuleWidget:hover {
                background-color: #BBDEFB;
                border: 2px solid #0D47A1;
            }
        """)
        
        # 确保模块可见
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAutoFillBackground(True)
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 模块标题
        title = QLabel(self.module_type)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; color: #1976D2;")
        layout.addWidget(title)
        
        # ID标签
        id_label = QLabel(f"ID: {self.module_id}")
        id_label.setAlignment(Qt.AlignCenter)
        id_label.setStyleSheet("font-size: 10px; color: #666;")
        layout.addWidget(id_label)
        
        # 创建连接点
        self.create_connection_points()
    
    def create_connection_points(self):
        # 根据模块类型创建不同的输入输出点
        configs = {
            "输入模块": {"inputs": 0, "outputs": 1},
            "处理模块": {"inputs": 2, "outputs": 2},
            "输出模块": {"inputs": 2, "outputs": 0},
            "转换模块": {"inputs": 1, "outputs": 1},
            "图像采集": {"inputs": 1, "outputs": 1},
            "图像处理": {"inputs": 1, "outputs": 1}
        }
        
        config = configs.get(self.module_type, {"inputs": 1, "outputs": 1})
        
        # 创建输入点（左侧）
        for i in range(config["inputs"]):
            point = ConnectionPoint(self, True, f"in_{i}")
            point.move(-8, 25 + i * 25)  # 位于模块左边缘外侧
            self.input_points.append(point)
        
        # 创建输出点（右侧）
        for i in range(config["outputs"]):
            point = ConnectionPoint(self, False, f"out_{i}")
            point.move(112, 25 + i * 25)  # 位于模块右边缘外侧
            self.output_points.append(point)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
    
    def mouseMoveEvent(self, event):
        # 如果画布正在拖拽连接，将鼠标事件传递给画布
        if self.canvas.is_dragging_connection:
            # 将模块坐标转换为画布坐标
            canvas_pos = self.mapToParent(event.pos())
            canvas_event = QMouseEvent(event.type(), canvas_pos, event.button(), event.buttons(), event.modifiers())
            self.canvas.mouseMoveEvent(canvas_event)
            return
            
        if not (event.buttons() & Qt.LeftButton):
            return
        
        if ((event.pos() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
        
        # 网格对齐 - 将模块移动到最近的网格点
        new_pos = self.pos() + event.pos() - self.drag_start_position
        grid_size = self.canvas.grid_size
        aligned_x = round(new_pos.x() / grid_size) * grid_size
        aligned_y = round(new_pos.y() / grid_size) * grid_size
        self.move(aligned_x, aligned_y)
        self.canvas.update_connections()

class Connection:
    """连接线类"""
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        start_point.connections.append(self)
        end_point.connections.append(self)
    
    def contains_point(self, pos, tolerance=5):
        """检查点是否在连接线附近"""
        start_pos = self.start_point.parent().pos() + self.start_point.pos() + QPoint(8, 8)
        end_pos = self.end_point.parent().pos() + self.end_point.pos() + QPoint(8, 8)
        
        # 创建与绘制时相同的贝塞尔曲线路径
        path = QPainterPath()
        path.moveTo(start_pos)
        
        # 计算控制点
        dx = end_pos.x() - start_pos.x()
        dy = end_pos.y() - start_pos.y()
        ctrl_offset = max(100, abs(dx) // 3)
        
        if dx > 0:  # 从左向右
            ctrl1 = QPoint(start_pos.x() + ctrl_offset, start_pos.y())
            ctrl2 = QPoint(end_pos.x() - ctrl_offset, end_pos.y())
        else:  # 从右向左
            ctrl1 = QPoint(start_pos.x() - ctrl_offset, start_pos.y())
            ctrl2 = QPoint(end_pos.x() + ctrl_offset, end_pos.y())
        
        path.cubicTo(ctrl1, ctrl2, end_pos)
        
        # 计算点到路径的距离
        path_distance = path.pointAtPercent(path.percentAtLength(path.length()/2)).manhattanLength()
        # 使用QPainterPath的contains方法，增加一些容差
        return path.contains(pos) or path_distance < tolerance

class Canvas(QWidget):
    """画布类 - 支持全屏自适应和网格显示"""
    def __init__(self):
        super().__init__()
        self.modules = []
        self.connections = []
        self.connection_start = None  # 保存连接起始点的ConnectionPoint对象
        self.mouse_pos = QPoint()
        self.is_dragging_connection = False
        self.grid_size = 30  # 网格大小，30x30像素
        self.show_grid = True  # 网格显示状态，默认为显示
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #F5F5F5; border: 1px solid #CCCCCC;")
        self.setAcceptDrops(True)
        self.setMouseTracking(True)  # 启用鼠标跟踪
    
    def toggle_grid(self):
        """切换网格显示状态"""
        self.show_grid = not self.show_grid
        self.update()  # 重绘画布
    
    def start_connection(self, point):
        """开始连接（只能从输出端口开始）"""
        if not point.is_input:  # 只有输出端口才能开始连接
            self.connection_start = point
            self.is_dragging_connection = True
            self.setCursor(Qt.CrossCursor)
            # 立即更新鼠标位置为连接点位置
            self.mouse_pos = self.get_point_center(point)
            self.update()  # 立即触发重绘
            print(f"开始从输出端口拖拽连接: {point.parent().module_id}.{point.point_id}")
    
    def mouseMoveEvent(self, event):
        self.mouse_pos = event.pos()
        if self.is_dragging_connection and self.connection_start:
            # 触发重绘以显示拖拽连接线
            self.update()
    
    def mouseReleaseEvent(self, event):
        """松开鼠标时尝试完成连接"""
        if event.button() == Qt.LeftButton and self.is_dragging_connection:
            # 检查是否释放在输入端口上
            widget = self.childAt(event.pos())
            if isinstance(widget, ConnectionPoint) and widget != self.connection_start:
                if widget.is_input:  # 只能连接到输入端口
                    if self.try_connect(self.connection_start, widget):
                        print(f"连接成功: {self.connection_start.parent().module_id}.{self.connection_start.point_id} -> {widget.parent().module_id}.{widget.point_id}")
                    else:
                        print("连接失败")
                else:
                    QMessageBox.warning(self, "连接错误", "只能连接到输入端口（绿色箭头）！")
            else:
                print("未连接到有效的输入端口")
            
            # 清除拖拽连接
            self.connection_start = None
            self.is_dragging_connection = False
            self.setCursor(Qt.ArrowCursor)
            self.update()
    
    def mousePressEvent(self, event):
        """鼠标按下事件 - 用于取消连接或删除连接线"""
        if event.button() == Qt.RightButton:
            if self.is_dragging_connection:
                # 右键取消连接
                self.connection_start = None
                self.is_dragging_connection = False
                self.setCursor(Qt.ArrowCursor)
                self.update()
                print("连接已取消")
            else:
                # 检查是否右键点击了连接线
                self.remove_connection_at(event.pos())
    
    def remove_connection_at(self, pos):
        """移除指定位置的连接线"""
        # 从后往前检查，优先处理上层的连接线
        for i in range(len(self.connections)-1, -1, -1):
            connection = self.connections[i]
            if connection.contains_point(pos):
                # 获取连接信息
                from_module = connection.start_point.parent().module_id
                from_port = connection.start_point.point_id
                to_module = connection.end_point.parent().module_id
                to_port = connection.end_point.point_id
                
                # 确认对话框
                #reply = QMessageBox.question(
                #    self, "确认删除",
                #    f"确定要删除连接 {from_module}.{from_port} → {to_module}.{to_port} 吗？",
                #    QMessageBox.Yes | QMessageBox.No
                #)
                
                #if reply == QMessageBox.Yes:
                #    # 从连接点中移除引用
                #    if connection in connection.start_point.connections:
                #        connection.start_point.connections.remove(connection)
                #    if connection in connection.end_point.connections:
                #        connection.end_point.connections.remove(connection)
                    
                    # 从画布中移除连接
                #    self.connections.pop(i)
                #    self.update()
                #    print(f"已删除连接: {from_module}.{from_port} → {to_module}.{to_port}")

                #直接右键删除连接线
                if connection in connection.start_point.connections:
                        connection.start_point.connections.remove(connection)
                if connection in connection.end_point.connections:
                        connection.end_point.connections.remove(connection)
                    
                # 从画布中移除连接
                self.connections.pop(i)
                self.update()
                print(f"已删除连接: {from_module}.{from_port} → {to_module}.{to_port}")
                return
    
    def try_connect(self, start_point, end_point):
        """尝试连接两个点（从输出端口到输入端口）"""
        # 检查连接规则
        if start_point == end_point:
            print("不能连接自己")
            return False
        
        # 确保是从输出连接到输入
        if start_point.is_input or not end_point.is_input:
            QMessageBox.warning(self, "连接错误", "只能从输出端口（橙色箭头）拖拽到输入端口（绿色箭头）！")
            return False
        
        if start_point.parent() == end_point.parent():
            QMessageBox.warning(self, "连接错误", "不能连接同一个模块的端口！")
            return False
        
        # 检查输入端口是否已经有连接（一个输入端口只能有一个连接）
        for conn in self.connections:
            if conn.end_point == end_point:
                QMessageBox.warning(self, "连接错误", "该输入端口已经有连接了！\n一个输入端口只能连接一个输出端口。")
                return False
        
        # 检查是否已经存在相同连接
        for conn in self.connections:
            if conn.start_point == start_point and conn.end_point == end_point:
                QMessageBox.information(self, "提示", "这两个端口已经连接过了！")
                return False
        
        # 创建连接
        connection = Connection(start_point, end_point)
        self.connections.append(connection)
        self.update()
        return True
    
    def draw_connection_curve(self, painter, start_pos, end_pos):
        """绘制连接线的贝塞尔曲线"""
        path = QPainterPath()
        path.moveTo(start_pos)
        
        # 计算控制点 - 更自然的曲线算法
        dx = end_pos.x() - start_pos.x()
        dy = end_pos.y() - start_pos.y()
        
        # 控制点距离为水平距离的1/3，但至少100像素
        ctrl_offset = max(100, abs(dx) // 3)
        
        # 根据方向确定控制点位置
        if dx > 0:  # 从左向右
            ctrl1 = QPoint(start_pos.x() + ctrl_offset, start_pos.y())
            ctrl2 = QPoint(end_pos.x() - ctrl_offset, end_pos.y())
        else:  # 从右向左
            ctrl1 = QPoint(start_pos.x() - ctrl_offset, start_pos.y())
            ctrl2 = QPoint(end_pos.x() + ctrl_offset, end_pos.y())
        
        path.cubicTo(ctrl1, ctrl2, end_pos)
        painter.drawPath(path)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制网格（如果启用）
        if self.show_grid:
            self.draw_grid(painter)
        
        # 绘制已完成的连接线
        painter.setPen(QPen(QColor(33, 150, 243), 3))
        for connection in self.connections:
            start_pos = self.get_point_center(connection.start_point)
            end_pos = self.get_point_center(connection.end_point)
            self.draw_connection_curve(painter, start_pos, end_pos)
        
        # 绘制拖拽中的连接线（实时跟随鼠标）
        if self.is_dragging_connection and self.connection_start:
            painter.setPen(QPen(QColor(255, 152, 0), 3, Qt.DashLine))
            start_pos = self.get_point_center(self.connection_start)
            end_pos = self.mouse_pos
            self.draw_connection_curve(painter, start_pos, end_pos)
    
    def draw_grid(self, painter):
        """绘制网格线"""
        # 获取画布大小
        width = self.width()
        height = self.height()
        
        # 创建网格画笔 - 浅灰色细实线
        grid_pen = QPen(QColor(200, 200, 200), 1, Qt.SolidLine)
        painter.setPen(grid_pen)
        
        # 绘制垂直线
        for x in range(0, width, self.grid_size):
            painter.drawLine(x, 0, x, height)
        
        # 绘制水平线
        for y in range(0, height, self.grid_size):
            painter.drawLine(0, y, width, y)
    
    def get_point_center(self, point):
        """获取连接点的中心位置"""
        module_pos = point.parent().pos()
        point_pos = point.pos()
        return module_pos + point_pos + QPoint(8, 8)  # 箭头中心点
    
    def update_connections(self):
        """更新连接线"""
        self.update()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        module_type = event.mimeData().text()
        position = event.pos()
        
        # 网格对齐 - 将模块放置在最近的网格点
        grid_size = self.grid_size
        aligned_x = round(position.x() / grid_size) * grid_size
        aligned_y = round(position.y() / grid_size) * grid_size
        
        self.add_module(module_type, QPoint(aligned_x, aligned_y))
        event.acceptProposedAction()
    
    def add_module(self, module_type, position):
        """添加模块到画布"""
        module_id = f"{module_type}_{len(self.modules) + 1}"
        module = ModuleWidget(module_type, module_id, self)
        module.move(position)
        module.show()
        self.modules.append(module)
    
    def get_connections_json(self):
        """生成连接关系的JSON"""
        connections_data = []
        for connection in self.connections:
            start_module = connection.start_point.parent()
            end_module = connection.end_point.parent()
            
            conn_data = {
                "from_module": start_module.module_id,
                "from_port": connection.start_point.point_id,
                "to_module": end_module.module_id,
                "to_port": connection.end_point.point_id
            }
            connections_data.append(conn_data)
        
        return json.dumps(connections_data, indent=2, ensure_ascii=False)

class ModuleItem(QLabel):
    """模块列表项"""
    def __init__(self, module_type):
        super().__init__(module_type)
        self.module_type = module_type
        self.setFixedHeight(40)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            ModuleItem {
                background-color: #F5F5F5;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 8px;
            }
            ModuleItem:hover {
                background-color: #E0E0E0;
                border-color: #999999;
            }
        """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText(self.module_type)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.CopyAction)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("模块拖拽连接框架")
        self.setGeometry(100, 100, 1000, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧模块面板
        left_panel = self.create_module_panel()
        main_layout.addWidget(left_panel, 0)
        
        # 右侧画布区域
        right_panel = self.create_canvas_panel()
        main_layout.addWidget(right_panel, 1)
        
        # 设置比例
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
    
    def create_module_panel(self):
        """创建左侧模块面板"""
        panel = QWidget()
        panel.setFixedWidth(200)
        panel.setStyleSheet("background-color: #F8F9FA; border-right: 1px solid #DEE2E6;")
        
        layout = QVBoxLayout(panel)
        
        # 标题
        title = QLabel("模块库")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # 模块列表
        modules = ["输入模块", "处理模块", "输出模块", "转换模块","图像采集","图像处理"]
        for module_type in modules:
            item = ModuleItem(module_type)
            layout.addWidget(item)
        
        layout.addStretch()
        return panel
    
    def create_canvas_panel(self):
        """创建右侧画布面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        # 生成关系按钮
        generate_btn = QPushButton("生成连接关系")
        generate_btn.clicked.connect(self.generate_connections)
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        toolbar.addWidget(generate_btn)
        
        # 清空画布按钮
        clear_btn = QPushButton("清空画布")
        clear_btn.clicked.connect(self.clear_canvas)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        toolbar.addWidget(clear_btn)
        
        # 显示/隐藏网格按钮
        self.grid_btn = QPushButton("隐藏网格")
        self.grid_btn.clicked.connect(self.toggle_grid)
        self.grid_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        toolbar.addWidget(self.grid_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # 说明文本
        instruction_layout = QHBoxLayout()
        instruction_label = QLabel("💡 操作说明：从橙色输出箭头拖拽到绿色输入箭头进行连接")
        instruction_label.setStyleSheet("""
            QLabel {
                background-color: #E8F5E8;
                border: 1px solid #4CAF50;
                border-radius: 4px;
                padding: 8px;
                color: #2E7D32;
                font-size: 12px;
            }
        """)
        instruction_layout.addWidget(instruction_label)
        instruction_layout.addStretch()
        layout.addLayout(instruction_layout)
        
        # 画布 - 添加滚动区域，支持更大的画布
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 允许滚动区域调整大小
        self.canvas = Canvas()
        scroll_area.setWidget(self.canvas)
        layout.addWidget(scroll_area)
        
        return panel
    
    def toggle_grid(self):
        """切换网格显示状态并更新按钮文本"""
        self.canvas.toggle_grid()
        # 更新按钮文本以反映当前状态
        if self.canvas.show_grid:
            self.grid_btn.setText("隐藏网格")
        else:
            self.grid_btn.setText("显示网格")
    
    def generate_connections(self):
        """生成连接关系"""
        connections_json = self.canvas.get_connections_json()
        
        # 显示结果对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("连接关系")
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setPlainText(connections_json)
        text_edit.setFont(QFont("Consolas", 10))
        layout.addWidget(text_edit)
        
        # 按钮
        button_layout = QHBoxLayout()
        copy_btn = QPushButton("复制到剪贴板")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(connections_json))
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def clear_canvas(self):
        """清空画布"""
        reply = QMessageBox.question(self, "确认", "确定要清空画布吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            for module in self.canvas.modules:
                module.deleteLater()
            self.canvas.modules.clear()
            self.canvas.connections.clear()
            self.canvas.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #FFFFFF;
        }
    """)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
