# PUMapMaker
This is a tool made for drone flights where the overlap of images is important.  This requires an input of a KML file of the four corner points of the area of interest as well as the desired altitude of flight and desired minimum overlap percentage.  It outputs a file with all of the waypoints needed for the drone flight to maintain a set minimum overlap percentage.  This is made for use alongside [Autopilot](https://autoflight.hangar.com/).
## Installing
PUMapMaker requires the utm and pykml libraries.
```
pip3 install utm
pip3 install pykml
```

## User Guide
### [PUMapMaker Tutorial](https://purdue0-my.sharepoint.com/personal/bullock8_purdue_edu/_layouts/15/guestaccess.aspx?docid=009f9433d13f84e9bb2e5dfc15546c65e&authkey=AU0qOeL4O9MEKjr2-hZw0Oo)
This is a step-by-step guide to using the PUMapMaker script.
### [PUMapMaker Setup](https://purdue0-my.sharepoint.com/personal/bullock8_purdue_edu/_layouts/15/guestaccess.aspx?docid=09f2908ced8fa4dc883620781fd9e7517&authkey=AWGWMReH-BM7f0LmI5AxVTg)
This is a setup guide to PUMapMaker in case there are any issues (such as using pip instead of pip3 :sweat_smile:).
