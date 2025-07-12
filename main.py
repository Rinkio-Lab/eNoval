import os
import shutil
import textwrap
import yaml
import re

from rich.console import Console
from rich.table import Table

# 常量定义
LIBRARY_DIR = "library"
SAVE_FILE = "progress.yaml"
CHAPTER_REGEX = r"^\s*第[一二两三四五六七八九十○零百千0-9１２３４５６７８９０]{1,12}(章|节|節|回)"
CHAPTER_PATTERN = re.compile(CHAPTER_REGEX)
CMD_CLEAR = "cls" if os.name == "nt" else "clear"

# rich 控制台
console = Console()

# 输出函数
def print_error(msg) -> None:
    console.print(f"[bold red][ERROR] {msg}[/bold red]")

def print_warning(msg) -> None:
    console.print(f"[yellow][WARNING] {msg}[/yellow]")

def print_info(msg) -> None:
    console.print(f"[green][INFO] {msg}[/green]")

def get_terminal_size() -> tuple[int, int]:
    try:
        size = shutil.get_terminal_size(fallback=(80, 24))
        return size.columns - 4, size.lines - 6
    except Exception as e:
        raise RuntimeError(f"无法获取终端尺寸：{str(e)}")

def load_progress() -> dict:
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}
    except Exception as e:
        print_error(f"加载阅读进度失败：{e}")
        return {}

def save_progress(progress) -> None:
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(progress, f)
    except Exception as e:
        print_error(f"保存阅读进度失败：{e}")

def list_books() -> list:
    try:
        if not os.path.exists(LIBRARY_DIR):
            os.makedirs(LIBRARY_DIR)
        return [f for f in os.listdir(LIBRARY_DIR) if f.endswith(".txt")]
    except Exception as e:
        print_error(f"读取 library 目录失败：{e}")
        return []

def generate_pages(content, width, height) -> tuple:
    if not isinstance(content, list):
        raise ValueError("内容必须是字符串列表。")
    if not all(isinstance(line, str) for line in content):
        raise ValueError("内容中所有元素都必须是字符串。")

    pages, starts, current, line_count, total = [], [], [], 0, 0
    for line in content:
        wrapped = textwrap.wrap(line, width) or [""]
        for wline in wrapped:
            if line_count >= height:
                pages.append("\n".join(current))
                starts.append(total - line_count)
                current, line_count = [], 0
            current.append(wline)
            line_count += 1
            total += 1
    if current:
        pages.append("\n".join(current))
        starts.append(total - line_count)
    return pages, starts

def extract_chapters(content_lines, page_starts):
    if not content_lines or not page_starts:
        raise ValueError("章节提取参数不能为空。")
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
        table = Table(title=f"章节目录 (共 {total} 章) - 第 {page + 1} / {(total - 1)//page_size + 1} 页")
        table.add_column("编号", justify="right", no_wrap=True, max_width=6)
        table.add_column("章节标题", justify="left", max_width=term_width - 20)
        table.add_column("页码", justify="right", no_wrap=True, max_width=6)

        for idx in range(page * page_size, min((page + 1) * page_size, total)):
            title, pnum = chapters[idx]
            table.add_row(str(idx + 1), title, str(pnum + 1))

        console.print(table)
        print(">>> [n]下一页 [p]上一页 [q]退出 [s]搜索")

        choice = input(">>> ").strip().lower()
        if choice in ("n", "") and (page + 1) * page_size < total:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "s":
            keyword = input(">>> 输入关键词：").strip()
            if keyword:
                filtered = [(t, p) for t, p in chapters if keyword in t]
                if filtered:
                    show_chapter_menu(filtered)
                else:
                    print_warning("未找到匹配章节。")
                    input(">>> 回车继续...")
        elif choice == "q":
            break

def read_book(file_path, progress_data):
    abs_path = os.path.abspath(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().splitlines()
    except Exception as e:
        print_error(f"读取文件失败：{e}")
        return

    try:
        width, height = get_terminal_size()
        pages, page_starts = generate_pages(content, width, height)
        total_pages = len(pages)
        chapters = extract_chapters(content, page_starts)
    except Exception as e:
        print_error(f"内容处理失败：{e}")
        return

    book_state = progress_data.get(abs_path, {})
    read_line = book_state.get("line", 0)
    current_page = next((i for i, start in enumerate(page_starts) if start <= read_line), 0)

    while True:
        os.system(CMD_CLEAR)
        print(f"📘 {os.path.basename(file_path)} — 第 {current_page + 1} / {total_pages} 页")
        print(pages[current_page])
        print("\n>>> [n]下一页 [p]上一页 [q]退出 [g]跳页 [m]目录 [j]跳章节 [c]清除进度 [b]章节书签")

        cmd = input(">>> ").strip().lower()
        if cmd in ("n", "") and current_page < total_pages - 1:
            current_page += 1
        elif cmd == "p" and current_page > 0:
            current_page -= 1
        elif cmd == "g":
            try:
                page_num = int(input(">>> 跳转到第几页？")) - 1
                if 0 <= page_num < total_pages:
                    current_page = page_num
            except ValueError:
                print_warning("请输入有效的页码。")
        elif cmd == "m":
            if chapters:
                show_chapter_menu(chapters)
            else:
                print_warning("未找到章节。")
                input(">>> 回车继续...")
        elif cmd == "j":
            if chapters:
                try:
                    chapter_id = int(input(">>> 请输入章节编号："))
                    if 1 <= chapter_id <= len(chapters):
                        current_page = chapters[chapter_id - 1][1]
                    else:
                        print_warning("无效编号。")
                except ValueError:
                    print_warning("请输入有效编号。")
            else:
                print_warning("未找到章节。")
                input(">>> 回车继续...")
        elif cmd == "b":
            if chapters:
                bookmark_line = page_starts[current_page]
                title = next((t for t, p in chapters if p == current_page), "未命名章节")
                progress_data[abs_path] = {"line": bookmark_line, "bookmark": title}
                save_progress(progress_data)
                print_info(f"已标记章节：{title}")
                input(">>> 回车继续...")
            else:
                print_warning("当前页无可标记章节。")
                input(">>> 回车继续...")
        elif cmd == "c":
            if abs_path in progress_data:
                del progress_data[abs_path]
                save_progress(progress_data)
                print_info("已清除当前书籍进度。")
                input(">>> 回车继续...")
        elif cmd == "q":
            progress_data[abs_path] = {"line": page_starts[current_page]}
            save_progress(progress_data)
            print_info("进度已保存，下次继续阅读！")
            break
        else:
            print_warning("无效命令。请输入 [n/p/q/g/m/j/c/b]")

def main() -> None:
    os.system(CMD_CLEAR)
    print("📚 欢迎使用终端小说阅读器！")

    books = list_books()
    if not books:
        print("请将小说（.txt）文件放入 library 文件夹中。")
        return

    progress = load_progress()
    last_file = next((path for path in progress if os.path.exists(path)), None)

    if last_file:
        print(f"\n📌 检测到上次阅读：{os.path.basename(last_file)}")
        if input(">>> 是否继续阅读？(Y/n) ").strip().lower() != "n":
            read_book(last_file, progress)
            return

    print("\n📂 可阅读的小说：")
    for i, book in enumerate(books):
        print(f"[{i + 1}] {book}")

    try:
        choice = int(input("\n>>> 请输入序号开始阅读："))
        if 1 <= choice <= len(books):
            file_path = os.path.join(LIBRARY_DIR, books[choice - 1])
            read_book(file_path, progress)
        else:
            print_warning("输入的序号超出范围。")
    except ValueError:
        print_warning("请输入有效的数字。")
    except Exception as e:
        print_error(f"发生了错误：{e}")

if __name__ == "__main__":
    main()
