import csv
import sys


def main():
    # ✅ Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # ✅ Read database file
    try:
        with open(sys.argv[1], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            database = list(reader)
            str_list = reader.fieldnames[1:]  # Exclude 'name'
    except FileNotFoundError:
        print("Database file not found.")
        sys.exit(1)

    # ✅ Read DNA sequence
    try:
        with open(sys.argv[2]) as file:
            dna_sequence = file.read()
    except FileNotFoundError:
        print("DNA sequence file not found.")
        sys.exit(1)

    # ✅ Count STRs
    str_counts = {}
    for STR in str_list:
        str_counts[STR] = longest_match(dna_sequence, STR)

    # ✅ Match against database
    for person in database:
        match = True
        for STR in str_list:
            try:
                if int(person[STR]) != str_counts[STR]:
                    match = False
                    break
            except ValueError:
                match = False
                break
        if match:
            print(person["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    sub_len = len(subsequence)
    seq_len = len(sequence)

    for i in range(seq_len):
        count = 0
        while sequence[i + count * sub_len:i + (count + 1) * sub_len] == subsequence:
            count += 1
        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
