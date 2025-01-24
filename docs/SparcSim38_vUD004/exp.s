.global	_start
_start:
	MOV  %o1,5

exp:	! %o1 = n
	! %o2 = e^n
	MOV %l2, 1
	MOV %l3, 1
	MOV %l4, 1
	MOV %l5, 1
	MOV %o2, 1

ciclo:	TST %l5
	BE fin 
	NOP
	
  SMUL %l3, %l3, %o1
  SMUL %l4, %l4, %l2
  SDIV %l5, %l3, %l4
  ADD  %o2, %o2, %l5

  ADD %l2,%l2,1 

	BA ciclo 
	NOP
	
fin:	NOP 



nop 
