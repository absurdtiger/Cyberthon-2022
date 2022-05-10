# Low Ceiling

Description
---
APOCALYPSE members frequent this server but we dont know what for. Help us find out what its for.

The URL for this challenge: http://chals.cyberthon22f.ctf.sg:40301/

Solution 
---
When we first see the webpage, we don't see anything other than a header reading:
> # Here are some flags for you 🏁 🚩 🏴 🏳

My first thought was to inspect the page, but we don't see anything special in the developer tools either. Thus, my next thought was to check `/robots.txt`.

On the `robots.txt` page, we see `Disallow:dev`. Therefore, we check `/dev`.

Upon loading the `dev` page, we download a file `dev.zip` from the webpage. Inside this zip archive, we find the javascript source code, `index.js`.

#### Contents of `index.js`:

    const path              = require('path');
    const express           = require('express');
    const router            = express.Router();

    router.get('/', (req, res) => {
        secret = req.headers["secret-header"];
        if (secret == "admin"){
            return res.sendFile(path.resolve('views/admin.html'));
        }
        return res.sendFile(path.resolve('views/index.html'));
    });

    router.get('/robots.txt', (req, res) => {
        res.type('text/plain');
        res.send("User-agent: *\nDisallow:dev");
    });

    router.get('/dev', (req, res) => {
        return res.sendFile(path.resolve('dev/source.zip'));
    })

    module.exports = router;

Within the source code, I noticed this snippet:

        secret = req.headers["secret-header"];
        if (secret == "admin"){
            return res.sendFile(path.resolve('views/admin.html'));
        }

This implies that we can visit `/views/admin.html` provided we submit a POST request with the http header `secret-header` set to `"admin"`. This can be done using cUrl, but I prefer using Burp Suite, where I sent the http history containing the url to Burp Suite's Repeater, and edited the request to change it from a GET request to a POST request, and added the http header `secret-header` to the request and set it to `"admin"`

On the `/views/admin.html` page we get the flag:

Cyberthon{l0w_ceiling_w4tch_ur_head_a6243746643baf3d}
