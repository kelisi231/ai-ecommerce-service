import re

FAQ_MIN_PAIRS = 3
FAQ_MIN_QUESTION_RATION = 0.1
ARTICLE_MIN_HEADING = 3
LINE_MIN_COUNT = 10
LINE_MAX_AVERAGE_LENGTH = 100


QUESTION_PATTERN = re.compile(r"^问题：", re.MULTILINE)
FAQ_PAIR_PATTERN = re.compile(
    r"问题：.+?(?:？|\?)\n答案：.+?(?=\n问题：|$)",
    re.DOTALL,
)

ARTICLE_HEADING_PATTERN = re.compile(r"^第.+?(?:条|章)", re.MULTILINE)



def get_non_empty_text(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]

#正则模式在文本中无重叠匹配的总次数。
def count_matches(pattern: re.Pattern, text: str) -> int:
    return len(pattern.findall(text))


def is_faq(text: str) -> bool:
    lines = get_non_empty_text(text)
    if not lines:
        return False

    has_enough_pairs = count_matches(FAQ_PAIR_PATTERN, text) >= FAQ_MIN_PAIRS
    question_ratio = count_matches(QUESTION_PATTERN, text) / len(lines)
    return has_enough_pairs and question_ratio >= FAQ_MIN_QUESTION_RATION


def is_article(text: str) -> bool:
    return count_matches(ARTICLE_HEADING_PATTERN, text) >= ARTICLE_MIN_HEADING

def is_line_based(text: str) -> bool:
    lines = get_non_empty_text(text)
    if len(lines) < LINE_MIN_COUNT:
        return False
    average_length = sum(len(line) for line in lines) / len(lines)
    return average_length <= LINE_MAX_AVERAGE_LENGTH