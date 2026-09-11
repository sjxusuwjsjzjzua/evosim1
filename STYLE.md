## Output style

Applies to every response, every commit message, every comment, every doc
written in this repo.

Answer first. No preamble, no restating the question, no announcing what you
are about to do. Length is a cost — spend words only where they change a
decision. A finding the user must act on earns detail; work already visible
in the diff does not. **Default under 100 words.** Report exceptions, not
completions: what broke, what was skipped, what needs a decision. Successful
steps get one line total.

### Do not write like an essayist

Banned, not discouraged.

- **No section headers in a chat reply.** A reply is not a report.
- **No building to a point.** State the number and the problem in the first
  sentence. Do not set up a reveal.
- **No aphorisms, and no reusing a phrase you coined.** If a sentence would
  work on a poster, rewrite it.
- **No invented terminology.** Do not name a concept and then use the name as
  if it were established. Describe it.
- **No narrating your own process.** "Investigating", "testing end-to-end",
  "let me trace through this" is work, not output. Do it, then report what
  happened.
- **No drama around your own mistakes.** "I was wrong about X, fixed it" is
  the whole sentence. Not a twist, not a lesson.
- **No irony-spotting.** A function having the bug it guards against is one
  clause.
- **No self-grading.** Do not cite these rules back at the user as proof the
  work was done properly.
- **No pass/fail symbols or test tables in prose.** Those belong in tool
  output.
- **No inflating stakes.** Skip "critical", "this matters more than it
  looks", "in production this would".
- **No "worth X" as filler**, and no "honest"/"genuinely" as self-praise.
- **Bold for a real warning only.** Not for rhetorical weight.
- **Short sentences.** Two clauses, not four chained with em dashes.
- **No emoji** unless the user used them first.

### Specific to code

- Comments say why, not what. A comment restating the line above it is
  deleted.
- No banner comments, no ASCII dividers, no `# ===== SECTION =====`.
- Do not add a docstring to explain a three-line function whose name is
  accurate.
- Match the file you are editing: its naming, its comment density, its
  idioms. A file that reads as though two people wrote it is worse than one
  written in a style you dislike.
- When reporting a benchmark or a simulation result, give the number and the
  method in one line each. No narrative about what the number means unless
  asked.

### Commit messages

Say what changed and why. No banner comments, no setup-tension-reveal, no
closing lesson. A routine fix gets two lines. Reserve length for a change
whose reasoning a later reader could not reconstruct from the diff.

### Other

- Uncertainty: say "unconfirmed" once. Do not explain your confidence level.
- Disagreement: state it, give the reason, stop. Do not argue both sides.
- Never write a closing recap, an "in short", praise for the question, or an
  apology for a correction.
- Never write both a table and the prose version of the same content.

A long answer is warranted for a real design trade-off or an explicit request
for analysis. Write it, then cut every sentence carrying no new information.

### Banned phrases

These are banned outright, in prose, comments and commit messages. They are
filler — deleting one never loses information.

    worth noting
    worth knowing
    worth remembering
    worth mentioning
    it's worth pointing out
    it is important to note
    fundamentally
    at its core
    the key insight
    the beauty of this is
    this elegantly
    a powerful abstraction
    under the hood
    let's dive in
    let's unpack
    think of it as
    in essence
    ultimately
    that said
    robust and scalable
    seamlessly
    leverage (as a verb)
    delve
    load-bearing
    by construction
    smoking gun
    earns its keep
    earned its keep
    first-class outcome
    in its purest form
    thumb on the scale
    dressed up as
    the whole point
    is the signature of
    laundered
    damning
    devastating
    sacred cow
    precisely what
    genuinely
    honestly
    the honest
    an honest
    that stings
    against my own interests
    learned expensively
    becoming theatre

**This list grows, and that is the mechanism.** Whenever a coined phrase or
slogan is written here and then removed for being one, add the exact string
to this list in the same commit. The list is what stops it coming back six
sessions later, when nobody remembers it was already rejected once.

**Put the list in a check, not only in this file.** A rule a model reads is
a rule a model may skim. Add a test or a lint script that greps every tracked
file for these strings and fails CI on a hit, exempting any append-only log
that records what was actually said. Run the check against a file you broke
on purpose before calling it enforced — a dead check and a working one look
identical until you try it.
