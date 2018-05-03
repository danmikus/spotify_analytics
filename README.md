![Stern](/assets/stern.png)

# Spotify Data Analytics

Created by:
* Anjum Bothra
* Dan Mikus
* Lauren Song
* Chen Wei

## Introduction

The initial guidance for our project was simple: set up a data pipeline using an API and create a database from the results. With this, however, a number of implied tasks and questions arise, the most important of which being what data to analyze. When looking for a project to work on, we wanted to analyze data that had social or popular cultural relevance. As avid users of the Spotify App, we decided that we wanted to gain deeper insights into what people are listening to. We therefore set out to answer some of our top questions the Spotify API could answer. Additionally, we wanted to present the answers to our questions in a practical and interactive manner, which led us to use Google's Datastudio for visualization.

#### Questions to Answer

Although we started with a much larger list of questions, we quickly found that the Spotify API doesn't expose many of the more interesting data points we were looking for. For example, information like number of plays for a song isn't retrievable programmatically. After assessing everything that was (and wasn't) available via the API, we decided to pursue answers to the following questions:

* What are the characteristics of the songs in the top playlists?
* Is there a relationship between popularity and followers?
* What genres are the most popular across current popular playlists?
* Who are the top artists?

## Designing and Building the Solution
#### Structuring the Problem

The step first in creating our solution was to structure it. We decided to structure it into three areas:
* the entity interacting with the process
* the process to retrieve and transform the data
* the datastore for the data

The idea was to design the process to be initiated by either a user or a service (either deployed on the cloud or via cron job). After initiation, the main script would run, which would make calls to the Spotify and BigQuery modules we created. Each module's main purpose was to interact with their namesake's respective outside service to retrieve data and store it in BigQuery. See figure 1 for the illustration.

![Data Flow Diagram](/assets/data_flow_diagram.png)
fig (1)

One important note is that we decided to use Biquery, Google's cloud based Big Data product. as our database solution. This mainly came from the ease of integration with Datastudio, which allows data to be easily ported from the database to the visualization tool.

#### Coding the Process
##### Main Script
The purpose for the main script is to pass in required arguments into each of the modules as well as transforming data to be loaded into the database. Specifically, when data is returned from the Spotify module, it is returned as a list of objects, which cannot be loaded into the tables as is. The main script transforms them into a more useable form. Likewise, the main script also organizes the data into tables for loading into BigQuery. This process is iterative for each of the playlists provided by the user.

##### Spotify Module
The Spotify modules primary purpose is to retrieve the data from the Spotify endpoint using the API. It does this by first creating a client using the the Spotipy library to interact with the API. It then sends the requests for track and artist data through the API and converts them to the respective track and artist classes defined in the module. Finally, it returns the objects back to the main script.

##### BigQuery Module
 After the main script passes the data into the BigQuery module, a client is set up using the Google.Cloud python library. Requests are made to check if the required database taxonomy is already created and, if not, to create it. At that point the data is loading into the tables.

#### BigQuery

We decided to load our tables in a streaming process instead of a jobs base process, which seemed to be much more conducive to working with data in memory. For the database structure, we created a dataset for each distinct playlist we collected data on. Each dataset functions as a structural entity for tables, but does not restrict the user from querying across them. Under each dataset the same tables are created:

* Artists
* Features
* Genres
* Related Artists
* Top Artist Tracks
* Tracks

To see the schemas, please see figure 2.

![Data Schema](/assets/Schema2.png)
fig (2)

## Presenting the Data
#### Queries

The queries we wrote were in support of answering some of our ultimate business questions. Since we had three different playlists, we had to union the data from each table into our final queries. The queries we wrote are:

* The artists with the most songs across the playlists
* The number of songs were explicit from each playlist
* The popularity of the artists on the playlists
* The features of the songs on the playlists

We were then able to use these queries to visualize our data.


#### Data Visualization

To visualize the data we queried, we used Datastudio to present our findings in a usable fashion. With Datastudio, you can connect your BigQuery project and write queries to import data into your charts and graphs. Please see figure 3 for a screenshot. To see the output of our work, please visit the link below:

[Spotify Datastudio Project](https://datastudio.google.com/reporting/1ELPtwKYgR3OrSuNjLelY04tmtFL4wuQS/page/JjCR)

![datastudio](/assets/datastudio.png)
fig (2)

#### Our Findings

We were able to glean some interesting insights from our data. One of the most interesting is how popular Drake is. He is far ahead of any other artist in terms of followers and popularity score. Also interesting is that despite his popularity, he is ties for two with J. Cole for number of songs on the countdowns, behind Post Malone. It was however, not surprising to us that a clear majority of the most popular songs in America are pop songs. Of course, we were also able to get features of the songs, but these seemed to only be useful when comparing against other songs.

## Lessons Learned
1. **Data Architecture Planning - **Planning for how you will realistically query the data is important up front. Because we didn't plan ahed enough on this, we had each set of tables broken out by playlists (e.g., three artist tables, three genre tables). We could still use this, but it could have been designed better.

2. **Spend more time structuring the code - **We learned that it is much easier to make an architecture of how the code is going to work upfront, otherwise you will be correcting code more than writing new code.

3. **Deploying your code - **We learned many lessons on deploying code. For example, we were unaware you needed to build your code before deploying it (rather building it after deployment).

4. **Research the API more - **We began this project with a large list of questions that we _assumed_ the Spotify API could answer. However, we quickly found that the data we wanted from them wasn't available programmatically. We then had to realign on what we wanted to learn in this project. Had we checked earlier we may have picked a different API.

5. **Writing tests - **It would have been useful to write test scripts to test functionality. Although we used a debugging library (PDB), we could have used smaller unit tests to save time.
