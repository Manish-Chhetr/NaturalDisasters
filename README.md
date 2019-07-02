# Earthquake Tracking System:

Our project mainly shows the real time plots and also the past occuence of earthquakes based on the user input. The database which we are using is from the offcial USGS wesite.

# Requirements:
```
- Python (3.0 and above)
- Python Libraries:
  - dash
  - dash-core-components
  - dash-html-components
  - plotly
  - pandas
  - geopandas
```
# Real Time Tracking:
This part of the project gives a track of all the earthquakes happened in the past hour, in the past 24 hours and last week. The points are plotted on a map. Based on the magnitude of the earthquake the colour changes.
It works based on the user's input and has very simple user interface. The working can be seen below.

![real_time_tracking](https://user-images.githubusercontent.com/26375997/52525008-4ccc0b00-2cc9-11e9-8b2b-757b145de2a1.gif)
      
# Earthquake History:
This part of the project deals with the history of earthquakes occured between the years 1965-2016. Country-wise plots can be obtained.
The working can be seen below.

![earthqauke_history](https://user-images.githubusercontent.com/26375997/52524977-fced4400-2cc8-11e9-8496-8c01428fa0de.gif)

# Milestone:
The aim for our project is to predict future earthquakes and alert people about the occurence and prevent any kind off damage.
    
In this, we mainly considered the highly prone regions like **Japan**, **Indonesia**, **India** etc to predict magnitude of the future calamities. The algorithm that we have used to predict is **GridSearchCV** algorithm that uses the **RandomForestRegressor** as an argument and fits the best estimator. The same is used to predict the **Accuracy**. We mainly have to tune the parameters in order to get the maximum accuracy.

## Contributors to the Project

[Manish Chhetri](https://github.com/In-finite)

[Shashank Sekhar](https://github.com/Shashank-Sekhar)

[Mohammed Sameeruddin](https://github.com/chaotic-enigma)

We are also looking forward to include the future enhancements like intimating the officials on different social media platforms or social network groups and take necessary precautions.
