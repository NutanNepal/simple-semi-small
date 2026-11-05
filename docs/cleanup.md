# Repository cleanup — 2026-11-04

This cleanup preserves the repository as a research record. It changes no
mathematical source, notebook, saved result, bibliography, or existing research
note. Existing untracked work is preserved. No files are committed or staged.

## Removed

52 files, about 1.13 MB, including ignored local build debris:

| Category | Files | Reason |
| --- | ---: | --- |
| Operating-system metadata | 16 | `.DS_Store` and Windows `:Zone.Identifier` sidecars. |
| Python bytecode | 14 | Cached `.pyc` files with corresponding Python source present. |
| LaTeX bookkeeping | 21 | Auxiliary files, logs, synchronization, back-references, and build state. |
| Empty placeholder | 1 | `examples/random.ipunb` contained zero bytes. |

No literal references to the removed filenames or paths were found in retained
project source, notebook cells, or research text. The sole match was the existing
`.DS_Store` exclusion in `.stignore`, which remains unchanged. This static check
excludes the copied `matroids/` tree and local editor/synchronization files.

## Preserved

- All 27 `.ipynb` notebooks and their outputs, including root-level tests,
  `parallelcon copy.ipynb`, and `deleconjright_RAW.ipynb`.
- `the-machine/HM_module - Copy.txt`, which contains notebook JSON and research
  outputs despite its `.txt` extension.
- All mathematical code, notes, papers, bibliography sources and `.bbl`
  snapshots, PDFs, HTML exports, and the `kl_profile` performance artifact.
- All computed JSON/CSV data, including differing copies, synchronization
  conflicts, and the malformed file identified below.
- All generated `.sage.py` scripts, especially the two without source originals.
- The existing untracked `conclusion wT/` manuscript and four right augmented
  Chow research files: `boolean_matroids_aug_chow.ipynb`, `closed_form_pg.py`,
  `deleconjright_PG.ipynb`, and `right_aug_chow_examples.ipynb`.
- The ignored `matroids/` reference tree, editor settings, Syncthing configuration,
  and synchronization-conflict records.

## Ignore-rule changes

Removed blanket exclusions for JSON, CSV, DAT, XML, YAML, and `.bbl` files so
research data, configuration, and bibliography snapshots can be versioned.
Added exceptions for the two orphan generated research scripts and divergent
polynomial-cache JSON snapshots. Added exclusions for Windows sidecars and
LaTeX `.brf` files. Other existing ignore rules remain intact.

Newly visible research files appear as untracked until explicitly added to Git;
this cleanup does not stage them or merge their contents.

## Existing issues retained for review

- `conclusion/explorations on complete graphs/chow_polynomial_cache.json` fails
  parsing at line 3356, column 3, at the end of the file. It appears truncated
  and is preserved byte-for-byte rather than repaired or discarded.
- `parsed_papers/texs/bhmpw/augmentedchow.tex` requests `refs.bib`, which is not
  present alongside it. Its `.bbl` and PDF snapshots remain.
- `test.sage.py` and `the-machine/test_perverse_chow.sage.py` have no matching
  `.sage` originals. The latter also contains an absolute path to another machine.
- Historical documentation mentions files absent from this checkout, including
  `sagemath_matroids_reference.md`, `definitions/computational_framework.md`, and
  `the-machine/example_usage.sage`. The new root index links to existing files.
- Mathematical claims and completion statements in older notes were not audited
  or rewritten. Use the existing verification checklist when continuing research.

## Validation

Removal candidates were fingerprinted before changes, checked for source
references, and backed up outside the repository. Retained-file fingerprints,
notebook JSON, index links, and ignore rules are checked after applying cleanup.
Historical computations are not rerun: they may be expensive or rewrite saved
polynomial tables.
