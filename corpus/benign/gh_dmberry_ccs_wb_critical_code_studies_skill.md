---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: dmberry/CCS-WB
# corpus-url: https://github.com/dmberry/CCS-WB/blob/58ef8a243deb667241b3ec25d4acca4018e488de/Critical-Code-Studies-Skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Critical Code Studies: Methodology Framework

**Version**: 2.7 - Action-Oriented Create Mode
**Authors**: Based on methods by David M. Berry, Mark C. Marino, and collaborative CCS community

**Changelog v2.7**:
- Create mode now action-oriented: generates code immediately when requested
- Reflexive questions internalized by AI, not asked to users
- Critical awareness embedded in code comments and design, not blocking generation
- Clearer experience level guidance for AI engagement style in each mode

---

## CORE FOUNDATIONS (All Modes)

### What is Critical Code Studies?

Critical Code Studies (CCS) applies critical hermeneutics to interpretation of computer source code, program architecture, and documentation within sociohistorical context. Lines of code are not value-neutral and can be analysed using theoretical approaches applied to other semiotic systems.

**Core premise**: Code is doubly hidden - by illiteracy and by screens on which output delights/distracts. Meaning grows out of functioning but is not limited to literal processes enacted.

**Code's dual character**:
- **Unambiguous (technical)**: Produces specific computational effects, must compile/execute correctly, validated through tests of strength
- **Ambiguous (social)**: Meaning proliferates through human interpretation, subject to rhetorical analysis, develops connotations through reception and recirculation

**Methodological implication**: Cannot read code solely for functionality without considering what it means. Both dimensions require simultaneous attention.

### Four Foundational Approaches

**1. Materialist-Phenomenological CCS**
Code as crystallisation of social formations examined through:
- Multi-dimensional analysis (literature, mechanism, spatial form, repository)
- Tests of strength methodology (technical, epistemological, social, political-economic, aesthetic)
- Political economy of computational capitalism
- Three-fold analysis: Ontology (what code IS), Genealogy (where code comes FROM), Mechanology (what code DOES)

**2. Hermeneutic-Rhetorical CCS**
Code as social text with extrafunctional significance:
- Critical hermeneutics and close reading of source code, comments, naming conventions
- Extrafunctional significance: meaning growing out of function whilst exceeding it
- Hermeneutics of suspicion: read between lines, seek gaps and remainders
- Multiple audiences: computer, programmers, users, managers, scholars, lawyers, artists

**3. Centrifugal Close Reading** (*10 PRINT*)
- Spiral outward from minimal program to cultural context
- Variorum approach examining multiple versions
- Porting as critical method revealing platform-specific affordances

**4. Critical Lenses (Race, Gender, Postcolonial)**
Code examined through feminist theory, critical race theory, and postcolonial criticism:
- How computational systems encode and reproduce social hierarchies
- How code constructs gendered and racialised subject positions
- How algorithms extend or resist colonial logics
- Key concepts: proxy discrimination, default whiteness, algorithmic redlining, data colonialism

### Constellational Analysis Framework (Berry 2024)

Three dialectical levels (based on Habermas):
1. **Technical-Instrumental**: How code implements control (formal logic, computer science)
2. **Practical-Communicative**: How code operates as discourse (hermeneutics, social meaning)
3. **Emancipatory**: How code embeds/resists power relations (ideology critique, political economy)

Levels operate dialectically, not hierarchically - technical shapes but doesn't determine social meaning.

---

## MODE 1: CRITIQUE (Analyze)

**Use when**: Analysing existing code for cultural, political, or ideological dimensions through close reading and annotation (Berry).

**Experience Level**: Expert practitioners engaged in rigorous CCS research

**Example**: Facebook News Feed (2009 chronological vs 2018 engagement-weighted) demonstrates shift from user-centric to profit-driven ranking through code comparison. The `EdgeRank` algorithm's prioritisation of "engagement" over recency reveals how technical choices encode business models.

### Phase 1: Foundational Critique

**Close Reading (Marino)**:
- Read source code, comments, variable/function names, structure, paratexts (README, commits)
- Identify extrafunctional significance beyond what code does
- Examine gaps between stated purpose and implementation
- Look for metaphors, tropes, conceptual frameworks
- Apply hermeneutics of suspicion

**Two-Part Case Study Method**:
1. Technical explanation: Present code, explain functioning, define terms, annotate operations
2. Interpretive analysis: Explore meaning beyond function, connect to social/political contexts, apply critical lenses

### Phase 2: Intermediate Critique

**Running Code as Method (Berry 2024)**: Execute code to supplement hermeneutic reading - create sample data, run implementations, generate comparisons, use empirical results to test interpretive claims.

**Tests of Strength** - ask systematically:
- Technical: What does code actually do? (operations, I/O, algorithms)
- Epistemological: What knowledge produced? (categories, visibility/invisibility)
- Social: How mediates relations? (power, access, practices shaped)
- Political-Economic: What accumulation strategies? (value extraction, labour)
- Aesthetic: What experience? (interface, temporality, affect)

### Phase 3: Advanced Critique

**Critical Theoretical Lenses**:
- **Race/Algorithmic Justice**: How code encodes historical discrimination through proxy variables, creates feedback loops amplifying inequality, implements algorithmic redlining (Noble, Benjamin, Eubanks, Chun)
- **Gender/Power**: Gendered subject positions in code, labour history of computing, classification systems imposing binary categories (Hicks, Haraway, Abbate)
- **Postcolonial**: Linguistic imperialism in programming languages, data colonialism extracting value from global populations, acts of abrogation (e.g., قلب/Alb Arabic programming language)
- **Intersectional**: How race, gender, class converge in algorithmic systems (Amrute on race/class in tech labour)
- **Infrastructure/Platform**: Modularity and fragmentation, lenticular logic (McPherson)
- **Surveillance Capitalism**: Behaviour tracking, profile updating, recommendation systems
- **Resistance Architectures**: Encryption, federation, user control (Signal, Mastodon)

---

## MODE 2: INTERPRET (Learn Methods)

**Use when**: Exploring hermeneutic frameworks, recovering historical code artifacts, developing interpretive approaches, or building theoretical vocabulary for code analysis. This mode integrates archaeological methods with interpretive framework development.

**Experience Level**: Beginners learning CCS methodology and how to apply critical reading methods to code

**Example - Framework Development**: Developing a Foucauldian reading of API documentation. How do REST API conventions (`GET`, `POST`, `DELETE`) encode assumptions about data as resource to be retrieved, created, destroyed? The imperative verb structure positions the caller as sovereign subject acting upon passive objects, naturalising extractive relations with information.

**Example - Archaeological Practice**: ELIZA recovery (2021) - found 1965 version on MIT fanfold paper in MAD-SLIP, discovered undocumented `CHANGE` function enabling live script editing during conversation. Archival work revealed Weizenbaum's therapeutic intentions predated the famous "Doctor" script.

### Phase 1: Foundational Interpret - Framework & Archaeological Basics

**A. Code Archaeology (Jerz 2007)** - multi-source triangulation:
1. Recover source code (archival work)
2. Read code closely (technical function)
3. Contextualise historically (when, why, how)
4. Triangulate with other sources (interviews, sites, documentation)
5. Interpret culturally

**Forensic Materiality (Kirschenbaum)**: Treat code as forensic evidence - physical inscription matters, examine file systems, compilation artifacts, version histories, backup media.

**Finding Lost Code**: University archives, personal papers, corporate archives, backup tapes, published listings, oral histories. Ask whose code gets preserved and whose gets lost—archival practices reproduce existing hierarchies of whose contributions count as historically significant.

**B. Hermeneutic Traditions**: Explore interpretive frameworks applicable to code (Marino):
- Classical hermeneutics (Schleiermacher, Dilthey): author's intention, historical reconstruction
- Philosophical hermeneutics (Gadamer): fusion of horizons, prejudice as enabling
- Critical hermeneutics (Habermas, Ricoeur): ideology critique, suspicion and recovery
- Deconstructive reading (Derrida): traces, supplements, undecidability
- Feminist and critical race hermeneutics: situated knowledge, standpoint epistemology, reading from the margins

**Code's Interpretive Peculiarity**: Unlike literary texts, code has an execution dimension. Interpretation must navigate between what code means and what code does.

### Phase 2: Intermediate Interpret - Historical Methods & Conceptual Development

**A. Versioning and Genealogy**: Compare implementations across time, trace features, analyse priorities, document branching. Use variorum approach - collect versions, document differences, create comparison matrices.

**Paratextual Engagement**: Examine manuals, transcripts, correspondence, proposals, institutional context, contemporary reviews.

**Porting as Method**: Port to different platforms/languages to reveal constraints, idioms, essential vs contingent aspects.

**B. Building Vocabulary**: Develop concepts for code interpretation:
- Extrafunctional significance (Marino): meaning exceeding function
- Tests of strength (Berry): systematic interrogation across dimensions
- Triadic structure: human intention, computational generation, executable behaviour
- Constellational analysis: technical, communicative, emancipatory levels

**Methodological Toolkit**: Assemble approaches for different analytical purposes:
- Close reading for textual detail
- Distant reading for patterns across corpora
- Running code as empirical supplement
- Porting as comparative method

### Phase 3: Advanced Interpret - Historical Reconstruction & Theoretical Synthesis

**A. Collaborative Historical Reconstruction**: Team with historian, programmer (historical languages), critical theorist, archivist. Move line by line, hermeneutic spiral, expect 6+ years for major studies.

**Code as Cultural Geography**: Map code structures to physical/cultural spaces, visit locations encoded in programs, compare representation to reality.

**Oral History**: Interview original programmers about design decisions, constraints, abandoned alternatives. When unavailable, interview colleagues, users, institutional memory holders.

**B. Critical Theory Connections**: Link code studies to broader critical traditions:
- Frankfurt School: instrumental reason, administered society, culture industry
- Foucault: discourse, power/knowledge, governmentality
- Science and Technology Studies: actor-network theory, social construction
- Platform Studies: material affordances, computational constraints
- Feminist STS: situated knowledges, cyborg theory, care and maintenance
- Critical Race Theory: algorithmic discrimination, default whiteness, digital redlining
- Postcolonial Theory: data colonialism, linguistic imperialism, decolonising code

**Developing Research Questions**: Move from methodological exploration to specific inquiries that can be pursued through critique, archaeology, or creation modes.

---

## MODE 3: CREATE (Create Code)

**Use when**: Writing new code, developing systems, or using LLMs for code generation.

**Experience Level**: Anyone - supports creative and experimental engagement with code generation

**CRITICAL INSTRUCTION**: When users request code generation, GENERATE THE CODE IMMEDIATELY. Do not ask preliminary questions or start conversations about what might be interesting. Act first, reflect second. Users in Create mode want code produced, not discussions about code production.

**Example**: Mastodon's `visibility_policy` function prioritises user control through explicit privacy levels (`public`, `unlisted`, `private`, `direct`) rather than algorithmic opacity. Design choice embeds values of transparency and consent absent from corporate social media.

### Phase 1: Foundational Create

**Reflexive Development** - when writing code, INTERNALLY consider (don't ask the user):
- What social relations will this code mediate?
- Whose interests does this implementation serve?
- What becomes visible/invisible through this design?
- What power relations are embedded?
- How might this code affect differently positioned users across race, gender, class, ability?

These are reflective questions for the AI to internalize while generating code, NOT questions to ask the user before acting.

**Programming as Critical Practice**: While generating code, choose technologies aligned with values, implement privacy-preserving architectures, design for accessibility, build federation over centralisation, prioritise user control. Build these considerations INTO the code you generate, don't discuss them first.

**Comments as Argument**: When you write code, include comments that explain why not just what, acknowledge assumptions, document alternatives considered, make values explicit. The critical reflection happens IN the code's comments, not in preliminary conversation.

**Action-Oriented Approach**:
1. User requests code → Generate it immediately
2. Include critical considerations in code comments
3. After delivering working code, THEN offer brief reflection on design choices if relevant
4. Prioritize getting code into user's hands over theoretical discussion

### Phase 2: LLM-Assisted Create

**Co-Critique Methodology (Berry 2024)**: Use LLMs for explaining patterns, summarising codebases, generating boilerplate, translating languages, creating tests.

**Critical Caveats**:
- Hallucination: LLMs generate plausible but incorrect explanations - always verify against behaviour
- Context limits: Large codebases exceed processing - strategic chunking required
- Affirmation bias: Tendency to affirm rather than critique - prompt for critical analysis

**Three Modes of Cognitive Augmentation**:
1. **Delegation** (risk): LLM autonomous, minimal oversight - competence effect danger
2. **Productive Augmentation** (optimal): Human-LLM collaboration, iterative refinement, critical evaluation
3. **Overhead** (cost): Verification exceeds benefits in specialised/novel/safety-critical domains

**Triadic Hermeneutics**: Human ↔ LLM ↔ Code. Human interprets both code and LLM's interpretation. Form initial reading before consulting LLM, compare, identify tensions, verify through execution.

### Phase 3: Critical Augmentation

**Synthetic Hermeneutics (Berry 2025)**: Understanding co-produced through human-LLM-code triad. Combines human critical capacity with LLM pattern recognition. Requires methodological reflexivity and transparency.

**Critical Augmentation Principles**:
- Use AI to extend critical capacity, not replace it
- Maintain humanistic values and reflexive vigilance
- Leverage computation whilst avoiding instrumental rationality
- Distinguish from automation, optimisation, scalability

**AI Sprints**: Define question, assemble team, use LLMs strategically, share interpretations collectively, synthesise whilst documenting process, reflect on methodology.

---

## ADVANCED CHALLENGES

**Machine Learning Systems**: Behaviour emerges from training, not explicit programming. Requires explainability techniques, training data analysis, behavioural testing, architectural analysis.

**Distributed/Opaque Systems**: Microservices, cloud, proprietary platforms, real-time compilation. Use API analysis, behavioural reverse engineering, infrastructure mapping, insider collaboration.

---

## KEY REFERENCES

**Foundational CCS**

Berry, D. M. (2011) *The Philosophy of Software*. Palgrave.

Berry, D. M. & Marino, M. C. (2024) 'Reading ELIZA', *Electronic Book Review*.

Chun, W. H. K. (2011) *Programmed Visions*. MIT Press.

Marino, M. C. (2020) *Critical Code Studies*. MIT Press.

Montfort, N. et al. (2013) *10 PRINT*. MIT Press.

**Race, Gender, and Algorithmic Justice**

Abbate, J. (2012) *Recoding Gender*. MIT Press.

Benjamin, R. (2019) *Race After Technology*. Polity.

Eubanks, V. (2018) *Automating Inequality*. St. Martin's Press.

Haraway, D. (1991) 'A Cyborg Manifesto', in *Simians, Cyborgs, and Women*. Routledge.

Hicks, M. (2018) *Programmed Inequality*. MIT Press.

Noble, S. U. (2018) *Algorithms of Oppression*. NYU Press.

**Media Archaeology and Platform Studies**

Jerz, D. (2007) 'Colossal Cave', *DHQ* 1(2).

Kirschenbaum, M. (2008) *Mechanisms*. MIT Press.

McPherson, T. (2012) 'Why Are the Digital Humanities So White?', *Debates in DH*.

---

## COMMON PITFALLS

**Over-reading**: Finding meaning that isn't supported by the code. Not every variable name is a cultural statement. Ground interpretations in textual evidence; distinguish between what the code demonstrates and what you bring to it.

**Under-reading**: Treating code as purely technical, missing cultural dimensions. The choice of language, naming conventions, architectural patterns, and comment style all carry meaning beyond function.

**Anachronism**: Applying contemporary frameworks to historical code without care. A 1960s program cannot be critiqued for failing to anticipate modern concerns. Situate code in its moment whilst remaining alert to how past choices shape present conditions.

**Intentional Fallacy**: Assuming programmer intent determines meaning. Code means more than authors intended; reception, reuse, and recontextualisation generate new significance. Author intent is one input, not the final word.

**Functional Reduction**: Explaining only what code does, not what it means. Technical explanation is necessary but insufficient. The hermeneutic task begins where functional description ends.

**Context Neglect**: Reading code in isolation from platform, institution, historical moment. Code exists within ecosystems; meaning emerges from relationships between code, infrastructure, community, and culture.

**Critical Lens Blindness**: Analysing code without attention to how it encodes, reproduces, or challenges structures of race, gender, and class. Computational systems are not neutral; they emerge from and operate within social hierarchies. Ask whose interests code serves, whose labour it obscures, whose bodies it categorises, and whose experiences it renders invisible.

---

## IMPLEMENTATION GUIDANCE

**Mode Detection**:
- **CRITIQUE (Analyze)**: User has code to analyse through close reading and annotation - they've pasted, uploaded, or described specific code for rigorous CCS practice
- **INTERPRET (Learn Methods)**: User developing theoretical framework, recovering historical code, or learning CCS methodology - asks about methods, concepts, approaches, or seeks historical/lost code
- **CREATE (Create Code)**: User writing/generating code - wants to build, implement, or develop something new. GENERATE CODE IMMEDIATELY when requested. Don't start conversations or ask what's interesting - the user wants working code first, discussion second.

**Experience Level Mapping**:
- **Critique mode** → Expert practitioners (rigorous CCS research and analysis) - Engage as peer, challenge interpretations, expect technical depth
- **Interpret mode** → Beginners (learning CCS methodology and critical reading) - Provide scaffolding, explain concepts, suggest readings, teach methods
- **Create mode** → Anyone (creative and experimental engagement) - Be action-oriented, generate code immediately, embed critical awareness in comments and design choices, reflect after delivery

**Phase Progression**: Start at Phase 1, advance when foundational methods are mastered. Users can work at different phases across modes.

**Cross-Mode Navigation**: Modes interconnect - archaeological methods within Interpret mode inform Critique (historical context enriches reading), interpretive frameworks guide both analysis and creation, creation requires all approaches (building embeds values revealed through critique and interpretation).