# Classifieds
- 1000 points
- we did not manage to do this challenge during the ctf

Description
---
You've been tasked to infiltrate a classified advertising firm operated by APOCALYSE. We suspect that they've been using it as a front for their money laundering activities, alongside other establishments such as a recently opened pie shop.

Interact with the service at:
chals.cyberthon22f.ctf.sg:10301

P.S. This may be of some use to you: https://libc.rip/

Note: once you get a shell, the flag.txt can be found in the user's home directory.

Files: [classifieds](./classifieds)

Solution
---
Running checksec,
```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
- Full RELRO means no overwriting got
- NX means we need to ret2libc
- PIE means we need to find the PIE base to overcome ASLR
- no canary implies that this is probably bof

Observing the binary in gdb, it is vulnerable to buffer overflow, with the rip at offset 120.

Opening in IDA,
```c
  char v4[112]; // [rsp+0h] [rbp-70h] BYREF

  setup_IO(argc, argv, envp);
  set_random_customer_id();
  banner();
  printf("Enter advertisement => ");
  __isoc99_scanf("%s", v4);
  puts("Thanks for submitting your advertisement, it'll be published after 3 working days!");
  return 0;
```
looking at the banner() function,
```c
int banner()
{
  puts(s);
  puts(&byte_2010);
  puts(&byte_20D0);
  puts(&byte_2190);
  puts(&byte_2250);
  puts(s);
  puts("---------------------------------------------------------------");
  puts("        Classified Advertising For Affordable Prices!");
  puts("---------------------------------------------------------------");
  printf("               CUSTOMER#%llu\n", &CUSTOMER_ID);
  return puts("---------------------------------------------------------------");
}
```
here we can see that the customer id given is a pointer `&CUSTOMER_ID`. So what is given to us isn't the customer id itself, but the address of the customer address. This means we can obtain the pie base, by finding leaked_pie_base - offset_of_customer_id.

then, just ret2libc as per normal

[exploit.py](./exploit.py)

`Cyberthon{4dv3rt153_my_fr35hLy_b4k3d_p135}`

remarks
---
- experimented with new pwntools formatting for this exploit
- yes it is very messy
