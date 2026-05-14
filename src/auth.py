import pyrebase


firebase_config = {

    "apiKey": "AIzaSyATgal32KWFndrnbtuRMIVNFvoyEx5QIoA",

    "authDomain": "greywater-awareness-hub.firebaseapp.com",

    "projectId": "greywater-awareness-hub",

    "storageBucket": "greywater-awareness-hub.firebasestorage.app",

    "messagingSenderId": "314282012850",

    "appId": "1:314282012850:web:1673443a3c320a4126d9ab",

    "databaseURL": ""
}


firebase = pyrebase.initialize_app(
    firebase_config
)

auth = firebase.auth()
