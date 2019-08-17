var express = require( 'express' ),
    vhost = require( 'vhost' );

function createVirtualHost(domainName, dirPath) {
    return vhost(domainName, express.static( dirPath ));
}

var app = express();

var homeHost = createVirtualHost("www.mdsharpe.com", "public/home");
var numchenHost = createVirtualHost("numchen.mdsharpe.com", "public/numchen");

app.use(homeHost);
app.use(numchenHost);

var port = process.env.PORT;
app.listen(port, function() {
    console.log( 'Express server listening on port %d in %s mode', port, app.settings.env );
});