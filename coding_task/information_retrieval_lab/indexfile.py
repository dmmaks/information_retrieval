import getopt
import sys
import string


class Node:
    def __init__(self, word):
        self.word = word
        self.freq = []
        self.next = None


def add_word_to_sorted_linked_list(head, word):
    new_node = Node(word)

    if not head or head.word > word:
        new_node.next = head
        return new_node

    current = head
    while current.next and current.next.word < word:
        current = current.next

    new_node.next = current.next
    current.next = new_node

    return head


def load_filenames_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


def remove_punctuation(word):
    return word.strip(string.punctuation).lower()


def index_files(files, index_filename="index", filenames_filename="filenames"):
    index_head = None
    filenames = []

    for file_name in files:
        filenames.append(file_name)
        with open(file_name, 'r') as f:
            for line in f:
                words = line.split()
                for word in words:
                    clean_word = remove_punctuation(word)
                    if not clean_word:
                        continue

                    current = index_head
                    prev = None
                    while current and current.word < clean_word:
                        prev = current
                        current = current.next

                    if current and current.word == clean_word:
                        idx = len(filenames) - 1
                        while len(current.freq) < len(filenames):
                            current.freq.append(0)
                        current.freq[idx] += 1
                    else:
                        new_node = Node(clean_word)
                        new_node.freq = [0] * len(filenames)
                        new_node.freq[-1] = 1

                        if not prev:
                            new_node.next = index_head
                            index_head = new_node
                        else:
                            prev.next = new_node
                            new_node.next = current

    with open(filenames_filename + '.txt', 'w') as f:
        for name in filenames:
            f.write(name + '\n')

    with open(index_filename + '.txt', 'w') as f:
        current = index_head
        while current:
            while len(current.freq) < len(filenames):
                current.freq.append(0)
            f.write(current.word + ' ' + ' '.join(map(str, current.freq)) + '\n')
            current = current.next


def main(argv):
    index_filename = "index"
    filenames_filename = "filenames"

    try:
        opts, args = getopt.getopt(argv, "hi:n:", ["index=", "name="])
    except getopt.GetoptError:
        print('Incorrect input')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--index"):
            index_filename = arg
        elif opt in ("-n", "--name"):
            filenames_filename = arg

    input_files = load_filenames_from_file("inputfilenames.txt")

    if not input_files:
        print("No files provided")
        sys.exit(2)

    index_files(input_files, index_filename, filenames_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
