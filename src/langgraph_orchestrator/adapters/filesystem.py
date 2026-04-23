from __future__ import annotations

from pathlib import Path

from langgraph_orchestrator.domain.models import ProjectSignals


class LocalWorkspaceInspector:
    def inspect(self, target_path: str) -> ProjectSignals:
        root = Path(target_path)
        return ProjectSignals(
            has_maven=(root / "pom.xml").exists(),
            has_gradle=(root / "build.gradle").exists() or (root / "build.gradle.kts").exists(),
            has_jib=self._has_jib(root),
            has_readme=(root / "README.md").exists(),
            has_changelog=(root / "CHANGELOG.md").exists(),
            has_obsidian_docs=(root / "docs" / "obsidian").exists(),
        )

    def _has_jib(self, root: Path) -> bool:
        pom = root / "pom.xml"
        if pom.exists() and "jib" in pom.read_text(encoding="utf-8", errors="ignore").lower():
            return True

        gradle_files = [root / "build.gradle", root / "build.gradle.kts"]
        for gradle_file in gradle_files:
            if gradle_file.exists() and "jib" in gradle_file.read_text(encoding="utf-8", errors="ignore").lower():
                return True

        return False
