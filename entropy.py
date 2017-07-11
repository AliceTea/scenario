import numpy as np


class entropy:

    def __init__(self):
        pass

    def calc_ent(self,x):
        """
            calculate shanno ent of x
        """

        x=np.array(x)
        x_value_list = set([x[i] for i in range(x.shape[0])])
        ent = 0.0
        for x_value in x_value_list:
            p = float(x[x == x_value].shape[0]) / x.shape[0]
            logp = np.log2(p)
            ent -= p * logp

        return ent
   
    def calc_condition_ent(self,x, y):
        """
            calculate ent H(y|x)
        """

        # calc ent(y|x)
        x=np.array(x)
        y=np.array(y)
        x_value_list = set([x[i] for i in range(x.shape[0])])
        ent = 0.0
        for x_value in x_value_list:
            sub_y = y[x == x_value]
            temp_ent = self.calc_ent(sub_y)
            ent += (float(sub_y.shape[0]) / y.shape[0]) * temp_ent

        return ent

    def calc_ent_grap(self,x,y):
        """
            calculate ent grap
        """

        x=np.array(x)
        y=np.array(y)
        base_ent = self.calc_ent(y)
        condition_ent = self.calc_condition_ent(x, y)
        ent_grap = base_ent - condition_ent

        return ent_grap
