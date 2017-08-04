import numpy
import numpy.random as nr
import random
import string

random.seed(1)
target_string_length = 16
mutation_probability = 0.9
max_generations = 1000000
selection_threshold = 0.2

# Supplementary Functions
def random_string_generator():
    """
    This function should return a string made up ascii characters
    :return:  A random string of ascii characters
    """
    return ''.join(random.choice(string.ascii_letters+string.digits) for letter in range(target_string_length))


def string_comparison(test_string, target_string):
    """
    Function describing how many letters of the target string the test string correctly predicted.
    Which letters were predicted is not relevant in this case.
    :param test_string: The string the algorithm has predicted
    :param target_string: The string the algorithm is trying to predict
    :return: The number of letters guessed correctly.
    """
    count = 0
    for index, letter in enumerate(test_string):
        if test_string[index] == target_string[index]:
            count += 1
    return count


# Genetic Algorithm Functions
def generate_initial_candidates(pop_size):
    """
    Function to generate the initial pop_size candidates
    :param pop_size: the number of candidates to generate initially
    :return: candidates: a list of candidates
    """
    initial_candidates = list()
    for i in range(pop_size):
        initial_candidates.append(random_string_generator())
    return initial_candidates


def evaluation(candidate_list, target_string):
    """
    Function to evaluate how closely the candidates matched the target string
    :param candidate_list: A list of all candidates for the target string
    :param target_string: The target string itself
    :return: candidates : The top selection threshold*100 of candidates
    :return: target_string_found: None, unless the string is found, in which case the target string
    """
    candidate_scores = list()
    target_string_found = None

    for cand in candidate_list:

        candidate_score = string_comparison(cand, target_string)
        candidate_scores.append([cand, candidate_score])

        if candidate_score == len(target_string):
            target_string_found = cand

    candidates = selection(candidate_scores)

    return candidates, target_string_found


def selection(candidate_scores):
    """
    Returns top 20% of candidates
    :param candidate_scores: A sorted list of 2 element lists where the first element is the candidate and
    the second element is the score
    :return: top_candidates: a reduced list of the best candidates (without their scores)
    """
    candidate_scores = sorted(candidate_scores, key=lambda x: x[1], reverse=True)
    cut_off = int(round(selection_threshold * len(candidate_scores)))
    return candidate_scores[:cut_off]


def crossover(parent_1, parent_2):
    """
    Function to perform crossover between two parents. Have chosen to use uniform crossover - this means that there is
    a 50% chance that a gene from each parent will be selected, for all genes
    :param parent_1: The first good candidate
    :param parent_2: The second good candidate
    :return: child: The result of crossing over the parents genes.
    """
    child_chromasome = ''
    for gene_index in range(len(parent_1[0])):
        # print (random.choice([parent_1[0][gene_index], parent_2[0][gene_index]]))
        child_chromasome += (random.choice([parent_1[0][gene_index], parent_2[0][gene_index]]))
    return child_chromasome


def mutation(child):
    """
    Function to mutate genes within a certain child. Mutation probability is a global variable.
    :param child: The child candidate; that is the result of the crossover of two high scoring candidates
    :return: child: The child candidate after (possibly) having some genes mutated
    """
    for gene_index, gene in enumerate(child):
        if random.random() < mutation_probability:
            child = child[:gene_index] + random.choice(string.ascii_uppercase+string.digits) + child[gene_index+1:]
    return child


def ga_find_string(target_string, number_of_candidates):
    """
    Generate list of initial candidates
    For gen < max_generations:
        Evaluate the candidates
        If a candidate_score == len(target_string):
            break
        Select the strongest
        Perform crossover until back to original pop_size
        Mutate all children, but not parents (to save time)

    :param target_string: The string to be found
    :param number_of_candidates: the number of candidates to try and find the target string
    :return: final_string: The final string produced by the algorithm, and its score.
    """
    generation_candidates = generate_initial_candidates(number_of_candidates)

    target_string_found = None

    for gen in range(max_generations):

        # Test candidates
        fittest_candidates, target_string_found = evaluation(generation_candidates, target_string)
        # print gen, fittest_candidates

        # Finish loop if target string is found
        if target_string_found:
            break

        # Make more new candidates via crossover/mutation
        generation_candidates = [candidate[0] for candidate in fittest_candidates]
        while len(generation_candidates) < number_of_candidates:
            generation_candidates.append(mutation(crossover(random.choice(fittest_candidates), random.choice(fittest_candidates))))

        print gen# , fittest_candidates[0:4], target_str

    return target_string_found


target_str = random_string_generator()
num_candidates = 1000

string_found_by_ga = ga_find_string(target_str, num_candidates)

print target_str, string_found_by_ga