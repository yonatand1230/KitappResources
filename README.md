# **Backend Scripts for** [**Kitapp**](https://play.google.com/store/apps/details?id=com.gurfi.GradeApp) **&** [**~~Kita Website~~**](https://sites.google.com/view/kita-g6)

Individual scripts to handle and update the Kitapp backend. \
An AIO program can be found in [yonatand1230/KitappUpdater](https://github.com/yonatand1230/KitappUpdater). 
The program uses all of the scripts here and creates an all-in-one, more comfortable environment to maintain the backend and keep the app working.

## Shachaf API:
Get holidays and schedule changes from shachaf as a JSON object.

### Built from:
+ shachaf python module - gets changes/holidays from shachaf's HTML, returns them as a Python dict.
+ main python script - gets changes and holidays using shachaf, writes info to a JSON file
+ changes.json - a JSON file containing the changes and holidays from shachaf as an object

<br/>
<br/>

## FireBase Updater
Used to automatically update Firebase's Real-Time Database with new Halacha Yomit every day.

### Built from:
+ Python script that connects to Firebase's API and updates current Halacha. Should be run automatically, scheduled to the same hour every day. 
+ JSON file containing Halachot for every date.
+ .env file containing the Firebase URL.

<br/>
<br/>

## Error Page:
Simply an error page for the website.

### Built from:
+ PNG picture with info about the error.
+ HTML file displaying the picture.

<br/>
<br/>

## Kitapp PWA
Passive-Web-App template.
Will be used as an iOS alternative for Kitapp, will possibly move to Firebase servers in the future.

### Built from:
+ HTML file w/ PyScript - main page.
+ Manifest (.webmanifest) file - for the website to be recognized as a PWA.
