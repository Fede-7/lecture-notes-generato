import unittest

from note_generator.pipeline import LectureNotesPipeline


class PipelineTests(unittest.TestCase):
    def test_pipeline_generates_markdown_with_sections_and_exercises(self) -> None:
        text = (
            "ok allora parliamo di compilatori. "
            "Il linguaggio ML è un linguaggio funzionale. "
            "Ad esempio, il compilatore visita l'albero sintattico. "
            "L'albero sintattico rappresenta 3 + 5 * 2. "
            "fun codegen tree = translate tree"
        )

        result = LectureNotesPipeline().run(text, output_format="markdown")

        self.assertIn("# Automated Lecture Notes", result.output)
        self.assertIn("## 1", result.output)
        self.assertIn("### Esercizi", result.output)
        self.assertIn("```mermaid", result.output)
        self.assertIn("```ml", result.output)
        self.assertIn("See Section", result.output)

    def test_pipeline_generates_latex_output(self) -> None:
        text = "Il file system è affidabile. Ad esempio, EXT3 usa un log."

        result = LectureNotesPipeline().run(text, output_format="latex")

        self.assertIn("\\documentclass{article}", result.output)
        self.assertIn("\\section{1", result.output)


if __name__ == "__main__":
    unittest.main()
