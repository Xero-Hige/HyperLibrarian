from hyper_client import HyperClient

c = HyperClient("0.0.0.0", 8081)
print(c.upload_folder(".", "hyper_text"))
