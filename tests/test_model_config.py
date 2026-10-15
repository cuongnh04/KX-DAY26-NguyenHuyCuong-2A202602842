import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def assigned_string(path: Path, name: str) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    return node.value.value
    raise AssertionError(f"{name} is not assigned a string in {path}")


class ModelConfigTest(unittest.TestCase):
    def test_examples_use_current_gemini_model(self) -> None:
        function_calling = ROOT / "01-function-calling" / "weather_function_calling.py"
        agent = ROOT / "04-lab" / "mcp-client" / "weather_agent" / "agent.py"

        self.assertEqual(assigned_string(function_calling, "MODEL"), "gemini-3.8-flash")
        self.assertIn('model="gemini-3.8-flash"', agent.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
