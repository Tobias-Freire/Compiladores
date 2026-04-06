var base = 10;

fun quadrado(x) {
    return x * x;
}

fun soma_quadrados(a, b) {
    var qa = 0;
    var qb = 0;
    qa = quadrado(a);
    qb = quadrado(b);
    return qa + qb;
}

main {
    return soma_quadrados(3, 4);
}
