---
name: textbook-instructions
description: Guidelines for writing and editing academic textbook chapters aimed at communication studies students. Use when the user asks to write, edit, review, or improve textbook chapters, course materials, or academic pedagogical content. Especially relevant for Croatian language academic texts, social science methodology textbooks, and any content where practical application of methods needs to be explained to non-technical students. Triggers include requests to review chapters, implement reviewer comments, write instructional content about research methods, or create style guides for academic authors.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: lusiki/Metodologija-za-komunikologe-v2
# corpus-url: https://github.com/lusiki/Metodologija-za-komunikologe-v2/blob/48d051db6687a08aaa925574aaa27cd2980c33d0/textbook-instructions-SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Textbook Chapter Writing Instructions

These instructions apply whenever writing, editing, or reviewing textbook chapters for social science students. They originate from an editorial review of a computational text analysis chapter but apply broadly to any methods-oriented textbook aimed at communication studies or similar programmes.

The target audience is social science students, not computer scientists or mathematicians. Every instruction flows from this fact.


## Structure

### Opening

Every chapter opens with a concrete scenario or problem that a researcher faces, not with abstract definitions. The first two to three paragraphs tell the reader what the chapter is about, why it matters for their discipline, and what they will learn.

Good: "Zamislimo istraživača koji želi analizirati pedeset tisuća komentara s portala..."
Bad: "Računalna analiza teksta je skup metoda koje..."

### Roadmap paragraph

The last paragraph of every chapter introduction explicitly announces the subsections that follow. This is not a bullet list but a natural paragraph that previews the structure.

### Closing

Every chapter ends with a summary of what was covered and a bridge to the next chapter. A student who reads only the introduction and conclusion should get a coherent picture.

### Transitions

Every transition between subsections needs at least one sentence that closes the previous topic and opens the next. The reader should never feel lost jumping from one heading to another.


## Practical Guidance and Tools

### Every method needs a HOW

This was the most frequent and most important reviewer comment. It is not enough to explain what tokenization or topic modelling is. The text must say which tool does it, in which software, with which function. Students need to know where to sit and what to run.

For every method described, the text must include at least one of: (a) the name of the R or Python package, (b) a short code example runnable on local-language text, or (c) an analogy with a tool students already know (e.g. SPSS for quantitative data).

### Code examples

Code blocks of 5 to 15 lines are ideal. Code must be commented in the language of the textbook. Data in examples should be in the local language (news headlines, portal comments, political speeches). Avoid English-language examples in a non-English textbook.

### End-to-end example

At least once per chapter, ideally near the end, show a complete workflow on a small dataset: from loading raw data to a final result. This helps students see how individual steps fit together.


## Local Language and Context

### Every method must be evaluated for the local language

Most text analysis methods were developed for English. When describing any method, the author must explicitly address: does this work for our language, and if so, with which tools? If a method does not work well, say so clearly and explain why (morphological complexity, lack of resources, free word order, etc).

It is not enough to say generically "there are challenges for our language". Specify which concrete challenges apply to that specific method and what workarounds exist.

Good: "Lemmatization in R uses the SnowballC package, but its support for Croatian is incomplete. For quality lemmatization of Croatian texts, the CLASSLA pipeline in Python is recommended, and results can be imported into R for further analysis."
Bad: "Lemmatization requires sophisticated linguistic tools." (Which tools? Do they exist for this language?)

### List available local-language resources

When discussing dictionaries, corpora, lexicons, or language models, always state what exists for the local language. If resources do not exist, that is also useful information. For every resource mentioned, provide a URL or project reference.


## Complexity Level

### Mathematical formulas only when necessary

Social science students do not need to understand the derivation of the Dirichlet distribution or the formal definition of betweenness centrality. Formulas for basic metrics (TF-IDF, PMI, accuracy/precision/recall) can stay because they help understanding. More complex formulas should be removed or moved to footnotes with a reference to the original work.

Every formula that remains in the text must have a plain-language explanation above or below it, written so that a student who skips the formula still understands the concept.

### Explain technical terms at first occurrence

When a term appears for the first time that students may not know (inflectional morphology, neural networks, emergent properties, language models, sentiment lexicons), explain it immediately. The explanation can be in the sentence itself, in a footnote, or in parentheses.

Good: "Croatian has inflectional morphology, meaning that grammatical meanings such as case, number, and gender are expressed by changing the form of the word."
Bad: "Given the inflectional nature of Croatian..." (no explanation)

### Focus algorithms on intuition and application, not mathematics

Instead of explaining how an algorithm works internally, focus on three questions: (1) what the algorithm does, (2) when to use it, and (3) how to run it. Technical details go in footnotes or a separate appendix for motivated readers.

### Balance theory and practice

Rough guideline: for every page of theoretical explanation there should be at least half a page of practical content (which tool, how to use it, example on local-language text). If a section stretches across multiple pages of pure theory with zero practical guidance, the proportion is off.


## Consistency and Flow

### Consistent terminology

If the same concept appears under different names (e.g. "stop words" and "function words" used interchangeably for the same thing), the reader may think they are two different concepts. Choose one term and use it consistently. At first occurrence, alternative names can appear in parentheses, but after that stick with the chosen term.

It is recommended to make a short glossary of key terms with chosen local-language names before starting to write, and to adhere to it consistently.

### Strategic use of footnotes

Footnotes are useful for: technical details that would interrupt reading flow, bibliographic references to original works, and supplementary explanations for motivated readers.

Footnotes should NOT be used for information that is essential for understanding the text. If the student cannot understand a paragraph without reading the footnote, that information belongs in the main text. Specifically, the name of the tool or package used to perform a method should never be only in a footnote, because that is precisely what the student is looking for.

Rule of thumb: if a footnote contains the only practical piece of information in an entire section, move it to the main text.


## Academic Standards

### Citations

Every claim that references authors must have a proper citation. If the text mentions WordNet, CroSentiLex, Entman, or any other author, work, or resource, a bibliographic entry is required. For online resources, include a URL.

### Avoid first person plural

The textbook should not use "we" forms ("we have seen", "we must note"). Use neutral or passive constructions instead ("it has been shown", "it should be noted", "the researcher can"). The exception is "let us imagine" as a rhetorical device to introduce examples.

### No real names in sensitive examples

In examples of tokenization, sentiment analysis, or classification, do not use names of real politicians, public figures, or private citizens. Use generic descriptions ("the Prime Minister", "the president") or fictional names instead.


## Tables and Visual Elements

### Comparative tables for synthesis

At the end of every major section, add a table that systematizes what was explained. A table comparing methods by advantages, disadvantages, and typical application helps the student gain overview and choose the right method.

### Every table needs a description above and interpretation below

A sentence below the table should direct the reader to what is most important. Do not repeat the entire table content; instead highlight key insights or unexpected relationships.

### Diagrams and visualizations

For a methods textbook, the following visual elements are especially useful: workflow diagrams showing the sequence of steps in an analysis, decision trees helping students choose the right method for their research question, example result visualizations (word clouds, network graphs, sentiment timelines), and schematic concept illustrations.

Every visualization needs a label, title, and description explaining what the reader should notice. Avoid decorative visualizations that add no information.


## Cross-Chapter Coherence

### Consistent examples across the book

Where possible, use the same or similar dataset across multiple chapters. For example, if one chapter uses a corpus of news articles about climate change, the same corpus can serve as an example in chapters on data preparation, sentiment analysis, and framing analysis. This helps students follow how the same data is processed with different methods.

### Cross-references

When the text mentions a concept covered in more detail elsewhere in the textbook (e.g. validity and reliability, sampling, research ethics), add a brief note and reference to the relevant chapter. This helps students know where to look for more detail and shows how chapters complement each other.


## Author Checklist

Before submitting a manuscript, check the following:

**Structure**: Opening example from practice? Roadmap paragraph at end of introduction? Summary and bridge at end of chapter? Clear transition sentences between all subsections?

**Practical guidance**: Tool named for every method? At least one code example per key method? Local-language data in examples? At least one end-to-end example in the chapter?

**Local language**: Every method evaluated for local-language applicability? Available local-language resources listed?

**Complexity**: All technical terms explained at first occurrence? Formulas accompanied by plain-language explanation? Complex formulas moved to footnotes? Theory-to-practice ratio balanced?

**Consistency**: Same term used for same concept throughout? Key information (tool names) in main text, not hidden in footnotes?

**Academic standards**: Every author/resource reference has a bibliographic entry? Text in third person or neutral form? No real names in sensitive examples?

**Visual elements**: At least one comparative summary table? Tables have description above and interpretation below? At least one diagram or visualization?

**Coherence**: Cross-references to related chapters? Examples aligned with other chapters in the book?