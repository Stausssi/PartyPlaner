class Statistik:
    fun_per_iter = []

    @staticmethod
    def save_iteration_stats(avg):
        Statistik.fun_per_iter.append(avg)

    @staticmethod
    def reset_iteration_stats():
        Statistik.fun_per_iter = []

    @staticmethod
    def party_fun_value(fun_list=None) -> float:
        if fun_list is None:
            fun_list = [123, 321, 123, 321]

        return Statistik.calc_average_som(fun_list)

    @staticmethod
    def calc_average_som(list_som) -> float:
        sum_som = 0
        for som in list_som:
            sum_som += som

        avg = sum_som / len(list_som)
        Statistik.save_iteration_stats(avg)
        return sum_som / len(list_som)

