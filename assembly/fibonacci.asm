.prog:
count:
    lda x
    add x,y
    sta z
    mov y,x
    mov z,y
    cmp z,lim
    jal end
    jmp count
end:
    lda x
    hlt

.data:
x := $00
y := $01
z := $00
lim := $1f