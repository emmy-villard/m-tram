from etl.etl_trr import etl_trr
from etl.etl_ligne import etl_ligne


def main():
    etl_trr()
    etl_ligne()

if __name__ == "__main__":
    main()