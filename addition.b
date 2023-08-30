#H=1 #D=7 #L=0 #B=1 #C=2 #C'=3 #T=4 E=5 #R=6
H is the size of the header
D is the block size per digit place
Inside the block here are the digit offsets
L is the digit flag indicating the presence of a digit
B is the first operand digit
C is the second operand digit
C' is the complement of C aka (9 minus C)
T is the 

//mark a blocks
> shift to l0 (right H)
, read na
[ while li
    - li minus 1
    [ while li
        >>>>>>> right D
        + lip1 add 1
        <<<<<<< left D
        - li minus 1
    ]
    + li add 1

    //configure c'
    >>> right C'
    +++++++++ c' add 9

    >>>> right D; right LmC'
] &

//read a digits
<<<<<<< left D
[ while li
    > right B
    , read ai //into slot bi then copy to ci
    [ while ai
        > right CmB
        + ci add 1
        > right C'mC
        - c'i minus 1
        << right BmC'
        - ai minus 1
    ]
    < left B
    <<<<<<< left D
]

//mark b blocks
>>>>> shift to t0 (right H; right T)
, read nb
[ while ti
    - ti minus 1
    [ while ti
        >>>>>>> right D
        + tip1 add 1
        <<<<<<< left D
        - ti minus 1
    ]
    >>>>>>> right D
]

<<<<<<< left D
<<<< right LmT
[ while li
    > right B
    , read bi
    < left B
    <<<<<<< left D
]

//add all digits
> shift to l0
[ while li
#
    > right BmL

    //add b to c
    [ while bi
        >>> right TmB
        + ti add 1 //ti should be 1 now
        < right C'mT
        [ if c'i //while
            > right TmC'
            - ti minus 1 //ti should be 0 now
        ]
        > right 1 (to get off 0)
        [ while not E
            > right 1
        ]

        << right C'mE
        - c'i minus 1
        < right CmC'
        + ci add 1

        >> right TmC
        [ if ti //while
            - ti minus 1
            >> right RmT
            + ri add 1
            <<< right C'mR
            +++++++++ c'i add 9
            < right CmC'
            --------- ci minus 9
            >> right TmC
        ]

        <<< right BmT
        - bi minus 1
    ] &

    //add ri to cip1
    >>>>> right RmB
    [ if ri //while
        //check overflow
        >>>>> right TmR; right D
        + ti add 1 //ti should be 1 now
        < right C'mT
        [ if c'i //while
            > right TmC'
            - ti minus 1 //ti should be 0 now
        ]
        > right 1 (to get off 0)
        [ while not E
            > right 1
        ]

        << right C'mE
        - c'i minus 1
        < right CmC'
        + ci add 1

        >> right TmC
        [ if ti //while
            - ti minus 1
            >> right RmT
            + ri add 1
            <<< right C'mR
            +++++++++ c'i add 9
            < right CmC'
            --------- ci minus 9
            >> right TmC
        ]

        <<<<< left D; right RmT
        - ri minus 1
    ] &

    //next digit
    > right D; right LmR
] &

//check if leading 0
+ li add 1 //ensure digit is valid
>> right CmL
[ if ci //while
    >>>>>>> right D
] &

<<<<<<< left D
<< right LmC

//print digits
[ while li
    >> right CmL
    . print ci
    << right LmC
    <<<<<<< left D
]