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
! i0 = size of vectors
! i1 = address of vector u
! i2 = address of vector v
! i3 = address of result


vector_add:
    sub %sp, 16, %sp            ! Allocate space on the stack for %l0-%l3
    st %l0, [%sp + 0]           ! Save %l0
    st %l1, [%sp + 4]           ! Save %l1
    st %l2, [%sp + 8]           ! Save %l2
    st %l3, [%sp + 12]          ! Save %l3

    clr %l0                     ! Clear index register (i = 0)

add_loop:
    ld [%i1 + %l0], %l1         ! Load u[i] into %l1
    ld [%i2 + %l0], %l2         ! Load v[i] into %l2
    add %l1, %l2, %l3           ! result[i] = u[i] + v[i]
    st %l3, [%i3 + %l0]         ! Store result in result[i]

    add %l0, 4, %l0             ! Increment i by 4 (int = 4 bytes)
    cmp %l0, %i0                ! Check if i < size
    bl add_loop                 ! Continue loop
    nop

    ld [%sp + 0], %l0           ! Restore %l0
    ld [%sp + 4], %l1           ! Restore %l1
    ld [%sp + 8], %l2           ! Restore %l2
    ld [%sp + 12], %l3          ! Restore %l3
    add %sp, 16, %sp            ! Deallocate stack space

    retl
    nop


! ============================
! Scalar Multiplication: scalar * u = result
! Parameters:
! i0 = size of vectors
! i1 = address of vector u
! i2 = scalar value (as an integer)
! i3 = address of result

scalar_multiply:
    sub %sp, 16, %sp            ! Allocate space on the stack for %l0-%l3
    st %l0, [%sp + 0]           ! Save %l0
    st %l1, [%sp + 4]           ! Save %l1
    st %l2, [%sp + 8]           ! Save %l2
    st %l3, [%sp + 12]          ! Save %l3

    clr %l0                     ! Clear index register (i = 0)

scalar_loop:
    ld [%i1 + %l0], %l1         ! Load u[i] into %l1
    smul %l1, %i2, %l2        ! result[i] = scalar * u[i] (using MULSCC)
    st %l2, [%i3 + %l0]         ! Store result in result[i]

    add %l0, 4, %l0             ! Increment i by 4
    cmp %l0, %i0                ! Check if i < size
    bl scalar_loop              ! Continue loop
    nop

    ld [%sp + 0], %l0           ! Restore %l0
    ld [%sp + 4], %l1           ! Restore %l1
    ld [%sp + 8], %l2           ! Restore %l2
    ld [%sp + 12], %l3          ! Restore %l3
    add %sp, 16, %sp            ! Deallocate stack space

    retl
    nop

! ============================
! Scalar Division: (1/scalar) * u = result
! Parameters:
! i0 = size of vectors
! i1 = address of vector u
! i2 = scalar value (as an integer)
! i3 = address of result

scalar_div:
    sub %sp, 16, %sp            ! Allocate space on the stack for %l0-%l3
    st %l0, [%sp + 0]           ! Save %l0
    st %l1, [%sp + 4]           ! Save %l1
    st %l2, [%sp + 8]           ! Save %l2
    st %l3, [%sp + 12]          ! Save %l3

    clr %l0                     ! Clear index register (i = 0)

div_loop:
    ld [%i1 + %l0], %l1         ! Load u[i] into %l1
    sdiv %l1, %i2, %l2        ! result[i] = scalar * u[i] (using MULSCC)
    st %l2, [%i3 + %l0]         ! Store result in result[i]

    add %l0, 4, %l0             ! Increment i by 4
    cmp %l0, %i0                ! Check if i < size
    bl div_loop              ! Continue loop
    nop

    ld [%sp + 0], %l0           ! Restore %l0
    ld [%sp + 4], %l1           ! Restore %l1
    ld [%sp + 8], %l2           ! Restore %l2
    ld [%sp + 12], %l3          ! Restore %l3
    add %sp, 16, %sp            ! Deallocate stack space

    retl
    nop





! ============================
! Vector Subtraction: u - v = result
! Parameters:
! i0 = size of vectors
! i1 = address of vector u
! i2 = address of vector v
! i3 = address of result

vector_subtract:
    sub %sp, 8, %sp            ! Allocate space 
    st %o7, [%sp + 0]           ! Save %o7 (return address)
    st %i1, [%sp + 4]          

    ! Multiply vector v by -1 to get (-1 * v)
    mov %i2, %i1
    set -1, %i2                 ! Set scalar value to -1 
    call scalar_multiply        ! Call scalar_multiply(u = %o1, result = %o2, size = %o2, scalar = %o3)
    nop                         ! Delay slot (SPARC requirement)

    ld [%sp + 4], %i1          
    mov %o3, %i2    
    call vector_add             ! Call vector_add(u, v, result, size)
    nop                         ! Delay slot

    ld [%sp + 0], %o7           ! Restore %o7 (return address)
    add %sp, 8, %sp            ! Deallocate stack space
    retl
    nop


    v_i:    .word 10, 20   ! Initial velocity (vx, vy)
    a:      .word 0, -1  ! Acceleration (ax, ay)
    v_f:    .word 0, 0   ! Final velocity (output)
    pos:    .word 0, 0   ! Position (output)
    define (t, 1)





!=========================================

.global _start

_start:
    mov  8, %i0          ! Size (2D vector, 2 elements * 4 bytes each)
    set v_i, %i1         ! Address of initial velocity vector
    set a, %i2           ! Address of acceleration vector
    mov t, %i3           ! Load scalar time
    set v_f, %i4         ! Address of final velocity result
    set pos, %i5         ! Address of position result

    call vector_motion   ! Call vector motion function
    nop

    ! Exit program
    !mov 1, %g1           ! syscall: exit
    !mov 0, %o0           ! status: 0
    !ta  0                ! Trap to OS
    nop
     
! ============================
! Vector Motion Calculation
! Calculates v_f = v_i + a * t
! Calculates pos = v_i * t + (a * t * t) / 2
! Parameters:
! i0 = size of vectors
! i1 = address of vector v_i (initial velocity)
! i2 = address of vector a (acceleration)
! i3 = scalar value t (time as an integer)
! i4 = address of vector v_f (final velocity result)
! i5 = address of vector pos (position result)

vector_motion:
    ! Allocate space on the stack for temporary storage
    sub %sp, 4, %sp            ! Allocate space 
    st %o7, [%sp + 0]          ! Save %o7 (return address)
    sub %sp, %i0, %sp          ! Allocate temp_vec1 (size = %i0)
    mov %sp, %l6               ! temp_vec1 = %l6
    sub %sp, %i0, %sp          ! Allocate temp_vec2 (size = %i0)
    mov %sp, %l7               ! temp_vec2 = %l7
    sub %sp, 12, %sp           ! Allocate space 
    st %i1, [%sp + 0]          ! v_i
    st %i2, [%sp + 4]          ! a
    st %i3, [%sp + 8]          ! t

    ! Compute v_f = v_i + a * t
    ld [%sp + 4], %i1           ! Pass acceleration vector
    ld [%sp + 8], %i2           ! Pass scalar t
    mov %l6, %i3                ! Store in temp_vec1
    call scalar_multiply        ! Compute a * t
    nop                         ! Delay slot
    ld [%sp + 0], %i1           ! Pass v_i vector
    mov %l6, %i2                ! Pass computed a * t
    mov %i4, %i3                ! Store result in v_f
    call vector_add             ! Compute v_f = v_i + temp_vec1
    nop                         ! Delay slot

    ! Compute pos = v_i * t + (a * t * t) / 2
    ld [%sp + 0], %i1           ! Pass v_i vector
    ld [%sp + 8], %i2           ! Pass scalar t
    mov %l6, %i3                ! Store in temp_vec1 (reuse)
    call scalar_multiply        ! Compute v_i * t
    nop                         ! Delay slot

    ld [%sp + 4], %i1           ! Pass acceleration vector
    ld [%sp + 8], %i2           ! Pass scalar t
    mov %l7, %i3                ! Store in temp_vec2
    call scalar_multiply        ! Compute a * t
    nop
    mov %l7, %i1               ! Pass temp_vec2
    ld [%sp + 8], %i2           ! Pass scalar t
    mov %l7, %i3                ! Store in temp_vec2
    call scalar_multiply        ! Compute a * t * t
    nop                         ! Delay slot
    mov %l7, %i1                ! Pass temp_vec2
    mov  2, %i2                 ! Pass scalar 2
    mov %l7, %i3                ! Store in temp_vec2
    call scalar_div        ! Compute (a * t * t) / 2
    nop                         ! Delay slot
 
    mov %l6, %i1                ! Pass computed v_i * t
    mov %l7, %i2                ! Pass computed (a * t * t) / 2
    mov %i5, %i3                ! Store result in pos
    call vector_add             ! Compute pos = temp_vec1 + temp_vec2
    nop                         ! Delay slot

    ! Restore stack
    add %sp, 12, %sp            ! free vi,a,t
    add %sp, %i0, %sp           ! Free temp_vec2
    add %sp, %i0, %sp           ! Free temp_vec1

    ld [%sp + 0], %o7           ! Restore %o7 (return address)
    add %sp, 8, %sp            ! Deallocate stack space
    retl
    nop
