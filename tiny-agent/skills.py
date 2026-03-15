import os
import warnings
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class SkillRecord:
    name: str
    description: str
    location: Path
    body: str


def discover_skills() -> dict[str, SkillRecord]:
    """Scan project-level and user-level skill directories for SKILL.md files."""
    skills: dict[str, SkillRecord] = {}
    search_dirs = [
        Path.home() / ".agents" / "skills",          # user-level (lower priority)
        Path.cwd() / ".agents" / "skills",            # project-level (higher priority)
    ]

    for base_dir in search_dirs:
        if not base_dir.is_dir():
            continue
        for child in sorted(base_dir.iterdir()):
            skill_file = child / "SKILL.md"
            if not child.is_dir() or not skill_file.exists():
                continue
            try:
                record = _parse_skill(skill_file)
                if not record.description:
                    warnings.warn(f"Skipping skill at {skill_file}: empty description")
                    continue
                skills[record.name] = record
            except Exception as e:
                warnings.warn(f"Error parsing {skill_file}: {e}")

    return skills


def _parse_skill(path: Path) -> SkillRecord:
    """Parse a SKILL.md file into a SkillRecord."""
    text = path.read_text()
    frontmatter = {}
    body = text

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()

    return SkillRecord(
        name=frontmatter.get("name", path.parent.name),
        description=frontmatter.get("description", ""),
        location=path.parent,
        body=body,
    )


def activate_skill(name: str, skills: dict[str, SkillRecord]) -> str:
    """Activate a skill by name and return its content."""
    record = skills.get(name)
    if not record:
        return f"Error: skill '{name}' not found. Available skills: {', '.join(skills.keys())}"

    # List bundled resource files (anything besides SKILL.md)
    resources = [
        f.name for f in record.location.iterdir()
        if f.is_file() and f.name != "SKILL.md"
    ]

    parts = [f'<skill_content name="{record.name}">']
    parts.append(f"Skill directory: {record.location}")
    if resources:
        parts.append(f"Bundled resources: {', '.join(resources)}")
    parts.append("")
    parts.append(record.body)
    parts.append("</skill_content>")
    return "\n".join(parts)
