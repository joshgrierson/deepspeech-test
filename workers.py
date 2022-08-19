import concurrent.futures

tasks = []

def register_task(fn, name, arg):
    params = dict()
    params["name"] = name
    params["fn"] = fn
    params["arg"] = arg
    tasks.append(params)

def run(on_complete):
    with concurrent.futures.ThreadPoolExecutor() as executor_pool:
        future_tasks = {executor_pool.submit(task["fn"], task["arg"]) for task in tasks}
        for i, future in enumerate(concurrent.futures.as_completed(future_tasks)):
            task = tasks[i]
            try:
                output = future.result()
            except Exception as ex:
                print("Failed task", task["name"])
                print(ex)
            else:
                print("Completed task", task["name"])
                on_complete(output)