This is a README

### Installation Instructions:

#### Install PTC Creo 
https://www.ptc.com/en/products/creo 
- Create a student login and install the free version - cause of you are a student.
- While installation make sure to install  JLINK for CREO - it is under the "Application Features" --> "Creo Object TOOLKIT Java and Jlink" within the Creo Setup Application.
https://creopyson.readthedocs.io/en/latest/usage.html 
- Install CREOSON (see link in Resources below) using the instruction on this Youtube video https://www.youtube.com/watch?v=-M4uzoCJYEg&t=10s&ab_channel=SimplifiedLogic%2CInc.. The path used for CREO Parametric was “C:\Program Files\PTC\Creo 9.0.0.0\Common Files”
- Run the CREOSON server and use the playground to test out the connection and then stopped it. 

#### Install Creopyson
- https://pypi.org/project/creopyson/ 
Read functionality https://creopyson.readthedocs.io/en/latest/creopyson.html 

### Running CRESON server and then starting PTC to connect to the service:

#### Running PTC Creo with the CREOSON server
-  Copy the parametric.bat from C:\Program Files\PTC\Creo 9.0.0.0\Parametric\bin this location to C:\working and renamed it to nitro_proe_remote.bat 
- Use this bat file to now open PTC  CREO.
- Start the CRESON server and read the quick start guide
- Create or move an existing *.prt to theC:/working folder. BecauseCRESON server is running from the C:/wroking folder it can access the prt files from there.

#### Running CREOSON
- Navigate to C:\working\CREOSON\CreosonServerWithSetup-2.8.1-win64
- Start CreosonSetup.exe 
- Make sure the path in step 1 matches “C:\Program Files\PTC\Creo 9.0.0.0\Common Files”
- Click “Start CREOSON” - this starts the server you will have to connect with
- Navigate to “http://localhost:9056/” to get access to documentation, playground etc. NOTE: The example here is for “JS” we are using python instead. 

### Resources
- Creopyson github: https://github.com/Zepmanbc/creopyson
- Creoson Download: http://www.creoson.com/