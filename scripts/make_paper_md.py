"""Accessible Markdown version of paper/paper.tex (the PDF is authoritative).
Citations become bracketed keys; the title, status and abstract are prepended."""
import re, subprocess, os
here = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(here, '..', 'paper')
s = open(os.path.join(P, 'paper.tex')).read()
def cite(m):
    opt, keys = m.group(1), m.group(2).replace(',', ', ')
    return f"[{keys}{', ' + opt if opt else ''}]"
s = re.sub(r'\\cite(?:\[([^\]]*)\])?\{([^}]*)\}', cite, s)
s = s.replace('\\path{', '\\texttt{')
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', s, re.S).group(1)
tmp = os.path.join(P, '_md_tmp.tex'); open(tmp, 'w').write(s)
body = subprocess.run(['pandoc', tmp, '-f', 'latex', '-t', 'gfm', '--wrap=none'], capture_output=True, text=True, check=True).stdout
abs_md = subprocess.run(['pandoc', '-f', 'latex', '-t', 'gfm', '--wrap=none'], input=s[:s.index('\\begin{document}')] + '\\begin{document}' + abstract + '\\end{document}', capture_output=True, text=True, check=True).stdout
os.remove(tmp)
head = ("# The Hilbert series of the invariants of ternary septics, octics and nonics\n\n"
        "Anonymous. Version 0.2.0-candidate, 26 September 2026. DOI 10.5281/zenodo.22978726. **Unrefereed candidate.** "
        "This Markdown text is an accessible rendering of `paper.tex`; the PDF is authoritative.\n\n## Abstract\n\n")
bib = re.search(r'\\begin\{thebibliography\}\{[^}]*\}(.*?)\\end\{thebibliography\}', s, re.S).group(1)
items = []
for m in re.finditer(r'\\bibitem\{([^}]*)\}(.*?)(?=\\bibitem|\Z)', bib, re.S):
    txt = subprocess.run(['pandoc', '-f', 'latex', '-t', 'gfm', '--wrap=none'], input=m.group(2).strip(), capture_output=True, text=True, check=True).stdout.strip()
    items.append(f"- \\[{m.group(1)}\\] {txt}")
open(os.path.join(P, 'paper.md'), 'w').write(head + abs_md.strip() + "\n\n" + body + "\n## References\n\n" + "\n".join(items) + "\n")
print("wrote paper/paper.md")
