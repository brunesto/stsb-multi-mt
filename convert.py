import csv
import math


def read_files(f1, f2, score_file):
    # load both sentence files
    with open(f1, encoding="utf-8") as f:
        content = f.readlines()
    with open(f2, encoding="utf-8") as f:
        content.extend(f.readlines())
    content = [c.strip() for c in content]
    #assert len(content) == (5749 + 1500 + 1379) * 2

    # load scores
    with open(score_file, encoding="utf-8") as f:
        scores_str = f.readlines()
    scores = []
    for s in scores_str:
        f = float(s)
        assert isinstance(f, float)
        assert f >= 0.0
        assert f <= 5.0
        scores.append(f)

    # create rows: s1 + s2 + score
    datasets = []
    for i, s in zip(range(min(len(scores),int(len(content)/2))), scores):
        row = [content[i*2], content[i*2+1], s]
        datasets.append(row)
    print("found ",len(datasets)," sentences ")        
    assert len(datasets) %2 == 0

    # split between train dev and test according to original ratios
    r1=5749/(5749 + 1500 + 1379)
    l1=r1*len(datasets)
    l1=int(l1/2)*2
    

    r2=(5749+1500)/(5749 + 1500 + 1379)
    l2=r2*len(datasets)
    l2=int(l2/2)*2
    
    print("l1",l1)
    print("l2",l2)

    # split data to train, dev and test
    train_data = datasets[:l1]
    dev_data = datasets[l1:l2]
    test_data = datasets[l2:]
    
    # bonus: return full scored datasets too
    return train_data, dev_data, test_data,datasets


def write_data(data, target_file):
    assert len(data) > 0
    print("Writing:", target_file)
    with open(target_file, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(
            csvfile,
            dialect='excel',  # excel is the default
        )
        for data_row in data:
            csv_writer.writerow(data_row)


if __name__ == "__main__":
    language = input('Which language do you want to convert? ')

    # load data
    train_data, dev_data, test_data,all_data = read_files(
        f"./data-raw/stsb-{language}-1.txt",
        f"./data-raw/stsb-{language}-2.txt",
        "./data-raw/stsb-scores.txt",
    )

    # write data
    write_data(train_data, f"./data/stsb-{language}-train.csv")
    write_data(dev_data, f"./data/stsb-{language}-dev.csv")
    write_data(test_data, f"./data/stsb-{language}-test.csv")
    write_data(all_data, f"./data/stsb-{language}-all.csv")
