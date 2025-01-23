.include "macros.s"  ! Include the macros file

.global vector_add
.global scalar_multiply
.global vector_subtract
.global dot_product
.global vector_norm
.global vector_distance

! ============================
! Vector Addition: u + v = result
! Parameters:
! o0 = size of vectors
! o1 = address of vector u
! o2 = address of vector v
! o3 = address of result




!!!!!!!!!!!!!!!!!! TEST




    u: .word 2, 3          ! Vector u = [2, 3]
    v: .word 4, 1          ! Vector v = [4, 1]
    result: .word 0, 0     ! Space for the result vector [0, 0]
    scalar: .word 2        ! Scalar value = 2

    .align 4               ! Align memory for result space


.global _start
_start:
    ! --------------------------
    ! Vector Addition: result = u + v
    ! --------------------------
    mov 8, %o0            ! Size of vector (2 elements*4)
    set u, %o1            ! Address of vector u
    set v, %o2            ! Address of vector v
    set result, %o3       ! Address of result vector
    call vector_add       ! Call vector_add routine
    nop

    ! Print result of vector addition
    !set result, %o0       ! Address of result vector
    !mov 4, %o1            ! Size of vector
    !call print_vector     ! Print the vector
    nop

    ! --------------------------
    ! Scalar Multiplication: result = scalar * u
    ! --------------------------
    mov 8, %o0            ! Size of vector
    set u, %o1            ! Address of vector u
    mov 5, %o2            ! Load scalar value into %o4
    set result, %o3       ! Address of result vector
 
    call scalar_multiply  ! Call scalar_multiply routine
    nop

    ! Print result of scalar multiplication
    !set result, %o0       ! Address of result vector
    !set 8, %o1            ! Size of vector
    !call print_vector     ! Print the vector
    nop

    ! --------------------------
    ! Vector Subtraction: result = u - v
    ! --------------------------
    set 8, %o0            ! Size of vector
    set u, %o1            ! Address of vector u
    set v, %o2            ! Address of vector v
    set result, %o3       ! Address of result vector

    !call vector_subtract  ! Call vector_subtract routine
    nop

    ! Print result of vector subtraction
    !!set result, %o0       ! Address of result vector
    !set 8, %o1            ! Size of vector
    !call print_vector     ! Print the vector
    nop

    ! Exit the program
    !mov 1, %g1            ! syscall: exit
    nop !ta 0

vector_add:
    sub %sp, 16, %sp            ! Allocate space on the stack for %l0-%l3
    st %l0, [%sp + 0]           ! Save %l0
    st %l1, [%sp + 4]           ! Save %l1
    st %l2, [%sp + 8]           ! Save %l2
    st %l3, [%sp + 12]          ! Save %l3

    clr %l0                     ! Clear index register (i = 0)

add_loop:
    ld [%o1 + %l0], %l1         ! Load u[i] into %l1
    ld [%o2 + %l0], %l2         ! Load v[i] into %l2
    add %l1, %l2, %l3           ! result[i] = u[i] + v[i]
    st %l3, [%o3 + %l0]         ! Store result in result[i]

    add %l0, 4, %l0             ! Increment i by 4 (int = 4 bytes)
    cmp %l0, %o0                ! Check if i < size
    bl add_loop                 ! Continue loop
    nop

    ld [%sp + 0], %l0           ! Restore %l0
    ld [%sp + 4], %l1           ! Restore %l1
    ld [%sp + 8], %l2           ! Restore %l2
    ld [%sp + 12], %l3          ! Restore %l3
    add %sp, 16, %sp            ! Deallocate stack space

    ret
    nop


! ============================
! Scalar Multiplication: scalar * u = result
! Parameters:
! o0 = size of vectors
! o1 = address of vector u
! o2 = scalar value (as an integer)
! o3 = address of result

scalar_multiply:
    sub %sp, 16, %sp            ! Allocate space on the stack for %l0-%l3
    st %l0, [%sp + 0]           ! Save %l0
    st %l1, [%sp + 4]           ! Save %l1
    st %l2, [%sp + 8]           ! Save %l2
    st %l3, [%sp + 12]          ! Save %l3

    clr %l0                     ! Clear index register (i = 0)

scalar_loop:
    ld [%o1 + %l0], %l1         ! Load u[i] into %l1
    mulscc %l1, %o2, %l2        ! result[i] = scalar * u[i] (using MULSCC)
    st %l2, [%o3 + %l0]         ! Store result in result[i]

    add %l0, 4, %l0             ! Increment i by 4
    cmp %l0, %o0                ! Check if i < size
    bl scalar_loop              ! Continue loop
    nop

    ld [%sp + 0], %l0           ! Restore %l0
    ld [%sp + 4], %l1           ! Restore %l1
    ld [%sp + 8], %l2           ! Restore %l2
    ld [%sp + 12], %l3          ! Restore %l3
    add %sp, 16, %sp            ! Deallocate stack space

    ret
    nop





! ============================
! Vector Subtraction: u - v = result
! Parameters:
! o0 = size of vectors
! o1 = address of vector u
! o2 = address of vector v
! o3 = address of result

vector_subtract:
    sub %sp, 8, %sp            ! Allocate space 
    st %o7, [%sp + 0]           ! Save %o7 (return address)
    st %o1, [%sp + 4]          

    ! Multiply vector v by -1 to get (-1 * v)
    mov %o2, %o1
    set -1, %o2                 ! Set scalar value to -1 
    call scalar_multiply        ! Call scalar_multiply(u = %o1, result = %o2, size = %o2, scalar = %o3)
    nop                         ! Delay slot (SPARC requirement)

    ld [%sp + 4], %o1          
    mov %o3, %o2    
    call vector_add             ! Call vector_add(u, v, result, size)
    nop                         ! Delay slot

    ld [%sp + 0], %o7           ! Restore %o7 (return address)
    add %sp, 8, %sp            ! Deallocate stack space
    ret
    nop
