.macro PUSH reg
    sub %sp, %sp , 4     ! Decrement stack pointer by 4 to allocate space
    st  reg ,[%sp]     ! Store the value of the register at the stack pointer
.endm

.macro POP reg
    ld reg, [%sp]       ! Load the value from the stack into the register
    add %sp, %sp  , 4    ! Increment the stack pointer by 4 to deallocate space
.endm


.global _start

_start:
    ! Assume we want to push and pop the register %o0
    mov  %o0 ,0x123        ! Load value 123 into %o0

    PUSH %o0             ! Push %o0 onto the stack
    ! You can do some operations here
    mov  %o0,0x456         ! Modify %o0 (just for demonstration)

    POP %o0              ! Pop the value from the stack back into %o0

    ! Now, %o0 should contain 123 again (the original value)
    
    ! Exit the program (for example, by using the exit system call)
    mov  %g1,0           ! Exit system call number
    nop
