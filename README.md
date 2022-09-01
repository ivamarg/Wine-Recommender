# Wine-Recommender
Wine recommendation system based on user taste preferences.

In this project, we explored a way of extracting features from wine application and used these features to produce
a simple wine recommendation engine. As a result, a model was built that calculates the similarity between wines 
based on price, vintage, region, grape variety, marked users of the rating, taste and flavor notes.

## Data
The [Vivino.com](https://www.vivino.com/) web application is best suited for data parsing as it contains a large database of both wines and users.
Vivino.com allows  to use an API to get wine data such as: wine name, vintage, wine rating, number of votes, country,
price, region, winery, wine style, bottle volume, acidity, intensity, body, sweetness, sparkling , flavor notes, etc.
You can also get data from the user profile: a list of all rated wines and rating, comments about the wine,
favorite style of wine, number of friends.

You can learn about extracted features in detail in this notebook.

## Implementation
To extract data about wine and user actions in the application, parsers were written that use regular expressions to
find the necessary information. An exploratory analysis was carried out in order to study the characteristics of 
vintage and non-vintage wines, their prices, rating, taste characteristics, the influence of the year and region. 
To reduce the dimension of the dataset, Multiple Correspondence Analysis (MCA) was carried out. For the reduced space 
and scaled data, a cluster analysis was performed, during which the wines were divided into 4 clusters. 
The idea behind clustering is that similar wines in the same cluster will be recommended together.

Recommending system uses cosine similarity which is a type of content-based filtering method to recommend similar
wines to the user. Cosine similarity is the measure of similarity between two items, by computing the cosine of the 
angle between two vectors projected into multidimensional space. The cosine scores between the user taste vector and
the untasted wine vector were sorted in descending order, and only the top 10 were displayed.


## Result
The result is a list of 10 wines that a particular user could potentially like. Each unique wine is recommended with 
the most appropriate vintage for the user (maximum 5).

