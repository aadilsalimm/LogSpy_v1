import multiprocessing as mp
from log_shipper import LogShipper
from llm_call_1 import classify

def main():
    logs_from_shipper = mp.Queue()
    logs_to_classifier = mp.Queue()
    result_from_classifier = mp.Queue()
    shipper = LogShipper()

    shipper_process = mp.Process(
        target=shipper.start,
        args=(logs_from_shipper,)
    )

    classifier_process = mp.Process(
        target=classify,
        args=(logs_to_classifier,
              result_from_classifier,)
    )

    shipper_process.start()
    classifier_process.start()

    # Controller loop
    while True:
        logs = logs_from_shipper.get()
        logs_to_classifier.put(logs)
        result = result_from_classifier.get()
        print(f'result: {result}')

    
if __name__ == "__main__":
    main()