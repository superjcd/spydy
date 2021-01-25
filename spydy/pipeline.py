'''
使用时 
   每一个过程step_class， 如果发生问题如何recover(定义recover: 1 完全忽略  2 把url加到队列的末尾 3 有条件的加入（这部分的逻辑交个使用者？） )
  step: 
    1 recover (step_class)
    2 step_class.recover("url")

'''