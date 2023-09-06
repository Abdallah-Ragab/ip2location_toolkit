from ip2location_toolkit.db_selector import select_db

if __name__ == '__main__':
    db_code = select_db()
    print('Downloading database [{}]...'.format(db_code))


