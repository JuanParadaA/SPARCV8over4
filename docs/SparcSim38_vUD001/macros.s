! Define PUSH macro to save registers
.macro PUSH reg
    ! Save register on stack
    sub %sp, 4, %sp             ! Decrement stack pointer (reserve space)
    st reg, [%sp]              ! Store the register value on the stack
.endm

! Define POP macro to restore registers
.macro POP reg
    ld [%sp], reg              ! Load the register value from the stack
    add %sp, 4, %sp             ! Increment stack pointer (restore space)
.endm

! Clear a register (set to zero)
.macro clr reg
    mov 0, reg                 ! Set register to zero
.endm



.macro set value, reg
!    .if ((value) & 0xFFFFFC00) == 0      ! Check if the value fits in 13 bits (small constant)
!        mov value, reg                  ! Use mov for small values
!    .elseif ((value) & 0x3FF) == 0       ! Check if the low 10 bits are zero (i.e., 1024-byte alignment)
!        sethi %hi(value), reg           ! Load high 22 bits (no need for OR since %lo(value) == 0)
!    .else                                 ! For general larger values
        sethi %hi(value), reg           ! Load high 22 bits
        or reg, %lo(value), reg        ! Combine with low 10 bits
!    .endif
.endm
