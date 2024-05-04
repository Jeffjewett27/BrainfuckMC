input is digits low to high

digits are ordered low to high every other mem cell
each digit preceded by a flag
first two spots empty

>>>
>>+<< setup empty input check
,[<+>>>,#] read all input
>>[<+>>>>>]<<
<<<#
[
    [>.<<<] print every other descending every digit
    >>
    [
        -> remove flag_i and go to digit_i
        [ if d_i was greater than 0
            <++>-  f_i=2 and decrement d_i
            [ if d_i was greater than 1
                <++>- f_i=4 and decrement d_i
                [ if d_i was greater than 2
                    <++>- f_i=6 and decrement d_i
                    [ if d_i was greater than 3
                        <++>- f_i=8 and decrement d_i
                        [ if d_i was greater than 5
                            <-------->> clear f_i (f_i=0)
                            - clear next flag f_ip1
                            ++<- f_ip1=2 and decrement d_i
                            [ f_i=2*(d_i minus 5)
                                <++>- f_i plus 2
                            ]
                        ]
                    ]
                ]
            ]
        ]
        <
        [ move f_i to d_i
            >+<-
        ]
        +>> f_i=1 go to next i
    ]
    | clear the screen/new line
    <<
]