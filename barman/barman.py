                                            # Задача о роботе-бармене
from pyke import knowledge_engine

def main():
    my_engine = knowledge_engine.engine('bases');
    my_engine.activate('barman_r');
    
    start = 'Robot3'; # Здесь задаётся начальная ситуация (описание возможных смотрите в файле barman_f)
    
    my_engine.assert_('barman_f', start, (True,));   
    
    if (start == 'Robot9'):
        final = True;
    else:
        final = False;
    
    if ((start == 'Robot5') or  (start == 'Robot6') or (start == 'Robot7')):
        glasses = [1,1,1,1]; # Здесь задаётся вектор стаканов (для данных ситуаций все стаканы полны), 
                             # по желанию можно увеличить размер вектора (в зависимости от того сколько стаканов)
    else:
        glasses = [0,0,0,0]; # Здесь задаётся вектор стаканов для остальных ситуаций (0 - если стакан пуст, 1 - если заполнен)
                             # по желанию можно увеличить размер вектора (в зависимости от того сколько стаканов)
    
    if not final:
        nGlasses = len(glasses);
        
        for i in range(nGlasses):
            if (glasses[i] == 0):
                if (start == 'Robot'):
                    my_engine.prove_1_goal('barman_r.robot_grasp_shaker()')[1](i);
                elif (start == 'Robot1'):
                    my_engine.prove_1_goal('barman_r.robot_dispense()')[1](i);
                elif (start == 'Robot2'):
                    my_engine.prove_1_goal('barman_r.robot_shake()')[1](i);
                else:
                    break;
                print('\n');
                glasses[i] = 1;
                break;           
        
        if ((start != 'Robot') and (start != 'Robot1')):
            my_engine.assert_('barman_f', 'Robot1', (True,));
            
        for i in range(nGlasses):
            if (glasses[i]==0):
                my_engine.prove_1_goal('barman_r.robot_dispense()')[1](i);
                print('\n');
                glasses[i] = 1;
        
        if ((start != 'Robot5') and (start != 'Robot6') and (start != 'Robot7')):
            if (start != 'Robot8'):
                my_engine.assert_('barman_f', 'Robot8', (True,));
            my_engine.prove_1_goal('barman_r.robot_put_shaker()')[1](0);
        elif (start == 'Robot6'):
            my_engine.assert_('barman_f', 'Robot5', (True,));
            my_engine.prove_1_goal('barman_r.robot_give_glass()')[1](0);
        elif (start == 'Robot5'):
            my_engine.prove_1_goal('barman_r.robot_grasp_glass()')[1](0);
        else:
            my_engine.assert_('barman_f', 'Robot5', (True,));
            my_engine.prove_1_goal('barman_r.robot_grasp_glass()')[1](0);
        print('\n');
        
        for i in range(1,nGlasses):
            my_engine.prove_1_goal('barman_r.robot_grasp_glass()')[1](i);
            print('\n');
                
        my_engine.assert_('barman_f', 'Robot9', (True,));
        my_engine.prove_1_goal('barman_r.final()')[1]();
    else:
        my_engine.prove_1_goal('barman_r.final()')[1]();
        
        
if (__name__ == "__main__"):
    main()