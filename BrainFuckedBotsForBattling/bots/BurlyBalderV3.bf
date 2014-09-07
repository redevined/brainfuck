>((-)*18>)*2                                  Make two minus seventeen decoys
(->)*6                                        Move to cell nine

[                                             special case for ten cell game 
   +[+[+[+[+[+[+[+[+[+[+[+[+[+[+[+[+[+[       if not minus one to minus eighteen 
   (-)*18                                     decrease by eighteen
   -[-[-[-[-[-[-[-[-[-[-[-[-[-[-[-[-[-[       if not plus one to plus eighteen
       (-)*107                                decrease by hundred and seven
       [-.]                                   slow clear
   ]]]]]]]]]]]]]]]]]]                         end plus conditionals
   ]]]]]]]]]]]]]]]]]]                         end minus conditionals
]                                             end special case
+
([>                                           while true go right
  [                                           start clear cell 
   +[+[+[+[+[+[+[+[+[+[+[+[+[+[+[+[+[+[       if not minus one to minus eighteen 
   (-)*18                                     decrease by eighteen
   -[-[-[-[-[-[-[-[-[-[-[-[-[-[-[-[-[-[       if not plus one to plus eighteen
       (-)*107                                decrease by hundred and seven
       [-.]                                   slow clear
   ]]]]]]]]]]]]]]]]]]                         end plus conditionals
   ]]]]]]]]]]]]]]]]]]                         end minus conditionals
  ]                                           end clear cell
  --                                          set to minus two 
 ]                                            while true end
 -                                           decrease and loop
)*5