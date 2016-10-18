# LiuD_Lesson_2
LiuD lesson two

We can describe GDL with GDL itself:

    main = (stmt NEWLINE)*
    stmt = NAME '=' stmt_value
    stmt_value = values_or | jiap | series
        values_or = NAME ^+ '|'
        series = value*
        jiap = NAME '^+' STRING

    value0 = NAME | STRING
    value1 = value0 ｜ enclosed
        enclosed = '(' stmt_value ')'
    value = itemd | value0
        itemd = value0 '*'


add a new syntax:

    A ^+ B means ABAB..A , thats is A separated by B. at least one B

add 2 base item:

    NEWLINE means '\n'. We assume it can be neglected, do not need a record in AST.
    STRING means string enclosed by '', can test if match Python RE pattern r"'[^'\\]*(?:\\.[^'\\]*)*'"

skip space on each step.

Lets write the parse code
