import os
import shutil
import textwrap
import yaml
import re
import os

from rich.console import Console
from rich.table import Table

# Constants
LIBRARY_DIR = "library"
SAVE_FILE = "progress.yaml"
CONFIG_FILE = "config.yaml"
CHAPTER_REGEX = r"^\s*第[一二两三四五六七八九十○零百千0-9１２３４５６７８９０]{1,12}(章|节|節|回)"
CHAPTER_PATTERN = re.compile(CHAPTER_REGEX)
CMD_CLEAR = "cls" if os.name == "nt" else "clear"

# Rich console
console = Console()

# Global variable for translations and config
translations = {}
config = {}

def load_config():
    global config
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        else:
            # Create default config if it doesn't exist
            config = {
                'default_language': 'zh-cn',
                'last_read_book': None,
                'last_read_progress': {},
                'bookmarks': {}
            }
            save_config()
    except Exception as e:
        print(f"Warning: Failed to load config file {CONFIG_FILE}: {e}")

def save_config():
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(config, f)
    except Exception as e:
        print(f"Warning: Failed to save config file {CONFIG_FILE}: {e}")

def load_language(lang_code=None):
    global translations
    if lang_code is None:
        lang_code = config.get('default_language', 'zh-cn')

    translations_file = os.path.join("lang", "translations.yaml")
    try:
        with open(translations_file, "r", encoding="utf-8") as f:
            all_translations = yaml.safe_load(f)
            translations = all_translations
    except FileNotFoundError:
        print(f"Warning: Translations file '{translations_file}' not found. Cannot load any language.")
        translations = {}
    except yaml.YAMLError:
        print(f"Warning: Error decoding YAML from '{translations_file}'. Cannot load any language.")
        translations = {}

def get_text(key, **kwargs):
    lang_code = config.get('default_language', 'zh-cn')
    # Try to get the translation for the current language, fallback to English, then to the key itself
    translated_text = translations.get(key, {}).get(lang_code, translations.get(key, {}).get('en', key))
    return translated_text.format(**kwargs)

# Output functions
def print_error(msg) -> None:
    console.print(f"[bold red]{get_text('error_prefix')} {msg}[/bold red]")

def print_warning(msg) -> None:
    console.print(f"[yellow]{get_text('warning_prefix')} {msg}[/yellow]")

def print_info(msg) -> None:
    console.print(f"[green]{get_text('info_prefix')} {msg}[/green]")

# Load config and language on startup
load_config()
load_language()

def get_terminal_size() -> tuple[int, int]:
    try:
        size = shutil.get_terminal_size(fallback=(80, 24))
        return size.columns - 4, size.lines - 6
    except Exception as e:
        raise RuntimeError(f"{get_text('cannot_get_terminal_size')}{str(e)}")

def load_progress() -> dict:
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}
    except Exception as e:
        print_error(f"{get_text('load_progress_failed')}{e}")
        return {}

def save_progress(progress) -> None:
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(progress, f)
    except Exception as e:
        print_error(f"{get_text('save_progress_failed')}{e}")

def list_books() -> list:
    try:
        if not os.path.exists(LIBRARY_DIR):
            os.makedirs(LIBRARY_DIR)
        return [f for f in os.listdir(LIBRARY_DIR) if f.endswith(".txt")]
    except Exception as e:
        print_error(f"{get_text('read_library_failed')}{e}")
        return []

def generate_pages(content, width, height) -> tuple:
    if not isinstance(content, list):
        raise ValueError(get_text('content_must_be_list'))
    if not all(isinstance(line, str) for line in content):
        raise ValueError(get_text('content_elements_must_be_string'))

    pages, starts, current_lines, line_count, total_lines = [], [], [], 0, 0
    for line in content:
        wrapped_lines = textwrap.wrap(line, width) or [""]
        for wrapped_line in wrapped_lines:
            if line_count >= height:
                pages.append("\n".join(current_lines))
                starts.append(total_lines - line_count)
                current_lines, line_count = [], 0
            current_lines.append(wrapped_line)
            line_count += 1
            total_lines += 1
    if current_lines:
        pages.append("\n".join(current_lines))
        starts.append(total_lines - line_count)
    return pages, starts

def extract_chapters(content_lines, page_starts):
    if not content_lines or not page_starts:
        raise ValueError(get_text('chapter_extract_params_empty'))
    chapters = []
    for i, line in enumerate(content_lines):
        if CHAPTER_PATTERN.match(line):
            current_page = 0
            for page_num, start in enumerate(page_starts):
                if i >= start:
                    current_page = page_num
            chapters.append((line.strip(), current_page))
    return chapters

def show_chapter_menu(chapters) -> None:
    try:
        term_width, term_height = get_terminal_size()
    except Exception as e:
        print_error(str(e))
        return

    page_size = max(term_height - 5, 5)
    total = len(chapters)
    page = 0

    while True:
        os.system(CMD_CLEAR)
        table = Table(title=get_text('chapter_menu_title', total=total, current=page + 1, total_pages=(total - 1)//page_size + 1))
        table.add_column(get_text('chapter_menu_col_id'), justify="right", no_wrap=True, max_width=6)
        table.add_column(get_text('chapter_menu_col_title'), justify="left", max_width=term_width - 20)
        table.add_column(get_text('chapter_menu_col_page'), justify="right", no_wrap=True, max_width=6)

        for idx in range(page * page_size, min((page + 1) * page_size, total)):
            title, pnum = chapters[idx]
            table.add_row(str(idx + 1), title, str(pnum + 1))

        console.print(table)
        print(f">>> {get_text('chapter_menu_prompt')}")

        choice = input(">>> ").strip().lower()
        if choice in ("n", "") and (page + 1) * page_size < total:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "s":
            keyword = input(f">>> {get_text('chapter_menu_input_keyword')}").strip()
            if keyword:
                filtered = [(t, p) for t, p in chapters if keyword in t]
                if filtered:
                    show_chapter_menu(filtered)
                else:
                    print_warning(get_text('chapter_not_found'))
                    input(f">>> {get_text('press_enter_to_continue')}")
        elif choice == "q":
            break

def read_book(file_path, progress_data):
    abs_path = os.path.abspath(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().splitlines()
    except Exception as e:
        print_error(f"{get_text('read_file_failed')}{e}")
        return

    try:
        width, height = get_terminal_size()
        pages, page_starts = generate_pages(content, width, height)
        total_pages = len(pages)
        chapters = extract_chapters(content, page_starts)
    except Exception as e:
        print_error(f"{get_text('content_process_failed')}{e}")
        return

    book_state = progress_data.get(abs_path, {})
    read_line = book_state.get("line", 0)
    current_page = next((i for i, start in enumerate(page_starts) if start <= read_line), 0)

    while True:
        os.system(CMD_CLEAR)
        print(get_text('book_title_page_info', book_name=os.path.basename(file_path), current_page=current_page + 1, total_pages=total_pages))
        print(pages[current_page])
        print(f"\n>>> {get_text('main_menu_prompt')}")

        cmd = input(">>> ").strip().lower()
        if cmd in ("n", "") and current_page < total_pages - 1:
            current_page += 1
        elif cmd == "p" and current_page > 0:
            current_page -= 1
        elif cmd == "g":
            try:
                page_num = int(input(f">>> {get_text('jump_to_page_prompt')}")) - 1
                if 0 <= page_num < total_pages:
                    current_page = page_num
            except ValueError:
                print_warning(get_text('invalid_page_number'))
        elif cmd == "m":
            if chapters:
                show_chapter_menu(chapters)
            else:
                print_warning(get_text('no_chapters_found'))
                input(f">>> {get_text('press_enter_to_continue')}")
        elif cmd == "j":
            if chapters:
                try:
                    chapter_id = int(input(f">>> {get_text('enter_chapter_number_prompt')}"))
                    if 1 <= chapter_id <= len(chapters):
                        current_page = chapters[chapter_id - 1][1]
                    else:
                        print_warning(get_text('invalid_chapter_number'))
                except ValueError:
                    print_warning(get_text('invalid_chapter_number'))
            else:
                print_warning(get_text('no_chapters_found'))
                input(f">>> {get_text('press_enter_to_continue')}")
        elif cmd == "b":
            if chapters:
                bookmark_line = page_starts[current_page]
                title = next((t for t, p in chapters if p == current_page), get_text('unnamed_chapter'))
                progress_data[abs_path] = {"line": bookmark_line, "bookmark": title}
                save_progress(progress_data)
                print_info(get_text('chapter_marked', title=title))
                input(f">>> {get_text('press_enter_to_continue')}")
            else:
                print_warning(get_text('no_chapter_to_mark'))
                input(f">>> {get_text('press_enter_to_continue')}")
        elif cmd == "c":
            if abs_path in progress_data:
                del progress_data[abs_path]
                save_progress(progress_data)
                print_info(get_text('current_book_progress_cleared'))
                input(f">>> {get_text('press_enter_to_continue')}")
            else:
                print_info(get_text('no_progress_to_clear'))
                input(f">>> {get_text('press_enter_to_continue')}")
        elif cmd == "q":
            progress_data[abs_path] = {"line": page_starts[current_page]}
            save_progress(progress_data)
            print_info(get_text('progress_saved'))
            break
        else:
            print_warning(get_text('invalid_command_read_book'))

def show_settings_menu():
    while True:
        os.system(CMD_CLEAR)
        print(get_text('settings_menu_title'))
        print(get_text('current_language_setting', lang=config.get('default_language', 'zh-cn')))
        print(get_text('settings_menu_prompt'))
        choice = input(">>> ").strip().lower()

        if choice == '1':
            print(get_text('available_languages'))
            print("  zh-cn: 简体中文")
            print("  en: English")
            print("  jp: 日本語")
            new_lang = input(f">>> {get_text('enter_new_language_code')}").strip().lower()
            if new_lang in ['zh-cn', 'en', 'jp']:
                config['default_language'] = new_lang
                try:
                    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                        yaml.safe_dump(config, f)
                    load_language(new_lang)
                    print_info(get_text('language_set_successfully', lang=new_lang))
                except Exception as e:
                    print_error(f"{get_text('failed_to_save_config')}{e}")
            else:
                print_warning(get_text('invalid_language_code'))
            input(f">>> {get_text('press_enter_to_continue')}")
        elif choice == 'q':
            break
        else:
            print_warning(get_text('invalid_command'))
            input(f">>> {get_text('press_enter_to_continue')}")

def main() -> None:
    os.system(CMD_CLEAR)
    print(get_text('welcome_message'))

    books = list_books()
    if not books:
        print(get_text('no_books_found_message'))
        return

    progress = load_progress()
    last_file = next((path for path in progress if os.path.exists(path)), None)

    if last_file:
        print(get_text('last_read_book_info', book_name=os.path.basename(last_file)))
        if input(f">>> {get_text('continue_reading_prompt')} ").strip().lower() != "n":
            read_book(last_file, progress)
            return

    while True:
        os.system(CMD_CLEAR)
        table = Table(title=get_text('available_books_title'))
        table.add_column(get_text('book_list_col_id'), justify="right", no_wrap=True, max_width=6)
        table.add_column(get_text('book_list_col_title'), justify="left")

        for i, book in enumerate(books):
            table.add_row(str(i + 1), book)
        console.print(table)
        
        print(get_text('settings_menu_option'))

        choice = input(f">>> {get_text('enter_main_menu_choice')}").strip().lower()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(books):
                file_path = os.path.join(LIBRARY_DIR, books[choice - 1])
                read_book(file_path, progress)
            else:
                print_warning(get_text('invalid_book_number_range'))
        elif choice == 's':
            show_settings_menu()
        elif choice == 'q':
            break
        else:
            print_warning(get_text('invalid_command'))
        input(f">>> {get_text('press_enter_to_continue')}")

if __name__ == "__main__":
    main()
