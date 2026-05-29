# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PySide6-Tutorial is a collection of standalone Python scripts demonstrating PySide6 (Qt for Python) widgets, layouts, and application patterns. Each file is self-contained and independently runnable.

## Running Examples

Each script runs directly with Python — no build step needed:

```powershell
python components\QPushButton\qt_QPushButton.py
python components\QTextEdit\qt_QTextEdit.py
python graph\matplotlib\MatplotlibDemo.py
```

Dependencies: `PySide6`, `pandas`, `pywencai`, `matplotlib`, `numpy`, `pyqtgraph`

## Code Structure

```
├── components/              # Basic Qt widget examples (QPushButton, QTextEdit, QProgressBar, QSlider, QDial, QLineEdit, QFormLayout)
├── Advaced-components/      # Advanced widget examples (QListWidget, QTableWidget, QTreeWidget, QListView/QTableView/QTreeView, QSqlQueryModel/QSqlTableModel, QDrag, QMessageBox, QColorDialog, QDialogButtonBox, QLCDNumber)
├── Advanced-Window-Control/ # Window/layout control examples (QSplitter, QDockWidget, QGridLayout, QFormLayout, QMdiArea, QStackedLayout/QStackedWidget, QTabWidget)
├── graph/
│   ├── matplotlib/          # matplotlib FigureCanvas + NavigationToolbar integration with PySide6
│   └── pygraph/             # pyqtgraph integration with PySide6
├── Qss/                     # Qt Stylesheet (QSS) demonstration
├── designer/                # Qt Designer .ui files and their generated/runner Python counterparts
├── Program/                 # Complete application examples
│   ├── customApplicationFrame/  # Frameless custom window with title bar, left menu, credits bar
│   ├── CollapsibleList.py       # Collapsible box widget with animation
│   ├── StockFilterApp.py        # Stock filter app using pywencai + pandas
│   ├── LogDisplay.py
│   ├── TreeNav.py
│   └── StylishLeftMenu.py
└── README.md
```

## Architecture Notes

- **Each file is standalone**: All examples import PySide6 directly and include an `if __name__ == "__main__":` block. No shared package, no test suite, no build system.
- **Standard pattern**: Every demo creates a `QApplication`, instantiates a main widget (QDialog, QMainWindow, or QWidget), calls `.show()`, and enters `app.exec()`.
- **Component files** typically define a single `Form(QDialog)` or demo class, demonstrate one widget's features, then run if executed directly.
- **Program files** combine multiple widgets into functional applications (stock filtering, custom window frames, tree navigation).
- The `designer/` folder contains `.ui` files (Qt Designer XML) paired with generated Python files and manual runner scripts.
