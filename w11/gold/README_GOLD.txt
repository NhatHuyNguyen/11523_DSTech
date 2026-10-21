Week 11 gold files - DSTS 11523 (for checking your pipeline; do not edit)
=========================================================================

gold_questions.csv  (11 rows, used for hit@k in Step 5e and for the optional grounded answer)
  id           Q01 ... Q11
  question     a question a student could ask the Course TA
  week         the tutorial week that answers it (blank for Q11)
  source_file  the tutorial file that answers it
  section_id   the section that holds the answer (e.g. w04_s005 = week 4, section 5)
  section      that section's heading
  quote        an exact line from the tutorial that answers the question; a search "hits" when one of the
               top-k chunks contains this whole quote
  answerable   False only for Q11 ("kubernetes" appears 0 times in the six tutorials)

gold_sections_week11.csv  (15 rows, used to compare the metadata prompts V1/V2/V3 in Step 4d)
  section_id, week, source_file, section   which section
  task_type    the expected task_type ("a|b" = either answer is accepted)
  tools        the expected tools (";"-separated; empty = no tool name is written in the section)
  tools_named_in_text   every allowed tool whose name appears in the section's first 1,500 characters
               (found by code; shown for information)

Every quote was checked by code: it appears exactly once in the corpus, only in its own week, and fits whole
inside one chunk at both chunk sizes (800/150 and 400/80).
