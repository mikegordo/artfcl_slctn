# This module is written using Cursor IDE with AI tool
# AI was responsible for writing function bodies as well as comments

class Comparator:
    
    # This function calculates the similarity between two strings using the Levenshtein distance algorithm
    def string_similarity(self, s1, s2):
        # If s1 is shorter than s2, swap them
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        if len(s1) == 0:
            return 1.0
        # Calculate the similarity using the Levenshtein distance algorithm
        return (len(s1) - self.levenshtein_distance(s1, s2)) / len(s1)
    
    # This function calculates the Levenshtein distance between two strings
    @staticmethod
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Calculate the cost of insertions, deletions, and substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                # Append the minimum cost to the current row
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
