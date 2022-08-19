from chunk import chunk_fn

def main():
    chunk_fn("./audio/long.wav", "chunk.wav", 0.2)

if __name__ == "__main__":
    main()