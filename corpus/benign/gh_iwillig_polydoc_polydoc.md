---
name: polydoc
description: |
  Build advanced documentation systems using Pandoc filters compiled with GraalVM for the JVM/Clojure ecosystem.
  Use when creating documentation filters, processing code blocks, building searchable documentation books,
  running code in documents, or when the user mentions Pandoc filters, documentation processing, document
  transformation, or interactive documentation systems.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: iwillig/polydoc
# corpus-url: https://github.com/iwillig/polydoc/blob/aadba9ab07dc40fcf0d22f3dbc621df6ca7208a9/POLYDOC_SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Polydoc - JVM-Native Pandoc Documentation System

Polydoc brings Pandoc's powerful filtering capabilities to the JVM/Clojure ecosystem, providing advanced
document processing without Python/Node.js dependencies. It compiles to native code with GraalVM for
fast execution.

## Quick Start

```bash
# Install dependencies
brew bundle

# Start development REPL
bb nrepl

# In REPL
(dev)           ; Load dev namespace
(refresh)       ; Reload all namespaces
(lint)          ; Lint with clj-kondo
(run-all)       ; Run all tests

# Build and use
bb build-cli
polydoc --help
```

**Key capabilities:**
- **Code execution filters**: Run Clojure, SQLite, JavaScript, Python code blocks
- **Rendering filters**: Process PlantUML diagrams
- **Linting filters**: Check Clojure code with clj-kondo
- **Include filters**: Compose documents from multiple sources
- **Book building**: Generate books with TOC and full-text search
- **Interactive viewer**: HTTP-based document browser with SQLite-powered search

## Core Concepts

### Pandoc Filter Architecture

Polydoc processes documents through Pandoc's filter system:

```
Document (Markdown/etc) 
  → Pandoc Parser 
  → JSON AST 
  → Polydoc Filter (JVM/Clojure) 
  → Modified AST 
  → Pandoc Writer 
  → Output (HTML/PDF/etc)
```

**Pandoc AST Structure:**

```clojure
;; Complete Pandoc document
{:pandoc-api-version [1 23 1]
 :meta {:title {:t "MetaString" :c "My Document"}}
 :blocks [{:t "Header" :c [1 ["id" [] []] [{:t "Str" :c "Title"}]]}
          {:t "Para" :c [{:t "Str" :c "Content"}]}
          {:t "CodeBlock" 
           :c [["" ["clojure"] []] 
               "(+ 1 2)"]}]}

;; Common block types
{:t "Para" :c [...]}           ; Paragraph
{:t "Header" :c [level attrs content]}  ; Header
{:t "CodeBlock" :c [attrs code]}        ; Code block
{:t "BulletList" :c [...]}              ; Bullet list
{:t "OrderedList" :c [...]}             ; Numbered list
```

### Filter Processing Pattern

All Polydoc filters follow this pattern:

```clojure
(ns polydoc.filters.example
  (:require [clojure.walk :as walk]
            [clojure.data.json :as json]))

(defn process-element
  "Transforms a single AST element."
  [element]
  (if (matches? element)
    (transform element)
    element))

(defn filter-document
  "Walks the entire AST and applies transformations."
  [ast]
  (walk/postwalk process-element ast))

(defn run-filter
  "Main entry point - reads JSON from stdin, processes, writes to stdout."
  []
  (let [ast (json/read *in* :key-fn keyword)
        modified (filter-document ast)]
    (json/write modified *out*)))
```

### Code Block Processing

Code blocks are the primary target for most filters:

```clojure
;; Code block structure
{:t "CodeBlock"
 :c [["id" ["language" "class"] [["key" "value"]]]  ; attributes
     "code content"]}                                 ; code string

;; Extract language and code
(defn code-block? [element]
  (= "CodeBlock" (:t element)))

(defn get-language [code-block]
  (-> code-block :c first second first))

(defn get-code [code-block]
  (-> code-block :c second))

;; Example: Process Clojure code blocks
(defn process-clojure-block [element]
  (when (and (code-block? element)
             (= "clojure" (get-language element)))
    (let [code (get-code element)
          result (eval-clojure code)]
      ;; Return modified block with result
      (assoc-in element [:c 1] 
                (str code "\n;; => " result)))))
```

## Common Workflows

### Workflow 1: Creating a New Filter

**Goal:** Add a filter that processes code blocks in a specific language.

```clojure
;; 1. Create filter namespace
(ns polydoc.filters.my-filter
  (:require [clojure.walk :as walk]
            [clojure.data.json :as json]))

;; 2. Define element matching
(defn my-code-block? [element]
  (and (= "CodeBlock" (:t element))
       (= "mylang" (-> element :c first second first))))

;; 3. Define transformation
(defn process-my-block [element]
  (if (my-code-block? element)
    (let [code (-> element :c second)
          result (execute-my-language code)]
      ;; Replace code block with result
      {:t "CodeBlock"
       :c [["" ["output"] []]
           (str code "\n\nOutput:\n" result)]})
    element))

;; 4. Walk the AST
(defn filter-ast [ast]
  (walk/postwalk process-my-block ast))

;; 5. Create CLI command handler
(defn run-my-filter
  "Process mylang code blocks in Pandoc AST."
  [opts]
  (let [ast (json/read *in* :key-fn keyword)
        modified (filter-ast ast)]
    (json/write modified *out*)
    {:exit 0}))

;; 6. Add to main.clj CLI configuration
;; In polydoc.main:
{:command "filter-mylang"
 :description "Process mylang code blocks"
 :opts []
 :runs polydoc.filters.my-filter/run-my-filter}
```

**Test the filter:**

```bash
# Create test document
echo '```mylang
my code here
```' > test.md

# Convert to Pandoc JSON
pandoc -t json test.md > test.json

# Run filter
clojure -M:main filter-mylang < test.json > output.json

# Convert back to markdown
pandoc -f json -t markdown output.json
```

### Workflow 2: Processing Code Execution

**Goal:** Execute code blocks and include output in the document.

```clojure
(ns polydoc.filters.run-code
  (:require [clojure.java.shell :as shell]))

(defn execute-clojure [code]
  "Execute Clojure code and capture output."
  (try
    (let [result (eval (read-string code))]
      {:success true
       :result (pr-str result)
       :output ""})
    (catch Exception e
      {:success false
       :error (.getMessage e)})))

(defn execute-shell [code language]
  "Execute code via shell interpreter."
  (try
    (let [result (shell/sh (interpreter-for language) "-c" code)]
      {:success (zero? (:exit result))
       :output (:out result)
       :error (:err result)})
    (catch Exception e
      {:success false
       :error (.getMessage e)})))

(defn interpreter-for [language]
  (case language
    "python" "python3"
    "javascript" "node"
    "bash" "bash"
    "sh"))

(defn process-executable-block [element]
  (if (and (code-block? element)
           (executable-language? (get-language element)))
    (let [lang (get-language element)
          code (get-code element)
          result (if (= lang "clojure")
                  (execute-clojure code)
                  (execute-shell code lang))]
      (if (:success result)
        ;; Create new block with code + output
        {:t "Div"
         :c [["" [] []]
             [{:t "CodeBlock" :c [["" [lang] []] code]}
              {:t "CodeBlock" :c [["" ["output"] []] (:output result)]}]]}
        ;; Show error
        {:t "Div"
         :c [["" ["error"] []]
             [{:t "CodeBlock" :c [["" [lang] []] code]}
              {:t "Para" :c [{:t "Strong" :c [{:t "Str" :c "Error:"}]}
                             {:t "Space" :c []}
                             {:t "Str" :c (:error result)}]}]]}))
    element))
```

### Workflow 3: Building a Documentation Book

**Goal:** Combine multiple documents into a searchable book with TOC.

```clojure
(ns polydoc.book
  (:require [next.jdbc :as jdbc]
            [honey.sql :as sql]
            [clojure.java.io :as io]
            [clojure.data.json :as json]))

;; Database schema for book index
(def schema
  {:books {:book_id :integer-primary-key
           :name :text
           :metadata :text}
   :sections {:section_id :integer-primary-key
              :book_id :integer
              :content :text
              :hash :text
              :title :text
              :level :integer}})

(defn create-index-db [db-path]
  "Create SQLite database for book index."
  (let [db {:dbtype "sqlite" :dbname db-path}
        ds (jdbc/get-datasource db)]
    (jdbc/execute! ds
      ["CREATE TABLE IF NOT EXISTS books (
          book_id INTEGER PRIMARY KEY,
          name TEXT,
          metadata TEXT)"])
    (jdbc/execute! ds
      ["CREATE TABLE IF NOT EXISTS sections (
          section_id INTEGER PRIMARY KEY,
          book_id INTEGER,
          title TEXT,
          content TEXT,
          hash TEXT,
          level INTEGER,
          FOREIGN KEY(book_id) REFERENCES books(book_id))"])
    (jdbc/execute! ds
      ["CREATE VIRTUAL TABLE IF NOT EXISTS sections_fts 
        USING fts5(title, content, content=sections)"])
    ds))

(defn index-section [ds book-id section]
  "Add a section to the index."
  (jdbc/execute! ds
    (sql/format {:insert-into :sections
                 :values [{:book_id book-id
                          :title (:title section)
                          :content (:content section)
                          :hash (:hash section)
                          :level (:level section)}]})))

(defn extract-sections [ast]
  "Extract sections from Pandoc AST."
  (let [sections (atom [])]
    (walk/postwalk
      (fn [element]
        (when (= "Header" (:t element))
          (let [[level [id classes attrs] content] (:c element)]
            (swap! sections conj
                   {:level level
                    :id id
                    :title (text-from-inlines content)
                    :content (serialize-blocks element)})))
        element)
      ast)
    @sections))

(defn build-book
  "Build book from TOC file and source documents."
  [{:keys [toc output-db output-html]}]
  (let [ds (create-index-db output-db)
        toc-data (parse-toc toc)
        book-id (create-book ds toc-data)]
    ;; Process each document in TOC
    (doseq [doc (:documents toc-data)]
      (let [ast (parse-document doc)
            sections (extract-sections ast)]
        (doseq [section sections]
          (index-section ds book-id section))))
    ;; Generate HTML with search
    (generate-html ds book-id output-html)))
```

### Workflow 4: Search Implementation

**Goal:** Provide full-text search across documentation.

```clojure
(ns polydoc.search
  (:require [next.jdbc :as jdbc]
            [honey.sql :as sql]
            [honey.sql.helpers :as h]))

(defn search-sections
  "Search for sections matching query."
  [ds query]
  (jdbc/execute! ds
    (sql/format
      {:select [:s.section_id :s.title :s.content :s.level
                [(sql/call :highlight :sections_fts 1 "<mark>" "</mark>")
                 :highlighted]]
       :from [[:sections :s]]
       :join [[:sections_fts :fts]
              [:= :s.section_id :fts.rowid]]
       :where [:match :sections_fts query]
       :order-by [[(sql/call :rank :sections_fts) :asc]]
       :limit 50})))

(defn format-search-results
  "Format search results for display."
  [results]
  (for [result results]
    {:title (:sections/title result)
     :snippet (:highlighted result)
     :level (:sections/level result)
     :section-id (:sections/section_id result)}))

;; CLI command
(defn run-search
  "Search documentation index."
  [{:keys [query db]}]
  (let [ds (jdbc/get-datasource {:dbtype "sqlite" :dbname db})
        results (search-sections ds query)]
    (doseq [result (format-search-results results)]
      (println (str "## " (:title result)))
      (println (:snippet result))
      (println))
    {:exit 0}))
```

### Workflow 5: Interactive Documentation Viewer

**Goal:** Serve documentation with live search via HTTP.

```clojure
(ns polydoc.viewer
  (:require [org.httpkit.server :as http]
            [hiccup.core :as h]
            [polydoc.search :as search]))

(defn render-page
  "Render HTML page with search."
  [content query results]
  (h/html
    [:html
     [:head
      [:title "Polydoc Viewer"]
      [:style "
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; }
        .search { padding: 20px 0; }
        .result { padding: 10px; margin: 10px 0; border-left: 3px solid #007bff; }
        mark { background: yellow; }
      "]]
     [:body
      [:h1 "Documentation"]
      [:div.search
       [:form {:method "GET"}
        [:input {:type "text" :name "q" :value query :placeholder "Search..."}]
        [:button "Search"]]]
      [:div.results
       (for [result results]
         [:div.result
          [:h3 (:title result)]
          [:div {:dangerouslySetInnerHTML {:__html (:snippet result)}}]])]]]))

(defn handler [ds]
  (fn [req]
    (let [query (get-in req [:params :q])
          results (when query (search/search-sections ds query))]
      {:status 200
       :headers {"Content-Type" "text/html"}
       :body (render-page nil query results)})))

(defn start-viewer
  "Start HTTP server for documentation viewer."
  [{:keys [db port]
    :or {port 8080}}]
  (let [ds (jdbc/get-datasource {:dbtype "sqlite" :dbname db})
        server (http/run-server (handler ds) {:port port})]
    (println (str "Viewer running at http://localhost:" port))
    (println "Press Ctrl+C to stop")
    @(promise)))
```

## CLI Command Structure with cli-matic

Polydoc uses cli-matic for command-line interface:

```clojure
(ns polydoc.main
  (:require [cli-matic.core :as cli]
            [polydoc.filters.run-clojure :as run-clojure]
            [polydoc.filters.plantuml :as plantuml]
            [polydoc.book :as book]
            [polydoc.search :as search]
            [polydoc.viewer :as viewer])
  (:gen-class))

(def CONFIGURATION
  {:app {:command "polydoc"
         :description "Advanced Pandoc documentation system for JVM"
         :version "0.1.0"}
   
   :global-opts []
   
   :commands
   [{:command "filter"
     :description "Pandoc filter commands"
     :subcommands
     [{:command "run-clojure"
       :description "Execute Clojure code blocks"
       :opts []
       :runs run-clojure/run-filter}
      
      {:command "run-sqlite"
       :description "Execute SQLite queries"
       :opts []
       :runs run-sqlite/run-filter}
      
      {:command "run-javascript"
       :description "Execute JavaScript code blocks"
       :opts []
       :runs run-js/run-filter}
      
      {:command "render-plantuml"
       :description "Render PlantUML diagrams"
       :opts [{:option "output-dir"
               :short "o"
               :as "Output directory for images"
               :type :string
               :default "./images"}]
       :runs plantuml/run-filter}
      
      {:command "lint-clojure"
       :description "Lint Clojure code with clj-kondo"
       :opts []
       :runs lint/run-filter}
      
      {:command "include"
       :description "Include external files in document"
       :opts [{:option "base-dir"
               :short "b"
               :as "Base directory for includes"
               :type :string
               :default "."}]
       :runs include/run-filter}]}
    
    {:command "book"
     :description "Book building commands"
     :subcommands
     [{:command "toc"
       :description "Print table of contents"
       :opts [{:option "file"
               :short "f"
               :as "TOC file path"
               :type :string
               :required true}]
       :runs book/print-toc}
      
      {:command "build"
       :description "Build entire book with index"
       :opts [{:option "toc"
               :short "t"
               :as "TOC file"
               :type :string
               :required true}
              {:option "output-db"
               :short "d"
               :as "Output database path"
               :type :string
               :default "book.db"}
              {:option "output-html"
               :short "o"
               :as "Output HTML file"
               :type :string
               :default "book.html"}]
       :runs book/build-book}]}
    
    {:command "search"
     :description "Search documentation"
     :opts [{:option "query"
             :short "q"
             :as "Search query"
             :type :string
             :required true}
            {:option "db"
             :short "d"
             :as "Database path"
             :type :string
             :default "book.db"}]
     :runs search/run-search}
    
    {:command "view"
     :description "Start interactive documentation viewer"
     :opts [{:option "db"
             :short "d"
             :as "Database path"
             :type :string
             :default "book.db"}
            {:option "port"
             :short "p"
             :as "HTTP port"
             :type :int
             :default 8080}]
     :runs viewer/start-viewer}]})

(defn -main [& args]
  (cli/run-cmd args CONFIGURATION))
```

## When to Use Each Feature

**Use `polydoc filter run-clojure` when:**
- Documenting Clojure libraries with live examples
- Including test results in documentation
- Generating tables/charts from data

**Use `polydoc filter render-plantuml` when:**
- Creating architecture diagrams
- Documenting system design
- Visualizing workflows

**Use `polydoc filter lint-clojure` when:**
- Ensuring code examples are valid
- Catching errors before publication
- Maintaining code quality in docs

**Use `polydoc book build` when:**
- Creating comprehensive documentation sites
- Combining multiple documents
- Need searchable documentation

**Use `polydoc search` when:**
- Finding information across documentation
- Testing search functionality
- Building search-based tools

**Use `polydoc view` when:**
- Developing documentation locally
- Previewing changes before publish
- Creating interactive documentation sites

## Best Practices

**DO:**
- Test filters with simple AST examples first
- Use `walk/postwalk` for AST transformations
- Handle errors gracefully (return original element if processing fails)
- Add comprehensive CLI help text
- Use SQLite FTS5 for full-text search
- Cache expensive operations (diagram rendering, code execution)
- Validate Pandoc AST structure before processing
- Use keyword keys for JSON parsing (`:key-fn keyword`)

**DON'T:**
- Mutate AST elements (return new ones)
- Execute untrusted code without sandboxing
- Skip error handling in filters
- Forget to flush output after JSON write
- Hardcode paths (use CLI options)
- Process the same element multiple times
- Modify elements you're not targeting

## Common Issues

### Issue: "Filter produces invalid JSON"

**Cause:** Malformed AST structure returned

**Solution:** Validate AST structure matches Pandoc spec

```clojure
;; Wrong: Missing required fields
{:t "CodeBlock" :c ["code"]}

;; Right: Complete structure
{:t "CodeBlock" :c [["" ["lang"] []] "code"]}

;; Use schema validation
(require '[malli.core :as m])

(def CodeBlock
  [:map
   [:t [:= "CodeBlock"]]
   [:c [:tuple
        [:tuple string? [:sequential string?] [:sequential [:tuple string? string?]]]
        string?]]])

(m/validate CodeBlock element)
```

### Issue: "Code execution fails"

**Cause:** Missing interpreter or invalid code

**Solution:** Add error handling and validation

```clojure
(defn safe-execute [code language]
  (try
    (if (interpreter-exists? language)
      (execute-code code language)
      {:error (str "No interpreter for " language)})
    (catch Exception e
      {:error (.getMessage e)})))
```

### Issue: "Search returns no results"

**Cause:** FTS index not synced with content table

**Solution:** Rebuild FTS index

```clojure
(defn rebuild-fts-index [ds]
  (jdbc/execute! ds
    ["INSERT INTO sections_fts(sections_fts) VALUES('rebuild')"]))
```

### Issue: "Performance degradation with large documents"

**Cause:** Processing entire AST multiple times

**Solution:** Use transducers or single-pass processing

```clojure
;; Instead of multiple walk/postwalk calls
(defn multi-filter [ast]
  (walk/postwalk
    (fn [element]
      (-> element
          (process-code-blocks)
          (process-diagrams)
          (process-includes)))
    ast))
```

## Development Workflow

### REPL-Driven Development

```clojure
;; 1. Start REPL
;; bb nrepl (in terminal)

;; 2. Load dev namespace
(dev)

;; 3. Load and test filter
(require '[polydoc.filters.my-filter :reload])

;; 4. Test with sample AST
(def test-ast
  {:blocks [{:t "CodeBlock" :c [["" ["clojure"] []] "(+ 1 2)"]}]})

(polydoc.filters.my-filter/filter-ast test-ast)

;; 5. Verify output
;; => {:blocks [{:t "CodeBlock" :c [["" ["clojure"] []] "(+ 1 2)\n;; => 3"]}]}

;; 6. Lint and test
(lint)
(run-all)

;; 7. Build and test CLI
;; bb build-cli (in terminal)
```

### Testing Filters End-to-End

```bash
# 1. Create test markdown
cat > test.md << EOF
# Test Document

\`\`\`clojure
(+ 1 2 3)
\`\`\`
EOF

# 2. Convert to Pandoc JSON
pandoc -t json test.md -o test.json

# 3. Run filter
clojure -M:main filter run-clojure < test.json > output.json

# 4. Convert back
pandoc -f json output.json -o output.md

# 5. Verify
cat output.md
```

### Building Native Image

```bash
# Full build pipeline
bb build-cli

# Separate steps
bb compile          # Compile Clojure to classes
bb build-uberjar    # Create standalone JAR
bb build-gvm        # Compile with GraalVM

# Test native binary
./polydoc --help
```

## Integration with Pandoc

### Basic Pipeline

```bash
# Markdown → Filter → HTML
pandoc input.md \
  --filter polydoc filter run-clojure \
  --filter polydoc filter render-plantuml \
  -o output.html

# Multiple filters in sequence
pandoc input.md \
  --filter "polydoc filter include" \
  --filter "polydoc filter run-clojure" \
  --filter "polydoc filter lint-clojure" \
  -o output.html
```

### Makefile Integration

```makefile
POLYDOC = polydoc
PANDOC = pandoc

%.html: %.md
	$(PANDOC) $< \
		--filter "$(POLYDOC) filter run-clojure" \
		--filter "$(POLYDOC) filter render-plantuml" \
		--standalone \
		-o $@

book: book.yaml chapters/*.md
	$(POLYDOC) book build -t book.yaml -o book.html -d book.db

search:
	$(POLYDOC) search -q "$(QUERY)" -d book.db

serve:
	$(POLYDOC) view -d book.db -p 8080

clean:
	rm -f *.html *.json book.db
```

## Dependencies

### Core Libraries

- **cli-matic** (0.5.4): CLI framework
- **clojure.data.json** (2.5.1): Pandoc AST parsing
- **next.jdbc** (1.3.1070): Database access
- **honeysql** (2.7.1350): SQL DSL
- **sqlite-jdbc** (3.47.1.0): SQLite driver
- **malli** (0.19.2): Schema validation
- **bling** (0.8.8): Terminal formatting

### Development Tools

- **clj-kondo**: Linting
- **kaocha**: Testing
- **clj-reload**: Namespace reloading
- **hashp**: Debug printing

### External Requirements

- **Pandoc** (>=2.0): Document processing
- **GraalVM** (optional): Native compilation
- **PlantUML** (optional): Diagram rendering

## Resources

### Related Skills

- **[Clojure REPL](../../language/clojure_repl.md)**: REPL-driven development
- **[cli-matic](../cli/cli_matic.md)**: CLI framework
- **[next.jdbc](../database/next_jdbc.md)**: Database operations
- **[HoneySQL](../database/honeysql.md)**: SQL generation
- **[Malli](../data_validation/malli.md)**: Data validation
- **[hashp](../debugging/hashp.md)**: Debug printing

### External Documentation

- [Pandoc Filters](https://pandoc.org/filters.html): Official filter documentation
- [Pandoc AST](https://pandoc.org/using-the-pandoc-api.html): AST specification
- [SQLite FTS5](https://www.sqlite.org/fts5.html): Full-text search

## Summary

Polydoc brings Pandoc's document processing to the JVM with:

1. **Fast execution** - GraalVM native compilation
2. **Rich filters** - Code execution, rendering, linting
3. **Searchable docs** - SQLite FTS5 full-text search
4. **Interactive viewer** - HTTP-based documentation browser
5. **JVM-native** - No Python/Node.js dependencies

**Core workflow:**
1. Write documents with code blocks
2. Process with Polydoc filters (execute, render, lint)
3. Build searchable books with TOC
4. Serve interactively with HTTP viewer

**Use Polydoc when:** Building advanced documentation systems on the JVM, processing code in documents, creating searchable documentation, or avoiding Python/Node.js dependencies for Pandoc filters.