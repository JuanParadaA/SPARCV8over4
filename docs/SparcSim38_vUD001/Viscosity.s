.global _start


_start:
    ! Initialize constants using define
    define (POSITION, 0)         ! Position (p) = 0 (scaled value)
    define (VELOCITY, 500)       ! Velocity (v) = 500 (initial velocity, scaled)
    define (VISCOSITY, 1000)     ! Viscosity (b) = 1000 (scaled)
    define (TIME_STEP, 100)      ! Time Step (dt) = 100 (scaled)
    define (NUM_STEPS, 10)       ! Number of simulation steps

    ! Load values into registers
    MOV POSITION, %l0         ! Position (p) = 0
    MOV VELOCITY, %l1         ! Velocity (v) = 500
    MOV VISCOSITY, %l2        ! Viscosity (b) = 1000
    MOV TIME_STEP, %l3        ! Time Step (dt) = 100
    MOV NUM_STEPS, %l4        ! Loop counter for steps (n = 10)

loop:
    ! Calculate force = -b * v
    ! force = -1 * (b * v)
    mulscc %l2, %l1, %l5      ! force = b * v, store result in %l5
    sub %g0, %l5, %l5         ! force = -force (negate the result)

    ! Update the velocity v = v + force * dt
    ! v = v + (force * dt)
    mulscc %l5, %l3, %l6      ! force * dt -> store in %l6
    add %l1, %l6, %l1         ! v = v + (force * dt)

    ! Update the position p = p + v * dt
    ! p = p + (v * dt)
    mulscc %l1, %l3, %l7      ! v * dt -> store in %l7
    add %l0, %l7, %l0         ! p = p + (v * dt)

    ! Decrement loop counter
    sub %l4, 1, %l4           ! n = n - 1
    cmp %l4, 0                ! Check if n == 0
    bne loop                  ! If n != 0, continue the loop
    nop

    ! End of simulation
    ba end_simulation         ! Branch to end_simulation
    nop

end_simulation:
    ! Exit the program
    mov 0, %g1                ! Exit status 0
    nop !ta 0                      ! Trap to exit the program
