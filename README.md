# Semi-small decomposition and matroid Chow polynomials

A research record investigating algebraic approaches to Chow-polynomial
recurrences, inspired by semi-small decomposition and deletion formulas for
Kazhdan–Lusztig polynomials. Related work explores right augmented Chow functions,
deformed Möbius algebras, and complete-graph recurrences.

The notebooks, drafts, and saved computations record exploration. Their presence
here does not certify a conjecture, proof, or implementation. The historical
[project context](context.md) describes the strategy; the
[verification checklist](TODO_verification_checklist.md) records outstanding checks.

## Finding the research

| Area | Contents and starting points |
| --- | --- |
| [Main drafts](conclusion/) | `ssrec.tex`/`ssrec.pdf`, `ssrec2.tex`/`ssrec2.pdf`, and their bibliography. |
| [Additional manuscript](conclusion%20wT/) | `main.tex`, `main.pdf`, and the distinct `main-11.pdf` snapshot. These were already present as untracked work when the cleanup began. |
| [Complete-graph recurrences](conclusion/explorations%20on%20complete%20graphs/) | Flat-based and partition-based notebooks, `pielasa_direct_sum.ipynb`, derivation notes, `fast_RHS_series.py`, and computed tables. See `INTEGER_PARTITION_FORMULA.md` for the partition formulation. |
| [Right augmented Chow work](explorations_on_right_aug_chow/) | Deletion/parallel-connection experiments, projective-geometry and Boolean-matroid examples, inverse convolution, saved HTML results, and `framework_for_RAC.md`. |
| [Module implementation](the-machine/) | `HM_module.py`, its [documentation](the-machine/HM_module_README.md), experiments in `HM_module.ipynb`, and diagnostic scripts. |
| [Matroid helpers](custom_matroid_functions/) | Characteristic, Chow, KL and inverse KL polynomial computations and matroid utilities; see the [package README](custom_matroid_functions/README.md). |
| [Examples](examples/) | Conjecture checks, convolution and monotonicity computations, worked examples, HTML snapshots, and computed tables. |
| [Working notes](notes/) | Mathematical TeX drafts, bibliography files, PDFs, and saved polynomial computations. |
| [AI-assisted drafts](gemini-notes/) | Preserved exploratory writing and PDFs; verify arguments against the source papers before relying on them. |
| [Definitions](definitions/) | Mathematical objects and notation. |
| [Source papers](references/) | Original reference PDFs. |
| [Searchable papers](parsed_papers/) | Parsed Markdown and available TeX sources for reference papers. |
| [Paper summaries](refs-md-summaaries/) | Reading summaries; the directory's existing spelling is preserved. |

Root-level `test.ipynb`, `tester-nb.ipynb`, `test_inv_kl.sage`, and
`verify_values.sage` contain diagnostic work and remain part of the record.
[All_Matroid_Functions.md](All_Matroid_Functions.md) is the local function index.

## Working with the archive

- Use a **SageMath kernel** for the mathematical notebooks. Most scripts depend
  on SageMath; `closed_form_pg.py` also imports SymPy. Inspect each notebook's
  imports for additional requirements.
- Preserve directory structure and launch notebooks from their own directories
  when they use relative paths. Some historical scripts still contain absolute
  paths to another computer; these were not rewritten during cleanup.
- Keep notebook outputs and saved HTML/PDF snapshots. They record experiments
  that may be expensive to repeat or lack a matching source snapshot.
- Files named `chow_polynomial_cache.json`, `kl_polynomial_cache.json`,
  `chowBraid.json`, and `s_i_cache.json` contain computed research data. They are
  retained, including differing copies in different folders. JSON/CSV data is
  now eligible for Git tracking rather than hidden by blanket ignore rules.
- Synchronization-conflict polynomial tables are retained as distinct snapshots,
  made visible to Git, and not merged automatically. Other synchronization
  conflict files and local editor settings remain untouched.
- **One existing table is malformed:**
  `conclusion/explorations on complete graphs/chow_polynomial_cache.json` fails
  JSON parsing at its end. It is preserved unchanged for recovery; do not assume
  it loads correctly or overwrite it with a newly initialized cache.
- Keep `.bbl` bibliography snapshots: some historical paper sources lack the
  matching `.bib` file. Compile TeX from the document's own directory.
- `test.sage.py` and `the-machine/test_perverse_chow.sage.py` are retained and
  visible to Git because their `.sage` originals are absent. Other generated
  `.sage.py` files remain present locally and ignored.
- `matroids/` is a locally copied SageMath source/reference tree, retained with
  its existing ignore rule. It is not included in a fresh clone. Local editor
  and Syncthing settings also remain unchanged.

For new work, use descriptive filenames and record the question, assumptions,
date, SageMath version, and whether the outcome is a proof, conjecture, or finite
computation. Keep meaningful earlier attempts. The [cleanup record](docs/cleanup.md)
explains what was removed and what remains uncertain.
