.prog:
count_up:           ; Count upwards from the initial value of x (whatever it is)
    add x,i
    sta x               ; x <== x + i
    cmp x,lim_up        ; flag <== (x ?= lim_up)
    jeq count_dn        ; flag = lim_up? jump to count_dn
    jmp count_up        ; flag != lim_up? jump back to count_up
count_dn:           ; Count down from the lim_up value
    sub x,i
    sta x               ; x <== x - i
    cmp x,lim_dn        ; flag <== (x ?= lim_dn)
    jeq count_up        ; flag = lim_dn? jummp to count_up
    jmp count_dn        ; flag != lim_dn? jump back to count_dn

.data:
x := $00
i := $01
lim_up := $8f
lim_dn := $40