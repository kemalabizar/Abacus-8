.prog:
decrement:          ; Decrement loop
    sub x,y             ; 
    sta x               ; x <== x - y
    cmp z,x             ; flag <== (z ?= x)
    nop                 ; do nothing here...
    jeq endprog         ; flag = eq? jump to endprog
    jmp decrement       ; flag != eq? jump to decrement
endprog:            ; Endprog loop
    hlt                 ;

.data:
x := $a3
y := $02
z := $8f