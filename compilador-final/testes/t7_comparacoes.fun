var dummy = 0;
var a = 0;
main {
  if (10 <= 10) { a += 1; } else { a += 0; }
  if (10 >= 5) { a += 2; } else { a += 0; }
  if (10 != 5) { a += 4; } else { a += 0; }
  if (5 <= 2) { a += 0; } else { a += 8; }
  return a;
}
