"""Create the large local page used in the context-size exercise."""
from pathlib import Path

rows = "\n".join(
    f"<tr><td>Student {number:04d}</td><td>Roll BA{number:04d}</td>"
    f"<td>Attendance {60 + number % 40}%</td>"
    "<td>Remarks: regular attendance recorded</td></tr>"
    for number in range(1, 3001)
)
page = (
    "<html><body><h1>Attendance Register</h1><table>"
    f"{rows}</table></body></html>"
)
output = Path(__file__).with_name("big.html")
output.write_text(page, encoding="utf-8")
print(f"{output.name} created: {len(page):,} characters")