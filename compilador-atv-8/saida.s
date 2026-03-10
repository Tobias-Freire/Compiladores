#
# modelo de saida para o compilador
#

  .section .text
  .globl _start

_start:
  mov $2, %rax
  push %rax
  mov $8, %rax
  pop %rbx
  sub %rbx, %rax
  push %rax
  mov $10, %rax
  pop %rbx
  sub %rbx, %rax

  call imprime_num
  call sair

  .include "runtime.s"
