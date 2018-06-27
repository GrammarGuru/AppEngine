const admin = require('firebase-admin');

var config = {
    apiKey: "AIzaSyARZrgVwe8DFCn-YWx3oIEbS9scLQbXkNA",
    authDomain: "sentence-92ceb.firebaseapp.com",
    databaseURL: "https://sentence-92ceb.firebaseio.com",
    projectId: "sentence-92ceb",
    storageBucket: "sentence-92ceb.appspot.com",
    messagingSenderId: "1035428194993"
};

admin.initializeApp(config);

module.exports = function(req, res) {
    admin.database().ref('news').once('value')
        .then(snapshot => {
            return res.send(snapshot.val());
        })
        .catch(err => res.status(422).send(err));
}