# Documentation of the result corpus #3
Date: 05.07.2021
Total projects found: 700
Possible non-software projects: 

All Iteration Example Projects have been filtered out, by using the regular expression: 
`#^(?!Example\\sProject\\s-\\sIteration\\s\\d.*$).*#`  
All programming languages can make up to 100% of a projects languages.  
All markup languages can make up to 60% of a projects languages. 

Difference to result corpus #1

Projects that are falsely considered as software projects, with the new threshold: 4
Projects that are correctly considered as software projects, with the new threshold: 3

Projects that are correctly not considered as software projects, with the new threshold: 3
Projects that are falsely not considered as software projects, with the new threshold: 6

View diff here: https://www.diffchecker.com/NxkoPsrC

The six projects in the last category, are projects which now have a language called `XSLT`. I falsely decided, not to 
include this language, because it is not a programming language. But I would still have to add it to the other markup 
languages. However, even if it would have been in the filter list, the projects would not be added to the corpus, 
because the language makes up over 70% of the projects languages.  
This is probably an exception. If a threshold of more than 70% for markup languages would make sense will be examined 
with the next query. Regarding the results of that query, I will then decide if only `XSLT` should get a higher 
threshold, or if it is possible to give that threshold to all markup languages.  
Until now it looks like the higher threshold for markup languages of 60% is worse than the one with 50%, as more false 
than correct categorizations have been made in comparison to the first corpus.  
Also, the language `Dockerfile` will be added to the filter list.