## Project Stage 1

1. [Original documents](https://github.com/WenFuLee/CS-839-Data-Science/tree/master/stage1/documents/original)
2. [Documents with markup](https://github.com/WenFuLee/CS-839-Data-Science/tree/master/stage1/documents/marked)<br>- [README](https://github.com/WenFuLee/CS-839-Data-Science/blob/master/stage1/documents/marked/README): the selected entity type
3. [Documents in set I](https://github.com/WenFuLee/CS-839-Data-Science/tree/master/stage1/documents/set_I)
4. [Documents in set J](https://github.com/WenFuLee/CS-839-Data-Science/tree/master/stage1/documents/set_J)
5. [Code](https://github.com/WenFuLee/CS-839-Data-Science/tree/master/stage1/code)
6. [Compressed file, including all the files above](https://github.com/WenFuLee/CS-839-Data-Science/blob/master/stage1/compressed_files.zip)
7. [PDF Report](https://github.com/WenFuLee/CS-839-Data-Science/blob/master/stage1/Project%20Stage%201_Report.pdf)

## Project Stage 2
Requirements
  - You must select two Web data sources from which structured data can be extracted by using the rule-based wrapper construction method discussed in the class. These two data sources must contain information about a set of overlapping entities, such as books, movies, cars, etc. This is because later we will have to perform entity matching as a class project stage, and we need the two sources to have overlapping entities, so that we can match between the two sources, to find data that refer to the same real-world entities.
  - Each of the above two sources should contain a reasonable amount of data, and the two sources should have a reasonable amount of overlapping entities. For example, suppose we extract a relational table A from the first source where each tuple describes a person, and suppose we extract a similar table B from the second source. Then each table should have at least 3000 tuples, and they should share at least 100 persons (you can only eyeball the data for this latter requirement, and that is sufficient). 
  - Then extract data from these two sources to form two tables A and B (one from each source). The two tables should have the same schema, and each tuple in each table must describe a single entity (all of the same type). For example, if the entity type is  person, then each tuple describes a person, and a possible table schema can be A(name, city, state, zip, phone) (and the same schema for Table B). 
**Each table must have at least 3000 tuples and be in CSV format. **

1. [A link to a DATA directory] that stores both tables A and B. They should be stored in two files, each file storing a table in CSV format. We should be able to browse these files to examine the tables. There should be a README file in the same directory that explains the tables (e.g., the meaning of the attributes) and lists the number of tuples per table.

2. [A link to a CODE directory] that stores all of your code (this directory must also be browsable). 

3. [A link to a pdf file] that describes the following:
  - a description of the two Web data sources that you have selected. Recall that you are supposed to select two Web data sources from which you can extract structured data.
  - a description of how you have extracted structured data from the two data sources.
  - describe the type of entity you extract, briefly describe the two tables, list the number of tuples per table.
  - the names of open-source tools you have used in this project stage and a brief description of what they do. 
