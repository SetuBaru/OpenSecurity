from inference import FaceId as Fd

# Main Test Function
if __name__ == "__main__":
    fd = Fd()
    fd.batched_learning()
    fd.detect()
