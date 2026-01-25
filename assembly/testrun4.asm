.prog:
check:
    add x,i
    sta x
    cmp x,a
    jeq end
    jmp check
filler:
    nop
    nop
    nop
    nop
end:
    hlt

.data:
x := $30
a := $33
i := $01