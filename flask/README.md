In this miniproject, we want to build an interactive "weather forecast" web app using "OpenWeatherMap" API.

**Note** : [Click here](http://openweathermap.org/appid) to get an API key for Free account if you don't have one yet. To get access to API you need to have an API key. Read the whole page to see how to use the API key in API call and the policies applied on the number of API calls you complete.

* You'll use [Flask](http://flask.pocoo.org/) to build your dashboard.
* You are building a dashboard. So be ready to learn how to write simple web pages using HTML.
* Download the starter_file.zip. Unzip the file and start implementing your code in the files and folders provided there. You'll learn later why some of the folders are included there and how you should add your HTML codes there. Here is the starter_file: starter_file.zip
According to Free plan information, [click here](http://openweathermap.org/price), we will have access to "current weather API" and "5 days/3hour forecast API". You can access "current weather API" doc: [here](http://openweathermap.org/current) and "5 days/3hour forecast API" doc: [here](http://openweathermap.org/forecast5).

The provided data is in JSON format by default. But you can change it to XML if you want.

# Question
* Build a dashboard that gets the name of a city and returns the current temperature and a plot of the 5 days temperature forecast. To get a better idea of how the graph should look like, check [this page](http://openweathermap.org/city). Your graph doesn't need to show the bars as shown in this graph. The bars here show the precipitation which we don't need now. To show the current weather and weather forecast, you may need to call both APIs mentioned above.

* Handle 404 and 500 error messages appropriately.
* When you report the current temperature, show the icon related to the weather condition beside it. (e.g. rain, cloud, ...)

# Submission
Submit a .zip file that contains all the required files to run your dashboard. You can remove your API key when you submit your code.

Please mention it if your code doesn't work, so it won't take time to figure it out while grading.