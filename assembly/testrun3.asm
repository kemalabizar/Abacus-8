.prog:
counttest:
    add x,i
    sta x
    cmp x,l
    jeq endtest
    jmp counttest
endtest:
    lda i
    hlt

.data:
x := $00
i := $01
l := $05