amazon_cells_labelled.txt  -  data file for DSTS 11523 Week 10 (Option: Sentiment)
=================================================================================

Source:   UCI Machine Learning Repository, "Sentiment Labelled Sentences" (dataset id 331)
          https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences
          Download used: https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip
Citation: Kotzias, D. (2015). Sentiment Labelled Sentences [Dataset]. UCI Machine Learning Repository.
          https://doi.org/10.24432/C57604
Paper:    Kotzias, D., Denil, M., de Freitas, N., & Smyth, P. (2015). From Group to Individual Labels
          Using Deep Features. KDD 2015.
Licence:  Creative Commons Attribution 4.0 International (CC BY 4.0)
          https://creativecommons.org/licenses/by/4.0/legalcode
Changes:  none. This file is copied unchanged from the UCI zip ("sentiment labelled sentences/" folder).
          The other two files in the zip (imdb_labelled.txt, yelp_labelled.txt) are not used in this lab.

Format:   one review sentence per line:  sentence <TAB> label   (1 = positive, 0 = negative)
          1,000 lines: 500 positive, 500 negative. 10 lines repeat an earlier sentence exactly
          (removed in Exercise 3, leaving 990 unique reviews).
Read it with:
          pd.read_csv("data/amazon_cells_labelled.txt", sep="\t", header=None,
                      names=["text", "label"], quoting=csv.QUOTE_NONE)
