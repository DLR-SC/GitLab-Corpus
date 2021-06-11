# Documentation of the result corpus #2
Date: 10.06.2021
Total projects found: 658

All Iteration Example Projects have been filtered out, by using the regular expression: 
`#^(?!Example\\sProject\\s-\\sIteration\\s\\d.*$).*#`  
All programming languages can make up to 100% of a projects languages.  
All markup languages can make up to 30% of a projects languages.  

Five completely new projects were found since the last query.  
One project with description "Erstellung der Dokumentation und Bedienungsanleitung für das FEMM Messsystem" was 
not detected as software project anymore, because the threshold of 30% for markup languages is lower than the 35.54% 
of CSS in the project. Regarding the description, this is very good, because the project most likely does not contain 
software but only documentation.  
Some other older projects are now considered as software projects, because the developers pushed source code to the 
repository.

On the negative side, a project with the description "This project aims to develop algorithms in the benefit of 
the walabot!" is now considered as a non-software project, because it contains too much HTML(37%) and TeX(36%). 
This also applies to some other projects. 

Projects that are correctly not considered as software projects, with the new threshold: 2

Projects that are falsely not considered as software projects, with the new threshold: 16

View diff here: https://www.diffchecker.com/WB4PQ4FI  

It seems that reducing the threshold for markup languages from 50% to 30% has a negative impact on the resulting corpus,
when trying to filter out software projects. Thus the following queries will be compared to the first corpus and not to 
this one.