! Para comentarios se usa !

!A continuación se hace un programa a que
!multiplica tres matrices D=ABC. 

!Primero multiplica E=AB y luego D=EC.

!las etiquetas MA,MB,MC,MD,ME son constantes
! con las posiciones donde comienzan cada una
! de las matrices.

.global	_start 
 _start:
	MOV %g1,MA 	!--A
	MOV %g2,MB	!--B
	MOV %g3,ME 	!--E
	CALL MULT	!--E=AB
	NOP
	MOV %g1,ME 	!--E
	MOV %g2,MC 	!--C
	MOV %g3,MD 	!--D
	CALL MULT	!--D=EC
	NOP

FIN:	BA FIN
	NOP

!A continuación se escribe la rutina MULT

MULT:
!-- para i
	MOV %g4,0
ciclo_i:	CMP %g4,3
	BE fin_i
	NOP


!para j
	MOV %g5,0
	
ciclo_j:	CMP %g5,3
	BE fin_j
	NOP



!--para k
	MOV %g6,0
	 MOV %o1,0
ciclo_k: 	CMP %g6,3
	BE fin_k
	NOP
!   --a_ik
	   UMUL %o2,%g4,3
	   ADD %o2,%o2,%g6 
	   UMUL %o2,%o2,4
	   LD %g7,[%g1+%o2]
!    --b_kj
	   UMUL %o2,%g6,3
	   ADD %o2,%o2,%g5
	   UMUL %o2,%o2,4
	   LD %o0,[%g2+%o2]
!   --sum
	   SMUL %o2,%g7,%o0
	   ADD %o1,%o1,%o2
   
	ADD %g6,%g6,1
	BA ciclo_k
	NOP
fin_k:	!--c_ij
	UMUL %o2,%g4,3
	ADD %o2,%o2,%g5
	UMUL %o2,%o2,4
       	ST %o1,[%g3+%o2]



	
	ADD %g5,%g5,1
	BA ciclo_j
	NOP
fin_j:



	ADD %g4,%g4,1
	BA ciclo_i
	NOP
fin_i:	RETL
	NOP


!A continuación se dan unos comandos para 
!que las direcciones comiencen desde cero y no de 
!0x000040C8 

ultimo: !esta etiqueta queda con 
        !la posición actual (0x0x000040C8)

.skip -ultimo !este comando indica que
              !cambie las direcciones 


!A continuación se colocan los datos de cada una
!de las matrices.

MA:
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
MB:
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
MC:
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
MD:
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
ME:
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1
 .word 2
 .word 1
 .word 0
 .word 1