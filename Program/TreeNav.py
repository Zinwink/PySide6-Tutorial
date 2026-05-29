import sys
from PySide6.QtWidgets import (QApplication, QListView, QWidget, QVBoxLayout, 
                              QStyledItemDelegate, QStyle)
from PySide6.QtCore import (Qt, QAbstractListModel, QModelIndex, Signal, Slot,
                          QSize, QRectF)
from PySide6.QtGui import (QPainter, QPen, QColor, QFont, QFontDatabase,
                         QImage)

class TreeNode:
    """树节点数据结构"""
    def __init__(self):
        self.level = 1       # 1=父节点, 2=子节点
        self.expand = False  # 是否展开
        self.last = False    # 是否是最后一个节点
        self.icon = ''       # 图标字符（FontAwesome）
        self.image = ''      # 图片路径
        self.text = ''       # 显示文本
        self.tip = ''        # 提示信息
        self.parentText = '' # 父节点文本
        self.children = []   # 子节点列表

class NavModel(QAbstractListModel):
    """导航数据模型"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listNode = []    # 扁平化存储的节点列表
        self._setupFontAwesome()
        
    def _setupFontAwesome(self):
        # 加载图形字体（实际使用时需要提供字体文件）
        font_db = QFontDatabase()
        if "FontAwesome" not in font_db.families():
            font_db.addApplicationFont("fontawesome-webfont.ttf")
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.listNode)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.listNode):
            return None
            
        node = self.listNode[index.row()]
        if role == Qt.DisplayRole:
            return node.text
        elif role == Qt.UserRole:
            return node
        return None
    
    def expand(self, index):
        """展开/折叠节点"""
        if not index.isValid() or index.row() >= len(self.listNode):
            return
            
        node = self.listNode[index.row()]
        if node.level != 1:  # 只有父节点可展开
            return
            
        node.expand = not node.expand
        
        if node.expand:
            self.beginInsertRows(index.parent(), 
                               index.row()+1, 
                               index.row()+len(node.children))
            self.listNode[index.row()+1:index.row()+1] = node.children
            self.endInsertRows()
        else:
            self.beginRemoveRows(index.parent(),
                               index.row()+1,
                               index.row()+len(node.children))
            del self.listNode[index.row()+1:index.row()+1+len(node.children)]
            self.endRemoveRows()
    
    def loadSampleData(self):
        """加载示例数据"""
        self.beginResetModel()
        self.listNode.clear()
        
        # 父节点1
        parent1 = TreeNode()
        parent1.text = "Dashboard"
        parent1.icon = "\uf015"  # 家图标
        parent1.expand = True
        
        # 子节点
        child1 = TreeNode()
        child1.text = "Overview"
        child1.level = 2
        child1.parentText = parent1.text
        child1.icon = "\uf06e"  # 眼睛图标
        
        child2 = TreeNode()
        child2.text = "Statistics"
        child2.level = 2
        child2.parentText = parent1.text
        child2.icon = "\uf080"  # 柱状图图标
        child2.last = True
        
        parent1.children = [child1, child2]
        
        # 父节点2
        parent2 = TreeNode()
        parent2.text = "Settings"
        parent2.icon = "\uf013"  # 齿轮图标
        
        # 子节点
        child3 = TreeNode()
        child3.text = "Account"
        child3.level = 2
        child3.parentText = parent2.text
        
        child4 = TreeNode()
        child4.text = "Privacy"
        child4.level = 2
        child4.parentText = parent2.text
        child4.last = True
        
        parent2.children = [child3, child4]
        
        self.listNode = [parent1, child1, child2, parent2]
        self.endResetModel()

class NavDelegate(QStyledItemDelegate):
    """导航项渲染委托"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fontAwesome = QFont("FontAwesome", 10)
        
    def paint(self, painter, option, index):
        # 获取节点数据
        node = index.data(Qt.UserRole)
        if not node:
            return
            
        # 保存 painter 状态
        painter.save()
        
        # 状态颜色设置
        if option.state & QStyle.State_Selected:
            bgColor = QColor("#1E90FF")
            textColor = QColor("#FFFFFF")
        elif option.state & QStyle.State_MouseOver:
            bgColor = QColor("#E6E6FA")
            textColor = QColor("#000000")
        else:
            bgColor = QColor("#FFFFFF")
            textColor = QColor("#000000")
            
        # 绘制背景
        painter.fillRect(option.rect, bgColor)
        
        # 设置缩进
        indent = 20 if node.level == 1 else 40
        
        # 绘制层级线条（子节点）
        if node.level == 2:
            painter.setPen(QPen(QColor("#D3D3D3"), 1))
            lineX = option.rect.left() + 30
            painter.drawLine(lineX, option.rect.top(),
                           lineX, option.rect.bottom())
        
        # 绘制图标
        if node.icon:
            painter.setFont(self.fontAwesome)
            painter.setPen(textColor)
            iconRect = QRectF(option.rect.left() + 10, 
                             option.rect.top(), 
                             20, option.rect.height())
            painter.drawText(iconRect, Qt.AlignCenter, node.icon)
        
        # 绘制文本
        painter.setPen(textColor)
        textRect = option.rect.adjusted(indent, 0, 0, 0)
        painter.drawText(textRect, Qt.AlignLeft | Qt.AlignVCenter, node.text)
        
        # 绘制展开指示器（父节点）
        if node.level == 1 and node.children:
            painter.setFont(self.fontAwesome)
            arrow = "\uf078" if node.expand else "\uf054"  # 右箭头/下箭头
            arrowRect = QRectF(option.rect.right() - 30, 
                              option.rect.top(), 
                              20, option.rect.height())
            painter.drawText(arrowRect, Qt.AlignCenter, arrow)
        
        # 恢复 painter 状态
        painter.restore()
    
    def sizeHint(self, option, index):
        return QSize(200, 35)

class NavListView(QListView):
    """导航列表视图"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setItemDelegate(NavDelegate())
        self.setModel(NavModel())
        self.setStyleSheet("""
            QListView {
                border: none;
                outline: none;
            }
            QListView::item {
                border-bottom: 1px solid #EEE;
            }
        """)
        
        # 加载示例数据
        self.model().loadSampleData()
        
        # 连接点击事件
        self.clicked.connect(self.onItemClicked)
    
    @Slot(QModelIndex)
    def onItemClicked(self, index):
        """处理项目点击"""
        node = index.data(Qt.UserRole)
        if node and node.level == 1:  # 只有父节点可展开
            self.model().expand(index)

class MainWindow(QWidget):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 树状导航栏")
        self.resize(800, 600)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加导航栏
        self.navView = NavListView()
        layout.addWidget(self.navView)
        
        # 添加内容区域（示例）
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())