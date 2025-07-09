import re
import logging
from collections import Counter
from typing import List, Tuple

logger = logging.getLogger(__name__)


ERROR_PATTERNS = [
    re.compile(r"Traceback \(.*?\)", re.DOTALL),
    re.compile(r"ERROR[: ]+(.*)")
]


def find_common_errors(log_lines: List[str], top_n: int = 3) -> List[Tuple[str, int]]:
    """Analyze log lines and return the most common error messages."""
    logger.info("Analyzing %d log lines", len(log_lines))
    errors = []
    for line in log_lines:
        for pattern in ERROR_PATTERNS:
            match = pattern.search(line)
            if match:
                # Use the entire matched message or group 1 if available
                msg = match.group(1) if match.groups() else match.group(0)
                errors.append(msg.strip())
                break
    counts = Counter(errors)
    common = counts.most_common(top_n)
    logger.info("Found %d unique errors", len(counts))
    return common

