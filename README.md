# PySide6-Tutorial

A comprehensive collection of PySide6 (Qt for Python) examples covering widgets, layouts, data visualization, and complete application demos. Each example is a standalone, runnable script designed for learning Qt6 concepts through hands-on code.

## Features

- **50+ standalone examples** covering basic to advanced PySide6 widgets
- **Qt Designer** integration with `.ui` files and generated Python code
- **Data visualization** demos using matplotlib and pyqtgraph within Qt
- **Database interaction** examples with SQLite (QSqlQueryModel, QSqlTableModel, QSqlRelationalTableModel)
- **Complete application demos** including a custom frameless window, stock filter tool, collapsible navigation, and more
- **Chinese-language comments** throughout for Chinese-speaking learners

## Prerequisites

- Python 3.9+
- PySide6

## Installation

```bash
pip install PySide6
```

Optional dependencies (for specific examples):

```bash
pip install matplotlib numpy pyqtgraph pandas pywencai
```

## Project Structure

```
├── components/                  # Basic Qt widget examples
│   ├── QPushButton/             # Button demo (checkable, disabled, shortcut, icon)
│   ├── QTextEdit/               # Rich text editor
│   ├── QPlainTextEdit/          # Plain text editor
│   ├── QTextBrowser/            # Read-only rich text browser
│   ├── QLineEdit/               # Line input (echo mode, input mask, validator)
│   ├── QProgressBar/            # Progress bar (basic + custom size)
│   ├── QSlider/                 # Slider control
│   ├── QDial/                   # Dial control
│   ├── QFormLayout/             # Form layout
│   ├── QFileDialog/             # File open/save dialogs
│   └── QSyntaxHighlighter/      # Custom syntax highlighting
│
├── Advaced-components/          # Advanced widget examples
│   ├── QListWidget/             # Item-based list
│   ├── QTableWidget/            # Item-based table
│   ├── QTreeWidget/             # Item-based tree
│   ├── QListView/               # Model-based list
│   ├── QTableView/              # Model-based table
│   ├── QTreeView/               # Model-based tree (simple + advanced)
│   ├── QTableModel/             # Custom table model
│   ├── QDataWidgetMapper/       # Map data to form widgets
│   ├── QTableDelegate/          # Custom table delegate
│   ├── QSqlQueryModel/          # SQL query model
│   ├── QSqlTableModel/          # SQL table model
│   ├── QSqlRelationalTableModel/ # SQL relational table model
│   ├── QSqlCustomModelDelegate/ # Custom delegate for SQL models
│   ├── QDrag/                   # Drag and drop
│   ├── QMimeData/               # MIME data handling
│   ├── QMessageBox/             # Message and dialog boxes
│   ├── QColorDialog/            # Color picker dialog
│   ├── QDialogButtonBox/        # Standard dialog buttons
│   ├── QLCDNumber/              # LCD-style number display
│   └── db/                      # SQLite database setup + demo database
│
├── Advanced-Window-Control/     # Window and layout management
│   ├── QSplitter/               # Splitter panels
│   ├── QDockWidget/             # Dockable panels (basic + advanced)
│   ├── QGridLayout/             # Grid layout
│   ├── QFormLayout/             # Form layout
│   ├── QLayout/                 # Custom layout
│   ├── QMdiArea/                # MDI (Multiple Document Interface)
│   ├── QStackedLayout/          # Stacked layout
│   ├── QStackedWidget/          # Stacked widget
│   └── QTabWidget/              # Tabbed panels
│
├── graph/                       # Data visualization
│   ├── matplotlib/              # matplotlib FigureCanvas + NavigationToolbar
│   └── pygraph/                 # pyqtgraph integration
│
├── Qss/                         # Qt Stylesheet (QSS) demos
│
├── designer/                    # Qt Designer examples
│   ├── MainWinMenuToolbar.ui    # Qt Designer source file
│   ├── MainWinMenuToolbar_ui.py # Generated Python from .ui
│   └── MainWinMenuToolbarRun.py # Manual runner with additional logic
│
├── Program/                     # Complete application demos
│   ├── customApplicationFrame/  # Frameless custom window
│   │   ├── MainWindow/          # Main window with title bar + resize grips
│   │   ├── titleBar/            # Custom title bar
│   │   ├── left_menu/           # Left sidebar menu
│   │   └── creditsBar/          # Bottom credits bar
│   ├── CollapsibleList.py       # Collapsible box with QPropertyAnimation
│   ├── LogDisplay.py            # Log display utility
│   ├── StockFilterApp.py        # Stock screener using pywencai + pandas
│   ├── TreeNav.py               # Tree navigation demo
│   └── StylishLeftMenu.py       # Styled left-side menu
└── README.md
```

## Usage

Run any example directly:

```bash
python components/QPushButton/qt_QPushButton.py
python components/QTextEdit/qt_QTextEdit.py
python Advanced-Window-Control/QDockWidget/qt_QDockWidget.py
python graph/matplotlib/MatplotlibDemo.py
python designer/MainWinMenuToolbarRun.py
python Program/CollapsibleList.py
```

## Key Learning Path

| Topic | Examples |
| ------- | ----------- |
| Basic Widgets | QPushButton, QLineEdit, QSlider, QDial, QProgressBar |
| Text & Documents | QTextEdit, QPlainTextEdit, QTextBrowser, QSyntaxHighlighter |
| Item Widgets | QListWidget, QTableWidget, QTreeWidget |
| Model/View | QListView, QTableView, QTreeView, QTableModel, custom delegates |
| SQL & Databases | QSqlQueryModel, QSqlTableModel, QSqlRelationalTableModel |
| Layouts | QFormLayout, QGridLayout, QStackedLayout, QSplitter |
| Window Management | QDockWidget, QMdiArea, QTabWidget, QStackedWidget |
| Dialogs | QFileDialog, QMessageBox, QColorDialog |
| Drag & Drop | QDrag, QMimeData |
| Visualization | matplotlib in Qt canvas, pyqtgraph |
| Styling | Qt Stylesheets (QSS) |
| Qt Designer | `.ui` files, `uic` code generation, manual runner scripts |
| Complete Apps | Custom window frame, stock filter, collapsible nav, tree nav |

## License

This project is for educational purposes.
