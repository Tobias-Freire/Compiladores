#
# modelo de saida para o compilador
#

  .section .text
  .globl _start

_start:
  mov $11, %rax
  push %rax
  mov $912, %rax
  pop %rbx
  imul %rbx, %rax
  push %rax
  mov $33, %rax
  pop %rbx
  add %rbx, %rax

  call imprime_num
  call sair

  .include "runtime.s"
