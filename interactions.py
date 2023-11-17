import servers as server

def main():
    # inp = input('TARGET NOMINATIM ')
    inp = ('donald bren hall, irvine')
    server.nominatim_search(inp)


if __name__ == '__main__':
    main()