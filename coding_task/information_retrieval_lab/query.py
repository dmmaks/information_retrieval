import sys
import getopt


class Node:
    def __init__(self, word):
        self.word = word
        self.freq = []
        self.next = None


def load_index(filename):
    head = Node("")
    current = head
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split()
            word = parts[0]
            frequencies = list(map(int, parts[1:]))

            new_node = Node(word)
            new_node.freq = frequencies

            current.next = new_node
            current = new_node

    return head.next


def load_filenames(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


def query(word, head, filenames):
    current = head
    while current:
        if current.word == word:
            frequencies = current.freq
            pairs = list(zip(frequencies, filenames))
            pairs.sort(reverse=True)
            for freq, filename in pairs:
                if freq > 0:
                    print(f"{freq} {filename}")
            return
        current = current.next

    print("Word not found in index")


def main(argv):
    index_filename = "index"
    filenames_filename = "filenames"

    try:
        opts, args = getopt.getopt(argv, "hn:i:", ["name=", "index="])
    except getopt.GetoptError:
        print('Incorrect input')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-n", "--name"):
            filenames_filename = arg
        elif opt in ("-i", "--index"):
            index_filename = arg

    filenames = load_filenames(filenames_filename)
    index_head = load_index(index_filename)

    if len(args) != 1:
        print("Please provide a single word to query")
        sys.exit(2)

    query(args[0], index_head, filenames)


if __name__ == "__main__":
    main(sys.argv[1:])
