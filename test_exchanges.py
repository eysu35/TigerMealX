from database.exchanges import Exchanges


def main():
    # add a new exchange
    # Exchanges.add_new_exchange('920228016', '920228342')

    # edit the line below to update your exchange as necessary
    success, msg = Exchanges.update_exchange('920228016', '920195317', '~quad_location_id~', '8:33')
    print(msg)


if __name__ == '__main__':
    main()
