import os
import sys
import json
import re
import random
import tempfile
from datetime import datetime
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal, QUrl, QTimer
from PyQt6.QtGui import (
    QFont, QDragEnterEvent, QDragMoveEvent, QDropEvent,
    QPainter, QColor, QPen, QBrush, QPixmap, QKeySequence, QShortcut,
    QPalette
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, QButtonGroup,
    QSpinBox, QComboBox, QTextEdit, QFileDialog, QMessageBox, QDialog,
    QListWidget, QListWidgetItem, QProgressBar, QGroupBox, QSplitter,
    QScrollArea, QFrame, QInputDialog, QSizePolicy
)

APP_NAME = "BATPAN VibeCoder"
APP_VERSION = "ver2.2.05"

# Base directory resolution
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
CHANGELOG_FILE = os.path.join(BASE_DIR, "CHANGELOG.txt")
SNIPPET_CACHE_DIR = os.path.join(BASE_DIR, ".vibecoder_snippets")

# Mappings for syntax highlighting
LANGUAGE_HINTS = {
    ".cs": "csharp",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".xml": "xml",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".sh": "bash",
    ".bat": "batch",
    ".ps1": "powershell",
    ".md": "markdown",
    ".txt": "text"
}

COMMON_EXTENSIONS = [
    ".cs", ".py", ".js", ".ts", ".go", ".rs", ".rb", ".kt", ".sh",
    ".cpp", ".c", ".h", ".css", ".php", ".ps1", ".xml", ".yml",
    ".sql", ".bat", ".java", ".json", ".yaml", ".html", ".swift"
]

POPULAR_SHORTCUTS = [".cs", ".py", ".js", ".ts", ".cpp", ".html", ".css", ".json", ".sql", ".go", ".rs"]

# Localization Dictionary (100% English vs 100% Persian)
TRANSLATIONS = {
    "en": {
        "app_title": f"{APP_NAME} — {APP_VERSION}",
        "settings_title": "Settings",
        "settings_language_label": "Application Language:",
        "settings_save": "Save Settings",
        "settings_saved_msg": "Settings saved successfully!",
        "input_mode_group": "Input Mode",
        "rdo_folder": "Folder Path",
        "rdo_drop": "Dropped Files",
        "rdo_snippet": "Pasted Snippets / Tags [Ctrl+V]",
        "folder_base_label": "Base Folder:",
        "btn_browse_folder": "Browse Folder...",
        "drop_zone_text": "Drag and drop source files or entire folders here",
        "btn_clear_drop": "Clear Files",
        "lbl_dropped_count": "{0} files added",
        "btn_paste_snippet": "📋 Paste New Snippet [Ctrl+V]",
        "btn_manual_snippet": "✏ Write Code...",
        "lbl_snippet_count": "{0} snippet tags stored",
        "btn_clear_snippets": "Clear All Tags",
        "config_group": "Configuration",
        "ext_label": "Active Extension Tags:",
        "ext_input_placeholder": "Type extension (e.g. .py or cs) & hit Enter...",
        "btn_add_ext": "Add Tag",
        "btn_add_all_common": "➕ All Common",
        "btn_clear_ext_tags": "Clear Tags",
        "chk_subfolders": "Search in subfolders",
        "chk_tree": "Show file tree structure",
        "chk_header_summary": "Include header and summary report",
        "format_label": "Output Format:",
        "part_count_label": "Number of Output Parts (1-10):",
        "clipboard_label": "Clipboard Action:",
        "clipboard_opts": ["None", "Copy Content", "Copy File"],
        "output_dest_group": "Output Destination",
        "output_file_label": "Output File Name:",
        "btn_browse_output": "Select Path...",
        "btn_combine": "⚡ Combine Files",
        "btn_save_tree": "Save Tree",
        "settings_btn": "⚙️ Settings",
        "select_dialog_title": "File Filter & Selection",
        "search_label": "Search (File name or path):",
        "search_placeholder": "Type to filter...",
        "btn_select_all": "Select All",
        "btn_deselect_all": "Deselect All",
        "btn_continue": "Continue",
        "btn_cancel": "Cancel",
        "select_count_label": "Total: {0} files | Selected: {1} files",
        "warn_select_empty": "No files selected to combine!",
        "warn_folder_invalid": "Please select a valid source folder!",
        "warn_drop_empty": "The dropped files list is empty!",
        "warn_snippets_empty": "No snippet tags added! Use Ctrl+V or Paste button first.",
        "warn_output_empty": "Please provide an output destination path!",
        "msg_combine_success": "Files combined successfully!",
        "msg_tree_success": "File tree saved successfully!",
        "log_folder_browsed": "Selected folder: {0}",
        "log_files_dropped": "{0} files added. Total: {1}",
        "log_folder_dropped": "Scanned dropped folder '{0}': found {1} matching script(s).",
        "log_drop_cleared": "Dropped files list cleared.",
        "log_snippet_added": "Snippet '{0}' added successfully as a tag.",
        "log_snippet_removed": "Snippet tag '{0}' removed.",
        "log_snippets_cleared": "All snippet tags cleared.",
        "log_combine_done": "Combined {0} files into {1} part(s) successfully.",
        "log_content_copied": "Final combined content copied to clipboard!",
        "log_file_copied": "Output file ({0} file(s)) copied to clipboard as native Windows attachment!",
        "log_settings_loaded": "Saved settings restored from settings.json",
        "snippet_prompt_title": "Pasted Snippet Name",
        "snippet_prompt_msg": "Confirm or rename snippet file:",
        "manual_dialog_title": "Add Code Snippet Manually",
        "manual_name_label": "Snippet Name (with extension e.g. script.py):",
        "manual_code_label": "Source Code:",
        "manual_code_placeholder": "Type or paste your code here..."
    },
    "fa": {
        "app_title": f"BATPAN VibeCoder — نسخه {APP_VERSION}",
        "settings_title": "تنظیمات برنامه",
        "settings_language_label": "زبان برنامه:",
        "settings_save": "ذخیره تنظیمات",
        "settings_saved_msg": "تنظیمات با موفقیت ذخیره شد!",
        "input_mode_group": "حالت ورودی",
        "rdo_folder": "مسیر پوشه",
        "rdo_drop": "فایل‌های رها شده (Drop)",
        "rdo_snippet": "اسکریپت‌های پیست شده / تگ‌ها [Ctrl+V]",
        "folder_base_label": "پوشه مبدأ:",
        "btn_browse_folder": "انتخاب پوشه...",
        "drop_zone_text": "فایل‌ها یا تمام پوشه سورس را اینجا بکشید و رها کنید",
        "btn_clear_drop": "پاکسازی فایل‌ها",
        "lbl_dropped_count": "{0} فایل اضافه شد",
        "btn_paste_snippet": "📋 پیست اسکریپت جدید [Ctrl+V]",
        "btn_manual_snippet": "✏️ نوشتن دستی کد...",
        "lbl_snippet_count": "{0} تگ اسکریپت ذخیره شده",
        "btn_clear_snippets": "پاکسازی همه تگ‌ها",
        "config_group": "تنظیمات پردازش",
        "ext_label": "تگ‌های پسوند فعال:",
        "ext_input_placeholder": "پسوند را تایپ کرده و Enter بزنید (مثلا cs یا .py)...",
        "btn_add_ext": "افزودن تگ",
        "btn_add_all_common": "➕ همه پسوندهای رایج",
        "btn_clear_ext_tags": "پاکسازی تگ‌ها",
        "chk_subfolders": "جستجو در زیرپوشه‌ها",
        "chk_tree": "نمایش ساختار درختی فایل‌ها",
        "chk_header_summary": "درج هدر و گزارش خلاصه نهایی",
        "format_label": "فرمت خروجی:",
        "part_count_label": "تعداد قسمت‌های خروجی (۱ تا ۱۰):",
        "clipboard_label": "عملیات کلیپ‌بورد:",
        "clipboard_opts": ["هیچ‌کدام", "کپی متن محتوا", "کپی فایل"],
        "output_dest_group": "مقصد فایل خروجی",
        "output_file_label": "نام فایل خروجی:",
        "btn_browse_output": "انتخاب مسیر...",
        "btn_combine": "⚡ ترکیب فایل‌ها",
        "btn_save_tree": "ذخیره درخت",
        "settings_btn": "⚙️ تنظیمات",
        "select_dialog_title": "فیلتر و انتخاب فایل‌ها",
        "search_label": "جستجو (نام فایل یا مسیر):",
        "search_placeholder": "برای جستجو تایپ کنید...",
        "btn_select_all": "انتخاب همه",
        "btn_deselect_all": "لغو انتخاب همه",
        "btn_continue": "ادامه",
        "btn_cancel": "انصراف",
        "select_count_label": "تعداد کل: {0} فایل | انتخاب شده: {1} فایل",
        "warn_select_empty": "هیچ فایلی برای ترکیب انتخاب نشده است!",
        "warn_folder_invalid": "لطفاً یک پوشه معتبر انتخاب کنید!",
        "warn_drop_empty": "لیست فایل‌های رها شده خالی است!",
        "warn_snippets_empty": "هیچ اسکریپت یا تگی افزوده نشده است! ابتدا از کلید Ctrl+V استفاده کنید.",
        "warn_output_empty": "لطفاً مسیر ذخیره فایل خروجی را مشخص کنید!",
        "msg_combine_success": "فایل‌ها با موفقیت ترکیب شدند!",
        "msg_tree_success": "درخت فایل‌ها با موفقیت ذخیره شد!",
        "log_folder_browsed": "پوشه انتخاب شده: {0}",
        "log_files_dropped": "{0} فایل اضافه شد. مجموع: {1}",
        "log_folder_dropped": "پوشه رها شده '{0}' پویش شد: تعداد {1} اسکریپت مطابق پیدا شد.",
        "log_drop_cleared": "لیست فایل‌های رها شده پاک شد.",
        "log_snippet_added": "اسکریپت '{0}' با موفقیت به عنوان تگ اضافه شد.",
        "log_snippet_removed": "تگ اسکریپت '{0}' حذف شد.",
        "log_snippets_cleared": "تمام تگ‌های اسکریپت پاک شدند.",
        "log_combine_done": "ترکیب {0} فایل در قالب {1} قسمت با موفقیت انجام شد.",
        "log_content_copied": "محتوای خروجی نهایی در کلیپ‌بورد کپی شد!",
        "log_file_copied": "فایل خروجی ({0} فایل) به عنوان فایل ویندوز در کلیپ‌بورد قرار گرفت!",
        "log_settings_loaded": "تنظیمات ذخیره شده بازیابی شدند.",
        "snippet_prompt_title": "نام اسکریپت پیست شده",
        "snippet_prompt_msg": "نام فایل یا اسکریپت را تایید یا ویرایش کنید:",
        "manual_dialog_title": "افزودن دستی قطعه کد",
        "manual_name_label": "نام اسکریپت (همراه با پسوند مثلا script.py):",
        "manual_code_label": "کد سورس:",
        "manual_code_placeholder": "کد خود را اینجا بنویسید یا پیست کنید..."
    }
}


def ensure_changelog_file():
    lines = [
        "=" * 80,
        f"                  {APP_NAME} — CHANGELOG",
        "=" * 80,
        "",
        "Version 2.2.05",
        "-" * 80,
        "- Changed versioning convention from 'v' to 'ver'.",
        "- Fixed checkboxes in the File Selection dialog to render in clear green rather than dark/black.",
        "- Full-row toggle: Clicking on the file path text now toggles the checkbox state.",
        "- Added adaptive version badge coloring: Yellow in Dark mode, Deep Slate in Light mode.",
        "",
        "Version 2.2",
        "-" * 80,
        "- Full folder drop support: Recursively scans and extracts matching scripts from dropped directories.",
        "- YouTube-style Tag Box for Extensions with interactive tag chips.",
        "- Added 'All Common' quick-add button and quick-pick pills for standard formats.",
        "",
        "Version 2.1",
        "-" * 80,
        "- Dedicated Settings panel opened via the gear icon.",
        "- Complete multilingual system: English (default) and Persian (Farsi).",
        "",
        "Version 2.0",
        "-" * 80,
        "- Full rebranding to BATPAN VibeCoder.",
        "- Intelligent function/void name extraction for auto-naming pasted scripts."
    ]
    try:
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception:
        pass


def create_indicator_icons():
    temp_dir = tempfile.gettempdir().replace("\\", "/")
    chk_path = temp_dir + "/batpan_chk_checked.png"
    rdo_path = temp_dir + "/batpan_rdo_checked.png"

    # Crisp white checkmark over green indicator
    chk_pix = QPixmap(18, 18)
    chk_pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(chk_pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(QPen(QColor("#ffffff"), 2.2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    p.drawLine(4, 9, 7, 13)
    p.drawLine(7, 13, 14, 5)
    p.end()
    chk_pix.save(chk_path)

    # Cyan circular dot for Radio Buttons
    rdo_pix = QPixmap(18, 18)
    rdo_pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(rdo_pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(QColor("#38bdf8")))
    p.drawEllipse(4, 4, 10, 10)
    p.end()
    rdo_pix.save(rdo_path)

    return chk_path, rdo_path


def format_file_size(size_in_bytes: int) -> str:
    val = float(size_in_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if val < 1024.0:
            return f"{val:3.1f} {unit}"
        val /= 1024.0
    return f"{val:.1f} PB"


def extract_function_or_method_name(code: str) -> tuple[str | None, str]:
    first_1000 = code[:1000]
    ext = ".txt"

    if "using System;" in first_1000 or "namespace " in first_1000 or "Console.WriteLine" in first_1000:
        ext = ".cs"
    elif "#include" in first_1000 or "std::" in first_1000:
        ext = ".cpp"
    elif "def " in first_1000 or "import " in first_1000 or "__name__" in first_1000:
        ext = ".py"
    elif "package main" in first_1000 or ("func " in first_1000 and "import (" in first_1000):
        ext = ".go"
    elif "fn " in first_1000 and ("let mut" in first_1000 or "println!" in first_1000 or "pub fn" in first_1000):
        ext = ".rs"
    elif "<?php" in first_1000:
        ext = ".php"
    elif "interface " in first_1000 or ": string" in first_1000 or ": number" in first_1000:
        ext = ".ts"
    elif "function " in first_1000 or "const " in first_1000 or "console.log" in first_1000:
        ext = ".js"
    elif "<!DOCTYPE html>" in first_1000.lower() or "<html" in first_1000.lower():
        ext = ".html"
    elif "{" in first_1000 and '"' in first_1000 and "}" in code[-200:]:
        ext = ".json"
    elif "SELECT " in first_1000.upper() or "CREATE TABLE" in first_1000.upper():
        ext = ".sql"

    void_match = re.search(r"\bvoid\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    if void_match:
        return void_match.group(1), (".cs" if ext == ".txt" else ext)

    py_match = re.search(r"^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code, re.MULTILINE)
    if py_match:
        return py_match.group(1), ".py"

    func_match = re.search(r"\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    if func_match:
        return func_match.group(1), (".js" if ext == ".txt" else ext)

    go_match = re.search(r"\bfunc\s+(?:\([^)]*\)\s*)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    if go_match:
        return go_match.group(1), ".go"

    rs_match = re.search(r"\bfn\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    if rs_match:
        return rs_match.group(1), ".rs"

    arrow_match = re.search(r"\b(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z_][a-zA-Z0-9_]*)\s*=>", code)
    if arrow_match:
        return arrow_match.group(1), (".js" if ext == ".txt" else ext)

    general_match = re.search(r"\b(?:public|private|protected|internal|static|async|virtual|override)?\s*(?:int|string|bool|float|double|Task|IActionResult|[A-Z][a-zA-Z0-9_<>]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    if general_match:
        m_name = general_match.group(1)
        if m_name not in ("if", "for", "while", "switch", "catch", "return"):
            return m_name, (".cs" if ext == ".txt" else ext)

    class_match = re.search(r"\b(?:class|struct|interface)\s+([a-zA-Z_][a-zA-Z0-9_]*)", code)
    if class_match:
        return class_match.group(1), (".cs" if ext == ".txt" else ext)

    return None, ext


def recommend_filename(code: str, index: int) -> str:
    func_name, ext = extract_function_or_method_name(code)
    if func_name:
        return f"{func_name}{ext}"
    rand_suffix = random.randint(100, 999)
    return f"snippet_{index}_{rand_suffix}{ext}"


class ExtensionTagChip(QFrame):
    """YouTube-like smooth rounded tag for file extensions."""
    deleted = pyqtSignal(str)

    def __init__(self, ext: str, parent=None):
        super().__init__(parent)
        self.ext = ext
        self.setObjectName("ext_tag")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 6, 3)
        layout.setSpacing(6)

        lbl_text = QLabel(ext)
        lbl_text.setObjectName("ext_tag_text")
        lbl_text.setStyleSheet("font-weight: bold; font-size: 11px;")

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(16, 16)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setObjectName("tag_close_btn")
        btn_close.clicked.connect(lambda: self.deleted.emit(self.ext))

        layout.addWidget(lbl_text)
        layout.addWidget(btn_close)


class SnippetTagChip(QFrame):
    """YouTube-like smooth rounded tag widget with delete button."""
    deleted = pyqtSignal(str)

    def __init__(self, filename: str, content: str, parent=None):
        super().__init__(parent)
        self.filename = filename
        self.content = content
        self.setObjectName("snippet_tag")

        size_str = format_file_size(len(content.encode("utf-8")))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 8, 4)
        layout.setSpacing(8)

        lbl_icon = QLabel("🏷️")
        lbl_text = QLabel(f"{filename}  ({size_str})")
        lbl_text.setObjectName("tag_text")
        lbl_text.setStyleSheet("font-weight: bold; font-size: 12px;")

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(20, 20)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setObjectName("tag_close_btn")
        btn_close.clicked.connect(lambda: self.deleted.emit(self.filename))

        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_text)
        layout.addWidget(btn_close)

        preview_lines = content.strip().splitlines()[:6]
        preview_text = "\n".join(preview_lines)
        if len(content.strip().splitlines()) > 6:
            preview_text += "\n..."
        self.setToolTip(f"<b>{filename}</b>\n<pre>{preview_text}</pre>")


class SettingsDialog(QDialog):
    def __init__(self, current_lang="en", parent=None):
        super().__init__(parent)
        self.current_lang = current_lang
        self.tr = TRANSLATIONS[current_lang]
        self.setWindowTitle(self.tr["settings_title"])
        self.resize(380, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        lbl = QLabel(f"<b>{self.tr['settings_language_label']}</b>")
        layout.addWidget(lbl)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("فارسی (Persian)", "fa")

        idx = 0 if self.current_lang == "en" else 1
        self.lang_combo.setCurrentIndex(idx)
        layout.addWidget(self.lang_combo)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_save = QPushButton(self.tr["settings_save"])
        btn_save.setObjectName("primary_btn")
        btn_save.clicked.connect(self.accept)

        btn_cancel = QPushButton(self.tr["btn_cancel"])
        btn_cancel.clicked.connect(self.reject)

        btn_row.addStretch()
        btn_row.addWidget(btn_save)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)

    def get_selected_language(self):
        return self.lang_combo.currentData()


class FileSelectionDialog(QDialog):
    def __init__(self, files: list[str], lang="en", parent=None):
        super().__init__(parent)
        self.lang = lang
        self.tr = TRANSLATIONS[lang]
        self.setWindowTitle(self.tr["select_dialog_title"])
        self.resize(760, 530)
        self.all_files = files
        self.selected_files = list(files)

        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel(self.tr["search_label"]))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr["search_placeholder"])
        self.search_input.textChanged.connect(self.filter_items)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.list_widget = QListWidget()
        for f in self.all_files:
            item = QListWidgetItem(f)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)

        # Allow clicking anywhere on the row to toggle checked/unchecked
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        self.lbl_counts = QLabel(self.tr["select_count_label"].format(len(self.all_files), len(self.all_files)))
        self.lbl_counts.setStyleSheet("color: #22c55e; font-weight: bold;")
        layout.addWidget(self.lbl_counts)

        btn_row = QHBoxLayout()
        btn_select_all = QPushButton(self.tr["btn_select_all"])
        btn_select_all.clicked.connect(lambda: self.set_all_checks(Qt.CheckState.Checked))
        btn_deselect_all = QPushButton(self.tr["btn_deselect_all"])
        btn_deselect_all.clicked.connect(lambda: self.set_all_checks(Qt.CheckState.Unchecked))

        btn_row.addWidget(btn_select_all)
        btn_row.addWidget(btn_deselect_all)
        btn_row.addStretch()

        btn_ok = QPushButton(self.tr["btn_continue"])
        btn_ok.setObjectName("primary_btn")
        btn_ok.clicked.connect(self.on_accept)
        btn_cancel = QPushButton(self.tr["btn_cancel"])
        btn_cancel.clicked.connect(self.reject)

        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)

        self.list_widget.itemChanged.connect(self.update_count_label)

    def on_item_clicked(self, item: QListWidgetItem):
        # Toggles checkbox when the text in front is clicked
        new_state = Qt.CheckState.Unchecked if item.checkState() == Qt.CheckState.Checked else Qt.CheckState.Checked
        item.setCheckState(new_state)

    def set_all_checks(self, state: Qt.CheckState):
        self.list_widget.blockSignals(True)
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setCheckState(state)
        self.list_widget.blockSignals(False)
        self.update_count_label()

    def filter_items(self, text: str):
        query = text.strip().lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(query not in item.text().lower())

    def update_count_label(self, *args):
        checked = sum(1 for i in range(self.list_widget.count()) if self.list_widget.item(i).checkState() == Qt.CheckState.Checked)
        self.lbl_counts.setText(self.tr["select_count_label"].format(self.list_widget.count(), checked))

    def on_accept(self):
        self.selected_files = [
            self.list_widget.item(i).text()
            for i in range(self.list_widget.count())
            if self.list_widget.item(i).checkState() == Qt.CheckState.Checked
        ]
        self.accept()


class DropArea(QLabel):
    files_dropped = pyqtSignal(list)

    def __init__(self, prompt_text=""):
        super().__init__(prompt_text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("drop_zone")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        paths = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile()]
        if paths:
            self.files_dropped.emit(paths)


class FileCombinerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "en"
        self.theme_mode = "dark"
        self.dropped_files = []
        self.snippets = []
        self.extension_tags = list(COMMON_EXTENSIONS)

        self.chk_icon, self.rdo_icon = create_indicator_icons()

        self.autosave_timer = QTimer(self)
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.timeout.connect(self.save_settings)

        self.setup_ui()
        self.setup_shortcuts()

        ensure_changelog_file()
        self.load_settings()
        self.apply_language(self.language)

    def t(self, key):
        return TRANSLATIONS.get(self.language, TRANSLATIONS["en"]).get(key, "")

    def setup_shortcuts(self):
        self.paste_shortcut = QShortcut(QKeySequence.StandardKey.Paste, self)
        self.paste_shortcut.activated.connect(self.handle_global_paste_shortcut)

    def handle_global_paste_shortcut(self):
        focused = QApplication.focusWidget()
        if isinstance(focused, (QLineEdit, QTextEdit)):
            focused.paste()
            return

        if self.rdo_snippet.isChecked():
            self.paste_snippet_from_clipboard()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(10)

        # 1. Top Bar: Modes + Theme Cycle + Settings Button + Version
        self.mode_box = QGroupBox()
        mode_layout = QHBoxLayout(self.mode_box)
        self.rdo_folder = QRadioButton()
        self.rdo_drop = QRadioButton()
        self.rdo_snippet = QRadioButton()
        self.rdo_folder.setChecked(True)

        self.rdo_folder.toggled.connect(self.toggle_input_mode)
        self.rdo_drop.toggled.connect(self.toggle_input_mode)
        self.rdo_snippet.toggled.connect(self.toggle_input_mode)

        self.rdo_folder.toggled.connect(self.save_settings)
        self.rdo_drop.toggled.connect(self.save_settings)
        self.rdo_snippet.toggled.connect(self.save_settings)

        mode_layout.addWidget(self.rdo_folder)
        mode_layout.addWidget(self.rdo_drop)
        mode_layout.addWidget(self.rdo_snippet)
        mode_layout.addStretch()

        self.btn_theme_toggle = QPushButton("🌙 Dark")
        self.btn_theme_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme_toggle.setStyleSheet("padding: 3px 10px; font-weight: bold; border-radius: 5px;")
        self.btn_theme_toggle.clicked.connect(self.cycle_theme)
        mode_layout.addWidget(self.btn_theme_toggle)

        self.btn_settings = QPushButton()
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_settings.setStyleSheet("padding: 3px 10px; font-weight: bold; border-radius: 5px;")
        self.btn_settings.clicked.connect(self.open_settings_dialog)
        mode_layout.addWidget(self.btn_settings)

        self.ver_badge = QLabel(APP_VERSION)
        self.ver_badge.setObjectName("version_badge")
        mode_layout.addWidget(self.ver_badge)
        self.main_layout.addWidget(self.mode_box)

        # 2. Folder Panel
        self.folder_panel = QWidget()
        folder_layout = QVBoxLayout(self.folder_panel)
        folder_layout.setContentsMargins(0, 0, 0, 0)

        dir_browse_row = QHBoxLayout()
        self.lbl_folder_base = QLabel()
        self.txt_folder_path = QLineEdit()
        self.txt_folder_path.textChanged.connect(self.schedule_save_settings)
        self.btn_browse_folder = QPushButton()
        self.btn_browse_folder.clicked.connect(self.browse_folder)
        dir_browse_row.addWidget(self.lbl_folder_base)
        dir_browse_row.addWidget(self.txt_folder_path)
        dir_browse_row.addWidget(self.btn_browse_folder)
        folder_layout.addLayout(dir_browse_row)
        self.main_layout.addWidget(self.folder_panel)

        # 3. Drop Panel
        self.drop_panel = QWidget()
        self.drop_panel.setVisible(False)
        drop_layout = QVBoxLayout(self.drop_panel)
        drop_layout.setContentsMargins(0, 0, 0, 0)
        self.drop_zone = DropArea()
        self.drop_zone.files_dropped.connect(self.handle_files_dropped)
        drop_layout.addWidget(self.drop_zone)

        drop_list_controls = QHBoxLayout()
        self.lbl_dropped_count = QLabel()
        self.btn_clear_drop = QPushButton()
        self.btn_clear_drop.clicked.connect(self.clear_dropped_files)
        drop_list_controls.addWidget(self.lbl_dropped_count)
        drop_list_controls.addStretch()
        drop_list_controls.addWidget(self.btn_clear_drop)
        drop_layout.addLayout(drop_list_controls)
        self.main_layout.addWidget(self.drop_panel)

        # 4. Snippet / Tag Panel
        self.snippet_panel = QWidget()
        self.snippet_panel.setVisible(False)
        snippet_layout = QVBoxLayout(self.snippet_panel)
        snippet_layout.setContentsMargins(0, 0, 0, 0)

        snippet_action_row = QHBoxLayout()
        self.btn_paste_snippet = QPushButton()
        self.btn_paste_snippet.setObjectName("accent_btn")
        self.btn_paste_snippet.clicked.connect(self.paste_snippet_from_clipboard)

        self.btn_manual_snippet = QPushButton()
        self.btn_manual_snippet.clicked.connect(self.add_manual_snippet_dialog)

        snippet_action_row.addWidget(self.btn_paste_snippet, stretch=2)
        snippet_action_row.addWidget(self.btn_manual_snippet, stretch=1)
        snippet_layout.addLayout(snippet_action_row)

        self.tag_scroll = QScrollArea()
        self.tag_scroll.setObjectName("tag_scroll")
        self.tag_scroll.setWidgetResizable(True)
        self.tag_scroll.setFixedHeight(105)

        self.tag_container = QWidget()
        self.tag_container_layout = QHBoxLayout(self.tag_container)
        self.tag_container_layout.setContentsMargins(8, 8, 8, 8)
        self.tag_container_layout.setSpacing(8)
        self.tag_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.tag_scroll.setWidget(self.tag_container)
        snippet_layout.addWidget(self.tag_scroll)

        snippet_status_row = QHBoxLayout()
        self.lbl_snippet_count = QLabel()
        self.lbl_snippet_count.setStyleSheet("color: #6366f1; font-weight: bold;")
        self.btn_clear_snippets = QPushButton()
        self.btn_clear_snippets.clicked.connect(self.clear_all_snippets)

        snippet_status_row.addWidget(self.lbl_snippet_count)
        snippet_status_row.addStretch()
        snippet_status_row.addWidget(self.btn_clear_snippets)
        snippet_layout.addLayout(snippet_status_row)

        self.main_layout.addWidget(self.snippet_panel)

        # 5. Configuration Group (with YouTube-style Extension Tags)
        self.settings_box = QGroupBox()
        settings_layout = QVBoxLayout(self.settings_box)

        # Extension controls row
        ext_control_row = QHBoxLayout()
        self.lbl_ext = QLabel()
        self.txt_ext_input = QLineEdit()
        self.txt_ext_input.returnPressed.connect(self.add_extension_tag_from_input)

        self.btn_add_ext = QPushButton()
        self.btn_add_ext.clicked.connect(self.add_extension_tag_from_input)

        self.btn_add_all_common = QPushButton()
        self.btn_add_all_common.setObjectName("accent_btn")
        self.btn_add_all_common.clicked.connect(self.add_all_common_extensions)

        self.btn_clear_ext_tags = QPushButton()
        self.btn_clear_ext_tags.clicked.connect(self.clear_all_extension_tags)

        ext_control_row.addWidget(self.lbl_ext)
        ext_control_row.addWidget(self.txt_ext_input, stretch=2)
        ext_control_row.addWidget(self.btn_add_ext)
        ext_control_row.addWidget(self.btn_add_all_common)
        ext_control_row.addWidget(self.btn_clear_ext_tags)
        settings_layout.addLayout(ext_control_row)

        # Quick common format pill-selector row
        self.quick_pills_layout = QHBoxLayout()
        self.quick_pills_layout.setSpacing(4)
        for p_ext in POPULAR_SHORTCUTS:
            pill = QPushButton(p_ext)
            pill.setObjectName("pill_btn")
            pill.setCursor(Qt.CursorShape.PointingHandCursor)
            pill.clicked.connect(lambda checked, e=p_ext: self.toggle_extension_tag(e))
            self.quick_pills_layout.addWidget(pill)
        self.quick_pills_layout.addStretch()
        settings_layout.addLayout(self.quick_pills_layout)

        # Scrollable container for YouTube-style Extension Tag chips
        self.ext_tag_scroll = QScrollArea()
        self.ext_tag_scroll.setObjectName("tag_scroll")
        self.ext_tag_scroll.setWidgetResizable(True)
        self.ext_tag_scroll.setFixedHeight(64)

        self.ext_tag_container = QWidget()
        self.ext_tag_container_layout = QHBoxLayout(self.ext_tag_container)
        self.ext_tag_container_layout.setContentsMargins(6, 6, 6, 6)
        self.ext_tag_container_layout.setSpacing(6)
        self.ext_tag_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.ext_tag_scroll.setWidget(self.ext_tag_container)
        settings_layout.addWidget(self.ext_tag_scroll)

        chk_row = QHBoxLayout()
        self.chk_subfolders = QCheckBox()
        self.chk_subfolders.setChecked(True)
        self.chk_subfolders.toggled.connect(self.save_settings)

        self.chk_tree = QCheckBox()
        self.chk_tree.setChecked(True)
        self.chk_tree.toggled.connect(self.save_settings)

        self.chk_header_summary = QCheckBox()
        self.chk_header_summary.setChecked(True)
        self.chk_header_summary.toggled.connect(self.save_settings)

        chk_row.addWidget(self.chk_subfolders)
        chk_row.addWidget(self.chk_tree)
        chk_row.addWidget(self.chk_header_summary)
        chk_row.addStretch()
        settings_layout.addLayout(chk_row)

        opts_row = QHBoxLayout()
        self.lbl_format = QLabel()
        self.rdo_txt = QRadioButton("Text (.txt)")
        self.rdo_md = QRadioButton("Markdown (.md)")
        self.rdo_txt.setChecked(True)
        self.rdo_txt.toggled.connect(self.save_settings)
        opts_row.addWidget(self.lbl_format)
        opts_row.addWidget(self.rdo_txt)
        opts_row.addWidget(self.rdo_md)
        opts_row.addSpacing(20)

        self.lbl_part_count = QLabel()
        self.num_parts = QSpinBox()
        self.num_parts.setRange(1, 10)
        self.num_parts.setValue(1)
        self.num_parts.valueChanged.connect(self.save_settings)
        opts_row.addWidget(self.lbl_part_count)
        opts_row.addWidget(self.num_parts)
        opts_row.addSpacing(20)

        self.lbl_clipboard = QLabel()
        self.cmb_clipboard = QComboBox()
        self.cmb_clipboard.currentIndexChanged.connect(self.save_settings)
        opts_row.addWidget(self.lbl_clipboard)
        opts_row.addWidget(self.cmb_clipboard)
        opts_row.addStretch()
        settings_layout.addLayout(opts_row)

        self.main_layout.addWidget(self.settings_box)

        # 6. Output Destination Group
        self.out_box = QGroupBox()
        out_layout = QHBoxLayout(self.out_box)
        self.lbl_output_file = QLabel()
        self.txt_output_path = QLineEdit("combined_output.txt")
        self.txt_output_path.textChanged.connect(self.schedule_save_settings)
        self.btn_browse_output = QPushButton()
        self.btn_browse_output.clicked.connect(self.browse_output)
        out_layout.addWidget(self.lbl_output_file)
        out_layout.addWidget(self.txt_output_path)
        out_layout.addWidget(self.btn_browse_output)
        self.main_layout.addWidget(self.out_box)

        # 7. Action Row
        act_row = QHBoxLayout()
        self.btn_combine = QPushButton()
        self.btn_combine.setObjectName("primary_btn")
        self.btn_combine.clicked.connect(self.combine_files)
        self.btn_save_tree = QPushButton()
        self.btn_save_tree.clicked.connect(self.save_tree_only)

        act_row.addWidget(self.btn_combine, stretch=3)
        act_row.addWidget(self.btn_save_tree, stretch=1)
        self.main_layout.addLayout(act_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.main_layout.addWidget(self.progress_bar)

        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setFixedHeight(180)
        self.main_layout.addWidget(self.txt_log)

    def apply_language(self, lang_code: str):
        self.language = lang_code
        tr = TRANSLATIONS[lang_code]

        if lang_code == "fa":
            QApplication.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.setWindowTitle(tr["app_title"])
        self.mode_box.setTitle(tr["input_mode_group"])
        self.rdo_folder.setText(tr["rdo_folder"])
        self.rdo_drop.setText(tr["rdo_drop"])
        self.rdo_snippet.setText(tr["rdo_snippet"])

        self.btn_settings.setText(tr["settings_btn"])

        self.lbl_folder_base.setText(tr["folder_base_label"])
        self.btn_browse_folder.setText(tr["btn_browse_folder"])

        self.drop_zone.setText(tr["drop_zone_text"])
        self.lbl_dropped_count.setText(tr["lbl_dropped_count"].format(len(self.dropped_files)))
        self.btn_clear_drop.setText(tr["btn_clear_drop"])

        self.btn_paste_snippet.setText(tr["btn_paste_snippet"])
        self.btn_manual_snippet.setText(tr["btn_manual_snippet"])
        self.lbl_snippet_count.setText(tr["lbl_snippet_count"].format(len(self.snippets)))
        self.btn_clear_snippets.setText(tr["btn_clear_snippets"])

        self.settings_box.setTitle(tr["config_group"])
        self.lbl_ext.setText(tr["ext_label"])
        self.txt_ext_input.setPlaceholderText(tr["ext_input_placeholder"])
        self.btn_add_ext.setText(tr["btn_add_ext"])
        self.btn_add_all_common.setText(tr["btn_add_all_common"])
        self.btn_clear_ext_tags.setText(tr["btn_clear_ext_tags"])

        self.chk_subfolders.setText(tr["chk_subfolders"])
        self.chk_tree.setText(tr["chk_tree"])
        self.chk_header_summary.setText(tr["chk_header_summary"])

        self.lbl_format.setText(tr["format_label"])
        self.lbl_part_count.setText(tr["part_count_label"])
        self.lbl_clipboard.setText(tr["clipboard_label"])

        cur_clip = self.cmb_clipboard.currentIndex()
        if cur_clip < 0: cur_clip = 2
        self.cmb_clipboard.blockSignals(True)
        self.cmb_clipboard.clear()
        self.cmb_clipboard.addItems(tr["clipboard_opts"])
        self.cmb_clipboard.setCurrentIndex(cur_clip)
        self.cmb_clipboard.blockSignals(False)

        self.out_box.setTitle(tr["output_dest_group"])
        self.lbl_output_file.setText(tr["output_file_label"])
        self.btn_browse_output.setText(tr["btn_browse_output"])

        self.btn_combine.setText(tr["btn_combine"])
        self.btn_save_tree.setText(tr["btn_save_tree"])

        self.apply_theme_mode(self.theme_mode)
        self.refresh_extension_tag_container()

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.language, self)
        if dialog.exec():
            selected_lang = dialog.get_selected_language()
            if selected_lang != self.language:
                self.apply_language(selected_lang)
                self.save_settings()
                QMessageBox.information(self, self.t("settings_title"), self.t("settings_saved_msg"))

    def cycle_theme(self):
        order = ["dark", "light", "system"]
        current_idx = order.index(self.theme_mode) if self.theme_mode in order else 0
        next_mode = order[(current_idx + 1) % len(order)]
        self.apply_theme_mode(next_mode)
        self.save_settings()

    def apply_theme_mode(self, mode: str):
        self.theme_mode = mode
        if mode == "dark":
            self.btn_theme_toggle.setText("🌙 Dark")
            self.render_dark_theme()
        elif mode == "light":
            self.btn_theme_toggle.setText("☀️ Light")
            self.render_light_theme()
        else:
            self.btn_theme_toggle.setText("💻 System")
            bg_color = QApplication.palette().color(QPalette.ColorRole.Window)
            if bg_color.lightness() < 128:
                self.render_dark_theme()
            else:
                self.render_light_theme()

    def render_dark_theme(self):
        base_style = """
            QMainWindow, QWidget {
                background-color: #121214;
                color: #e4e4e7;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 13px;
            }
            QLabel#version_badge {
                color: #facc15;
                font-weight: bold;
                font-size: 11px;
                padding: 3px 8px;
                background-color: #292524;
                border-radius: 4px;
                border: 1px solid #ca8a04;
            }
            QGroupBox {
                border: 1px solid #27272a;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
                padding: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #a1a1aa;
            }
            QLineEdit, QTextEdit {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 5px;
                color: #fafafa;
                padding: 6px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #6366f1;
            }
            QPushButton {
                background-color: #27272a;
                border: 1px solid #3f3f46;
                border-radius: 5px;
                padding: 6px 14px;
                font-weight: bold;
                color: #fafafa;
            }
            QPushButton:hover {
                background-color: #3f3f46;
            }
            QPushButton#primary_btn {
                background-color: #4338ca;
                border: 1px solid #4f46e5;
                color: #ffffff;
            }
            QPushButton#primary_btn:hover {
                background-color: #4f46e5;
            }
            QPushButton#accent_btn {
                background-color: #1e1b4b;
                border: 1px solid #6366f1;
                color: #c7d2fe;
            }
            QPushButton#accent_btn:hover {
                background-color: #312e81;
                color: #ffffff;
            }
            QPushButton#pill_btn {
                background-color: #1c1917;
                border: 1px solid #44403c;
                border-radius: 12px;
                padding: 2px 10px;
                font-size: 11px;
                color: #a8a29e;
            }
            QPushButton#pill_btn:hover {
                background-color: #292524;
                color: #f5f5f4;
                border-color: #6366f1;
            }
            QProgressBar {
                border: 1px solid #27272a;
                border-radius: 4px;
                text-align: center;
                height: 18px;
            }
            QProgressBar::chunk {
                background-color: #4f46e5;
            }
            QCheckBox {
                color: #e4e4e7;
                spacing: 8px;
            }
            QCheckBox:checked {
                color: #4ade80;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #71717a;
                border-radius: 4px;
                background-color: #27272a;
            }
            QCheckBox::indicator:hover {
                border-color: #4ade80;
            }
            QCheckBox::indicator:checked {
                background-color: #16a34a;
                border: 2px solid #22c55e;
                image: url('__CHK_ICON__');
            }
            QRadioButton {
                color: #e4e4e7;
                spacing: 8px;
            }
            QRadioButton:checked {
                color: #38bdf8;
                font-weight: bold;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #71717a;
                border-radius: 10px;
                background-color: #27272a;
            }
            QRadioButton::indicator:hover {
                border-color: #38bdf8;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #38bdf8;
                background-color: #18181b;
                image: url('__RDO_ICON__');
            }
            QComboBox, QSpinBox {
                background-color: #1f1f23;
                border: 1px solid #3f3f46;
                border-radius: 4px;
                padding: 5px 8px;
                color: #fafafa;
                font-weight: bold;
            }
            QComboBox QAbstractItemView {
                background-color: #18181b;
                border: 1px solid #3f3f46;
                color: #fafafa;
                selection-background-color: #4f46e5;
                selection-color: #ffffff;
                padding: 4px;
            }

            /* --- FILE SELECTION LIST WIDGET & GREEN TOGGLES --- */
            QListWidget {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 6px;
                padding: 6px;
                color: #f4f4f5;
            }
            QListWidget::item {
                padding: 6px 8px;
                border-radius: 5px;
                margin-bottom: 2px;
            }
            QListWidget::item:hover {
                background-color: #27272a;
            }
            QListWidget::item:selected {
                background-color: #312e81;
                color: #ffffff;
            }
            QListWidget::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #52525b;
                border-radius: 4px;
                background-color: #27272a;
                margin-right: 6px;
            }
            QListWidget::indicator:hover {
                border-color: #22c55e;
            }
            QListWidget::indicator:checked {
                background-color: #16a34a;
                border: 2px solid #22c55e;
                image: url('__CHK_ICON__');
            }

            QScrollArea#tag_scroll {
                background-color: #151518;
                border: 1px solid #27272a;
                border-radius: 6px;
            }
            QFrame#snippet_tag {
                background-color: #1e1e2d;
                border: 1px solid #4f46e5;
                border-radius: 8px;
            }
            QFrame#snippet_tag:hover {
                background-color: #28283d;
                border-color: #818cf8;
            }
            QFrame#ext_tag {
                background-color: #172554;
                border: 1px solid #2563eb;
                border-radius: 6px;
            }
            QFrame#ext_tag:hover {
                background-color: #1e3a8a;
                border-color: #38bdf8;
            }
            QLabel#tag_text, QLabel#ext_tag_text {
                color: #e0e7ff;
            }
            QPushButton#tag_close_btn {
                background: transparent;
                border: none;
                color: #a5b4fc;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton#tag_close_btn:hover {
                background-color: #ef4444;
                color: #ffffff;
            }
            QLabel#drop_zone {
                border: 2px dashed #6366f1;
                border-radius: 8px;
                background-color: #1e1e24;
                color: #c7d2fe;
                font-weight: bold;
                padding: 24px;
            }
            QLabel#drop_zone:hover {
                background-color: #272733;
                border-color: #818cf8;
            }
        """
        final_style = base_style.replace("__CHK_ICON__", self.chk_icon).replace("__RDO_ICON__", self.rdo_icon)
        self.setStyleSheet(final_style)

    def render_light_theme(self):
        base_style = """
            QMainWindow, QWidget {
                background-color: #f8fafc;
                color: #0f172a;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 13px;
            }
            QLabel#version_badge {
                color: #1e293b;
                font-weight: bold;
                font-size: 11px;
                padding: 3px 8px;
                background-color: #e2e8f0;
                border-radius: 4px;
                border: 1px solid #475569;
            }
            QGroupBox {
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
                padding: 12px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #475569;
            }
            QLineEdit, QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                color: #0f172a;
                padding: 6px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #4f46e5;
            }
            QPushButton {
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                padding: 6px 14px;
                font-weight: bold;
                color: #1e293b;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton#primary_btn {
                background-color: #4f46e5;
                border: 1px solid #4338ca;
                color: #ffffff;
            }
            QPushButton#primary_btn:hover {
                background-color: #4338ca;
            }
            QPushButton#accent_btn {
                background-color: #e0e7ff;
                border: 1px solid #c7d2fe;
                color: #3730a3;
            }
            QPushButton#accent_btn:hover {
                background-color: #c7d2fe;
            }
            QPushButton#pill_btn {
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 12px;
                padding: 2px 10px;
                font-size: 11px;
                color: #475569;
            }
            QPushButton#pill_btn:hover {
                background-color: #e2e8f0;
                color: #0f172a;
                border-color: #4f46e5;
            }
            QProgressBar {
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                text-align: center;
                height: 18px;
            }
            QProgressBar::chunk {
                background-color: #4f46e5;
            }
            QCheckBox {
                color: #0f172a;
                spacing: 8px;
            }
            QCheckBox:checked {
                color: #15803d;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #94a3b8;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:hover {
                border-color: #16a34a;
            }
            QCheckBox::indicator:checked {
                background-color: #16a34a;
                border: 2px solid #15803d;
                image: url('__CHK_ICON__');
            }
            QRadioButton {
                color: #0f172a;
                spacing: 8px;
            }
            QRadioButton:checked {
                color: #0284c7;
                font-weight: bold;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #94a3b8;
                border-radius: 10px;
                background-color: #ffffff;
            }
            QRadioButton::indicator:hover {
                border-color: #0284c7;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #0284c7;
                background-color: #ffffff;
                image: url('__RDO_ICON__');
            }
            QComboBox, QSpinBox {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                padding: 5px 8px;
                color: #0f172a;
                font-weight: bold;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                color: #0f172a;
                selection-background-color: #4f46e5;
                selection-color: #ffffff;
                padding: 4px;
            }

            /* --- FILE SELECTION LIST WIDGET & GREEN TOGGLES --- */
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px;
                color: #0f172a;
            }
            QListWidget::item {
                padding: 6px 8px;
                border-radius: 5px;
                margin-bottom: 2px;
            }
            QListWidget::item:hover {
                background-color: #f1f5f9;
            }
            QListWidget::item:selected {
                background-color: #e0e7ff;
                color: #312e81;
            }
            QListWidget::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #94a3b8;
                border-radius: 4px;
                background-color: #ffffff;
                margin-right: 6px;
            }
            QListWidget::indicator:hover {
                border-color: #16a34a;
            }
            QListWidget::indicator:checked {
                background-color: #16a34a;
                border: 2px solid #15803d;
                image: url('__CHK_ICON__');
            }

            QScrollArea#tag_scroll {
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
            }
            QFrame#snippet_tag {
                background-color: #e0e7ff;
                border: 1px solid #818cf8;
                border-radius: 8px;
            }
            QFrame#snippet_tag:hover {
                background-color: #c7d2fe;
            }
            QFrame#ext_tag {
                background-color: #dbeafe;
                border: 1px solid #3b82f6;
                border-radius: 6px;
            }
            QFrame#ext_tag:hover {
                background-color: #bfdbfe;
            }
            QLabel#tag_text, QLabel#ext_tag_text {
                color: #1e1b4b;
            }
            QPushButton#tag_close_btn {
                background: transparent;
                border: none;
                color: #4338ca;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton#tag_close_btn:hover {
                background-color: #ef4444;
                color: #ffffff;
            }
            QLabel#drop_zone {
                border: 2px dashed #4f46e5;
                border-radius: 8px;
                background-color: #eef2ff;
                color: #3730a3;
                font-weight: bold;
                padding: 24px;
            }
            QLabel#drop_zone:hover {
                background-color: #e0e7ff;
            }
        """
        final_style = base_style.replace("__CHK_ICON__", self.chk_icon).replace("__RDO_ICON__", self.rdo_icon)
        self.setStyleSheet(final_style)

    # --- EXTENSION TAGS MANAGEMENT (YOUTUBE TAG STYLE) ---
    def add_extension_tag_from_input(self):
        text = self.txt_ext_input.text().strip().lower()
        if not text:
            return

        for part in re.split(r"[,;\s]+", text):
            cleaned = part.strip()
            if cleaned:
                if not cleaned.startswith("."):
                    cleaned = "." + cleaned
                if cleaned not in self.extension_tags:
                    self.extension_tags.append(cleaned)

        self.txt_ext_input.clear()
        self.refresh_extension_tag_container()
        self.save_settings()

    def toggle_extension_tag(self, ext: str):
        clean = ext.strip().lower()
        if not clean.startswith("."):
            clean = "." + clean
        if clean in self.extension_tags:
            self.extension_tags.remove(clean)
        else:
            self.extension_tags.append(clean)
        self.refresh_extension_tag_container()
        self.save_settings()

    def remove_extension_tag(self, ext: str):
        if ext in self.extension_tags:
            self.extension_tags.remove(ext)
            self.refresh_extension_tag_container()
            self.save_settings()

    def add_all_common_extensions(self):
        for ext in COMMON_EXTENSIONS:
            if ext not in self.extension_tags:
                self.extension_tags.append(ext)
        self.refresh_extension_tag_container()
        self.save_settings()

    def clear_all_extension_tags(self):
        self.extension_tags.clear()
        self.refresh_extension_tag_container()
        self.save_settings()

    def refresh_extension_tag_container(self):
        while self.ext_tag_container_layout.count():
            item = self.ext_tag_container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for ext in self.extension_tags:
            chip = ExtensionTagChip(ext, self.ext_tag_container)
            chip.deleted.connect(self.remove_extension_tag)
            self.ext_tag_container_layout.addWidget(chip)

    # --- SNIPPET / TAG MANAGEMENT ---
    def paste_snippet_from_clipboard(self):
        text = QApplication.clipboard().text()
        if not text.strip():
            QMessageBox.warning(self, self.t("settings_title"), self.t("warn_snippets_empty"))
            return

        idx = len(self.snippets) + 1
        rec_name = recommend_filename(text, idx)

        name, ok = QInputDialog.getText(
            self,
            self.t("snippet_prompt_title"),
            self.t("snippet_prompt_msg"),
            QLineEdit.EchoMode.Normal,
            rec_name
        )

        if ok and name.strip():
            final_name = name.strip()
            existing_names = [s["name"] for s in self.snippets]
            if final_name in existing_names:
                base, ext = os.path.splitext(final_name)
                final_name = f"{base}_{idx}{ext}"

            self.add_snippet_tag(final_name, text)
            self.save_settings()
            self.log(self.t("log_snippet_added").format(final_name))

    def add_manual_snippet_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.t("manual_dialog_title"))
        dialog.resize(650, 450)
        vbox = QVBoxLayout(dialog)

        vbox.addWidget(QLabel(self.t("manual_name_label")))
        name_edit = QLineEdit(f"script_{len(self.snippets) + 1}.py")
        vbox.addWidget(name_edit)

        vbox.addWidget(QLabel(self.t("manual_code_label")))
        code_edit = QTextEdit()
        code_edit.setPlaceholderText(self.t("manual_code_placeholder"))
        vbox.addWidget(code_edit)

        btn_box = QHBoxLayout()
        btn_ok = QPushButton(self.t("btn_continue"))
        btn_ok.setObjectName("primary_btn")
        btn_cancel = QPushButton(self.t("btn_cancel"))
        btn_box.addStretch()
        btn_box.addWidget(btn_ok)
        btn_box.addWidget(btn_cancel)
        vbox.addLayout(btn_box)

        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        if dialog.exec() and code_edit.toPlainText().strip() and name_edit.text().strip():
            self.add_snippet_tag(name_edit.text().strip(), code_edit.toPlainText())
            self.save_settings()
            self.log(self.t("log_snippet_added").format(name_edit.text().strip()))

    def add_snippet_tag(self, name: str, content: str):
        self.snippets.append({"name": name, "content": content})
        self.refresh_tag_container()

    def remove_snippet_tag(self, filename: str):
        self.snippets = [s for s in self.snippets if s["name"] != filename]
        self.refresh_tag_container()
        self.save_settings()
        self.log(self.t("log_snippet_removed").format(filename))

    def clear_all_snippets(self):
        if not self.snippets:
            return
        self.snippets.clear()
        self.refresh_tag_container()
        self.save_settings()
        self.log(self.t("log_snippets_cleared"))

    def refresh_tag_container(self):
        while self.tag_container_layout.count():
            item = self.tag_container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for s in self.snippets:
            chip = SnippetTagChip(s["name"], s["content"], self.tag_container)
            chip.deleted.connect(self.remove_snippet_tag)
            self.tag_container_layout.addWidget(chip)

        self.lbl_snippet_count.setText(self.t("lbl_snippet_count").format(len(self.snippets)))

    # --- PERSISTENT SETTINGS AUTO-SAVE & RESTORE ---
    def schedule_save_settings(self):
        self.autosave_timer.start(350)

    def save_settings(self):
        try:
            current_mode = "folder"
            if self.rdo_drop.isChecked():
                current_mode = "drop"
            elif self.rdo_snippet.isChecked():
                current_mode = "snippet"

            data = {
                "version": APP_VERSION,
                "language": self.language,
                "theme_mode": self.theme_mode,
                "input_mode": current_mode,
                "folder_path": self.txt_folder_path.text(),
                "dropped_files": self.dropped_files,
                "snippets": self.snippets,
                "extension_tags": self.extension_tags,
                "search_subfolders": self.chk_subfolders.isChecked(),
                "show_tree": self.chk_tree.isChecked(),
                "header_summary": self.chk_header_summary.isChecked(),
                "output_format": "md" if self.rdo_md.isChecked() else "txt",
                "part_count": self.num_parts.value(),
                "clipboard_mode": self.cmb_clipboard.currentIndex(),
                "output_path": self.txt_output_path.text()
            }
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            self.apply_theme_mode("dark")
            return
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.language = data.get("language", "en")
            self.theme_mode = data.get("theme_mode", "dark")

            self.rdo_folder.blockSignals(True)
            self.rdo_drop.blockSignals(True)
            self.rdo_snippet.blockSignals(True)
            self.txt_folder_path.blockSignals(True)
            self.chk_subfolders.blockSignals(True)
            self.chk_tree.blockSignals(True)
            self.chk_header_summary.blockSignals(True)
            self.rdo_txt.blockSignals(True)
            self.rdo_md.blockSignals(True)
            self.num_parts.blockSignals(True)
            self.cmb_clipboard.blockSignals(True)
            self.txt_output_path.blockSignals(True)

            mode = data.get("input_mode", "folder")
            if mode == "drop":
                self.rdo_drop.setChecked(True)
            elif mode == "snippet":
                self.rdo_snippet.setChecked(True)
            else:
                self.rdo_folder.setChecked(True)
            self.toggle_input_mode()

            self.txt_folder_path.setText(data.get("folder_path", ""))
            self.dropped_files = data.get("dropped_files", [])
            self.snippets = data.get("snippets", [])
            self.refresh_tag_container()

            if "extension_tags" in data and isinstance(data["extension_tags"], list):
                self.extension_tags = data["extension_tags"]
            self.refresh_extension_tag_container()

            if "search_subfolders" in data:
                self.chk_subfolders.setChecked(data["search_subfolders"])
            if "show_tree" in data:
                self.chk_tree.setChecked(data["show_tree"])
            if "header_summary" in data:
                self.chk_header_summary.setChecked(data["header_summary"])

            if data.get("output_format") == "md":
                self.rdo_md.setChecked(True)
            else:
                self.rdo_txt.setChecked(True)

            if "part_count" in data:
                self.num_parts.setValue(data["part_count"])
            if "clipboard_mode" in data:
                self.cmb_clipboard.setCurrentIndex(data["clipboard_mode"])
            if "output_path" in data:
                self.txt_output_path.setText(data["output_path"])

            self.rdo_folder.blockSignals(False)
            self.rdo_drop.blockSignals(False)
            self.rdo_snippet.blockSignals(False)
            self.txt_folder_path.blockSignals(False)
            self.chk_subfolders.blockSignals(False)
            self.chk_tree.blockSignals(False)
            self.chk_header_summary.blockSignals(False)
            self.rdo_txt.blockSignals(False)
            self.rdo_md.blockSignals(False)
            self.num_parts.blockSignals(False)
            self.cmb_clipboard.blockSignals(False)
            self.txt_output_path.blockSignals(False)

            self.log(self.t("log_settings_loaded"))
        except Exception as ex:
            self.apply_theme_mode("dark")
            self.log(f"Config Load Error: {str(ex)}")

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

    def toggle_input_mode(self, *args):
        self.folder_panel.setVisible(self.rdo_folder.isChecked())
        self.drop_panel.setVisible(self.rdo_drop.isChecked())
        self.snippet_panel.setVisible(self.rdo_snippet.isChecked())

    def browse_folder(self, *args):
        current_text = self.txt_folder_path.text().strip()
        if current_text and os.path.isdir(current_text):
            initial_dir = current_text
        elif current_text and os.path.isdir(os.path.dirname(current_text)):
            initial_dir = os.path.dirname(current_text)
        else:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            initial_dir = desktop if os.path.exists(desktop) else os.path.expanduser("~")

        folder = QFileDialog.getExistingDirectory(self, self.t("btn_browse_folder"), initial_dir)
        if folder:
            self.txt_folder_path.setText(folder)
            default_out = os.path.join(folder, "combined_output.txt" if self.rdo_txt.isChecked() else "combined_output.md")
            self.txt_output_path.setText(default_out)
            self.save_settings()
            self.log(self.t("log_folder_browsed").format(folder))

    def browse_output(self, *args):
        current_text = self.txt_output_path.text().strip()
        if current_text and os.path.isdir(os.path.dirname(current_text)):
            initial_dir = current_text
        else:
            folder_text = self.txt_folder_path.text().strip()
            if folder_text and os.path.isdir(folder_text):
                initial_dir = os.path.join(folder_text, "combined_output.txt" if self.rdo_txt.isChecked() else "combined_output.md")
            else:
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                initial_dir = os.path.join(desktop if os.path.exists(desktop) else os.path.expanduser("~"), "combined_output.txt")

        ext_filter = "Text Files (*.txt);;All Files (*.*)" if self.rdo_txt.isChecked() else "Markdown Files (*.md);;All Files (*.*)"
        file_path, _ = QFileDialog.getSaveFileName(self, self.t("btn_browse_output"), initial_dir, ext_filter)
        if file_path:
            self.txt_output_path.setText(file_path)
            self.save_settings()

    def handle_files_dropped(self, dropped_paths: list[str]):
        allowed_exts = set(self.extension_tags)
        added_files = []

        for path in dropped_paths:
            if os.path.isfile(path):
                if not allowed_exts or os.path.splitext(path)[1].lower() in allowed_exts:
                    if path not in self.dropped_files and path not in added_files:
                        added_files.append(path)
            elif os.path.isdir(path):
                folder_matches = 0
                for root, _, filenames in os.walk(path):
                    for fn in filenames:
                        full_p = os.path.join(root, fn)
                        if not allowed_exts or os.path.splitext(fn)[1].lower() in allowed_exts:
                            if full_p not in self.dropped_files and full_p not in added_files:
                                added_files.append(full_p)
                                folder_matches += 1
                self.log(self.t("log_folder_dropped").format(os.path.basename(path), folder_matches))

        self.dropped_files.extend(added_files)
        self.lbl_dropped_count.setText(self.t("lbl_dropped_count").format(len(self.dropped_files)))
        self.log(self.t("log_files_dropped").format(len(added_files), len(self.dropped_files)))
        self.save_settings()

    def clear_dropped_files(self, *args):
        self.dropped_files.clear()
        self.lbl_dropped_count.setText(self.t("lbl_dropped_count").format(0))
        self.log(self.t("log_drop_cleared"))
        self.save_settings()

    def log(self, message: str):
        time_stamp = datetime.now().strftime("%H:%M:%S")
        self.txt_log.append(f"[{time_stamp}] {message}")

    def get_source_files(self) -> tuple[str, list[str]]:
        allowed_exts = set(self.extension_tags)

        if self.rdo_folder.isChecked():
            root_dir = self.txt_folder_path.text().strip()
            if not root_dir or not os.path.exists(root_dir):
                QMessageBox.warning(self, self.t("settings_title"), self.t("warn_folder_invalid"))
                return "", []

            matched = []
            if self.chk_subfolders.isChecked():
                for root, _, files in os.walk(root_dir):
                    for fn in files:
                        if not allowed_exts or os.path.splitext(fn)[1].lower() in allowed_exts:
                            matched.append(os.path.join(root, fn))
            else:
                for fn in os.listdir(root_dir):
                    full = os.path.join(root_dir, fn)
                    if os.path.isfile(full) and (not allowed_exts or os.path.splitext(fn)[1].lower() in allowed_exts):
                        matched.append(full)
            return root_dir, matched

        elif self.rdo_drop.isChecked():
            if not self.dropped_files:
                QMessageBox.warning(self, self.t("settings_title"), self.t("warn_drop_empty"))
                return "", []
            matched = [f for f in self.dropped_files if (not allowed_exts or os.path.splitext(f)[1].lower() in allowed_exts)]
            common_root = os.path.commonpath(matched) if matched else ""
            return common_root, matched

        else:
            if not self.snippets:
                QMessageBox.warning(self, self.t("settings_title"), self.t("warn_snippets_empty"))
                return "", []

            os.makedirs(SNIPPET_CACHE_DIR, exist_ok=True)
            matched = []
            for item in self.snippets:
                file_name = item["name"]
                full_path = os.path.join(SNIPPET_CACHE_DIR, file_name)
                with open(full_path, "w", encoding="utf-8", errors="replace") as sf:
                    sf.write(item["content"])
                matched.append(full_path)

            return SNIPPET_CACHE_DIR, matched

    def build_tree_structure(self, root_dir: str, file_list: list[str]) -> str:
        root_title = "Pasted Snippets" if self.rdo_snippet.isChecked() else (root_dir if root_dir else "Files")
        lines = ["[Root] " + root_title]
        rel_paths = sorted([os.path.relpath(f, root_dir) if root_dir else os.path.basename(f) for f in file_list])

        tree = {}
        for path in rel_paths:
            parts = path.split(os.sep)
            curr = tree
            for part in parts:
                curr = curr.setdefault(part, {})

        def recurse(node, prefix=""):
            keys = list(node.keys())
            for i, key in enumerate(keys):
                is_last = (i == len(keys) - 1)
                connector = "└── " if is_last else "├── "
                lines.append(prefix + connector + key)
                recurse(node[key], prefix + ("    " if is_last else "│   "))

        recurse(tree)
        return "\n".join(lines)

    def save_tree_only(self, *args):
        root_dir, matched = self.get_source_files()
        if not matched:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, self.t("btn_save_tree"), "file_tree.txt", "Text Files (*.txt)")
        if not save_path:
            return

        tree_str = self.build_tree_structure(root_dir, matched)
        header_lines = [
            "// ================================================================================",
            "//     FILE TREE REPORT",
            f"//     Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"//     Root      : {root_dir}",
            f"//     Total     : {len(matched)} file(s)",
            "// ================================================================================",
            "",
            tree_str,
            "",
            "// End of Tree"
        ]
        with open(save_path, "w", encoding="utf-8") as f:
            f.write("\n".join(header_lines))

        self.log(f"Tree saved to '{save_path}'")
        QMessageBox.information(self, self.t("settings_title"), self.t("msg_tree_success"))

    def combine_files(self, *args):
        root_dir, matched = self.get_source_files()
        if not matched:
            return

        dialog = FileSelectionDialog(matched, self.language, self)
        if not dialog.exec():
            return

        selected = dialog.selected_files
        if not selected:
            QMessageBox.warning(self, self.t("settings_title"), self.t("warn_select_empty"))
            return

        output_file = self.txt_output_path.text().strip()
        if not output_file:
            QMessageBox.warning(self, self.t("settings_title"), self.t("warn_output_empty"))
            return

        parts_count = self.num_parts.value()
        is_md = self.rdo_md.isChecked()
        self.progress_bar.setMaximum(len(selected))
        self.progress_bar.setValue(0)

        chunks = [[] for _ in range(parts_count)]
        for idx, fpath in enumerate(selected):
            chunks[idx % parts_count].append(fpath)

        base_out_name, ext = os.path.splitext(output_file)
        if not ext:
            ext = ".md" if is_md else ".txt"

        total_bytes = sum(os.path.getsize(f) for f in selected if os.path.exists(f))
        folders_processed = sorted(list(set(os.path.dirname(f) for f in selected)))

        first_part_content = ""
        created_output_files = []

        for p_idx, chunk in enumerate(chunks):
            current_part = p_idx + 1
            cur_out_path = f"{base_out_name}_part{current_part}{ext}" if parts_count > 1 else f"{base_out_name}{ext}"

            content_blocks = []
            for fpath in chunk:
                rel = os.path.relpath(fpath, root_dir) if root_dir else os.path.basename(fpath)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as file_handle:
                        body = file_handle.read()
                except Exception as ex:
                    body = f"[ERROR: Unable to read file - {str(ex)}]"

                if is_md:
                    hint = LANGUAGE_HINTS.get(os.path.splitext(fpath)[1].lower(), "")
                    block_lines = [
                        f"### `{rel}`",
                        f"```{hint}",
                        body,
                        "```",
                        ""
                    ]
                    content_blocks.append("\n".join(block_lines))
                else:
                    block_lines = [
                        f"// Relative Path: {rel}",
                        "// --------------------------------------------------------------------------------",
                        body,
                        ""
                    ]
                    content_blocks.append("\n".join(block_lines))
                self.progress_bar.setValue(self.progress_bar.value() + 1)

            tree_text = self.build_tree_structure(root_dir, chunk) if self.chk_tree.isChecked() else ""
            report_text = self.render_report(
                is_md=is_md,
                root_dir=root_dir,
                total_files=len(selected),
                total_folders=len(folders_processed),
                total_size_str=format_file_size(total_bytes),
                current_part=current_part,
                total_parts=parts_count,
                tree_structure=tree_text,
                file_blocks="\n".join(content_blocks),
                all_folders=folders_processed,
                output_name=os.path.basename(cur_out_path)
            )

            if p_idx == 0:
                first_part_content = report_text

            with open(cur_out_path, "w", encoding="utf-8") as out_f:
                out_f.write(report_text)

            created_output_files.append(cur_out_path)

        self.log(self.t("log_combine_done").format(len(selected), parts_count))

        clipboard_mode = self.cmb_clipboard.currentIndex()
        if clipboard_mode == 1 and first_part_content:
            QApplication.clipboard().setText(first_part_content)
            self.log(self.t("log_content_copied"))
        elif clipboard_mode == 2 and created_output_files:
            mime = QMimeData()
            file_urls = [QUrl.fromLocalFile(os.path.abspath(f)) for f in created_output_files if os.path.exists(f)]
            mime.setUrls(file_urls)
            mime.setText("\n".join([os.path.abspath(f) for f in created_output_files if os.path.exists(f)]))
            QApplication.clipboard().setMimeData(mime)
            self.log(self.t("log_file_copied").format(len(file_urls)))

        self.save_settings()
        QMessageBox.information(self, self.t("settings_title"), self.t("msg_combine_success"))

    def render_report(self, is_md: bool, root_dir: str, total_files: int, total_folders: int,
                      total_size_str: str, current_part: int, total_parts: int, tree_structure: str,
                      file_blocks: str, all_folders: list[str], output_name: str) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exts_display = "; ".join(self.extension_tags) if self.extension_tags else "All Files"
        source_display = "Pasted Snippets / Tags" if self.rdo_snippet.isChecked() else root_dir

        if is_md:
            sections = []
            if self.chk_header_summary.isChecked():
                header_lines = [
                    "# Combined Files Report",
                    "",
                    "| Key | Value |",
                    "| --- | --- |",
                    f"| Generated | {now} |",
                    f"| Source Folder | `{source_display}` |",
                    f"| Extensions | `{exts_display}` |",
                    f"| Total Files | {total_files} |",
                    f"| Total Folders | {total_folders} |",
                    f"| Part | {current_part} of {total_parts} |",
                    ""
                ]
                sections.append("\n".join(header_lines))

            if tree_structure:
                tree_lines = [
                    "## Folder & File Structure",
                    "```",
                    tree_structure,
                    "```",
                    ""
                ]
                sections.append("\n".join(tree_lines))

            sections.append(f"## File Contents\n\n{file_blocks}\n")

            if self.chk_header_summary.isChecked():
                folder_items = "\n".join([f"- `{f}`" for f in all_folders])
                summary_lines = [
                    "## Summary",
                    "",
                    f"| Total Files Processed | {total_files} |",
                    f"| Total Size | {total_size_str} |",
                    f"| Extension Filter | `{exts_display}` |",
                    f"| Output File | `{output_name}` |",
                    "",
                    "### Folders processed:",
                    folder_items,
                    ""
                ]
                sections.append("\n".join(summary_lines))

            return "\n".join(sections)
        else:
            border = "// " + ("#" * 78)
            div = "// " + ("-" * 78)
            sections = []

            if self.chk_header_summary.isChecked():
                header_lines = [
                    border,
                    "// #                                COMBINED FILES REPORT                          #",
                    border,
                    f"// Generated             : {now}",
                    f"// Source Folder         : {source_display}",
                    f"// File Extensions       : {exts_display}",
                    f"// Total Files           : {total_files}",
                    f"// Total Folders         : {total_folders}",
                    f"// Part                  : {current_part} of {total_parts}",
                    border,
                    ""
                ]
                sections.append("\n".join(header_lines))

            if tree_structure:
                tree_lines = [
                    "// FOLDER & FILE STRUCTURE",
                    div,
                    tree_structure,
                    ""
                ]
                sections.append("\n".join(tree_lines))

            sections.append(
                border + "\n// #                                      FILE CONTENTS                            #\n" + border + "\n\n" + file_blocks + "\n"
            )

            if self.chk_header_summary.isChecked():
                folder_lines = "\n".join([f"//   - {f}" for f in all_folders])
                summary_lines = [
                    border,
                    "// #                                         SUMMARY                               #",
                    border,
                    f"// Total Files Processed   : {total_files}",
                    f"// Total Folders           : {total_folders}",
                    f"// Total Size              : {total_size_str}",
                    f"// Extension Filter        : {exts_display}",
                    f"// Source Folder           : {source_display}",
                    f"// Output File             : {output_name}",
                    f"// Generated               : {now}",
                    "// List of all processed folders:",
                    folder_lines,
                    border,
                    ""
                ]
                sections.append("\n".join(summary_lines))

            return "\n".join(sections)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileCombinerApp()
    window.show()
    sys.exit(app.exec())