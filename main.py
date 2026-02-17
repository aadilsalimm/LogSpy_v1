import multiprocessing as mp
from log_shipper import LogShipper
from log_classifierV1 import LogClassifier

def main():
    logs_from_shipper = mp.Queue()
    logs_to_classifier = mp.Queue()
    result_from_classifier = mp.Queue()
    shipper = LogShipper(buffer_size=5, filter_logs=True)
    classifier = LogClassifier()

    shipper_process = mp.Process(
        target=shipper.start,
        args=(logs_from_shipper,)
    )

    classifier_process = mp.Process(
        target=classifier.classify,
        args=(logs_to_classifier,
              result_from_classifier,)
    )

    shipper_process.start()
    classifier_process.start()

    # Controller loop
    while True:
        with open("dataset/dataset.jsonl", "a") as f:
            logs = logs_from_shipper.get()
            logs_to_classifier.put(logs)
            result = result_from_classifier.get()
            print(f'result: {result}')
            f.write(result + "\n")


    
if __name__ == "__main__":
    main()