.global	_start
_start:
	MOV 5, %o1

exp:	! %o1 = n
	! %o2 = e^n
	MOV 1, %l2
	MOV 1, %l3
	MOV 1, %l4
	MOV 1, %l5
	MOV 1, %o2

ciclo:	TST %l5
	BE fin 
	NOP
	
  SMUL %l3, %o1, %l3
  SMUL %l4, %l2, %l4
  SDIV %l3, %l4, %l5
  ADD  %o2, %l5, %o2

  ADD %l2,1, %l2

	BA ciclo 
	NOP
	
fin:	NOP 



nop 
