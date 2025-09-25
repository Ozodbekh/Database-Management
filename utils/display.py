from config import TABLE_WIDTH, MENU_WIDTH, SYSTEM_NAME, SYSTEM_VERSION


def print_header(title, width=None):
    if width is None:
        width = TABLE_WIDTH

    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_subheader(title, width=None):
    if width is None:
        width = MENU_WIDTH

    print("\n" + "-" * width)
    print(title.center(width))
    print("-" * width)


def print_separator(width=None, char="-"):
    if width is None:
        width = TABLE_WIDTH

    print(char * width)


def print_table_header(headers, widths):
    header_line = ""
    for i, header in enumerate(headers):
        header_line += f"{header:<{widths[i]}} "

    print(header_line.rstrip())
    print_separator(sum(widths) + len(widths) - 1)


def print_table_row(values, widths):
    row_line = ""
    for i, value in enumerate(values):
        row_line += f"{str(value):<{widths[i]}} "

    print(row_line.rstrip())


def print_welcome():
    print("=" * 60)
    print(SYSTEM_NAME.center(60))
    print(f"Version {SYSTEM_VERSION}".center(60))
    print("=" * 60)


def print_menu_options(options, title="MENU"):
    print_subheader(title, MENU_WIDTH)

    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")


def print_user_info(user):
    print(f"Logged in as: {user.full_name} ({user.role.title()})")
    print(f"Phone: {user.phone_number}")
    if user.email:
        print(f"Email: {user.email}")


def print_success(message):
    print(f"\n✓ SUCCESS: {message}")


def print_error(message):
    print(f"\n✗ ERROR: {message}")


def print_warning(message):
    print(f"\n⚠ WARNING: {message}")


def print_info(message):
    print(f"\nℹ INFO: {message}")


def format_attendance_summary(summary_data):
    if not summary_data or summary_data[0] == 0:
        return "No attendance records"

    total, present, absent, late, percentage = summary_data
    return f"Total: {total}, Present: {present}, Absent: {absent}, Late: {late}, Percentage: {percentage}%"


def format_grade_summary(grade_data):
    if not grade_data or grade_data[0] == 0:
        return "No grades available"

    assignments, avg_percentage, total_obtained, total_possible = grade_data
    return f"Assignments: {assignments}, Average: {avg_percentage}%, Points: {total_obtained}/{total_possible}"


def print_stats_box(title, stats):
    max_width = max(len(title), max(len(f"{k}: {v}") for k, v in stats.items())) + 4

    print("\n" + "┌" + "─" * (max_width - 2) + "┐")
    print(f"│{title.center(max_width - 2)}│")
    print("├" + "─" * (max_width - 2) + "┤")

    for key, value in stats.items():
        line = f"{key}: {value}"
        print(f"│ {line:<{max_width - 4}} │")

    print("└" + "─" * (max_width - 2) + "┘")


def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\nPress Enter to continue...")


def print_loading(message="Loading"):
    import time
    import sys

    for i in range(3):
        sys.stdout.write(f"\r{message}{'.' * (i + 1)}")
        sys.stdout.flush()
        time.sleep(0.5)

    print()


def format_date_display(date_string):
    if not date_string:
        return "N/A"

    try:
        from datetime import datetime
        dt = datetime.strptime(date_string, '%Y-%m-%d')
        return dt.strftime('%B %d, %Y')
    except ValueError:
        return date_string


def truncate_text(text, max_length):
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length - 3] + "..."


def print_progress_bar(current, total, width=30):
    if total == 0:
        progress = 0
    else:
        progress = current / total

    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = int(progress * 100)

    print(f"\r[{bar}] {percentage}% ({current}/{total})", end="", flush=True)


def print_grade_distribution(grades):
    if not grades:
        print("No grades to display")
        return

    from utils.validation import get_grade_letter

    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}

    for grade in grades:
        letter = get_grade_letter(grade)
        grade_counts[letter] += 1

    print("\nGrade Distribution:")
    print("-" * 20)

    max_count = max(grade_counts.values()) if grade_counts.values() else 1

    for letter, count in grade_counts.items():
        if max_count > 0:
            bar_length = int((count / max_count) * 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            print(f"{letter}: [{bar}] {count}")
