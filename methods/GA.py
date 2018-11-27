# _*_ coding:utf-8 _*_

import random


class GA(object):
    """
    遗传算法
    """

    def __init__(self, gene_length, population_nums=100, cross_prob=0.8, mutation_prob=.03, match_fun=lambda gene:1):
        self.gene_length = gene_length
        self.population_nums = population_nums
        self.cross_prob = cross_prob
        self.mutation_prob = mutation_prob
        self.match_fun = match_fun
        self.generation = 0
        self.total_score = 0.0
        self.best = None
        self.elites = None
        self.elites_num = 20

        self.init_population()

    def init_population(self):
        """
        种群初始化
        :return: 初始化种群
        """
        self.population = []
        for i in range(self.population_nums):
            gene = list(range(self.gene_length))
            random.shuffle(gene)
            self.population.append(Life(gene))
        self.evaluate()

    def evaluate(self):
        self.total_score = 0.0
        for p in self.population:
            p.score = self.match_fun(p.gene)
            self.total_score = self.total_score + p.score

        self.elites = sorted(self.population, key=lambda x:x.score, reverse=True)
        self.best = self.elites[0]

    def cross(self, parent1, parent2):
        """
        交叉运算
        :param parent1: 父代1
        :param parent2: 父代2
        :return: 子代
        """
        i1 = random.randint(0, self.gene_length - 1)
        i2 = random.randint(i1, self.gene_length - 1)
        temp_gene = parent2.gene[i1:i2]
        next_gene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == i1:
                next_gene.extend(temp_gene)
                p1len += 1
            if g not in temp_gene:
                next_gene.append(g)
                p1len += 1
        return next_gene

    def mutation(self, gene, method='order'):
        """
        变异运算
        :param gene: 要进行变异的基因
        :return: 变异后的新基因
        """
        if method == 'order':
            i1 = random.randint(0, self.gene_length - 1)
            i2 = random.randint(0, self.gene_length - 1)
            gene[i1], gene[i2] = gene[i2], gene[i1]
        elif method == 'shuffle':
            i1 = random.randint(0, self.gene_length - 2)
            i2 = random.randint(i1+1, self.gene_length - 1)
            temp_gene = gene[i1:i2]
            random.shuffle(temp_gene)
            gene[i1:i2] = temp_gene
        elif method == 'position':
            i1 = random.randint(0, self.gene_length - 1)
            i2 = random.randint(0, self.gene_length - 1)
            # TODO 完善基于位置的变异算子
        return gene

    def select(self):
        """
        选择算子
        按照赌盘轮转法选择个体
        :return: 返回被选择的一个个体
        """
        r = random.uniform(0, self.total_score)
        for life in self.population:
            r -= life.score
            if r <= 0:
                return life

    def generate_one(self):
        """
        对选择的一个个体
        根据概率cross_prob进行交叉运算
        根据概率mutation_prob进行变异运算
        :return: 下一代种群的一个个体
        """
        parent1 = self.select()

        if random.random() < self.cross_prob:
            parent2 = self.select()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene

        if random.random() < self.mutation_prob:
            gene = self.mutation(gene, method='order')

        return Life(gene)

    def generate_next(self):
        """
        产生下一代种群
        :return: 将当前种群更新为下一代种群
        """
        next_population = []
        next_population.extend(self.elites[0:self.elites_num])

        while len(next_population) < self.population_nums-self.elites_num:
            next_population.append(self.generate_one())
        self.population = next_population
        self.generation += 1
        self.evaluate()

    def finished(self):
        """
        判断遗传算法是否终止
        :return: True or False
        """
        return self.generation < 3000

    def evolution(self):
        """
        遗传算法演化过程
        :return: 演化结束后的最优种群
        """
        while self.finished():
            self.generate_next()
            print("generation: {}".format(self.generation))
            print(1.0 / self.best.score)
        return self.population


class Life(object):
    """
    种群中的个体
    """

    def __init__(self, mGene=None, mScore=-1):
        self.gene = mGene
        self.score = mScore
