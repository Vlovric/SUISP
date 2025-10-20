# SUISP_projekt

## Compile

Instalirajte TeX Live full verziju i LaTeX Workbench extention za Visual Studio Code. Moći ćete kroz GUI onda compileat i na svakom saveu će vam generirat PDF. Par stvari za znat:
- Prvi put kad želite compileat napravite `pdflatex ime.tex` u terminalu, vidite ako imate neki warning u outputu
- Koliko sam shvatio, kada dodate u literaturu nešto, da bi mogli koristit to za citiranje morate sa `biber` "refreshat" literaturu, znači napravite `pdflatex ime.tex` pa `biber ime` pa DVA puta `pdflatex ime.tex`, mislim pisat će vam sve u warning logu ili outputu u terminal tako da samo čitajte ako ima problema, malo je goofy treba par puta runnat commande u specifičnom redoslijedu.
