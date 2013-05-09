The app is up and running at http://librarywebchat.appspot.com/

Note: when you open the webapp, if you do not receive automatic welcome message "You are now successfully connected to Ask A Librarian. Ask away!
", it means our backend on the library server must be down. Please contact mengyalan@gmail.com.


- Use at least one Javascript library that you didn't write.
JQuery & Jquery Mobile UI, Strophe
- Use at least one Javascript library that you did write.
libs/chatapp.js
- Use at least one advanced feature in the App Engine. Examples of advanced features include: Blob store, Channel API, Image processing, or task queues.
Google AppEngine SendMail --- send log
-Use memcache (and use it correctly) on the server side.
Datastore names so we can identify which are used
-Use at least one HTML5 feature. Examples include WebSQL, IndexedDB, Camera, Geolocation, Application cache, and DeviceMotion events.
Adrenaline webpush
-Generate all of your HTML using a templating language. You may use either Jinja for server-side templating, dust.js for client side templating, or a combination of both.
Patron username -- only thing that need templating
-Provide unit tests for your server-side code and you must achieve 100% code coverage.
in test/modelsUnitTest
-Provide unit tests for Javascript libraries you write.
We didn't do.
-Provide selenium test cases that exercise all functionality. Anything that you can't exercise using selenium must have a written script that someone other than you can follow to test out a feature.
The app uses an old library(strophe.js) that is not compatible with jquery mobile ui library and jquery 1.9.1. So it cannot be used on firefox for weird reasons.
