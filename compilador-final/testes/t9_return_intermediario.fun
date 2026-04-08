fun test_return(x) {
  if (x < 0) {
    return 10;
  } else {
    if (x == 0) {
      return 20;
    } else {
      return 30;
    }
  }
  return 0;
}

main {
  return test_return(0 - 1) + test_return(1);
}
