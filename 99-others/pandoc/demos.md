# Demos

[[contents\]](https://pandoc.org/demos.html#tocul)

- [Try pandoc online](https://pandoc.org/demos.html#try-pandoc-online)
- [Examples](https://pandoc.org/demos.html#examples)

# Try pandoc online

You can try pandoc online [here](http://johnmacfarlane.net/pandoc/try).

# Examples

To see the output created by each of the commands below, click on the name of the output file:

1. HTML fragment:

   ```
   pandoc MANUAL.txt -o example1.html
   ```

2. Standalone HTML file:

   ```
   pandoc -s MANUAL.txt -o example2.html
   ```

3. HTML with table of contents, CSS, and custom footer:

   ```
   pandoc -s --toc -c pandoc.css -A footer.html MANUAL.txt -o example3.html
   ```

4. LaTeX:

   ```
   pandoc -s MANUAL.txt -o example4.tex
   ```

5. From LaTeX to markdown:

   ```
   pandoc -s example4.tex -o example5.text
   ```

6. reStructuredText:

   ```
   pandoc -s -t rst --toc MANUAL.txt -o example6.text
   ```

7. Rich text format (RTF):

   ```
   pandoc -s MANUAL.txt -o example7.rtf
   ```

8. Beamer slide show:

   ```
   pandoc -t beamer SLIDES -o example8.pdf
   ```

9. DocBook XML:

   ```
   pandoc -s -t docbook MANUAL.txt -o example9.db
   ```

10. Man page:

    ```
    pandoc -s -t man pandoc.1.md -o example10.1
    ```

11. ConTeXt:

    ```
    pandoc -s -t context MANUAL.txt -o example11.tex
    ```

12. Converting a web page to markdown:

    ```
    pandoc -s -r html http://www.gnu.org/software/make/ -o example12.text
    ```

13. From markdown to PDF:

    ```
    pandoc MANUAL.txt --pdf-engine=xelatex -o example13.pdf
    ```

14. PDF with numbered sections and a custom LaTeX header:

    ```
    pandoc -N --template=template.tex --variable mainfont="Palatino" --variable sansfont="Helvetica" --variable monofont="Menlo" --variable fontsize=12pt --variable version=2.0 MANUAL.txt --pdf-engine=xelatex --toc -o example14.pdf
    ```

15. ipnyb (Jupyter notebook):

    ```
    pandoc example15.md -o example15.ipynb
    ```

16. HTML slide shows:

    ```
    pandoc -s --mathml -i -t dzslides SLIDES -o example16a.html
    ```

    ```
    pandoc -s --webtex -i -t slidy SLIDES -o example16b.html
    ```

    ```
    pandoc -s --mathjax -i -t revealjs SLIDES -o example16d.html
    ```

17. TeX math in HTML:

    ```
    pandoc math.text -s -o mathDefault.html
    ```

    ```
    pandoc math.text -s --mathml  -o mathMathML.html
    ```

    ```
    pandoc math.text -s --webtex  -o mathWebTeX.html
    ```

    ```
    pandoc math.text -s --mathjax -o mathMathJax.html
    ```

    ```
    pandoc math.text -s --katex   -o mathKaTeX.html
    ```

18. Syntax highlighting of delimited code blocks:

    ```
    pandoc code.text -s --highlight-style pygments -o example18a.html
    ```

    ```
    pandoc code.text -s --highlight-style kate -o example18b.html
    ```

    ```
    pandoc code.text -s --highlight-style monochrome -o example18c.html
    ```

    ```
    pandoc code.text -s --highlight-style espresso -o example18d.html
    ```

    ```
    pandoc code.text -s --highlight-style haddock -o example18e.html
    ```

    ```
    pandoc code.text -s --highlight-style tango -o example18f.html
    ```

    ```
    pandoc code.text -s --highlight-style zenburn -o example18g.html
    ```

19. GNU Texinfo, converted to info, HTML, and PDF formats:

    ```
    pandoc MANUAL.txt -s -o example19.texi
    ```

    ```
    makeinfo --no-validate --force example19.texi -o example19.info
    ```

    ```
    makeinfo --no-validate --force example19.texi --html -o example19
    ```

    ```
    texi2pdf example19.texi  # produces example19.pdf
    ```

20. OpenDocument XML:

    ```
    pandoc MANUAL.txt -s -t opendocument -o example20.xml
    ```

21. ODT (OpenDocument Text, readable by OpenOffice):

    ```
    pandoc MANUAL.txt -o example21.odt
    ```

22. MediaWiki markup:

    ```
    pandoc -s -t mediawiki --toc MANUAL.txt -o example22.wiki
    ```

23. EPUB ebook:

    ```
    pandoc MANUAL.txt -o MANUAL.epub
    ```

24. Markdown citations:

    ```
    pandoc -s --bibliography biblio.bib --filter pandoc-citeproc CITATIONS -o example24a.html
    ```

    ```
    pandoc -s --bibliography biblio.json --filter pandoc-citeproc --csl chicago-fullnote-bibliography.csl CITATIONS -o example24b.html
    ```

    ```
    pandoc -s --bibliography biblio.yaml --filter pandoc-citeproc --csl ieee.csl CITATIONS -t man -o example24c.1
    ```

25. Textile writer:

    ```
    pandoc -s MANUAL.txt -t textile -o example25.textile
    ```

26. Textile reader:

    ```
    pandoc -s example25.textile -f textile -t html -o example26.html
    ```

27. Org-mode:

    ```
    pandoc -s MANUAL.txt -o example27.org
    ```

28. AsciiDoc:

    ```
    pandoc -s MANUAL.txt -t asciidoc -o example28.txt
    ```

29. Word docx:

    ```
    pandoc -s MANUAL.txt -o example29.docx
    ```

30. LaTeX math to docx:

    ```
    pandoc -s math.tex -o example30.docx
    ```

31. DocBook to markdown:

    ```
    pandoc -f docbook -t markdown -s howto.xml -o example31.text
    ```

32. MediaWiki to html5:

    ```
    pandoc -f mediawiki -t html5 -s haskell.wiki -o example32.html
    ```

33. Custom writer:

    ```
    pandoc -t sample.lua example33.text -o example33.html
    ```

34. Docx with a reference docx:

    ```
    pandoc --reference-doc twocolumns.docx -o UsersGuide.docx MANUAL.txt
    ```

35. Docx to markdown, including math:

    ```
    pandoc -s example30.docx -t markdown -o example35.md
    ```

36. EPUB to plain text:

    ```
    pandoc MANUAL.epub -t plain -o example36.text
    ```

37. [Producing slide shows with pandoc](https://pandoc.org/MANUAL.html#producing-slide-shows-with-pandoc)
You can use pandoc to produce an HTML + JavaScript slide presentation that can be viewed via a web browser. There are five ways to do this, using [S5](http://meyerweb.com/eric/tools/s5/), [DZSlides](http://paulrouget.com/dzslides/), [Slidy](http://www.w3.org/Talks/Tools/Slidy/), [Slideous](http://goessner.net/articles/slideous/), or [reveal.js](http://lab.hakim.se/reveal-js/). You can also produce a PDF slide show using LaTeX [`beamer`](https://ctan.org/pkg/beamer), or slides shows in Microsoft [PowerPoint](https://en.wikipedia.org/wiki/Microsoft_PowerPoint) format.

    ```
    pandoc -t s5 -s habits.md -o habits_s5.html
    pandoc -t revealjs -s habits.md -o habits_revealjs.html -V revealjs-url=https://revealjs.com
    pandoc habits.md -o habits.pptx
    
    
    pandoc -t revealjs -s take_notes.md -o take_notes.html -V revealjs-url=https://revealjs.com --slide-leve=2 -V theme=moon
    ```
