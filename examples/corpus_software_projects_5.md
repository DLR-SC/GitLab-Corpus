# Documentation of the result corpus #5
Date: 06.07.2021
Total projects found: 764

All Iteration Example Projects have been filtered out, by using the regular expression: 
`#^(?!Example\\sProject\\s-\\sIteration\\s\\d.*$).*#`  
All programming languages can make up to 100% of a projects languages.  
All markup languages can make up to 50% of a projects languages.

Difference to corpus \#4

Projects that are falsely considered as software projects, with the new threshold: 
Projects that are correctly considered as software projects, with the new threshold: 

Projects that are correctly not considered as software projects, with the new threshold: 10
Projects that are falsely not considered as software projects, with the new threshold: 24

By comparing these two corpi, it seems that the lower threshold of 50% for non-programming languages is worse than 
the one with a threshold of 75%. When I compared the corpi, I realized that most software projects were not 
considered as such, because of four languages:  
- `HTML`
- `CSS`
- `Vue`
- `XSLT`  
It seems that these languages can make up more than 50% of a projects languages. To prove this, I will make another 
query where I raise the threshold for these four languages to a value of 80%.
