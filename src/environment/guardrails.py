def truncate_observation(output: str, max_lines: int = 30, max_chars: int = 2000) -> str:
    if len(output.splitlines()) <= max_lines and len(output) <= max_chars:
        return output
    lines = output.splitlines()[:max_lines]
    summary = f"\n... (truncated {len(output.splitlines()) - max_lines} lines) ..."
    result = "\n".join(lines) + summary
    if len(result) > max_chars:
        result = result[:max_chars] + "... (truncated)"
    return result