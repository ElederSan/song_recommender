![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

## Project | Song recommender

#### Business goal:

Take a user input and recommend 5 similar songs.

#### Instructions:

This song recommender takes an input from the user, who types in the song he/she wants to get recommendations for.

The recommender obtains the song ids from accessing the Spotify API and returns 5 matches for the input string.

The user is then prompted to select and index between 0 and 4 to confirm the title he/she wants to confirm the right track he/she meant.

The recommender retrieves the song id for the user selection and obtains the audio features for that track.

The audio features dataframe is modelled with the dimensionallity reduction UMAP and compared with the entire song database.

The cluster to the closest song match is obtained.

The recommender checks if the song is flagged as "hot" (top 100 bilboard"), and returns 5 recommendations from the same cluster.

In case the song was not flagged as "hot", the recommender will return 5 recommendations from the same cluster and the "not_hot" database.

The user can repeat the process and obtain recommendations for songs as many times as he wants.

Once ready the user can simply answer "no" and the prompting process will stop.

