from os.path import join
from codecs import open


def build_corpus(split, make_vocab=True, data_dir="./ResumeNER"):
    """读取数据"""
    assert split in ['train', 'dev', 'test']

    word_lists = []
    tag_lists = []
    # with open(join(data_dir, split+".char.bmes"), 'r', encoding='utf-8') as f:
    with open(join(data_dir, split + "_500.txt"), 'r', encoding='utf-8') as f:
        word_list = []
        tag_list = []
        for line in f:
            if line != '\n' and line!='\r\n':
                try:

                    word, tag = line.strip('\n').split()
                    word_list.append(word)
                    tag_list.append(tag)
                except:
                    # print(line)
                    temp = line.strip('\n').split()
                    if temp:
                        tag = line.strip('\n').split()[0]
                        word_list.append(" ")
                        tag_list.append(tag)
                    pass
            else:
                word_lists.append(word_list)
                tag_lists.append(tag_list)
                word_list = []
                tag_list = []

    # 如果make_vocab为True，还需要返回word2id和tag2id
    if make_vocab:
        word2id = build_map(word_lists)
        tag2id = build_map(tag_lists)
        return word_lists, tag_lists, word2id, tag2id
    else:
        return word_lists, tag_lists


def build_map(lists):
    maps = {}
    for list_ in lists:
        for e in list_:
            if e not in maps:
                maps[e] = len(maps)

    return maps
