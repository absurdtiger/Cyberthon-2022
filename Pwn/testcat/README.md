# testcat
- 992 points
- did not solve at the time

Description
---
While scanning one of APOCALYPSE's internal systems, we managed to find a pretty barebone service named "testcat". Based on our intel, they're using it on their systems to check if their netcat command works. Can you try to get a shell on their testcat server? If you do manage to compromise their service, submit the flag on their system as proof!

Interact with the service at:
chals.cyberthon22f.ctf.sg:10401

P.S. This may be of some use to you: https://libc.rip/

Note: once you get a shell, the flag.txt can be found in the user's home directory.

Files: [testcat](./testcat)

Solution
---
There are multiple approaches to this challenge, since it is vulnerable to both format string and buffer overflow.

First things first,
```
$ checksec testcat
[*] '/[redacted]/testcat'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
- canary means immediately overwriting the rip is impossible.
  - for format string, this would not be an issue and in fact we would be using this to overcome a seperate problem
  - for bof, this will have to be handled before a ret2libc rop chain
- NX (non-executable) means that the stack is not executable.
  - for fmtstr, the program needs to repeat at least once to leak the libc base before sending in the final got write (possible thanks to partial relro)
  - rop chain once canary is overcome

there

STRATEGY:
1) first i need to make the program repeat. typically there would be an exit() func>but here the program terminates with a return call, and the canary makes it so you > there's the fmtstr approach and the bof approach
 overwrite the fini_array
 or overwrite stackchk got

`Cyberthon{w3LL_1_gu355_y0u_c0uLd_54y_t35tc4t_w45_4_C4T45tr0ph3}`


